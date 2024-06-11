import abc
from dataclasses import dataclass

from llama_index.core import PromptTemplate as LmxPromptTemplate
from llama_index.core.base.query_pipeline.query import QueryComponent


@dataclass
class BasePromptTemplate(abc.ABC):
    template_str: str

    def to_lmx(self) -> LmxPromptTemplate:
        return LmxPromptTemplate(template=self.template_str)

    def as_query_component(self) -> QueryComponent:
        return self.to_lmx().as_query_component()

    @abc.abstractmethod
    def get_prompt_inputs_dict(self) -> dict: ...

    def format(self) -> str:
        return self.to_lmx().format(**self.get_prompt_inputs_dict())
