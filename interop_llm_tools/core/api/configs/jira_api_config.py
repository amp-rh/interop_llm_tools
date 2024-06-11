from dataclasses import dataclass

from core.base.base_api_config import BaseApiConfig
from mixins.from_env import FromEnvMixin


@dataclass
class JiraApiConfig(BaseApiConfig, FromEnvMixin): ...
