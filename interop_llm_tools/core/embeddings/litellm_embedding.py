from typing import Optional

import litellm
from llama_index.core.base.embeddings.base import Embedding
from llama_index.core.embeddings import BaseEmbedding


class LiteLLMEmbedding(BaseEmbedding):
    api_base: Optional[str]
    api_key: Optional[str]

    def __init__(
        self,
        model: str,
        api_base: Optional[str] = None,
        api_key: Optional[str] = None,
        **kwargs
    ):
        super().__init__(model_name=model, api_base=api_base, api_key=api_key, **kwargs)

    def _get_query_embedding(self, query: str) -> Embedding:
        return litellm.embedding(
            model=self.model_name,
            api_base=self.api_base,
            api_key=self.api_key,
            input=[query],
        )["data"][0]["embedding"]

    async def _aget_query_embedding(self, query: str) -> Embedding:
        return litellm.embedding(
            model=self.model_name,
            api_base=self.api_base,
            api_key=self.api_key,
            input=[query],
        )["data"][0]["embedding"]

    async def _aget_text_embedding(self, text: str) -> Embedding:
        return litellm.embedding(
            model=self.model_name,
            api_base=self.api_base,
            api_key=self.api_key,
            input=[text],
        )["data"][0]["embedding"]

    def _get_text_embedding(self, text: str) -> Embedding:
        return litellm.embedding(
            model=self.model_name,
            api_base=self.api_base,
            api_key=self.api_key,
            input=[text],
        )["data"][0]["embedding"]
