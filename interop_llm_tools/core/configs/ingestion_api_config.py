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
from core.configs.config_loader import get_configs
from core.data_loaders.jira_reader import JiraReader
from mixins.from_env import FromDefaultsMixin


@dataclass
class IngestionApiConfig(BaseApiConfig, FromDefaultsMixin):
    embed_model: BaseEmbedding = field(
        default_factory=lambda: LlmApi.from_defaults().embed_model
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
        return cls.from_defaults(reader=SimpleDirectoryReader(input_files=paths))

    @classmethod
    def from_defaults(
        cls,
        reader=BaseReader(),
    ) -> "IngestionApiConfig":
        return cls(
            reader=reader,
        )

    @classmethod
    def from_loaded_configs(cls, data_source_name: str) -> "IngestionApiConfig":
        def _parse_data_loader_class_from_name(n) -> type[JiraReader]:
            match n.lower():
                case "jira_reader":
                    return JiraReader
                case _:
                    raise ValueError(
                        f'data_loader defined in data_source "{data_source_name}" '
                        f"could not be matched to a valid Reader class"
                    )

        ds = get_configs().data_sources.get(data_source_name)
        reader = _parse_data_loader_class_from_name(ds.data_loader).from_inputs(
            ds.data_loader_inputs
        )
        return cls(reader=reader)
