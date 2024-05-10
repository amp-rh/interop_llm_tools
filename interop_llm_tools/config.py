import logging
import os
from dataclasses import dataclass

from dotenv import load_dotenv
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.litellm import LiteLLM

from core.embeddings.litellm_embedding import LiteLLMEmbedding

load_dotenv()

DEFAULT_LLM_API_BASE_ENV = "LLM_API_BASE"
DEFAULT_OLLAMA_API_BASE_ENV = "OLLAMA_API_BASE"
DEFAULT_OPENAI_API_BASE_ENV = "OPENAI_API_BASE"
DEFAULT_OPENAI_API_KEY_ENV = "OPENAI_API_KEY"

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
    ollama_default_instruct_model = "mistral-7b-instruct-v0.2.Q4_K_M.gguf"
    hugging_face_default_embed_model = "BAAI/bge-large-en-v1.5"

    def get_default_openai_instruct_llm(self):
        return LiteLLM(
            model=f"openai/{self.openai_default_instruct_model}",
            temperature=0.0,
            api_base=self.openai_api_base,
            api_key=self.openai_api_key,
            organization="",
        )

    def get_default_ollama_instruct_llm(self):
        return LiteLLM(
            api_base=self.default_llm_api_base_url,
            model=f"ollama/{self.ollama_default_instruct_model}",
            temperature=0.0,
        )

    def get_default_hugging_face_embedding(self):
        return HuggingFaceEmbedding(self.hugging_face_default_embed_model)

    def get_default_openai_embedding(self):
        return LiteLLMEmbedding(
            model=f"openai/{self.openai_default_embed_model}",
            api_base=self.openai_api_base,
            api_key=self.openai_api_key,
        )


def get_config() -> Config:
    return Config()
