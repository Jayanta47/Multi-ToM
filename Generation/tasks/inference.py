import os
import sys
import logging
from datetime import datetime
from tqdm import tqdm

# include the file in python path
script_dir = os.path.dirname(os.path.abspath(__file__))
generation_dir = os.path.abspath(os.path.join(script_dir, "../"))
sys.path.append(generation_dir)

from components.agent.agent import Agent
from components.llm.chatgpt import ChatGpt
from components.prompt.prompt_manager import InferencePromptManager
from components.data_handler.inference_data_handler import InferenceDataHandler
from components.processor.base_processor import InferenceProcessor


def create_prompter(language):
    prompter = InferencePromptManager(language=language)
    return prompter


def create_agent(processor, prompter, **kwargs):
    try:
        model = kwargs.get("model")
    except Exception as e:
        print(e)
        raise Exception("Please provide model name in the config file")

    llm = ChatGpt(model_name=model)

    inference_agent = Agent(
        llm=llm, processor=processor, prompter=prompter, agent_serial=0
    )

    return inference_agent


def create_data_handler(config_file):
    data_handler = InferenceDataHandler(config=config_file)
    return data_handler


def create_processor():
    processor = InferenceProcessor()
    return processor


def executor(
    data_handler: InferenceDataHandler,
    inference_agent: Agent,
    logger: logging.Logger,
):
    logger.info("Starting execution")
    for data_sample in tqdm(data_handler.return_data_point(1)):
        logger.info(f"Processing data sample: {data_sample['INDEX']}")
        inference_response = inference_agent.invoke(input=data_sample)
        logger.debug(f"Inference response: {inference_response}")

        content = {
            "inference_response": inference_response["response"],
        }

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
    inference_agent = create_agent(
        processor=processor,
        prompter=prompter,
        model=data_handler.get_attribute("model"),
    )

    executor(data_handler, inference_agent, logger)
