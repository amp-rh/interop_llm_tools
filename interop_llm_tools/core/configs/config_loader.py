import abc
import os
import re
from dataclasses import dataclass
from pathlib import Path

import yaml

DEFAULT_CONFIG_DIR = Path(__file__).with_name("default_configs").as_posix()


@dataclass
class BaseUserConfig(abc.ABC):
    raw: dict

    @classmethod
    @abc.abstractmethod
    def from_raw(cls, raw_config_dict: dict) -> "BaseUserConfig": ...

    def get(self, k: str):
        return self.raw.get(k)


@dataclass
class ModelService:
    client_type: str = None
    base_api_url: str = None
    request_timeout: float = None
    instruct_model_name: str = None
    embed_model_name: str = None
    temperature: float = None


@dataclass
class DataSource:
    data_loader: str = None
    data_loader_inputs: dict = None


@dataclass
class ModelServicesConfig(BaseUserConfig):
    default_config = {}

    def get(self, k: str):
        return ModelService(**self.raw.get(k))

    @classmethod
    def from_raw(cls, d: dict[str, any]) -> "ModelServicesConfig":
        raw = d.get("model_services", cls.default_config)
        return cls(raw=raw)


@dataclass
class DataSourcesConfig(BaseUserConfig):
    default_config = {}

    def get(self, k: str):
        return DataSource(**self.raw.get(k))

    @classmethod
    def from_raw(cls, d: dict) -> "DataSourcesConfig":
        raw = d.get("data_sources", cls.default_config)
        return cls(raw=raw)


@dataclass
class LoadedConfigs:
    model_services: ModelServicesConfig
    data_sources: DataSourcesConfig

    @classmethod
    def from_raw(cls, raw_configs_dict: dict):
        return cls(
            model_services=ModelServicesConfig.from_raw(raw_configs_dict),
            data_sources=DataSourcesConfig.from_raw(raw_configs_dict),
        )


@dataclass
class ConfigLoader:
    @classmethod
    def load_configs(cls) -> LoadedConfigs:
        d = {}
        env_pat = re.compile(r"\$\w+")
        for p in cls.get_config_dir().iterdir():
            t = p.read_text()
            if not t:
                continue
            for m in env_pat.findall(t):
                t = cls._inject_from_env(m, t)
            for k, v in yaml.safe_load(t).items():
                d.update({k: v})
        return LoadedConfigs.from_raw(d)

    @classmethod
    def _inject_from_env(cls, m, t):
        k = str(m).removeprefix("$")
        v = os.getenv(k)
        if v is None:
            raise ValueError(
                f"environment variable specified in loaded config files was not found: {k}"
            )
        t = t.replace(m, v)
        return t

    @classmethod
    def get_config_dir(cls) -> Path:
        p = Path(os.getenv("CONFIG_DIR", DEFAULT_CONFIG_DIR))
        p.mkdir(exist_ok=True, parents=True)
        return p


get_configs = ConfigLoader.load_configs
