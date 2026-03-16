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


def test_ingest_then_query_retrieves_content(api, random_number_file_path, random_int):
    api.ingest_file(random_number_file_path)
    retriever = api.context.vector_index.as_retriever(similarity_top_k=2)
    nodes = retriever.retrieve("what is the secret number?")
    texts = [n.get_text() for n in nodes]
    assert any(str(random_int) in t for t in texts)


def test_knowledge_graph_triplet_is_retrievable(api):
    api.update_knowledge_from_triplet("Alice", "favorite color is", "blue")
    rel_map = api.context.kg_index.graph_store.get_rel_map()
    assert "Alice" in rel_map
    triplets = rel_map["Alice"]
    assert any(
        t[1] == "favorite color is" and t[2] == "blue" for t in triplets
    )


def test_multiple_file_ingestion_accumulates_in_store(api, tmp_path):
    file1 = tmp_path / "france.txt"
    file1.write_text("the capital of France is Paris")
    file2 = tmp_path / "physics.txt"
    file2.write_text("the speed of light is 299792458 meters per second")

    api.ingest_file(file1)
    api.ingest_file(file2)

    results = api.context.chroma_collection.get()
    all_docs = " ".join(results["documents"])
    assert "Paris" in all_docs
    assert "299792458" in all_docs


def test_chunking_produces_multiple_nodes(api, tmp_path):
    long_text = " ".join(
        f"Sentence number {i} contains some filler text to increase the document length."
        for i in range(500)
    )
    doc_file = tmp_path / "long_document.txt"
    doc_file.write_text(long_text)

    api.ingest_file(doc_file)

    chunk_count = api.context.chroma_collection.count()
    assert chunk_count > 1, f"Expected multiple chunks, got {chunk_count}"
