from dataclasses import dataclass

from llama_index.core.base.llms.base import BaseLLM as LmxBaseLlmClient
from llama_index.core.llms import LLM
from llama_index.llms.ollama import Ollama

from core.api.configs.llm_client_config import LlmClientConfig, LlmClientType
from core.base.base_wrapper import BaseWrapper
from mixins.from_config import FromConfigMixin


@dataclass
class LlmClient(BaseWrapper[LmxBaseLlmClient | LLM], FromConfigMixin[LlmClientConfig]):
    client_type: LlmClientType = None

    @classmethod
    def from_config(cls, config: LlmClientConfig) -> "LlmClient":
        client_type = config.client_type
        if client_type == client_type.OLLAMA:
            return cls(inner=Ollama(**config.to_ollama_dict()), client_type=client_type)
