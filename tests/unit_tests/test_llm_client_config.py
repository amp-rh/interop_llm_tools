from core.configs.llm_client_config import LlmClientConfig


def test_init_from_default_loaded_global_configs():
    assert isinstance(LlmClientConfig.from_loaded_configs("default"), LlmClientConfig)
