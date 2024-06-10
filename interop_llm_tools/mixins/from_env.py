import abc
from dataclasses import dataclass


@dataclass
class FromEnvMixin(abc.ABC):
    @classmethod
    def from_env(cls):
        return cls()
