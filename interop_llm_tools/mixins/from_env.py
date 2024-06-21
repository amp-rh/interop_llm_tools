import abc
from dataclasses import dataclass


@dataclass
class FromDefaultsMixin(abc.ABC):
    @classmethod
    def from_defaults(cls):
        return cls()
