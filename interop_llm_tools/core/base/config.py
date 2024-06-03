import abc
from dataclasses import dataclass


@dataclass
class BaseLanguageModelConfig(abc.ABC):
    model_name: str
