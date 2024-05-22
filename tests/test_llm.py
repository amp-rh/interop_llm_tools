from interop_llm_tools.core.llm import Llm


def test_init_llm(mock_generic_llm):
    assert isinstance(Llm(inner=mock_generic_llm), Llm)


def test_init_from_env():
    assert isinstance(Llm.from_env(), Llm)
