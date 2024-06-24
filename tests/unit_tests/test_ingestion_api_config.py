import pytest

from core.configs.ingestion_api_config import IngestionApiConfig


@pytest.fixture(autouse=True)
def setup_env(jira_issue_keys, monkeypatch, static_config_dir):
    monkeypatch.setenv("TEST_JIRA_ISSUE_KEY_ONE", jira_issue_keys.pop())
    monkeypatch.setenv("TEST_JIRA_ISSUE_KEY_TWO", jira_issue_keys.pop())


def test_init_from_loaded_global_configs():
    assert isinstance(
        IngestionApiConfig.from_loaded_configs("my_jira_tickets"), IngestionApiConfig
    )
