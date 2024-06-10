import os
from dataclasses import dataclass

from interop_llm_tools.core.base import BaseLanguageModelConfig
from interop_llm_tools.mixins.from_env import FromEnvMixin


@dataclass
class InstructModelConfig(BaseLanguageModelConfig, FromEnvMixin):
    temperature: float

    @classmethod
    def from_env(cls) -> "InstructModelConfig":
        return cls(
            model_name=os.getenv("LLM_INSTRUCT_MODEL_NAME"),
            temperature=float(os.getenv("LLM_INSTRUCT_MODEL_TEMPERATURE", 0.0)),
            base_api_url=os.getenv("LLM_CLIENT_API_BASE"),
        )
