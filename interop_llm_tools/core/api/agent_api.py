from dataclasses import dataclass

from core.api.configs.agent_api_config import AgentApiConfig
from core.base.base_api import BaseApi
from core.data_models import AgentRunner, AgentWorker
from mixins.from_config import FromConfigMixin
from mixins.from_env import FromEnvMixin


@dataclass
class AgentApi(BaseApi, FromConfigMixin[AgentApiConfig], FromEnvMixin):
    agent_worker: AgentWorker
    agent_runner: AgentRunner

    async def aquery(self, query: str) -> str:
        resp = await self.agent_runner.inner.aquery(query)
        return resp.response

    def query(self, query: str) -> str:
        resp = self.agent_runner.inner.query(query)
        return resp.response

    async def achat(self, message: str) -> str:
        resp = await self.agent_runner.inner.achat(
            message=message, chat_history=self.agent_runner.inner.chat_history
        )
        return resp.response

    def chat(self, message: str):
        resp = self.agent_runner.inner.chat(
            message=message, chat_history=self.agent_runner.inner.chat_history
        )
        return resp.response

    def repl(self) -> None:
        self.agent_runner.inner.chat_repl()

    @classmethod
    def from_config(cls, config: AgentApiConfig) -> "AgentApi":
        agent_worker = AgentWorker(
            inner=config.worker_config.worker_type.from_tools(
                tools=config.worker_config.tools, verbose=True
            )
        )
        config.runner_config.agent_worker = agent_worker.inner
        agent_runner = AgentRunner.from_config(config.runner_config)
        return cls(agent_worker=agent_worker, agent_runner=agent_runner)

    @classmethod
    def from_env(cls) -> "AgentApi":
        return cls.from_config(config=AgentApiConfig.from_env())
