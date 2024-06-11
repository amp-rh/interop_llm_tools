from dataclasses import dataclass

from core.base.base_prompt_template import BasePromptTemplate


@dataclass
class RefinePromptTemplate(BasePromptTemplate):
    user_query: str = ""
    agent_response: str = ""

    def get_prompt_inputs_dict(self) -> dict:
        return {"user_query": self.user_query, "agent_response": self.agent_response}

    template_str: str = (
        "You are provided with a User query and Assistant response to the user. "
        "Refine the Agent response to better satisfy the User query."
        "\n\nThe User query:\n\t"
        "\n\n{user_query}\n\n"
        "\n\nThe Agent response:\n\t"
        "\n\n{agent_response}\n\n"
    )
