from dataclasses import dataclass
from typing import Sequence

from llama_index.core import VectorStoreIndex
from llama_index.core.ingestion.pipeline import (
    IngestionPipeline as LmxIngestionPipeline,
)
from llama_index.core.readers.base import BaseReader
from llama_index.core.schema import BaseNode

from core.base.base_wrapper import BaseWrapper


@dataclass
class IngestionPipeline(BaseWrapper[LmxIngestionPipeline]):
    reader: BaseReader

    async def aget_nodes(self) -> Sequence[BaseNode]:
        return await self.inner.arun(
            show_progress=True,
            documents=await self.reader.aload_data(show_progress=True),
        )

    async def ato_index(self) -> VectorStoreIndex:
        return VectorStoreIndex(
            nodes=await self.aget_nodes(),
            show_progress=True,
        )
