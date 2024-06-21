from core.configs.llm_client_config import LlmClientConfig


def test_init_from_loaded_global_configs(static_config_dir):
    assert isinstance(LlmClientConfig.from_loaded_configs("ollama"), LlmClientConfig)
