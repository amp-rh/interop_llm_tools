import logging
import os
from dataclasses import dataclass

from dotenv import load_dotenv

from interop_llm_tools.core.common.llm_api_type import LlmApiType

DEFAULT_LLM_API_TYPE = "ollama"
DEFAULT_LLM_INSTRUCT_MODEL_NAME = "mistral-7b-instruct-v0.2.Q4_K_M.gguf:latest"
DEFAULT_LLM_EMBED_MODEL_NAME = "mxbai-embed-large:latest"

load_dotenv()

logger = logging.getLogger(__name__)


@dataclass
class LlmConfig:
    llm_api_type: LlmApiType = LlmApiType.from_str(
        os.getenv("LLM_API_TYPE", DEFAULT_LLM_API_TYPE)
    )
    llm_instruct_model_name: str = os.getenv(
        "LLM_INSTRUCT_MODEL_NAME", DEFAULT_LLM_INSTRUCT_MODEL_NAME
    )
    llm_embed_model_name: str = os.getenv(
        "LLM_EMBED_MODEL_NAME", DEFAULT_LLM_EMBED_MODEL_NAME
    )
    llm_api_base: str = os.getenv("LLM_API_BASE")
    llm_temperature: float = os.getenv("LLM_TEMPERATURE", 0.0)
    llm_request_timeout: float = os.getenv("LLM_REQUEST_TIMEOUT", 300.0)

    def __post_init__(self):
        if not self.llm_api_base:
            logger.warning("LLM_API_BASE not found in env! Default will be used.")
