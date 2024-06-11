from api import (
    get_agent_api,
    get_factory_api,
    get_ingestion_api,
    get_jira_api,
    get_llm_api,
    get_pipeline_api,
)
from core.api.agent_api import AgentApi
from core.api.factory_api import FactoryApi
from core.api.ingestion_api import IngestionApi
from core.api.jira_api import JiraApi
from core.api.llm_api import LlmApi
from core.api.pipeline_api import PipelineApi


def test_get_llm_api():
    llm_api = get_llm_api()
    assert isinstance(llm_api, LlmApi)


def test_get_factory_api():
    assert isinstance(get_factory_api(), FactoryApi)


def test_get_agent_api():
    assert isinstance(get_agent_api(), AgentApi)


def test_get_jira_api():
    assert isinstance(get_jira_api(), JiraApi)


def test_get_ingestion_api():
    assert isinstance(get_ingestion_api(), IngestionApi)


def test_get_pipeline_api():
    assert isinstance(get_pipeline_api(), PipelineApi)
