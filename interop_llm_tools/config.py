import logging
import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

DEFAULT_LLM_API_BASE_ENV = "LLM_API_BASE"
DEFAULT_OLLAMA_API_BASE_ENV = "OLLAMA_API_BASE"
DEFAULT_OPENAI_API_BASE_ENV = "OPENAI_API_BASE_ENV"
DEFAULT_OPENAI_API_KEY_ENV = "OPENAI_API_KEY_ENV"

os.environ[DEFAULT_OLLAMA_API_BASE_ENV] = os.getenv(
    DEFAULT_OLLAMA_API_BASE_ENV, DEFAULT_LLM_API_BASE_ENV
)

logger = logging.getLogger(__name__)


@dataclass
class Config:
    default_llm_api_base_url = os.getenv(DEFAULT_LLM_API_BASE_ENV)
    openai_api_base = os.getenv(DEFAULT_OPENAI_API_BASE_ENV)
    openai_api_key = os.getenv(DEFAULT_OPENAI_API_KEY_ENV)
    openai_default_instruct_model = "/models/Mistral-7B-Instruct-v0.2"
    openai_default_embed_model = "/models/bge-large-en-v1.5"


def get_config() -> Config:
    return Config()
