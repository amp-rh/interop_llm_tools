from dataclasses import dataclass
from pathlib import Path

from llama_index.core.ingestion.pipeline import (
    IngestionPipeline as LmxIngestionPipeline,
)

from core.api.configs.ingestion_api_config import IngestionApiConfig
from core.base.base_api import BaseApi
from core.data_models.ingestion_pipeline import IngestionPipeline
from mixins.from_config import FromConfigMixin


@dataclass
class IngestionApi(
    BaseApi,
    FromConfigMixin[IngestionApiConfig],
):
    config: IngestionApiConfig

    def get_ingestion_pipeline(self) -> IngestionPipeline:
        return IngestionPipeline(
            inner=LmxIngestionPipeline(
                transformations=[
                    self.config.splitter,
                    self.config.node_parser,
                    self.config.embed_model,
                ]
            ),
            reader=self.config.reader,
        )

    @classmethod
    def from_paths(cls, paths: list[Path]) -> "IngestionApi":
        return cls.from_config(IngestionApiConfig.from_paths(paths))

    @classmethod
    def from_config(cls, config: IngestionApiConfig) -> "IngestionApi":
        return cls(config=config)
