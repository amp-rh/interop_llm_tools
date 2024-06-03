import os
from dataclasses import dataclass, field

from core.base import BaseLanguageModelConfig, BaseApiConfig, BaseApi
from core.common import LlmClientType
from core.data_models import LlmClient


@dataclass
class LlmClientConfig:
    client_type: LlmClientType
    base_api_url: str
    request_timeout: int


@dataclass
class InstructModelConfig(BaseLanguageModelConfig):
    model_name: str
    temperature: float


class EmbedModelConfig(BaseLanguageModelConfig):
    model_name: str


@dataclass
class LlmApiConfig(BaseApiConfig):
    client_config: LlmClientConfig
    instruct_model_config: InstructModelConfig
    embed_model_config: EmbedModelConfig

    @classmethod
    def from_env(cls):
        return cls(
            client_config=LlmClientConfig(
                client_type=LlmClientType.from_str(os.getenv("LLM_CLIENT_TYPE")),
                base_api_url=os.getenv("LLM_CLIENT_API_BASE"),
                request_timeout=int(os.getenv("LLM_REQUEST_TIMEOUT", 0)),
            ),
            instruct_model_config=InstructModelConfig(
                model_name=os.getenv("LLM_INSTRUCT_MODEL_NAME"),
                temperature=float(os.getenv("LLM_INSTRUCT_MODEL_TEMPERATURE", 0.0)),
            ),
            embed_model_config=EmbedModelConfig(
                model_name=os.getenv("LLM_EMBED_MODEL_NAME")
            ),
        )


@dataclass
class LlmApi(BaseApi[LlmApiConfig]):
    config: LlmApiConfig = field(default_factory=LlmApiConfig.from_env)
    client: LlmClient = None

    def __post_init__(self):
        if self.config.client_config.client_type is LlmClientType.OLLAMA:
            from llama_index.llms.ollama import Ollama

            inner = Ollama(
                model=self.config.instruct_model_config.model_name,
                base_url=self.config.client_config.base_api_url,
                temperature=self.config.instruct_model_config.temperature,
                request_timeout=self.config.client_config.request_timeout,
            )
        else:
            raise NotImplemented()
        self.client = LlmClient(inner=inner)

    @classmethod
    def from_config(cls, config: LlmApiConfig):
        return cls(config=config)

    def get_embed_model(self):
        if self.config.client_config.client_type is LlmClientType.OLLAMA:
            from llama_index.embeddings.ollama import OllamaEmbedding

            return OllamaEmbedding(
                base_url=self.config.client_config.base_api_url,
                model_name=self.config.embed_model_config.model_name,
            )
        raise NotImplemented

    async def acomplete(self, prompt):
        resp = await self.client.inner.acomplete(prompt)
        return resp.text
