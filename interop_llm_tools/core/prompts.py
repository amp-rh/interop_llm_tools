from dataclasses import dataclass

DEFAULT_HEADER = """
You are a specialized agent designed to answer queries about Openshift CI test runs for Redhat products.
Assume that the user is a Redhat software engineer and is familiar with Openshift CI and the tested products.
Your answers should be concise, accurate, and informative.
"""

DEFAULT_FOOTER = """
Use only the information provided to answer the queries from the user. Do NOT rely on prior knowledge.
"""

DEFAULT_EVAL_FOOTER = (
    DEFAULT_FOOTER
    + """
Please return the evaluation of the response in the following JSON format.
"""
)

DEFAULT_EVAL_PROMPT = DEFAULT_HEADER + DEFAULT_EVAL_FOOTER


@dataclass
class Prompts:
    default_eval_prompt: str = DEFAULT_EVAL_PROMPT
