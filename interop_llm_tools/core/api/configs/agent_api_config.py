from dataclasses import dataclass

from core.api.configs.agent_runner_config import AgentRunnerConfig
from core.api.configs.agent_worker_config import AgentWorkerConfig
from core.base.base_api_config import BaseApiConfig
from mixins.from_env import FromEnvMixin


@dataclass
class AgentApiConfig(BaseApiConfig, FromEnvMixin):
    worker_config: AgentWorkerConfig
    runner_config: AgentRunnerConfig

    @classmethod
    def from_env(cls) -> "AgentApiConfig":
        worker_config = AgentWorkerConfig()
        runner_config = AgentRunnerConfig()
        return cls(
            worker_config=worker_config,
            runner_config=runner_config,
        )
