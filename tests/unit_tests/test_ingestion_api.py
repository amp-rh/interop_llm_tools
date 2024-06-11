from core.api.configs.ingestion_api_config import IngestionApiConfig
from core.api.ingestion_api import IngestionApi


def test_init_ingestion_api():
    assert isinstance(IngestionApi(IngestionApiConfig.from_env()), IngestionApi)


def test_init_ingestion_api_from_config():
    assert isinstance(
        IngestionApi.from_config(IngestionApiConfig.from_env()), IngestionApi
    )


def test_init_ingestion_api_from_paths(simple_file_path):
    assert isinstance(IngestionApi.from_paths([simple_file_path]), IngestionApi)
