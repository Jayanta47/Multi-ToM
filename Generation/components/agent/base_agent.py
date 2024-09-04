from abc import ABC, abstractmethod
from components.llm.base_llm import LLM
from components.processor.base_processor import Processor
from components.prompt.prompt_manager import BasePromptManager


class BaseAgent(ABC):
    @abstractmethod
    def set_config(
        self, llm: LLM, processor: Processor, prompter: BasePromptManager, **kwargs
    ):
        pass

    @abstractmethod
    def invoke(self, user_prompt: str):
        pass
