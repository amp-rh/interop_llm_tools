from dataclasses import dataclass

from llama_index.core.base.llms.base import BaseLLM
from llama_index.embeddings.ollama import OllamaEmbedding

from interop_llm_tools.core.common.llm_api_type import LlmApiType
from interop_llm_tools.core.llm_config import LlmConfig

config = LlmConfig()


@dataclass
class Llm:
    inner: BaseLLM
    api_type: LlmApiType = config.llm_api_type

    def complete(self, prompt: str) -> str:
        return self.inner.complete(prompt=prompt).text

    @classmethod
    def from_env(cls) -> "Llm":
        inner: BaseLLM
        if config.llm_api_type is LlmApiType.OLLAMA:
            from llama_index.llms.ollama import Ollama

            return Llm(
                inner=Ollama(
                    model=config.llm_instruct_model_name,
                    base_url=config.llm_api_base,
                    temperature=config.llm_temperature,
                    request_timeout=config.llm_request_timeout,
                ),
                api_type=LlmApiType.OLLAMA,
            )
        else:
            raise NotImplemented()

    def get_embed_model(self):
        if self.api_type == LlmApiType.OLLAMA:
            return OllamaEmbedding(
                model_name=config.llm_embed_model_name, base_url=config.llm_api_base
            )
        raise NotImplemented()
