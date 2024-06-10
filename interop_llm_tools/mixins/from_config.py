import abc
from dataclasses import dataclass


@dataclass
class FromConfigMixin[T](abc.ABC):

    @classmethod
    @abc.abstractmethod
    def from_config[T](cls, config: T) -> any: ...
