from dataclasses import dataclass

from llama_index.core.base.llms.base import BaseLLM as LmxBaseLlmClient
from llama_index.core.llms import LLM

from core.base.wrapper import BaseWrapper


@dataclass
class LlmClient(BaseWrapper[LmxBaseLlmClient | LLM]): ...
