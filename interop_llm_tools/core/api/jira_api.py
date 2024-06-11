import os
import pprint
from dataclasses import asdict, dataclass
from json import JSONDecodeError

import requests
from requests import Response

from core.api.configs.jira_api_config import JiraApiConfig
from core.base.base_api import BaseApi
from mixins.from_config import FromConfigMixin
from mixins.from_env import FromEnvMixin


@dataclass
class JiraIssue:
    key: str
    _id: str = None
    project_url: str = None
    created_dt: str = None
    updated_dt: str = None
    labels: list[str] = None
    status_name: str = None
    status_url: str = None
    components: list[any] = None
    attachment: list[any] = None
    description: str = None
    creator: any = None
    reporter: any = None
    subtasks: list[any] = None
    summary: str = None
    progress: any = None
    comment: any = None
    issue_links: list[any] = None
    issue_type: str = None

    @classmethod
    def from_dict(cls, d: dict) -> "JiraIssue":
        key = d["key"]
        _id = d["id"]

        fields = d["fields"]
        status = fields["status"]

        project_url = fields["project"]["self"]
        created_dt = fields["created"]
        labels = fields["labels"]
        components = fields["components"]
        attachment = fields["attachment"]
        description = fields["description"]
        creator = fields["creator"]
        reporter = fields["reporter"]
        subtasks = fields["subtasks"]
        progress = fields["progress"]
        comment = fields["comment"]
        updated_dt = fields["updated"]
        issue_links = fields["issuelinks"]
        issue_type = fields["issuetype"]["name"]

        status_name = status["name"]
        status_url = status["self"]

        return cls(
            key=key,
            _id=_id,
            project_url=project_url,
            created_dt=created_dt,
            labels=labels,
            status_name=status_name,
            status_url=status_url,
            components=components,
            attachment=attachment,
            description=description,
            creator=creator,
            reporter=reporter,
            subtasks=subtasks,
            progress=progress,
            comment=comment,
            updated_dt=updated_dt,
            issue_links=issue_links,
            issue_type=issue_type,
        )

    def to_dict(self) -> dict[str, any]:
        return asdict(self)

    def to_str(self) -> str:
        return pprint.pformat(self.to_dict())


@dataclass
class JiraApi(BaseApi, FromConfigMixin[JiraApiConfig], FromEnvMixin):
    domain_url: str = None
    session: requests.Session = requests.session()

    def _get(self, url: str) -> Response:
        return self.session.get(url=url)

    def _get_json(self, url: str):
        resp = self._get(url)
        try:
            return resp.json()
        except JSONDecodeError as e:
            # TODO: Add logger
            print(f"failed to parse JSON response from {resp.url}")

    def get_issue(self, key: str) -> JiraIssue:
        return JiraIssue.from_dict(
            self._get_json(f"{self.domain_url}/rest/api/2/issue/{key}")
        )

    @classmethod
    def from_config(cls, config: JiraApiConfig) -> "JiraApi":
        return cls.from_env()

    @classmethod
    def from_env(cls) -> "JiraApi":
        domain_url_env_key = "JIRA_DOMAIN_URL"
        jira_token_env_key = "JIRA_TOKEN"

        domain_url = os.getenv(domain_url_env_key, "").strip("/")
        jira_token = os.getenv(jira_token_env_key, "")

        env_err_msg = "please set {0} to use the JIRA API"
        assert domain_url, env_err_msg.format(domain_url_env_key)
        assert jira_token, env_err_msg.format(jira_token_env_key)

        session = requests.session()
        session.headers.update(
            {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {jira_token}",
            }
        )

        return cls(session=session, domain_url=domain_url)
