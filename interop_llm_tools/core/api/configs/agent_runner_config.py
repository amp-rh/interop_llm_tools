from dataclasses import dataclass

from llama_index.core.agent import ParallelAgentRunner
from llama_index.core.agent.runner.base import BaseAgentRunner
from llama_index.core.base.agent.types import BaseAgentWorker as LmxBaseAgentWorker
from llama_index.core.callbacks import CallbackManager


@dataclass
class AgentRunnerConfig:
    runner_type: type[BaseAgentRunner] = ParallelAgentRunner
    agent_worker: LmxBaseAgentWorker | CallbackManager = None
