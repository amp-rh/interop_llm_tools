from dataclasses import dataclass

from interop_llm_tools.core.base.base_api_config import BaseApiConfig
from interop_llm_tools.core.configs.embed_model_config import EmbedModelConfig
from interop_llm_tools.core.configs.instruct_model_config import InstructModelConfig
from interop_llm_tools.core.configs.llm_client_config import LlmClientConfig
from interop_llm_tools.mixins.from_env import FromDefaultsMixin

DEFAULT_MODEL_SERVICE = "default"


@dataclass
class LlmApiConfig(BaseApiConfig, FromDefaultsMixin):
    client_config: LlmClientConfig
    instruct_model_config: InstructModelConfig
    embed_model_config: EmbedModelConfig

    @classmethod
    def from_defaults(cls) -> "LlmApiConfig":
        return cls(
            client_config=LlmClientConfig.from_loaded_configs(
                model_service_name=DEFAULT_MODEL_SERVICE
            ),
            instruct_model_config=InstructModelConfig.from_loaded_configs(
                DEFAULT_MODEL_SERVICE
            ),
            embed_model_config=EmbedModelConfig.from_loaded_configs(
                DEFAULT_MODEL_SERVICE
            ),
        )
