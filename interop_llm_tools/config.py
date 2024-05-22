import logging
import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

DEFAULT_LLM_API_BASE_ENV = "LLM_API_BASE"
DEFAULT_OLLAMA_API_BASE_ENV = "OLLAMA_API_BASE"

os.environ[DEFAULT_OLLAMA_API_BASE_ENV] = os.getenv(
    DEFAULT_OLLAMA_API_BASE_ENV, DEFAULT_LLM_API_BASE_ENV
)

logger = logging.getLogger(__name__)


@dataclass
class Config:
    default_llm_api_base_url = os.getenv(DEFAULT_LLM_API_BASE_ENV)


def get_config() -> Config:
    return Config()
