import os

import phoenix as px
from phoenix.evals import HallucinationEvaluator, QAEvaluator, LiteLLMModel
from phoenix.evals import run_evals
from phoenix.trace import SpanEvaluations

import interop_llm_tools.config

config = interop_llm_tools.config.get_config()
llm = LiteLLMModel(
    model_name="ollama/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
    model_kwargs={
        "base_url": config.default_llm_api_base_url
    },
    temperature=0.0,
)

df = px.Client().get_spans_dataframe('name == "query"')

df["input"] = df["attributes.input.value"]
df["output"] = df["attributes.output.value"]
df["reference"] = ""

hallucination_evaluator = HallucinationEvaluator(llm)
qa_evaluator = QAEvaluator(llm)

hallucination_eval_df, qa_eval_df = run_evals(
    dataframe=df,
    evaluators=[hallucination_evaluator, qa_evaluator],
    provide_explanation=True,
)

px.Client().log_evaluations(
    SpanEvaluations(eval_name="Hallucination", dataframe=hallucination_eval_df),
    SpanEvaluations(eval_name="QA Correctness", dataframe=qa_eval_df),
)
