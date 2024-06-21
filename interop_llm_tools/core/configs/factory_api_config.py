from dataclasses import dataclass

from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.llms import LLM

from core.api.llm_api import LlmApi
from core.base.base_api_config import BaseApiConfig
from mixins.from_env import FromDefaultsMixin


@dataclass
class FactoryApiConfig(BaseApiConfig, FromDefaultsMixin):
    llm_api: LlmApi
    embed_model: BaseEmbedding
    instruct_model: LLM

    @classmethod
    def from_defaults(cls):
        llm_api = LlmApi.from_defaults()
        return cls(
            llm_api=llm_api,
            embed_model=llm_api.embed_model,
            instruct_model=llm_api.client.inner,
        )
