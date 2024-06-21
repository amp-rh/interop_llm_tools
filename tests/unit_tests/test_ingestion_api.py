from core.api.ingestion_api import IngestionApi
from core.configs.ingestion_api_config import IngestionApiConfig


def test_init_ingestion_api():
    assert isinstance(
        IngestionApi(config=IngestionApiConfig.from_defaults()), IngestionApi
    )


def test_init_ingestion_api_from_config():
    assert isinstance(
        IngestionApi.from_config(config=IngestionApiConfig.from_defaults()),
        IngestionApi,
    )


def test_init_ingestion_api_from_paths(simple_file_path):
    assert isinstance(IngestionApi.from_paths([simple_file_path]), IngestionApi)
