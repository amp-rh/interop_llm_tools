import logging
from dataclasses import dataclass

from dotenv import load_dotenv

from interop_llm_tools.core.llm import Llm

load_dotenv()

logger = logging.getLogger(__name__)


@dataclass
class Config:
    def get_default_llm(self) -> Llm:
        return Llm.from_env()


def get_config() -> Config:
    return Config()
