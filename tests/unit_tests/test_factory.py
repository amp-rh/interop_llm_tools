import pytest

from core.api.agent_api import AgentApi
from core.data_models.ingestion_pipeline import IngestionPipeline


@pytest.mark.asyncio
async def test_aget_document_agent_from_file_path_returns_agent_api(
    factory_api, simple_file_path
):
    assert isinstance(
        await factory_api.aget_document_agent(document_path=simple_file_path), AgentApi
    )


@pytest.mark.asyncio
async def test_aget_document_agent_from_file_path_ingested_data_available_to_queries(
    factory_api, secret_numbers
):
    secret_number = secret_numbers.pop()
    agent = await factory_api.aget_document_agent(document_path=secret_number.path)
    resp = (await agent.agent_runner.inner.aquery("secret number")).response
    assert secret_number.str in resp


@pytest.mark.asyncio
async def test_aget_multi_document_agent_from_file_paths_returns_agent_api(
    factory_api, simple_file_path
):
    other_file_path = simple_file_path.with_name("other-doc.log")
    other_file_path.write_text("This is a test.")
    assert isinstance(
        await factory_api.aget_multi_document_agent(
            document_paths=[simple_file_path, other_file_path]
        ),
        AgentApi,
    )


@pytest.mark.asyncio
async def test_aget_ingestion_pipeline_from_document_paths(
        factory_api, simple_file_path
):
    assert isinstance(
        await factory_api.aget_ingestion_pipeline_from_paths(
            document_paths=[simple_file_path]
        ),
        IngestionPipeline,
    )
