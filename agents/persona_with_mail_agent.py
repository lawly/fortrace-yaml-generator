import logging
from typing import Any
from agents.agent_base import AgentBase
from langchain_core.runnables.base import RunnableLike
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.messages import AIMessage

from langchain_core.prompts import ChatPromptTemplate
from langchain.agents.agent import AgentExecutor
from langchain.agents import AgentExecutor, create_tool_calling_agent

from services.tools import (
    get_mail_providers,
    get_mail_provider_configuration,
)


class PersonaWithMailAgent(AgentBase):
    def __init__(self, model: BaseChatModel, prompt: str) -> None:
        """
        Initialize the Persona Agent with custom mail providers.

        Args:
            model (BaseChatModel): The underlying language model to use for generating the personas.
        """
        self.__model: BaseChatModel = model
        self.__prompt: str = prompt

    def __extract_response(self, response: str, marker: str):
        response = response.split(f'<{marker}>')[1].split(f'</{marker}>')[0]
        return response

    def __get_completion_with_tools(self, tools: dict):
        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}"),
            ]
        )

        agent = create_tool_calling_agent(self.__model, tools, prompt_template)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        result = agent_executor.invoke({"input": self.__prompt})
        return result['output']
    
    def node_action(self, state: Any) -> RunnableLike:
        """
        This function is called by the LangChain executor to generate a story based on the given task.

        Args:
            state (Any): The current state of the executor. Contains the task to generate a story for.

        Returns:
            RunnableLike: The updated state with the generated story and messages.
        """
        logging.info("---PERSONA START---")
        self.__prompt = self.__prompt.replace('{count}', str(state["count"]))
        response: str = self.__get_completion_with_tools([get_mail_providers, get_mail_provider_configuration])
        logging.debug(f"PersonaAgent response: {response}")
        personas: str = self.__extract_response(response, 'personas')
        logging.info(f"Extracted personas: {personas}")
        logging.info("---PERSONA EXTRACTOR END---")
        content: str = f"""
**Personas**

```json
{personas}
```
        """
        #return {**state, "personas": personas, "messages": [response]}
        return {**state, "personas": personas, "messages": [AIMessage(content=content)]}
