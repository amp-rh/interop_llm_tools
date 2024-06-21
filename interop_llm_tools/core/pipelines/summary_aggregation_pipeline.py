from dataclasses import dataclass

from core.api.pipeline_api import PipelineApi
from core.base.base_prompt_template import BasePromptTemplate
from core.pipelines.condense_pipeline import CondensePipeline
from core.pipelines.summary_pipeline import SummaryPipeline
from core.prompt_templates.summarize import SummarizePromptTemplate


@dataclass
class SummaryAggregationPipeline(PipelineApi):
    prompt_template_cls: BasePromptTemplate = SummarizePromptTemplate
    condense_iterations = 1

    async def arun(self, contexts: list[str]) -> str:
        summary_pipeline = SummaryPipeline.from_defaults()
        condense_pipeline = CondensePipeline.from_defaults()

        async def summarize(s: str):
            return await summary_pipeline.arun(context=s)

        async def condense(s: str, i=0, m=self.condense_iterations):
            if i >= m:
                return s
            return await condense(await condense_pipeline.arun(context=s), i + 1)

        summaries = []
        for c in contexts:
            condensed_summary = await condense(await summarize(c))
            summaries.append(condensed_summary)

        return await condense(await summarize("\n\n".join(summaries)))
