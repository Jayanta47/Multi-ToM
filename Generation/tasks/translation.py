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


def create_agents():
    pass


def create_data_handler():
    data_handler = TranslationDataHandler(config="test.yaml")
    return data_handler


def create_processor():
    processor = TranslationProcessor()
    return processor


if __name__ == "__main__":
    prompter = create_prompter(source_language="English", target_language="French")
    prompt = prompter.create_prompt(
        user_query="What is the capital of France?", agent_serial=2
    )
    print(prompt)
