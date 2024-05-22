import random
from typing import Any, Sequence

import pytest
from llama_index.core.base.llms.base import BaseLLM
from llama_index.core.base.llms.types import (
    CompletionResponseAsyncGen,
    ChatMessage,
    ChatResponseAsyncGen,
    CompletionResponse,
    ChatResponse,
    CompletionResponseGen,
    ChatResponseGen,
    LLMMetadata,
)
from llama_index.core.base.query_pipeline.query import QueryComponent

from api import Api
from interop_llm_tools.core.config import Config
from interop_llm_tools.core.llm import Llm


@pytest.fixture
def random_number_file_path(tmp_path, random_int):
    p = tmp_path / "secret_number.txt"
    p.parent.mkdir(exist_ok=True, parents=True)
    p.write_text(f"the secret number is {random_int}")
    return p


@pytest.fixture
def random_int():
    return random.randint(0, 10_000)


@pytest.fixture
def mock_generic_llm():
    class MockGenericLlm(BaseLLM):
        @property
        def metadata(self) -> LLMMetadata:
            return LLMMetadata()

        def chat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
            raise NotImplemented

        def complete(
            self, prompt: str, formatted: bool = False, **kwargs: Any
        ) -> CompletionResponse:
            return CompletionResponse(text=f'Simply repeating: "{prompt}"')

        def stream_chat(
            self, messages: Sequence[ChatMessage], **kwargs: Any
        ) -> ChatResponseGen:
            raise NotImplemented

        def stream_complete(
            self, prompt: str, formatted: bool = False, **kwargs: Any
        ) -> CompletionResponseGen:
            raise NotImplemented

        async def achat(
            self, messages: Sequence[ChatMessage], **kwargs: Any
        ) -> ChatResponse:
            raise NotImplemented

        async def acomplete(
            self, prompt: str, formatted: bool = False, **kwargs: Any
        ) -> CompletionResponse:
            raise NotImplemented

        async def astream_chat(
            self, messages: Sequence[ChatMessage], **kwargs: Any
        ) -> ChatResponseAsyncGen:
            raise NotImplemented

        async def astream_complete(
            self, prompt: str, formatted: bool = False, **kwargs: Any
        ) -> CompletionResponseAsyncGen:
            raise NotImplemented

        def _as_query_component(self, **kwargs: Any) -> "QueryComponent":
            raise NotImplemented

        def predict(self, *args, **kwargs):
            return "mocked predict response"

    return MockGenericLlm()


@pytest.fixture(autouse=True, scope="function")
def patch_chroma_collection_name(monkeypatch):
    collection_name = f"unit_{str(random.randint(0, 100_000)).zfill(6)}"
    monkeypatch.setenv("CHROMA_COLLECTION_NAME", collection_name)


@pytest.fixture
def api(llm):
    return Api(llm=llm)


@pytest.fixture
def llm(mock_generic_llm):
    return Llm(inner=mock_generic_llm)


@pytest.fixture
def config() -> Config:
    return Config()
