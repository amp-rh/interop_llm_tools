from core.api.factory_api import FactoryApi, FactoryApiConfig
from interop_llm_tools.core.api import LlmApi, LlmApiConfig


def get_llm_api(config: LlmApiConfig = LlmApiConfig.from_env()):
    return LlmApi.from_config(config)


def get_factory_api(config: FactoryApiConfig = FactoryApiConfig.from_env()):
    return FactoryApi.from_config(config)
