from abc import ABC, abstractmethod
from components.constants import *


class Processor(ABC):
    @abstractmethod
    def save_current_user_input(self, input: dict):
        pass

    @abstractmethod
    def process(self, input: dict, **kwargs) -> str:
        """
        Process the given input and return the processed output.

        Args:
            input (dict): The input to be processed.

        Returns:
            str: The processed output.
        """
        pass


class TranslationProcessor(Processor):
    def __init__(self) -> None:
        super().__init__()
        self.current_user_input = None

    def save_current_user_input(self, input: dict):
        self.current_user_input = input

    def process_translator_output(self, input: dict):
        return {
            "prompt": self.current_user_input["user_prompt"],
            "response": input["content"],
            "status": "success",
        }

    def process_feedback_output(self, input: str):
        return input

    def process_refinement_output(self, input: str):
        return input

    def process_translator_input(self, input: dict) -> str:
        user_prompt = TOMQA_TEMPLATE.format(
            story=input["STORY"],
            question=input["QUESTION"],
            option_a=input["OPTION-A"],
            option_b=input["OPTION-B"],
            option_c=input["OPTION-C"],
            option_d=input["OPTION-D"],
        )

        return user_prompt

    def process_feedback_input(self, input: str):
        return REFINEMENT_TEMPLATE.format(
            original_text=input["prompt"],
            translated_text=input["response"],
        )

    def process_refinement_input(self, input: str):
        return input

    def preprocess(self, input, agent_serial):
        if agent_serial == 0:
            return self.process_translator_input(input)
        elif agent_serial == 1:
            return self.process_feedback_input(input)
        elif agent_serial == 2:
            return self.process_refinement_input(input)

    def postprocess(self, input, agent_serial):
        if agent_serial == 0:
            return self.process_translator_output(input)
        elif agent_serial == 1:
            return self.process_feedback_output(input)
        elif agent_serial == 2:
            return self.process_refinement_output(input)

    def process(self, input: dict | str, **kwargs) -> str:
        agent_serial = kwargs.get("agent_serial")
        task_type = kwargs.get("task_type")
        if task_type == "pre-processing":
            return self.preprocess(input, agent_serial=agent_serial)

        return self.postprocess(input, agent_serial=agent_serial)
