from dataclasses import dataclass
from pathlib import Path

from core.llm import Llm
from core.llm_context import LlmContext


@dataclass
class Api:
    llm: Llm

    def __post_init__(self):
        self.context = LlmContext(llm=self.llm)

    def complete(self, prompt: str) -> str:
        return self.llm.complete(prompt=prompt)

    def query(self, query: str) -> str:
        return self.context.query_engine.query(query).response

    def update_knowledge_from_triplet(self, subj: str, rel: str, obj: str):
        self.context.kg_index.graph_store.upsert_triplet(subj=subj, rel=rel, obj=obj)

    def ingest_file(self, path: Path):
        self.context.ingest_file(path)


def get_api(llm: Llm = None):
    llm = llm or Llm.from_env()
    return Api(llm=llm)
