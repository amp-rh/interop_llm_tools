import pytest
from llama_index.core.schema import Document

from core.data_loaders.jira_reader import JiraReader


def test_init_jira_reader():
    assert isinstance(JiraReader(), JiraReader)


@pytest.mark.asyncio
async def test_aload_data_returns_list_of_documents(jira_issue_key):
    docs = await JiraReader().aload_data(issue_keys=[jira_issue_key])
    assert isinstance(docs, list)
    assert isinstance(docs.pop(), Document)
