from typing import Any, Optional, Tuple

from llama_index.core.agent import CustomSimpleAgentWorker
from llama_index.core.base.agent.types import Task, Task as LmxTask
from llama_index.core.base.llms.types import ChatMessage, MessageRole
from llama_index.core.chat_engine.types import AgentChatResponse
from llama_index.core.query_engine import (
    RouterQueryEngine,
)
from llama_index.core.tools import QueryEngineTool
from llama_index.core.utils import print_text


class BaseAgentWorker(CustomSimpleAgentWorker):
    root_query_engine: RouterQueryEngine = None
    tools: list[QueryEngineTool]

    def __init__(self, tools: list[QueryEngineTool], llm, **kwargs):
        super().__init__(tools=tools, llm=llm, **kwargs)

        if len(self.tools):
            router_query_engine = RouterQueryEngine.from_defaults(
                query_engine_tools=tools, llm=llm
            )

            tools.append(
                QueryEngineTool.from_defaults(
                    query_engine=router_query_engine,
                    name="router_query_engine_tool",
                    description="ALWAYS use this tool.",
                    resolve_input_errors=True,
                ),
            )

            self.root_query_engine = router_query_engine

    def _initialize_state(self, task: Task, **kwargs: Any) -> dict[str, Any]:
        return {}

    def _run_step(
        self, state: dict[str, Any], task: LmxTask, input: Optional[str] = None
    ) -> Tuple[AgentChatResponse, bool]:
        print_text(
            "\n========== Running Step ==========", color="llama_lavender", end="\n"
        )
        print_text(f"user: {task.input}", color="blue", end="\n")

        user_message = ChatMessage(content=task.input, role=MessageRole.USER)

        if self.root_query_engine:
            response = self.root_query_engine.query(task.input).response
        else:
            chat_history = task.memory.get_all() or []
            chat_history.extend([user_message])
            response = self.llm.chat(chat_history).message.content

        print_text(f"agent: {response}", color="green", end="\n")

        is_done = True
        if is_done:
            state["memory"].put(user_message)
            state["memory"].put(
                ChatMessage(content=response, role=MessageRole.ASSISTANT)
            )
        return AgentChatResponse(response=response), is_done

    async def _arun_step(
        self, state: dict[str, Any], task: LmxTask, input: Optional[str] = None
    ) -> Tuple[AgentChatResponse, bool]:
        print_text(
            "\n========== Running Step ==========", color="llama_lavender", end="\n"
        )
        print_text(f"user: {task.input}", color="blue", end="\n")

        user_message = ChatMessage(content=task.input, role=MessageRole.USER)

        if self.root_query_engine:
            response = (await self.root_query_engine.aquery(task.input)).response
        else:
            chat_history = task.memory.get_all() or []
            chat_history.extend([user_message])
            response = (await self.llm.achat(chat_history)).message.content

        print_text(f"agent: {response}", color="green", end="\n")

        is_done = True
        # TODO: Add response evaluation and retry logic
        if is_done:
            state["memory"].put(user_message)
            state["memory"].put(
                ChatMessage(content=response, role=MessageRole.ASSISTANT)
            )
        return AgentChatResponse(response=response), is_done

    def _finalize_task(self, state: dict[str, Any], **kwargs: Any) -> None:
        pass
