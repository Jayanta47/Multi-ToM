import os
import sys
import yaml
import logging
from datetime import datetime
from tqdm import tqdm

# include the file in python path
script_dir = os.path.dirname(os.path.abspath(__file__))
generation_dir = os.path.abspath(os.path.join(script_dir, "../"))
sys.path.append(generation_dir)

from components.agent.agent import Agent
from components.llm.chatgpt import ChatGpt
from components.prompt.prompt_manager import TranslatorPromptManager
from components.data_handler.translate_data_handler import TranslationDataHandler
from components.processor.base_processor import TranslationProcessor


def create_prompter(source_language, target_language):
    prompter = TranslatorPromptManager(
        source_language=source_language, target_language=target_language
    )
    return prompter


def create_agents(processor, prompter, **kwargs):
    try:
        primary_model = kwargs.get("primary_agent_llm")
        secondary_model = kwargs.get("secondary_agent_llm")
    except Exception as e:
        print(e)
        raise Exception(
            "Please provide primary and secondary model name in the config file"
        )

    llm1 = ChatGpt(model_name=primary_model)
    llm2 = ChatGpt(model_name=secondary_model)

    translator_agent = Agent(
        llm=llm1, processor=processor, prompter=prompter, agent_serial=0
    )
    feedback_agent = Agent(
        llm=llm2, processor=processor, prompter=prompter, agent_serial=1
    )
    refinement_agent = Agent(
        llm=llm2, processor=processor, prompter=prompter, agent_serial=2
    )

    return translator_agent, feedback_agent, refinement_agent


def create_data_handler(config_file):
    data_handler = TranslationDataHandler(config=config_file)
    return data_handler


def create_processor():
    processor = TranslationProcessor()
    return processor


def executor(
    data_handler: TranslationDataHandler,
    translator_agent: Agent,
    feedback_agent: Agent,
    refinement_agent: Agent,
    logger: logging.Logger,
    feedback_enabled: bool = False,
):
    logger.info("Starting execution")
    for data_sample in tqdm(data_handler.return_data_point(20)):
        logger.info(f"Processing data sample: {data_sample['INDEX']}")
        translator_response = translator_agent.invoke(input=data_sample)
        logger.debug(f"Translator response: {translator_response}")

        content = {
            "translator_response": translator_response["response"],
            "original": translator_response["prompt"],
        }

        if feedback_enabled:

            feedback_response = feedback_agent.invoke(input=translator_response)
            logger.debug(f"Feedback response: {feedback_response}")

            for _ in range(2):
                if feedback_response["status"] == "modify":
                    logger.info("REFINEMENT:required")
                    refinement_input = {
                        "original_text": translator_response["prompt"],
                        "translated_text": translator_response["response"],
                        "feedback": feedback_response["response"],
                    }
                    refinement_response = refinement_agent.invoke(input=refinement_input)
                    logger.debug(f"Refinement response: {refinement_response}")

                    feedback_response = feedback_agent.invoke(
                        user_prompt=refinement_response
                    )
                    logger.debug(f"Feedback response after refinement: {feedback_response}")
                else:
                    logger.info("REFINEMENT: not required")
                    refinement_response = {"response": feedback_response["response"]}
                    logger.debug(f"Refinement response: {refinement_response}")
                    break

            content['feedback_response'] = feedback_response['response']
            content['refinement_response'] = refinement_response['response']

        logger.info(f"Saving data point: {data_sample['INDEX']}")
        data_handler.save_data_point(index=data_sample["INDEX"], content=content)

    logger.info("Execution completed")


if __name__ == "__main__":
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_folder = "logs"
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    log_file = os.path.join(log_folder, f"{current_time}.log")
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    data_handler = create_data_handler("Generation/tasks/translation_config.yaml")
    prompter = create_prompter(
        source_language=data_handler.get_attribute("source_language"),
        target_language=data_handler.get_attribute("target_language"),
    )
    processor = create_processor()
    translator_agent, feedback_agent, refinement_agent = create_agents(
        processor=processor,
        prompter=prompter,
        primary_agent_llm=data_handler.get_attribute("model"),
        secondary_agent_llm=data_handler.get_attribute("secondary_model"),
    )

    executor(data_handler, translator_agent, feedback_agent, refinement_agent, logger)
