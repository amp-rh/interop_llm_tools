from dataclasses import dataclass
from pathlib import Path

import nest_asyncio
from llama_index.core.agent import ParallelAgentRunner
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.tools import QueryEngineTool

from core.agent_workers.simple import SimpleAgentWorker
from core.api.agent_api import AgentApi
from core.api.configs.agent_api_config import AgentApiConfig
from core.api.configs.agent_runner_config import AgentRunnerConfig
from core.api.configs.agent_worker_config import AgentWorkerConfig
from core.api.configs.factory_api_config import FactoryApiConfig
from core.api.configs.pipeline_api_config import PipelineApiConfig
from core.api.ingestion_api import IngestionApi
from core.api.llm_api import LlmApi
from core.base.base_api import BaseApi
from core.data_models.ingestion_pipeline import IngestionPipeline
from core.pipelines.jira_issue_summary_pipeline import JiraIssueSummaryPipeline
from core.pipelines.summary_pipeline import SummaryPipeline


@dataclass
class FactoryApi(BaseApi):
    llm_api: LlmApi
    embed_model: BaseEmbedding

    @classmethod
    def from_config(cls, config: FactoryApiConfig) -> "FactoryApi":
        return cls(llm_api=config.llm_api, embed_model=config.embed_model)

    @staticmethod
    async def aget_ingestion_pipeline_from_paths(
        document_paths: list[Path],
    ) -> IngestionPipeline:
        return IngestionApi.from_paths(document_paths).get_ingestion_pipeline()

    async def aget_document_agent(self, document_path: Path):
        ingestion_pipeline = await self.aget_ingestion_pipeline_from_paths(
            [document_path]
        )
        index = await ingestion_pipeline.ato_index()

        agent = AgentApi.from_config(
            config=AgentApiConfig(
                runner_config=AgentRunnerConfig(runner_type=ParallelAgentRunner),
                worker_config=AgentWorkerConfig(
                    worker_type=SimpleAgentWorker,
                    tools=[
                        QueryEngineTool.from_defaults(
                            query_engine=index.as_query_engine(),
                            resolve_input_errors=True,
                            name=f"{document_path.name}_tool",
                            description=f"Provides information about the document {document_path.name}",
                        )
                    ],
                ),
            )
        )
        return agent

    async def aget_multi_document_agent(self, document_paths: list[Path]):
        nest_asyncio.apply()

        tools = []

        for p in document_paths:
            agent = (await self.aget_document_agent(document_path=p)).agent_runner.inner
            tools.append(
                QueryEngineTool.from_defaults(
                    query_engine=agent,
                    name=f"{p.name}_agent_tool",
                    description=f"Provides information about the document {p.name}",
                )
            )

        root_agent = AgentApi.from_config(
            config=AgentApiConfig(
                runner_config=AgentRunnerConfig(runner_type=ParallelAgentRunner),
                worker_config=AgentWorkerConfig(
                    worker_type=SimpleAgentWorker, tools=tools
                ),
            )
        )
        return root_agent

    @staticmethod
    def get_summary_pipeline() -> SummaryPipeline:
        return SummaryPipeline.from_config(
            config=PipelineApiConfig(
                agent_api=AgentApi.from_config(AgentApiConfig.from_env()),
            )
        )

    @staticmethod
    def get_jira_issue_summary_pipeline() -> JiraIssueSummaryPipeline:
        return JiraIssueSummaryPipeline.from_config(
            config=PipelineApiConfig(
                agent_api=AgentApi.from_config(AgentApiConfig.from_env())
            )
        )
