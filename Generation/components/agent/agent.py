from components.llm.base_llm import LLM
from components.processor.base_processor import Processor
from components.agent.base_agent import BaseAgent
from components.prompt.prompt_manager import BasePromptManager


class Agent(BaseAgent):
    """Agent class is the base class for all agents

    Args:
        llm (LLM): The language model to use
        processor (Processor): The processor to use
    """

    def __init__(self, llm: LLM, processor: Processor, prompter: BasePromptManager):
        super().__init__()
        self.llm = llm
        self.processor = processor
        self.prompter = prompter

    def set_config(self, **kwargs):
        raise NotImplementedError

    def invoke(self, user_prompt: str):
        prompt = self.prompter.create_prompt(user_query=user_prompt)
        while True:
            model_response = self.llm.create_response(prompt)
            refined_output, is_satisfied = self.processor.process(
                model_response["content"]
            )
            if is_satisfied:
                return refined_output
