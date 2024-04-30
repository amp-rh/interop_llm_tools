from dataclasses import dataclass
from pathlib import Path

import chromadb
from llama_index.core import (
    Settings,
    SimpleDirectoryReader,
    VectorStoreIndex,
    set_global_handler,
)
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.tools import QueryEngineTool
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.litellm import LiteLLM
from llama_index.vector_stores.chroma import ChromaVectorStore

from core.agents.workers.retry_worker import (
    RetryWorker,
)
from core.prompts import Prompts
from interop_llm_tools.config import get_config

config = get_config()

ingest_dir = Path() / "ingest"
ingest_dir.mkdir(exist_ok=True, parents=True)


def main():
    chroma_client = chromadb.EphemeralClient()

    Settings.llm = llm = LiteLLM(
        api_base=config.default_llm_api_base_url,
        model="ollama/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
        temperature=0.0,
    )

    Settings.embed_model = embed_model = HuggingFaceEmbedding("BAAI/bge-large-en-v1.5")

    Settings.callback_manager = llm.callback_manager

    @dataclass
    class DocWrapper:
        path: Path
        name_safe: str
        description: str
        chunk_size: int = 1024
        chunk_overlap: int = 0
        num_workers: int = 4

        def to_nodes(self):
            _docs = SimpleDirectoryReader(input_files=[self.path]).load_data(
                show_progress=True, num_workers=self.num_workers
            )

            _nodes = SentenceSplitter(
                chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
            ).get_nodes_from_documents(documents=_docs, show_progress=True)

            return _nodes

    build_log_path = ingest_dir.joinpath("build-log.txt")

    docs = [
        DocWrapper(
            path=build_log_path,
            name_safe="build_log",
            description=f"""
            The Openshift CI build log artifact for the job run referenced in the user's query.
            Contains the following information:
                - Step names
                - Step results
                - Errors from steps
                - Stacktrace messages from steps
""",
        )
    ]

    tools = []

    for d in docs:
        chroma_collection = chroma_client.create_collection(name=d.name_safe)
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        nodes = IngestionPipeline(
            transformations=[embed_model],
            vector_store=vector_store,
        ).run(
            nodes=d.to_nodes(),
            show_progress=True,
        )
        index = VectorStoreIndex(vector_store=vector_store, nodes=nodes)
        tools.append(
            QueryEngineTool.from_defaults(
                query_engine=index.as_query_engine(),
                name=f"{d.name_safe}_tool",
                description=d.description,
                resolve_input_errors=True,
                return_direct=True,
            )
        )

    agent = RetryWorker.from_tools(
        tools=tools,
        llm=llm,
        verbose=True,
        max_iterations=3,
        prompt_str=Prompts.default_eval_prompt,
    ).as_agent()

    resp = agent.chat(message="Why did the job run fail?")
    print(resp)


if __name__ == "__main__":
    set_global_handler("arize_phoenix")
    main()
