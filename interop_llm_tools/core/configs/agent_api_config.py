from dataclasses import dataclass

from core.base.base_api_config import BaseApiConfig
from core.configs.agent_runner_config import AgentRunnerConfig
from core.configs.agent_worker_config import AgentWorkerConfig
from mixins.from_env import FromDefaultsMixin


@dataclass
class AgentApiConfig(BaseApiConfig, FromDefaultsMixin):
    worker_config: AgentWorkerConfig
    runner_config: AgentRunnerConfig

    @classmethod
    def from_defaults(cls) -> "AgentApiConfig":
        worker_config = AgentWorkerConfig()
        runner_config = AgentRunnerConfig()
        return cls(
            worker_config=worker_config,
            runner_config=runner_config,
        )
