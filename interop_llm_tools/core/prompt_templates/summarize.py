from dataclasses import dataclass

from core.base.base_prompt_template import BasePromptTemplate


@dataclass
class SummarizePromptTemplate(BasePromptTemplate):
    context: str = ""

    template_str: str = (
        "Provide a summary from the following context:"
        "\n\n{context}\n\n"
        "Here are some rules to follow when forming your response:\n"
        "\tDo NOT provide your own suggestions; only describe what is observed in the context.\n"
        "\tYour response should be written at the same technical level as observed in the context.\n"
        "\tAssume the reader of your response is familiar with the origin of the context and any mentioned users.\n"
        "\tUse email addresses instead of names when referring to users.\n"
        "\tDo not directly refer to the context."
    )

    def get_prompt_inputs_dict(self) -> dict:
        return {"context": self.context}
