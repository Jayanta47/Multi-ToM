import logging

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
        self.logger = logging.getLogger(__name__)

    def invoke(self, input: dict | str):
        self.logger.info(f"Agent {self.agent_serial}.invoke: Started")
        user_prompt = self.processor.process(
            input=input, agent_serial=self.agent_serial, task_type="pre-processing"
        )
        self.logger.info(f"Agent {self.agent_serial}.invoke: Pre-processing done")
        input["user_prompt"] = user_prompt
        self.processor.save_current_user_input(input)

        prompt = self.prompter.create_prompt(
            user_query=user_prompt, agent_serial=self.agent_serial
        )
        self.logger.info(f"Agent {self.agent_serial}.invoke: Prompt created")

        for _ in range(2):
            model_response = self.llm.create_response(prompt)
            self.logger.info(f"Agent {self.agent_serial}.invoke: Model response created")

            refined_output = self.processor.process(
                input=model_response,
                agent_serial=self.agent_serial,
                task_type="post-processing",
            )
            self.logger.info(f"Agent {self.agent_serial}.invoke: Post-processing done")

            self.logger.info(
                f"Agent {self.agent_serial}.invoke: Response status: {refined_output['status']}"
            )
            if refined_output["status"] == "success":
                break

            prompt = self.prompter.correction_prompt(
                previous_prompt=prompt,
                model_response=model_response["content"],
                agent_serial=self.agent_serial,
            )
            self.logger.info(f"Agent {self.agent_serial}.invoke: Correction prompt created")

        self.logger.info(f"Agent {self.agent_serial}.invoke: Finished")
        return refined_output

