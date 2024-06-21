from dataclasses import dataclass
from typing import Type

from core.api.agent_api import AgentApi
from core.base.base_api_config import BaseApiConfig
from core.base.base_prompt_template import BasePromptTemplate
from mixins.from_env import FromDefaultsMixin


@dataclass
class PipelineApiConfig(BaseApiConfig, FromDefaultsMixin):
    agent_api: AgentApi = None
    prompt_template_cls: Type[BasePromptTemplate] = None
