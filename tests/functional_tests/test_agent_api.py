import pytest

from api import get_agent_api


class TestAgentApi:
    @pytest.mark.asyncio
    async def test_agent_chat_history(self):
        agent = get_agent_api()
        resp = await agent.achat('repeat the following: "this is a test"')
        assert "test" in resp
        resp = await agent.achat("what was the last thing you said?")
        assert "test" in resp
