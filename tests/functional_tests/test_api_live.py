import random

import llama_index.core as lmx
import phoenix as px
import pytest

from interop_llm_tools.api import get_agent_api, get_factory_api, get_llm_api


@pytest.fixture(autouse=True)
def init_tracing():
    px.launch_app()
    lmx.set_global_handler("arize_phoenix")


@pytest.fixture
def secret_number():
    yield random.randint(1, 999_999)


@pytest.fixture
def secret_number_document_path(tmp_path, secret_number):
    p = tmp_path / "secret_number.txt"
    p.write_text(f"the secret number is {secret_number}")
    yield p


class TestApi:
    @pytest.mark.asyncio
    async def test_llm_api_functionality(self):
        api = get_llm_api()
        resp = await api.acomplete("say that this is a test")
        assert "test" in resp

    @pytest.mark.asyncio
    async def test_factory_api_functionality_with_changing_contexts(
        self, secret_number, secret_number_document_path
    ):
        api = get_factory_api()
        agent = await api.aget_document_agent(document_path=secret_number_document_path)
        resp = await agent.aquery("what is the secret number?")
        assert str(secret_number) in resp

        second_secret_number = 123 - secret_number

        second_secret_number_document_path = secret_number_document_path.with_name(
            "other_doc.json"
        )
        second_secret_number_document_path.write_text(
            '{"secret_number": ' + str(second_secret_number) + "}"
        )

        agent = await api.aget_multi_document_agent(
            document_paths=[
                secret_number_document_path,
                second_secret_number_document_path,
            ]
        )
        resp = await agent.aquery("what are the two secret numbers?")
        assert str(secret_number) in resp
        assert str(second_secret_number) in resp

    @pytest.mark.asyncio
    async def test_agent_api_functionality(self):
        agent = get_agent_api()
        resp = await agent.achat('repeat the following: "this is a test"')
        assert "test" in resp
        # test chat history is available to agent
        resp = await agent.achat("what was the last thing you said?")
        assert "test" in resp
