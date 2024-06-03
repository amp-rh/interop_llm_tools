import random

import llama_index.core as lmx
import phoenix as px
import pytest

from interop_llm_tools.api import get_llm_api, get_factory_api


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
        assert "test" in (await self.aget_responses_from_traces()).pop()

    @pytest.mark.asyncio
    async def test_factory_api_functionality(
        self, secret_number, secret_number_document_path
    ):
        api = get_factory_api()
        agent = await api.aget_document_agent(document_path=secret_number_document_path)
        resp = await agent.aquery("what is the secret number?")
        assert str(secret_number) in resp.response

    @staticmethod
    async def aget_responses_from_traces():
        async def aget_spans_df(max_retries=20, i=0):
            df = px.active_session().get_spans_dataframe()
            if i >= max_retries:
                return df
            if df.empty:
                return await aget_spans_df(i=i + 1)
            return df

        spans_df = await aget_spans_df()
        return spans_df["attributes.output.value"].to_list()
