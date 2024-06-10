import pytest

from api import get_factory_api
from core.api.agent_api import AgentApi


@pytest.fixture
def factory_api():
    yield get_factory_api()


@pytest.fixture
def simple_file_path(tmp_path):
    tmp_path.mkdir(exist_ok=True, parents=True)
    p = tmp_path.with_name("my-doc.txt")
    p.write_text("Hello, World!")
    yield p


@pytest.mark.asyncio
async def test_aget_document_agent_from_file_path_returns_agent_api(
    factory_api, simple_file_path
):
    agent = await factory_api.aget_document_agent(document_path=simple_file_path)
    assert isinstance(agent, AgentApi)


@pytest.mark.asyncio
async def test_aget_multi_document_agent_from_file_paths_returns_agent_api(
    factory_api, simple_file_path
):
    other_file_path = simple_file_path.with_name("other-doc.log")
    other_file_path.write_text("This is a test.")
    agent = await factory_api.aget_multi_document_agent(
        document_paths=[simple_file_path, other_file_path]
    )
    assert isinstance(agent, AgentApi)
