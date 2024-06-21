from dataclasses import dataclass

from core.configs.config_loader import get_configs
from interop_llm_tools.core.base import BaseLanguageModelConfig
from interop_llm_tools.mixins.from_env import FromDefaultsMixin


@dataclass
class InstructModelConfig(BaseLanguageModelConfig, FromDefaultsMixin):
    temperature: float

    @classmethod
    def from_loaded_configs(cls, model_service_name: str):
        m = get_configs().model_services.get(model_service_name)
        return cls(
            temperature=m.temperature,
            model_name=m.instruct_model_name,
            base_api_url=m.base_api_url,
        )
