import random

import pytest

import interop_llm_tools.api


@pytest.fixture(autouse=True, scope="function")
def patch_chroma_collection_name(monkeypatch):
    collection_name = f"unit_{str(random.randint(0, 100_000)).zfill(6)}"
    monkeypatch.setenv("CHROMA_COLLECTION_NAME", collection_name)


def test_live_completion():
    api = interop_llm_tools.api.get_api()
    response = api.complete("say that this is a test")
    assert "test" in response


def test_live_knowledge_graph_query():
    api = interop_llm_tools.api.get_api()
    secret_number = random.randint(0, 10_000)
    api.update_knowledge_from_triplet("secret number", "is", secret_number)
    response = api.query("What is the secret number?")
    assert str(secret_number) in response


def test_live_ingestion_and_query(tmp_path):
    api = interop_llm_tools.api.get_api()
    secret_number = random.randint(0, 10_000)
    tmp_path.mkdir(exist_ok=True, parents=True)
    p = tmp_path / "secret_number_file.txt"
    p.write_text(f"the secret number is {secret_number}.")
    api.ingest_file(p)
    response = api.query("What is the secret number?")
    assert str(secret_number) in response
