from dataclasses import dataclass, field
from typing import ClassVar

from core.api.jira_api import JiraApi
from core.pipelines.summary_pipeline import SummaryPipeline
from core.prompt_templates.summarize import SummarizePromptTemplate


@dataclass
class JiraIssueSummaryPipeline(SummaryPipeline):
    prompt_template_cls = SummarizePromptTemplate
    jira_api: ClassVar = field(default=JiraApi.from_defaults())

    async def arun(self, jira_issue_key: str) -> str:
        return await super().arun(
            context=await self.get_context_from_jira_issue_key(jira_issue_key)
        )

    async def get_context_from_jira_issue_key(self, jira_issue_key):
        return self.jira_api.get_issue(jira_issue_key).to_str()
