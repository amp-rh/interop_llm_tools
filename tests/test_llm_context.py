from interop_llm_tools.core.llm_context import LlmContext


def test_init_llm_context(llm):
    assert isinstance(LlmContext(llm=llm), LlmContext)
