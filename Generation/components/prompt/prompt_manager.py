from abc import ABC, abstractmethod

class BasePromptManager(ABC):
    @abstractmethod
    def set_system_prompt(self, system_prompt: str, **kwargs):
        pass

    @abstractmethod
    def create_prompt(self, user_query, **kwargs):
        pass

class TranslatorPromptManager(BasePromptManager):
    """
    A prompt manager for translation tasks.
    """
    def __init__(self, source_language: str, target_language: str):
        self.source_language = source_language
        self.target_language = target_language
        self.system_prompt = None

    def set_system_prompt(self, system_prompt: str, **kwargs):
        self.system_prompt = system_prompt

    def create_prompt(self, user_query, **kwargs) -> str:
        """
        Creates a prompt for the translation task.
        """
        if self.system_prompt is None:
            raise ValueError("System prompt is not set")

        prompt = f"Translate the following text from {self.source_language} to {self.target_language}:\n\n{user_query}"
        if self.system_prompt:
            prompt += f"\n\n{self.system_prompt}"

        return prompt
