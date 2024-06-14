from dataclasses import dataclass, field
from pathlib import Path

from llama_index.core import SimpleDirectoryReader
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.node_parser import (
    HierarchicalNodeParser,
    SemanticSplitterNodeParser,
)
from llama_index.core.readers.base import BaseReader

from core.api.llm_api import LlmApi
from core.base.base_api_config import BaseApiConfig
from mixins.from_env import FromEnvMixin


@dataclass
class IngestionApiConfig(BaseApiConfig, FromEnvMixin):
    embed_model: BaseEmbedding = field(
        default_factory=lambda: LlmApi.from_env().embed_model
    )
    splitter: SemanticSplitterNodeParser = None
    node_parser: HierarchicalNodeParser = field(
        default_factory=lambda: HierarchicalNodeParser.from_defaults(
            chunk_sizes=[1024, 512, 256]
        )
    )
    reader: BaseReader | SimpleDirectoryReader = field(default_factory=BaseReader)

    def __post_init__(self):
        self.splitter = self.splitter or SemanticSplitterNodeParser.from_defaults(
            embed_model=self.embed_model
        )

    @classmethod
    def from_paths(cls, paths: list[Path]) -> "IngestionApiConfig":
        return cls.from_env(reader=SimpleDirectoryReader(input_files=paths))

    @classmethod
    def from_env(
        cls,
        reader=BaseReader(),
    ) -> "IngestionApiConfig":
        return cls(
            reader=reader,
        )