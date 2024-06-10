import abc
from dataclasses import dataclass

from mixins.from_env import FromEnvMixin


@dataclass
class BaseLanguageModelConfig(FromEnvMixin, abc.ABC):
    model_name: str
    base_api_url: str
