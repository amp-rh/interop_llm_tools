import pytest

from api import get_llm_api


class TestLlmApi:
    @pytest.mark.asyncio
    async def test_get_llm_api_and_acomplete(self):
        api = get_llm_api()
        resp = await api.acomplete("say that this is a test")
        assert "test" in resp
