import logging

from abc import ABC, abstractmethod
from components.constants import *


class Processor(ABC):
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

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
        self.logger.info("PROCESSOR: Saving current user input")
        self.current_user_input = input

    def process_translator_output(self, input: dict):
        self.logger.info("PROCESSOR: Processing translator output")
        if (
            "<STORY>" in input["content"]
            and "</STORY>" in input["content"]
            and "<QUESTION>" in input["content"]
            and "</QUESTION>" in input["content"]
            and "<OPTIONS>" in input["content"]
            and "</OPTIONS>" in input["content"]
        ):
            status = "success"
        else:
            status = "incorrect"

        self.logger.info(
            "PROCESSOR: Returning translator output with status %s", status
        )
        return {
            "prompt": self.current_user_input["user_prompt"],
            "response": input["content"],
            "status": status,
        }

    def process_feedback_output(self, input: dict):
        self.logger.info("PROCESSOR: Processing feedback output")
        message = input["content"]
        if "###Quality" in message and "okay" in message.lower():
            self.logger.info("PROCESSOR: Returning feedback output with status success")
            return {"response": "No Feedback", "status": "success"}
        elif "###Feedback" in message:
            feedback = message.split("###Feedback")[-1].strip().strip(":")
            self.logger.info("PROCESSOR: Returning feedback output with status modify")
            return {"response": feedback, "status": "modify"}

        self.logger.info("PROCESSOR: Returning feedback output with status incorrect")
        return {"status": "incorrect"}

    def process_refinement_output(self, input: str):
        self.logger.info("PROCESSOR: Processing refinement output")
        return input

    def process_translator_input(self, input: dict) -> str:
        self.logger.info("PROCESSOR: Processing translator input")
        user_prompt = TOMQA_TEMPLATE_V2.format(
            story=input["STORY"],
            query=input["QUERY"],
        )

        self.logger.info("PROCESSOR: Returning translator input")
        return user_prompt

    def process_feedback_input(self, input: str):
        self.logger.info("PROCESSOR: Processing feedback input")
        return FEEDBACK_TEMPLATE.format(
            original_text=input["prompt"],
            translated_text=input["response"],
        )

    def process_refinement_input(self, input: str):
        self.logger.info("PROCESSOR: Processing refinement input")
        return REFINEMENT_TEMPLATE.format(
            original_text=input["original_text"],
            translated_text=input["translated_text"],
            feedback=input["feedback"],
        )

    def preprocess(self, input, agent_serial):
        self.logger.info("PROCESSOR: Preprocessing input for agent %d", agent_serial)
        if agent_serial == 0:
            return self.process_translator_input(input)
        elif agent_serial == 1:
            return self.process_feedback_input(input)
        elif agent_serial == 2:
            return self.process_refinement_input(input)

    def postprocess(self, input, agent_serial):
        self.logger.info("PROCESSOR: Postprocessing input for agent %d", agent_serial)
        if agent_serial == 0:
            return self.process_translator_output(input)
        elif agent_serial == 1:
            return self.process_feedback_output(input)
        elif agent_serial == 2:
            return self.process_refinement_output(input)

    def process(self, input: dict | str, **kwargs) -> str:
        self.logger.info(
            "PROCESSOR: Processing input with task type %s", kwargs.get("task_type")
        )
        agent_serial = kwargs.get("agent_serial")
        task_type = kwargs.get("task_type")
        if task_type == "pre-processing":
            return self.preprocess(input, agent_serial=agent_serial)

        return self.postprocess(input, agent_serial=agent_serial)
