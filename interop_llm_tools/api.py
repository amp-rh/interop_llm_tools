from core.api.agent_api import AgentApi
from core.api.configs.agent_api_config import AgentApiConfig
from core.api.configs.factory_api_config import FactoryApiConfig
from core.api.configs.llm_api_config import LlmApiConfig
from core.api.factory_api import FactoryApi
from core.api.llm_api import LlmApi


def get_llm_api(config: LlmApiConfig = LlmApiConfig.from_env()):
    return LlmApi.from_config(config=config)


def get_factory_api(config: FactoryApiConfig = FactoryApiConfig.from_env()):
    return FactoryApi.from_config(config=config)


def get_agent_api(config: AgentApiConfig = AgentApiConfig.from_env()):
    return AgentApi.from_config(config=config)
