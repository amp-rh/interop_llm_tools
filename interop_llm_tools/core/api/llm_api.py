from dataclasses import dataclass

from llama_index.core import Settings
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.embeddings.ollama import OllamaEmbedding

from core.base.base_api import BaseApi
from core.configs.embed_model_config import EmbedModelConfig
from core.configs.llm_api_config import LlmApiConfig
from core.data_models import LlmClient
from mixins.from_config import FromConfigMixin
from mixins.from_env import FromDefaultsMixin


@dataclass
class LlmApi(BaseApi, FromConfigMixin[LlmApiConfig], FromDefaultsMixin):
    client: LlmClient
    embed_model: BaseEmbedding

    def __post_init__(self):
        Settings.llm = self.client.inner
        Settings.embed_model = self.embed_model
        Settings.callback_manager = self.client.inner.callback_manager

    async def acomplete(self, prompt: str) -> str:
        resp = await self.client.inner.acomplete(prompt=prompt)
        return resp.text

    @classmethod
    def get_embed_model(cls, client: LlmClient, config: EmbedModelConfig):
        if client.client_type == client.client_type.OLLAMA:
            return OllamaEmbedding(
                model_name=config.model_name, base_url=config.base_api_url
            )

    @classmethod
    def from_config(cls, config: LlmApiConfig) -> "LlmApi":
        client = LlmClient.from_config(config=config.client_config)
        embed_model = cls.get_embed_model(
            client=client, config=config.embed_model_config
        )
        return cls(
            client=client,
            embed_model=embed_model,
        )

    @classmethod
    def from_defaults(cls) -> "LlmApi":
        return cls.from_config(config=LlmApiConfig.from_defaults())
