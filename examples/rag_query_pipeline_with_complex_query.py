import asyncio
import logging
import os
import sys
from pathlib import Path

import chromadb
import requests
from llama_index.core import (
    Settings,
    SimpleDirectoryReader,
    get_response_synthesizer,
    VectorStoreIndex,
    set_global_handler,
)
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.core.query_pipeline import (
    QueryPipeline,
)
from llama_index.core.response_synthesizers import ResponseMode
from llama_index.core.schema import BaseNode
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.litellm import LiteLLM
from llama_index.vector_stores.chroma import ChromaVectorStore

import interop_llm_tools.config
from interop_llm_tools.core.pipelines.query_pipeline import QueryPipeline


async def main():
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

    print(llm)

    def get_index_query_engine_from_nodes(
        nodes: list[BaseNode], chroma_collection_name
    ):
        chroma_collection = chroma_client.create_collection(name=chroma_collection_name)
        vector_store = ChromaVectorStore(chroma_collection)
        nodes = IngestionPipeline(
            transformations=[
                embed_model,
            ],
            vector_store=vector_store,
        ).run(nodes=nodes, show_progress=True)
        index = VectorStoreIndex(vector_store=vector_store, nodes=nodes)
        return index.as_query_engine()

    def get_prow_job_doc_tool(
        job_name_short,
        job_name_full,
        job_build_number,
        nodes,
        doc_name,
        doc_contents_description,
    ):
        tool_name = f"{job_name_short}_{job_build_number}_{doc_name}"
        for n in nodes:
            n.metadata.update(
                {
                    "full_name": job_name_full,
                    "build_number": job_build_number,
                    "product_name": job_name_short,
                }
            )
        qe = get_index_query_engine_from_nodes(nodes, chroma_collection_name=tool_name)
        metadata = ToolMetadata(
            name=tool_name,
            description=f"""
            The {doc_name} document contains the following information for the Redhat product \"{job_name_short}\":
            {doc_contents_description.strip()}
            """,
        )

        qe_tool = QueryEngineTool(query_engine=qe, metadata=metadata)
        return qe_tool

    def get_build_log_tool(
        job_name_short,
        job_name_full,
        job_build_number,
        doc_url,
        chunk_size,
        chunk_overlap=0,
        ingest_dir: Path = ingest_dir,
    ):
        r = requests.get(doc_url)
        file_name = "build-log.txt"
        p = ingest_dir / file_name
        p.write_text(r.text)
        docs = SimpleDirectoryReader(input_files=[p]).load_data(show_progress=True)
        nodes = SentenceSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        ).get_nodes_from_documents(documents=docs, show_progress=True)
        return get_prow_job_doc_tool(
            job_name_short=job_name_short,
            job_name_full=job_name_full,
            job_build_number=job_build_number,
            nodes=nodes,
            doc_name="build_log",
            doc_contents_description="""
            - Top-level reasons for test failures
            - Logged messages
            - Pod Failures
            - Timestamps
            """,
        )

    def get_finished_json_tool(
        job_name_short,
        job_name_full,
        job_build_number,
        doc_url,
        ingest_dir: Path = ingest_dir,
    ):
        r = requests.get(doc_url)
        file_name = "finished.json"
        p = ingest_dir / file_name
        p.write_text(r.text)
        docs = SimpleDirectoryReader(input_files=[p]).load_data()
        nodes = SentenceSplitter().get_nodes_from_documents(documents=docs)
        return get_prow_job_doc_tool(
            job_name_short=job_name_short,
            job_name_full=job_name_full,
            job_build_number=job_build_number,
            nodes=nodes,
            doc_name="finished_json",
            doc_contents_description="""
            - Overall Prow job run result (FAILURE or SUCCESS)
            - The Prow job workspace name
            - The Openshift release (4.14, 4.15, 4.16, etc.)
            """,
        )

    def get_prow_job_run_tools(
        job_name_short,
        job_name_full,
        job_build_number,
        artifacts_url_root=os.getenv("OSCI_ARTIFACTS_ROOT_URL"),
        default_chunk_size=1024,
    ):
        artifacts_url = f"{artifacts_url_root}/{job_name_full}/{job_build_number}/"
        build_log_url = artifacts_url + "build-log.txt"
        finished_json_url = artifacts_url + "finished.json"
        kw = {
            "job_name_short": job_name_short,
            "job_name_full": job_name_full,
            "job_build_number": job_build_number,
        }

        tools = [
            get_build_log_tool(
                **kw, doc_url=build_log_url, chunk_size=default_chunk_size
            ),
            get_finished_json_tool(**kw, doc_url=finished_json_url),
        ]
        return tools

    job_name_short = os.getenv("TEST_JOB_NAME_SHORT")
    job_name_full = os.getenv("TEST_JOB_NAME_FULL")
    job_build_number = os.getenv("TEST_JOB_BUILD_NUMBER")

    default_chunk_size = 1024

    query = f"""You are a specialized agent designed to answer queries about Openshift CI test runs for the Redhat product "{job_name_short}".
    If you do not know the answer to the question, simply say so.
    Use only the current context to generate your responses. If you are unable to find any matching sources, say that you do not have the information available.

    Answer the following:
        - What was the result of the most recent Prow job run for {job_name_short}?

    If the test failed, also answer the following using only on the output of the Prow job build log:
        - Of the steps that failed, why did they most likely fail?
        - What errors are present in the build log and how can they errors be remedied?
        - Why did the Prow job run fail?
        - Which steps should be investigated further, if any?
        - Were any JIRA tickets created or mentioned in the build log?

    Finally, review your findings and respond in valid Markdown format with the following information:

    # Test Report for `{job_name_short}`

    ## Job Name
    `{job_name_full}`

    ## Build Number
    `{job_build_number}`

    ## Result
    `[overall_result]`

    ## JIRA tickets:
    - `[jira_ticket_1]` ([relation])
    - `[jira_ticket_2]` ([relation])
    - `[jira_ticket_3]` ([relation])
    - etc...

    [if the result was a failure, also include the following, below]
    ## Failure Details

    ### Classification
    `[infrastructure_failure_or_test_failure]`

    #### Reason 
    [short_failure_reason]

    ### Summary of Findings
    [detailed_summary_of_findings_as_bulleted_list]

    ### Errors Observed
      - [error_1_short_description]
        - [error_1_possible_causes_as_list]
      - [error_2_short_description]
        - [error_2_possible_causes_as_list]
      - etc...

    ### Recommended Actions for Remediation:
      - [recommended_action_1]
      - [recommended_action_2]
      - [recommended_action_3]
      - etc...
    """

    job_run_tools = get_prow_job_run_tools(
        job_name_short=job_name_short,
        job_name_full=job_name_full,
        job_build_number=job_build_number,
        default_chunk_size=default_chunk_size,
    )

    sub_question_qe = SubQuestionQueryEngine.from_defaults(
        query_engine_tools=job_run_tools, use_async=True
    )

    p = QueryPipeline(
        verbose=True,
        summarizer=get_response_synthesizer(
            response_mode=ResponseMode.COMPACT_ACCUMULATE,
            llm=llm,
            structured_answer_filtering=True,
            use_async=True,
        ),
        query_engines={"sub_question_qe": sub_question_qe},
    )

    resp = await p.arun(input=query)

    Path(f"{job_name_short}_{job_build_number}_report.md").write_text(resp.response)
    print(resp)
    print(f"Time taken: {p.time_taken}")


if __name__ == "__main__":
    set_global_handler("arize_phoenix")
    asyncio.run(main())
