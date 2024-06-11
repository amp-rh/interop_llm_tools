from dataclasses import dataclass

from core.base.base_prompt_template import BasePromptTemplate


@dataclass
class DefaultPromptTemplate(BasePromptTemplate):
    def get_prompt_inputs_dict(self) -> dict:
        return {}

    template_str: str = ""
