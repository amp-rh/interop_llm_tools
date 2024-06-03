from interop_llm_tools import api


def test_get_llm_api():
    llm_api = api.get_llm_api()
    assert isinstance(llm_api, api.LlmApi)


def test_get_factory_api():
    factory_api = api.get_factory_api()
    assert isinstance(factory_api, api.FactoryApi)
