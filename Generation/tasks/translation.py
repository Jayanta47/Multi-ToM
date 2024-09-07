import os
import sys
import yaml

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


def create_data_handler():
    data_handler = TranslationDataHandler(
        config="Generation/tasks/translation_config.yaml"
    )
    return data_handler


def create_processor():
    processor = TranslationProcessor()
    return processor


def executor(
    data_handler: TranslationDataHandler,
    translator_agent: Agent,
    feedback_agent: Agent,
    refinement_agent: Agent,
):
    for data_sample in data_handler.return_data_point():
        translator_response = translator_agent.invoke(input=data_sample)

        feedback_response = feedback_agent.invoke(input=translator_response)

        for _ in range(2):
            if feedback_response["decision"] == "yes":
                refinement_response = refinement_agent.invoke(
                    user_prompt=translator_response
                )

                feedback_response = feedback_agent.invoke(
                    user_prompt=refinement_response
                )
            else:
                refinement_response = translator_response
                break

        content = {
            "translator_response": translator_response["content"],
            "feedback_response": feedback_response["content"],
            "refinement_response": refinement_response["content"],
        }

        data_handler.save_data_point(index=data_sample["INDEX"], content=content)


if __name__ == "__main__":
    data_handler = create_data_handler()

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

    executor(data_handler, translator_agent, feedback_agent, refinement_agent)
