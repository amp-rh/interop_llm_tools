import abc
from dataclasses import dataclass


@dataclass
class BaseWrapper[T](abc.ABC):
    inner: T
