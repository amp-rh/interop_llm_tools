from dataclasses import dataclass
from pathlib import Path

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.agent import ParallelAgentRunner
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import (
    HierarchicalNodeParser,
    SemanticSplitterNodeParser,
)
from llama_index.core.tools import QueryEngineTool

from core.agent_workers.simple import SimpleAgentWorker
from core.api.agent_api import AgentApi
from core.api.configs.agent_api_config import AgentApiConfig
from core.api.configs.agent_runner_config import AgentRunnerConfig
from core.api.configs.agent_worker_config import AgentWorkerConfig
from core.api.configs.factory_api_config import FactoryApiConfig
from core.api.llm_api import LlmApi
from core.base.base_api import BaseApi


@dataclass
class FactoryApi(BaseApi):
    llm_api: LlmApi
    embed_model: BaseEmbedding

    @classmethod
    def from_config(cls, config: FactoryApiConfig) -> "FactoryApi":
        return cls(llm_api=config.llm_api, embed_model=config.embed_model)

    async def aget_document_agent(self, document_path: Path):
        doc_loader = SimpleDirectoryReader(input_files=[document_path])
        docs = await doc_loader.aload_data(show_progress=True)
        text_splitter = SemanticSplitterNodeParser.from_defaults(
            embed_model=self.embed_model
        )
        node_parser = HierarchicalNodeParser.from_defaults(
            chunk_sizes=[1024, 512, 256],
        )

        nodes = await IngestionPipeline(
            transformations=[text_splitter, node_parser, self.embed_model]
        ).arun(show_progress=True, documents=docs)

        index = VectorStoreIndex(nodes=nodes, show_progress=True)

        tools = [
            QueryEngineTool.from_defaults(
                query_engine=index.as_query_engine(),
                return_direct=True,
                resolve_input_errors=True,
            )
        ]

        agent = AgentApi.from_config(
            config=AgentApiConfig(
                runner_config=AgentRunnerConfig(runner_type=ParallelAgentRunner),
                worker_config=AgentWorkerConfig(
                    worker_type=SimpleAgentWorker, tools=tools
                ),
            )
        )
        return agent
