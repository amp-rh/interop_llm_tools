import abc
from dataclasses import dataclass


@dataclass
class BaseWrapper[_inner_cls](abc.ABC):
    inner: _inner_cls
