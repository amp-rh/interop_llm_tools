from dataclasses import dataclass

from llama_index.core.base.agent.types import BaseAgent as LmxBaseAgentRunner

from core.base.base_wrapper import BaseWrapper
from core.configs.agent_runner_config import AgentRunnerConfig
from mixins.from_config import FromConfigMixin


@dataclass
class AgentRunner(BaseWrapper[LmxBaseAgentRunner], FromConfigMixin[AgentRunnerConfig]):
    @classmethod
    def from_config(cls, config: AgentRunnerConfig) -> "AgentRunner":
        return cls(inner=config.runner_type(config.agent_worker))
