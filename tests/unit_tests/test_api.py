from api import get_agent_api, get_factory_api, get_llm_api
from core.api.agent_api import AgentApi
from core.api.factory_api import FactoryApi
from core.api.llm_api import LlmApi


def test_get_llm_api():
    llm_api = get_llm_api()
    assert isinstance(llm_api, LlmApi)


def test_get_factory_api():
    factory_api = get_factory_api()
    assert isinstance(factory_api, FactoryApi)


def test_get_agent_api():
    agent_api = get_agent_api()
    assert isinstance(agent_api, AgentApi)
