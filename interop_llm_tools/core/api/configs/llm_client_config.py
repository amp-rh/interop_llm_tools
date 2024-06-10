import enum
import os
from dataclasses import dataclass

from interop_llm_tools.mixins.from_env import FromEnvMixin


class LlmClientType(enum.Enum):
    OLLAMA = enum.auto()

    @classmethod
    def from_str(cls, s: str) -> "LlmClientType":
        for k, v in cls.__members__.items():
            if k.lower() == s.lower():
                return cls(value=v)


@dataclass
class LlmClientConfig(FromEnvMixin):
    client_type: LlmClientType
    base_api_url: str
    request_timeout: int
    model_name: str
    temperature: float

    @classmethod
    def from_env(cls) -> "LlmClientConfig":
        return cls(
            client_type=LlmClientType.from_str(os.getenv("LLM_CLIENT_TYPE")),
            base_api_url=os.getenv("LLM_CLIENT_API_BASE"),
            request_timeout=int(os.getenv("LLM_REQUEST_TIMEOUT", 0)),
            model_name=os.getenv("LLM_INSTRUCT_MODEL_NAME"),
            temperature=os.getenv("LLM_INSTRUCT_MODEL_TEMPERATURE", 0.0),
        )

    def to_ollama_dict(self):
        return {
            "base_url": self.base_api_url,
            "model": self.model_name,
            "temperature": self.temperature,
            "request_timeout": self.request_timeout,
        }
