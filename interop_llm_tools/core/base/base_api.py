import abc
from dataclasses import dataclass

from core.base.base_api_config import BaseApiConfig
from mixins.from_config import FromConfigMixin


@dataclass
class BaseApi(FromConfigMixin[BaseApiConfig], abc.ABC): ...
