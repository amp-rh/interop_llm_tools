from core.api.agent_api import AgentApi
from core.api.configs.agent_api_config import AgentApiConfig
from core.api.configs.factory_api_config import FactoryApiConfig
from core.api.configs.ingestion_api_config import IngestionApiConfig
from core.api.configs.jira_api_config import JiraApiConfig
from core.api.configs.llm_api_config import LlmApiConfig
from core.api.configs.pipeline_api_config import PipelineApiConfig
from core.api.factory_api import FactoryApi
from core.api.ingestion_api import IngestionApi
from core.api.jira_api import JiraApi
from core.api.llm_api import LlmApi
from core.api.pipeline_api import PipelineApi


def get_llm_api(config: LlmApiConfig = LlmApiConfig.from_env()):
    return LlmApi.from_config(config=config)


def get_factory_api(config: FactoryApiConfig = FactoryApiConfig.from_env()):
    return FactoryApi.from_config(config=config)


def get_agent_api(config: AgentApiConfig = AgentApiConfig.from_env()):
    return AgentApi.from_config(config=config)


def get_jira_api(config: JiraApiConfig = JiraApiConfig.from_env()):
    return JiraApi.from_config(config=config)


def get_ingestion_api(config: IngestionApiConfig = IngestionApiConfig.from_env()):
    return IngestionApi.from_config(config=config)


def get_pipeline_api(config: PipelineApiConfig = PipelineApiConfig.from_env()):
    return PipelineApi.from_config(config=config)
