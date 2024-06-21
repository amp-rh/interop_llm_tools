import enum
from dataclasses import dataclass

from core.configs.config_loader import get_configs


class LlmClientType(enum.Enum):
    OLLAMA = enum.auto()

    @classmethod
    def from_str(cls, s: str) -> "LlmClientType":
        for k, v in cls.__members__.items():
            if k.lower() == s.lower():
                return cls(value=v)


@dataclass
class LlmClientConfig:
    client_type: LlmClientType
    base_api_url: str
    request_timeout: float
    instruct_model_name: str
    embed_model_name: str
    temperature: float

    @classmethod
    def from_loaded_configs(cls, model_service_name: str):
        m = get_configs().model_services.get(model_service_name)
        return cls(
            client_type=LlmClientType.from_str(m.client_type),
            base_api_url=m.base_api_url,
            request_timeout=m.request_timeout,
            instruct_model_name=m.instruct_model_name,
            embed_model_name=m.embed_model_name,
            temperature=m.temperature,
        )

    def to_ollama_dict(self):
        return {
            "base_url": self.base_api_url,
            "model": self.instruct_model_name,
            "temperature": self.temperature,
            "request_timeout": self.request_timeout,
        }
