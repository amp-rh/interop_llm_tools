from dataclasses import dataclass

from core.base.base_api_config import BaseApiConfig
from mixins.from_env import FromDefaultsMixin


@dataclass
class JiraApiConfig(BaseApiConfig, FromDefaultsMixin): ...
