import abc
from dataclasses import dataclass

from mixins.from_env import FromDefaultsMixin


@dataclass
class BaseLanguageModelConfig(FromDefaultsMixin, abc.ABC):
    model_name: str
    base_api_url: str
