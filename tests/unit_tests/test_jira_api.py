from core.api.jira_api import JiraApi


def test_init_jira_api():
    assert isinstance(JiraApi(), JiraApi)


def test_init_jira_api_from_env():
    assert isinstance(JiraApi.from_defaults(), JiraApi)


def test_get_jira_issue_by_key(jira_api, jira_issue_keys):
    key = jira_issue_keys.pop()
    issue = jira_api.get_issue(key=key)
    assert issue.key == key
