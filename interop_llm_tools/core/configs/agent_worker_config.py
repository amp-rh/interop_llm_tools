from dataclasses import dataclass, field

from llama_index.core.tools import BaseTool

from core.agent_workers.simple import SimpleAgentWorker
from core.base.base_agent_worker import BaseAgentWorker


@dataclass
class AgentWorkerConfig:
    tools: list[BaseTool] = field(default_factory=list)
    worker_type: type[BaseAgentWorker] = SimpleAgentWorker
