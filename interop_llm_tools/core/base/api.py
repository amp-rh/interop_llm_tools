import abc
from dataclasses import dataclass


@dataclass
class BaseApiConfig(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def from_env(cls): ...


@dataclass
class BaseApi[T: BaseApiConfig](abc.ABC):
    config: BaseApiConfig

    @classmethod
    @abc.abstractmethod
    def from_config(cls, config: T): ...
