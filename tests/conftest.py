import os
import random
from dataclasses import dataclass
from pathlib import Path

import pytest

from api import get_factory_api, get_jira_api


@pytest.fixture
def factory_api():
    yield get_factory_api()


@pytest.fixture
def simple_file_path(tmp_path):
    tmp_path.mkdir(exist_ok=True, parents=True)
    p = tmp_path.with_name("my-doc.txt")
    p.write_text("Hello, World!")
    yield p


@pytest.fixture
def secret_numbers(tmp_path) -> list:
    @dataclass
    class SecretNumberDoc:
        path: Path
        value: int = random.randint(0, 999_999_999)

        def __post_init__(self):
            self.path.write_text(f"the secret number is {self.value}")

        @property
        def str(self) -> str:
            return str(self.value)

    d = tmp_path.joinpath("secret_numbers")
    d.mkdir(exist_ok=True, parents=True)
    docs = []
    for i in range(10):
        p = d.joinpath(f"secret_number_{i}")
        docs.append(SecretNumberDoc(path=p))
    return docs


@pytest.fixture
def jira_api(jira_issue_keys):
    yield get_jira_api()


@pytest.fixture
def jira_issue_keys():
    env_var_name = "TEST_JIRA_ISSUE_KEYS"
    issue_keys = os.getenv(env_var_name)
    assert (
        issue_keys
    ), f"please set {env_var_name} to run this test. use comma-separated values (no spaces)."
    return issue_keys.split(",")


@pytest.fixture
def static_test_resources_dir():
    p = Path(__file__).with_name("test_resources")
    assert p.is_dir()
    return p


@pytest.fixture
def static_config_dir(monkeypatch, static_test_resources_dir):
    p = static_test_resources_dir.joinpath("configs")
    monkeypatch.setenv("CONFIG_DIR", p.as_posix())
    assert p.is_dir()
    return p


@pytest.fixture
def static_model_services_config_path(static_config_dir):
    p = static_config_dir / "model_services.yaml"
    assert p.is_file()
