from abc import ABC, abstractmethod
import logging
from components.constants import *


class BasePromptManager(ABC):
    @abstractmethod
    def set_system_prompt(self, system_prompt: str, **kwargs):
        pass

    @abstractmethod
    def correction_prompt(self, previous_prompt, model_response, **kwargs):
        pass

    @abstractmethod
    def create_prompt(self, user_query, **kwargs):
        pass


class TranslatorPromptManager(BasePromptManager):
    """
    A prompt manager for translation tasks.
    """

    def __init__(self, source_language: str, target_language: str, num_agents: int = 3):
        """
        Initialize the TranslatorPromptManager.

        Args:
            source_language (str): The source language of the translation task.
            target_language (str): The target language of the translation task.
            num_agents (int, optional): The number of agents to use for this task. Defaults to 3.

        Raises:
            AssertionError: If the number of agents is greater than the number of system prompts.
        """
        self.source_language = source_language
        self.target_language = target_language
        self.agents_sys_prompt = []
        self.agents_sys_prompt.append(
            SYSTEM_PROMPT_TRANS_AGENT_1.format(
                source_language=source_language, destination_language=target_language
            )
        )
        self.agents_sys_prompt.append(
            SYSTEM_PROMPT_TRANS_AGENT_2.format(
                source_language=source_language, destination_language=target_language
            )
        )
        self.agents_sys_prompt.append(
            SYSTEM_PROMPT_TRANS_AGENT_3.format(
                source_language=source_language, destination_language=target_language
            )
        )

        self.correction_prompt_list = [
            CORRECTION_TEMPLATE_1,
            CORRECTION_TEMPLATE_1,
            CORRECTION_TEMPLATE_1,
        ]

        assert num_agents <= len(
            self.agents_sys_prompt
        ), "Number of agents must be less than or equal to the number of system prompts"

        self.logger = logging.getLogger(__name__)

    def set_system_prompt(self, system_prompt: str, **kwargs):
        """
        Sets the system prompt for the given agent.

        Args:
            system_prompt (str): The system prompt to set.
            **kwargs: Additional keyword arguments.
                agent_serial (int): The serial number of the agent to set the prompt for.
        """
        agent_serial = kwargs.get("agent_serial")
        assert agent_serial < len(self.agents_sys_prompt), "Invalid agent serial"
        self.logger.info(f"Setting system prompt for agent {agent_serial}")
        self.agents_sys_prompt[agent_serial] = system_prompt

    def create_prompt(self, user_query, **kwargs) -> list:
        """
        Creates a prompt for the given agent.

        Args:
            user_query (str): The user query to generate a prompt for.
            **kwargs: Additional keyword arguments.
                agent_serial (int): The serial number of the agent to generate the prompt for.

        Returns:
            list: A prompt in the format of [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_query}].
        """
        agent_serial = kwargs.get("agent_serial")
        assert agent_serial < len(self.agents_sys_prompt), "Invalid agent serial"
        system_prompt = self.agents_sys_prompt[agent_serial]
        self.logger.info(f"Creating prompt for agent {agent_serial}")
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query},
        ]

    def correction_prompt(self, previous_prompt, model_response, **kwargs):
        agent_serial = kwargs.get("agent_serial")
        correction_prompt = self.correction_prompt_list[agent_serial]
        extension = [
            {"role": "assistant", "content": model_response},
            {"role": "user", "content": correction_prompt},
        ]
        previous_prompt.extend(extension)

        return previous_prompt
