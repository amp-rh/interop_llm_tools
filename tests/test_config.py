from interop_llm_tools.core.config import Config, get_config
from interop_llm_tools.core.llm import Llm


def test_init_config():
    assert isinstance(Config(), Config)


def test_get_config():
    assert isinstance(get_config(), Config)


def test_get_default_llm(config):
    assert isinstance(config, Config)
    assert isinstance(config.get_default_llm(), Llm)
