from core.api.configs.pipeline_api_config import PipelineApiConfig
from core.api.pipeline_api import PipelineApi
from core.pipelines.jira_issue_summary_pipeline import JiraIssueSummaryPipeline


def test_init_pipeline_from_config():
    assert isinstance(
        PipelineApi.from_config(PipelineApiConfig.from_env()), PipelineApi
    )


def test_init_pipeline_from_env():
    assert isinstance(PipelineApi.from_env(), PipelineApi)


def test_init_jira_issue_summary_pipeline_from_config():
    assert isinstance(
        JiraIssueSummaryPipeline.from_config(PipelineApiConfig.from_env()),
        JiraIssueSummaryPipeline,
    )


def test_init_jira_issue_summary_pipeline_from_env():
    assert isinstance(JiraIssueSummaryPipeline.from_env(), JiraIssueSummaryPipeline)
