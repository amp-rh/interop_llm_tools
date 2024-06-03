from dataclasses import dataclass
from pathlib import Path

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.agent import ReActAgentWorker
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import (
    HierarchicalNodeParser,
    SemanticSplitterNodeParser,
)
from llama_index.core.tools import QueryEngineTool

from interop_llm_tools.core.base import BaseApiConfig, BaseApi
from .llm_api import LlmApi, LlmApiConfig


@dataclass
class FactoryApiConfig(BaseApiConfig):
    llm_api: LlmApi = None

    def __post_init__(self):
        self.embed_model = self.llm_api.get_embed_model()
        self.instruct_model = self.llm_api.client.inner

    @classmethod
    def from_env(cls):
        return FactoryApiConfig(
            llm_api=LlmApi.from_config(config=LlmApiConfig.from_env())
        )


@dataclass
class FactoryApi(BaseApi[FactoryApiConfig]):
    config: FactoryApiConfig

    def __post_init__(self):
        Settings.llm = self.config.instruct_model
        Settings.embed_model = self.config.embed_model

    @classmethod
    def from_config(cls, config):
        return cls(config=config)

    async def aget_document_agent(self, document_path: Path):
        doc_loader = SimpleDirectoryReader(input_files=[document_path])
        docs = await doc_loader.aload_data(show_progress=True)
        text_splitter = SemanticSplitterNodeParser.from_defaults(
            embed_model=self.config.embed_model
        )
        node_parser = HierarchicalNodeParser.from_defaults(
            chunk_sizes=[1024, 512, 256],
        )

        nodes = await IngestionPipeline(
            transformations=[text_splitter, node_parser, self.config.embed_model]
        ).arun(show_progress=True, documents=docs)

        index = VectorStoreIndex(nodes=nodes, show_progress=True)

        agent = ReActAgentWorker.from_tools(
            llm=self.config.instruct_model,
            tools=[QueryEngineTool.from_defaults(query_engine=index.as_query_engine())],
            verbose=True,
        ).as_agent()
        return agent
