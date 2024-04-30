import asyncio
import logging
import sys
import time
from pathlib import Path

import chromadb
from llama_index.core import (
    Settings,
    SimpleDirectoryReader,
    VectorStoreIndex, set_global_handler,
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.query_pipeline import (
    QueryPipeline,
    InputComponent,
    ArgPackComponent,
)
from llama_index.core.response_synthesizers import TreeSummarize
from llama_index.core.schema import NodeWithScore, TextNode
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.litellm import LiteLLM

import interop_llm_tools.config

chroma_client = chromadb.EphemeralClient()
logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

config = interop_llm_tools.config.get_config()
Settings.llm = llm = LiteLLM(
    api_base=config.default_llm_api_base_url,
    model="ollama/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
    temperature=0.0,
)

Settings.embed_model = embed_model = HuggingFaceEmbedding("BAAI/bge-large-en-v1.5")

Settings.callback_manager = llm.callback_manager

ingest_dir = Path() / "ingest"
ingest_dir.mkdir(exist_ok=True, parents=True)

chunk_sizes = [128, 256, 512, 1024]
query_engines = {}

for chunk_size in chunk_sizes:
    reader = SimpleDirectoryReader(input_files=[ingest_dir.joinpath("build-log.txt")])
    documents = reader.load_data()
    splitter = SentenceSplitter(chunk_size=chunk_size, chunk_overlap=0)
    nodes = splitter.get_nodes_from_documents(documents)
    vector_index = VectorStoreIndex(nodes)
    query_engines[str(chunk_size)] = vector_index.as_query_engine(llm=llm)


async def main():
    p = QueryPipeline(verbose=True)
    module_dict = {
        **query_engines,
        "input": InputComponent(),
        "summarizer": TreeSummarize(),
        "join": ArgPackComponent(
            convert_fn=lambda x: NodeWithScore(node=TextNode(text=str(x)))
        ),
    }

    p.add_modules(module_dict)

    for chunk_size in chunk_sizes:
        p.add_link("input", str(chunk_size))
        p.add_link(str(chunk_size), "join", dest_key=str(chunk_size))
    p.add_link("join", "summarizer", dest_key="nodes")
    p.add_link("input", "summarizer", dest_key="query_str")

    start_time = time.time()
    response = await p.arun(input="What was the primary reason that this Openshift CI test run failed?")
    print(str(response))
    end_time = time.time()
    print(f"Time taken: {end_time - start_time}")

if __name__ == "__main__":
    set_global_handler("arize_phoenix")
    asyncio.run(main())
