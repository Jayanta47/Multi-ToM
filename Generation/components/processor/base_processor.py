from abc import ABC, abstractmethod


class Processor(ABC):
    @abstractmethod
    def process(self, input: str, **kwargs) -> str:
        """
        Process the given input string and return the processed string.

        Args:
            input (str): The string to process.

        Returns:
            str: The processed string.

        Notes:
            This method is abstract and must be implemented by any subclass of Processor.
        """
        pass


class TranslationProcessor(Processor):
    def process(self, input: str, **kwargs) -> str:
        return input
