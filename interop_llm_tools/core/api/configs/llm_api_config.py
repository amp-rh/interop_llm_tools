from dataclasses import dataclass

from interop_llm_tools.core.api.configs.embed_model_config import EmbedModelConfig
from interop_llm_tools.core.api.configs.instruct_model_config import InstructModelConfig
from interop_llm_tools.core.api.configs.llm_client_config import LlmClientConfig
from interop_llm_tools.core.base.base_api_config import BaseApiConfig
from interop_llm_tools.mixins.from_env import FromEnvMixin


@dataclass
class LlmApiConfig(BaseApiConfig, FromEnvMixin):
    client_config: LlmClientConfig
    instruct_model_config: InstructModelConfig
    embed_model_config: EmbedModelConfig

    @classmethod
    def from_env(cls) -> "LlmApiConfig":
        return cls(
            client_config=LlmClientConfig.from_env(),
            instruct_model_config=InstructModelConfig.from_env(),
            embed_model_config=EmbedModelConfig.from_env(),
        )
