import time
from dataclasses import dataclass, field
from typing import Coroutine

from llama_index.core import get_response_synthesizer
from llama_index.core.base.base_query_engine import BaseQueryEngine
from llama_index.core.base.query_pipeline.query import Link
from llama_index.core.bridge.pydantic import BaseModel
from llama_index.core.query_pipeline import (
    InputComponent,
    ArgPackComponent,
    QueryPipeline as QP,
)
from llama_index.core.response_synthesizers import (
    BaseSynthesizer,
    ResponseMode,
)
from llama_index.core.schema import NodeWithScore, TextNode


@dataclass
class QueryPipeline:
    verbose: bool = True
    query_engines: dict[str, BaseQueryEngine] = field(default_factory=dict)
    links: list[Link] = field(
        default_factory=lambda: [
            Link(src="input", dest="summarizer", dest_key="query_str"),
            Link(src="join", dest="summarizer", dest_key="nodes"),
        ]
    )
    response_mode: ResponseMode = ResponseMode.COMPACT
    output_cls: BaseModel = None
    summarizer: BaseSynthesizer = None
    time_taken: float = None

    def __post_init__(self):
        if self.summarizer is None:
            self.summarizer = get_response_synthesizer(
                verbose=self.verbose,
                structured_answer_filtering=True,
                response_mode=self.response_mode,
                use_async=True,
            )
        for k, v in self.query_engines.items():
            self.links.append(Link(src="input", dest=k))
            self.links.append(Link(src=k, dest="join", dest_key=k))

    @property
    def module_dict(self):
        return {
            **self.query_engines,
            "input": InputComponent(),
            "summarizer": self.summarizer,
            "join": ArgPackComponent(
                convert_fn=lambda x: NodeWithScore(node=TextNode(text=str(x)))
            ),
        }

    async def arun(self, input: str) -> Coroutine:
        start_time = time.time()
        resp = await self.to_llama_index_query_pipeline().arun(input=input)
        self.time_taken = time.time() - start_time
        return resp

    def to_llama_index_query_pipeline(self) -> QP:
        return QP(verbose=self.verbose, modules=self.module_dict, links=self.links)
