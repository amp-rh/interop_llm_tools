from dataclasses import dataclass

from llama_index.core.base.agent.types import BaseAgentWorker as LmxBaseAgentWorker

from core.base.base_wrapper import BaseWrapper


@dataclass
class AgentWorker(BaseWrapper[LmxBaseAgentWorker]): ...
