import logging
from typing import Optional, Sequence

import pydantic
from llama_index.core import (
    ChatPromptTemplate,
    PromptTemplate,
    get_response_synthesizer,
)
from llama_index.core import Response
from llama_index.core.agent import (
    CustomSimpleAgentWorker,
    Task,
    AgentChatResponse,
)
from llama_index.core.base.base_query_engine import BaseQueryEngine
from llama_index.core.base.llms.types import ChatMessage, MessageRole
from llama_index.core.base.response.schema import (
    StreamingResponse,
    AsyncStreamingResponse,
    PydanticResponse,
)
from llama_index.core.bridge.pydantic import Field, BaseModel, PrivateAttr
from llama_index.core.output_parsers import PydanticOutputParser
from llama_index.core.program import LLMTextCompletionProgram
from llama_index.core.query_engine import (
    SubQuestionQueryEngine,
)
from llama_index.core.response_synthesizers import ResponseMode
from llama_index.core.tools import QueryEngineTool

from core.prompts import Prompts

DEFAULT_PROMPT_STR = Prompts.default_eval_prompt

type RawMessageSequence = tuple[str, str]

type AgentResponseWithTaskDoneFlag = tuple[AgentChatResponse, bool]

type AgentStateDict = dict[str, int | list[any]]

type AgentReasoningChatPair = list[tuple[str, any] | tuple[str, str]]

type AgentQueryResponse = Response | StreamingResponse | AsyncStreamingResponse | PydanticResponse

type AgentRouterInputResponsePair = tuple[any, AgentQueryResponse]


class ResponseEval(BaseModel):
    """Evaluation of the response"""

    question_answered: bool = Field(
        ..., description="Whether the question was completely answered."
    )
    new_question: Optional[str] = Field(
        "",
        description="The suggested new question, if question_answered is False.",
    )
    explanation: str = Field(
        ...,
        description=(
            "The explanation for question_answered as well as for the new question."
        ),
    )


logger = logging.getLogger(__name__)
logger.info("initialized logger")


class RetryWorker(CustomSimpleAgentWorker):
    prompt_str: str = DEFAULT_PROMPT_STR
    max_iterations: int = 10
    _root_query_engine: BaseQueryEngine = PrivateAttr(...)

    def __init__(
        self,
        tools: Sequence[QueryEngineTool],
        prompt_str: str = DEFAULT_PROMPT_STR,
        max_iterations: int = 10,
        **kwargs,
    ):
        super().__init__(tools=tools, **kwargs)

        self.max_iterations = max_iterations
        self.prompt_str = prompt_str

        self._root_query_engine = SubQuestionQueryEngine.from_defaults(
            verbose=True,
            query_engine_tools=tools,
            response_synthesizer=get_response_synthesizer(
                response_mode=ResponseMode.COMPACT_ACCUMULATE,
                verbose=True,
                structured_answer_filtering=True,
            ),
        )

    def _initialize_state(self, task: Task, **kwargs: any) -> AgentStateDict:
        return {"count": 0, "current_reasoning": []}

    def _run_step(
        self, state: AgentStateDict, task: Task, input: Optional[str] = None
    ) -> AgentResponseWithTaskDoneFlag:
        new_input = self._get_new_input_from_task_state(state, task)
        response = self._get_response(new_input)
        new_reasoning = self._get_new_reasoning(new_input, response)
        current_reasoning = self._extend_current_reasoning(new_reasoning, state)
        chat_prompt_tmpl = self._get_update_chat_prompt_template(
            self.prompt_str, current_reasoning
        )
        try:
            response_eval = self._get_response_eval(
                chat_prompt_tmpl, new_input, response
            )
            state["new_input"] = response_eval.new_question
        except pydantic.v1.error_wrappers.ValidationError as e:
            logger.error(e)
            response_eval = None

        state["count"] += 1

        logger.info(f"iteration {state["count"]} of {self.max_iterations} complete.")

        is_done = False
        if state["count"] >= self.max_iterations:
            is_done = True
        elif response_eval:
            is_done = response_eval.question_answered

        return AgentChatResponse(response=str(response)), is_done

    def _get_response_eval(self, chat_prompt_tmpl, new_input, response):
        llm_program = LLMTextCompletionProgram.from_defaults(
            output_parser=PydanticOutputParser(output_cls=ResponseEval),
            prompt=chat_prompt_tmpl,
            llm=self.llm,
        )
        response_eval = llm_program(
            query_str=new_input, response_str=response, verbose=True
        )
        return response_eval

    @staticmethod
    def _extend_current_reasoning(new_reasoning, state):
        (res := state["current_reasoning"]).extend(new_reasoning)
        logger.info(f"new reasoning: {new_reasoning}")
        return res

    @staticmethod
    def _get_new_reasoning(new_input, response) -> AgentReasoningChatPair:
        return [("user", new_input), ("assistant", str(response))]

    @staticmethod
    def _get_new_input_from_task_state(state, task):
        new_input = state.get("new_input", task.input)
        return new_input

    @staticmethod
    def _get_update_chat_prompt_template(
        system_prompt: str, current_reasoning: RawMessageSequence
    ) -> ChatPromptTemplate | PromptTemplate:
        messages = [ChatMessage(role=MessageRole.SYSTEM, content=system_prompt)]
        for role_str, content in current_reasoning:
            role = MessageRole.USER if role_str == "user" else MessageRole.ASSISTANT
            messages.append(ChatMessage(role=role, content=content))
        return ChatPromptTemplate(message_templates=messages)

    def _get_response(self, query) -> AgentQueryResponse:
        response = self._root_query_engine.query(query)
        return response

    def _finalize_task(self, state: dict[str, any], **kwargs: any) -> None:
        pass
