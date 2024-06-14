from dataclasses import dataclass
from typing import Type

from llama_index.core.query_pipeline import (
    QueryPipeline as LmxQueryPipeline,
)

from core.api.agent_api import AgentApi
from core.api.configs.pipeline_api_config import PipelineApiConfig
from core.base.base_api import BaseApi
from core.base.base_prompt_template import BasePromptTemplate
from core.prompt_templates.default import DefaultPromptTemplate
from mixins.from_config import FromConfigMixin
from mixins.from_env import FromEnvMixin


@dataclass
class PipelineApi(BaseApi, FromConfigMixin[PipelineApiConfig], FromEnvMixin):
    agent_api: AgentApi
    prompt_template_cls: Type[BasePromptTemplate] = DefaultPromptTemplate
    _chain = []

    @classmethod
    def from_config(cls, config: PipelineApiConfig) -> "PipelineApi":
        return cls(
            prompt_template_cls=config.prompt_template_cls or cls.prompt_template_cls,
            agent_api=config.agent_api or AgentApi.from_env(),
        )

    @classmethod
    def from_env(cls) -> "PipelineApi":
        return cls.from_config(PipelineApiConfig.from_env())

    def get_formatted_prompt(self, **kwargs) -> str:
        return self.prompt_template_cls(**kwargs).format()

    async def arun(self, **kwargs) -> str:
        return (
            await self.to_lmx().arun(input=self.get_formatted_prompt(**kwargs))
        ).response

    def chain(self, other: "PipelineApi") -> "PipelineApi":
        self._chain = self._get_chain() + other._get_chain()
        return self

    def to_lmx(self):
        return LmxQueryPipeline(chain=self._get_chain())

    def _get_chain(self):
        return self._chain or [self._get_agent_component()]

    def _get_agent_component(self):
        return self.agent_api.agent_runner.inner.as_query_component()