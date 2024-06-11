from dataclasses import dataclass

from core.base.base_prompt_template import BasePromptTemplate


@dataclass
class CondensePromptTemplate(BasePromptTemplate):
    context: str = ""

    template_str: str = (
        "Rewrite the following context to be more succinct and less redundant without affecting its overall meaning."
        "\n\n{context}\n\n"
    )

    def get_prompt_inputs_dict(self) -> dict:
        return {"context": self.context}
