from interop_llm_tools.api import Api, get_api


def test_init_api(llm):
    assert isinstance(Api(llm=llm), Api)


def test_get_api():
    assert isinstance(get_api(), Api)


def test_api_completion(api):
    assert api.complete("Hello, World!") == 'Simply repeating: "Hello, World!"'


def test_add_to_knowledge(api):
    api.update_knowledge_from_triplet("Alice", "favorite color is", "blue")


def test_api_query(api):
    resp = api.query("say that this is a test")
    assert resp


def test_api_ingest_file(api, random_number_file_path):
    api.ingest_file(random_number_file_path)
