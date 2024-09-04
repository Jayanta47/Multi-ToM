from components.llm.base_llm import LLM
from components.processor.base_processor import Processor

class Agent(BaseAgent):
    """Agent class is the base class for all agents

    Args:
        llm (LLM): The language model to use
        processor (Processor): The processor to use
    """

    def __init__(self, llm: LLM, processor: Processor):
        super().__init__()
        self.llm = llm
        self.processor = processor

    def set_config(self, **kwargs):
        raise NotImplementedError

    def invoke(self, user_prompt: str):
        raise NotImplementedError
