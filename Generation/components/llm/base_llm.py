from abc import ABC, abstractmethod

class LLM(ABC):
    @abstractmethod
    def create_response(self, model_message):
        pass

    @abstractmethod
    def calculate_cost(self, input_tokens, output_tokens):
        pass
