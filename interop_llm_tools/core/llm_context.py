import os
from dataclasses import dataclass
from pathlib import Path

from chromadb import EphemeralClient
from llama_index.core import (
    Settings,
    KnowledgeGraphIndex,
    StorageContext,
    SimpleDirectoryReader,
    VectorStoreIndex,
    SummaryIndex,
)
from llama_index.core.graph_stores import SimpleGraphStore
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import HierarchicalNodeParser
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import IndexNode
from llama_index.vector_stores.chroma import ChromaVectorStore

from interop_llm_tools.core.llm import Llm


@dataclass
class LlmContext:
    llm: Llm

    def __post_init__(self):
        Settings.llm = self.llm.inner
        Settings.embed_model = self.llm.get_embed_model()

        self.chroma_client = EphemeralClient()
        self.chroma_collection = self.chroma_client.create_collection(
            name=os.getenv("CHROMA_COLLECTION_NAME", "default")
        )

        self.vector_store = ChromaVectorStore(chroma_collection=self.chroma_collection)

        self.graph_store = SimpleGraphStore()

        self.storage_context = StorageContext.from_defaults(
            graph_store=self.graph_store,
            vector_store=self.vector_store,
        )

        self.vector_index = VectorStoreIndex.from_vector_store(
            vector_store=self.vector_store
        )

        self.kg_index = KnowledgeGraphIndex.from_documents(
            storage_context=self.storage_context, show_progress=True, documents=[]
        )

        self.summary_index = SummaryIndex(
            objects=[
                IndexNode(
                    index_id="vector",
                    obj=self.vector_index.as_retriever(similarity_top_k=2),
                    text="vector retriever",
                ),
                IndexNode(
                    index_id="knowledge",
                    obj=self.kg_index.as_retriever(similarity_top_k=2),
                    text="knowledge retriever",
                ),
            ]
        )

        self.query_engine = self.summary_index.as_query_engine()

    def ingest_file(self, path: Path):
        docs = SimpleDirectoryReader(input_files=[path]).load_data(show_progress=True)
        IngestionPipeline(
            vector_store=self.vector_store,
            transformations=[
                SentenceSplitter.from_defaults(chunk_size=1024),
                HierarchicalNodeParser.from_defaults(
                    chunk_sizes=[512, 256],
                    include_prev_next_rel=True,
                    include_metadata=False,
                ),
                Settings.embed_model,
            ],
        ).run(show_progress=True, documents=docs)
