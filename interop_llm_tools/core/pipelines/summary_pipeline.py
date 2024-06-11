from dataclasses import dataclass

from core.api.pipeline_api import PipelineApi
from core.base.base_prompt_template import BasePromptTemplate
from core.prompt_templates.summarize import SummarizePromptTemplate


@dataclass
class SummaryPipeline(PipelineApi):
    prompt_template_cls: BasePromptTemplate = SummarizePromptTemplate

    async def arun(self, context: str) -> str:
        return await super().arun(context=context)
