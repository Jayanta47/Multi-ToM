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

    def __init__(
        self, llm: LLM, processor: Processor, prompter: BasePromptManager, **kwargs
    ):
        super().__init__()
        self.llm = llm
        self.processor = processor
        self.prompter = prompter
        self.agent_serial = kwargs.get("agent_serial", 0)

    def invoke(self, input: dict | str):
        user_prompt = self.processor.process(
            input=input, agent_serial=self.agent_serial, task_type="pre-processing"
        )
        input["user_prompt"] = user_prompt
        self.processor.save_current_user_input(input)

        prompt = self.prompter.create_prompt(
            user_query=user_prompt, agent_serial=self.agent_serial
        )

        model_response = self.llm.create_response(prompt)

        refined_output = self.processor.process(
            input=model_response,
            agent_serial=self.agent_serial,
            task_type="post-processing",
        )

        return refined_output
