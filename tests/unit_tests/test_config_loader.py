from pathlib import Path

import pytest

from core.configs.config_loader import (
    ConfigLoader,
    DataSource,
    DataSourcesConfig,
    LoadedConfigs,
    ModelServicesConfig,
    get_configs,
)


@pytest.fixture(autouse=True)
def setup_env(jira_issue_keys, monkeypatch):
    monkeypatch.setenv("TEST_JIRA_ISSUE_KEY_ONE", jira_issue_keys.pop())
    monkeypatch.setenv("TEST_JIRA_ISSUE_KEY_TWO", jira_issue_keys.pop())


@pytest.fixture
def loaded_configs(loaded_configs_from_test_resources):
    return loaded_configs_from_test_resources


def test_init_config_loader():
    assert isinstance(ConfigLoader(), ConfigLoader)


def test_get_config_dir_returns_existing_dir():
    config_dir = ConfigLoader.get_config_dir()
    assert config_dir, "a path should be returned"
    assert Path(
        ConfigLoader.get_config_dir()
    ).is_dir(), "a default config dir should exist or be created"


def test_get_config_dir_from_env_creates_dir(monkeypatch, tmp_path):
    tmp_config_dir = tmp_path / "configs"
    monkeypatch.setenv("CONFIG_DIR", tmp_config_dir.as_posix())
    assert not tmp_config_dir.exists(), "config dir should not be created yet"
    config_dir_from_cls = Path(ConfigLoader.get_config_dir())
    assert (
        config_dir_from_cls == tmp_config_dir
    ), "config dir from cls should match config dir from env"
    assert tmp_config_dir.is_dir(), "config dir should be created"


def test_load_configs_from_static_config_dir(static_config_dir):
    assert isinstance(ConfigLoader.load_configs(), LoadedConfigs)


def test_loaded_configs_has_model_services_config(static_config_dir):
    assert isinstance(get_configs().model_services, ModelServicesConfig)


def test_model_services_config(static_config_dir):
    assert "ollama" in get_configs().model_services.raw.keys()


def test_get_model_services_from_global_configs():
    assert isinstance(get_configs().model_services, ModelServicesConfig)


def test_get_data_sources_from_global_configs(static_config_dir):
    assert isinstance(get_configs().data_sources, DataSourcesConfig)


def test_get_data_source_objects_by_name_from_loaded_configs(static_config_dir):
    data_sources = get_configs().data_sources
    ds = data_sources.get("my_jira_tickets")
    assert isinstance(ds, DataSource)
