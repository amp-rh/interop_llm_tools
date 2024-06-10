import os

from interop_llm_tools.core.base import BaseLanguageModelConfig
from interop_llm_tools.mixins.from_env import FromEnvMixin


class EmbedModelConfig(BaseLanguageModelConfig, FromEnvMixin):
    @classmethod
    def from_env(cls) -> "EmbedModelConfig":
        return cls(
            model_name=os.getenv("LLM_EMBED_MODEL_NAME"),
            base_api_url=os.getenv("LLM_CLIENT_API_BASE"),
        )
