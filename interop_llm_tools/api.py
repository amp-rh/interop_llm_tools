from core.api.agent_api import AgentApi
from core.api.factory_api import FactoryApi
from core.api.ingestion_api import IngestionApi
from core.api.jira_api import JiraApi
from core.api.llm_api import LlmApi
from core.api.pipeline_api import PipelineApi
from core.configs.agent_api_config import AgentApiConfig
from core.configs.factory_api_config import FactoryApiConfig
from core.configs.ingestion_api_config import IngestionApiConfig
from core.configs.jira_api_config import JiraApiConfig
from core.configs.llm_api_config import LlmApiConfig
from core.configs.pipeline_api_config import PipelineApiConfig


def get_llm_api(config: LlmApiConfig = LlmApiConfig.from_defaults()):
    return LlmApi.from_config(config=config)


def get_factory_api(config: FactoryApiConfig = FactoryApiConfig.from_defaults()):
    return FactoryApi.from_config(config=config)


def get_agent_api(config: AgentApiConfig = AgentApiConfig.from_defaults()):
    return AgentApi.from_config(config=config)


def get_jira_api(config: JiraApiConfig = JiraApiConfig.from_defaults()):
    return JiraApi.from_config(config=config)


def get_ingestion_api(config: IngestionApiConfig = IngestionApiConfig.from_defaults()):
    return IngestionApi.from_config(config=config)


def get_pipeline_api(config: PipelineApiConfig = PipelineApiConfig.from_defaults()):
    return PipelineApi.from_config(config=config)
