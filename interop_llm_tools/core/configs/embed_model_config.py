from core.configs.config_loader import get_configs
from interop_llm_tools.core.base import BaseLanguageModelConfig


class EmbedModelConfig(BaseLanguageModelConfig):

    @classmethod
    def from_loaded_configs(cls, model_service_name):
        m = get_configs().model_services.get(model_service_name)
        return cls(
            model_name=m.embed_model_name,
            base_api_url=m.base_api_url,
        )
