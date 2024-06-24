from typing import Any, Iterable, List

from llama_index.core import Document
from llama_index.core.readers.base import BaseReader

from core.api.jira_api import JiraApi


class JiraReader(BaseReader):
    issue_keys: list[str] = None
    jira_api: JiraApi = JiraApi.from_defaults()

    def __init__(self, issue_keys: list[str] = None):
        super().__init__()
        self.issue_keys = issue_keys or []

    async def aload_data(
        self, issue_keys: list[str] = None, **load_kwargs: Any
    ) -> List[Document]:
        issue_keys = issue_keys or self.issue_keys
        assert issue_keys, "can not load data without defined issue_keys"
        return await super().aload_data(issue_keys=issue_keys, **load_kwargs)

    def lazy_load_data(self, *args: Any, **load_kwargs: Any) -> Iterable[Document]:
        for k in load_kwargs.get("issue_keys"):
            # TODO: extract metadata and link nodes
            yield Document.from_dict(data=self.jira_api.get_issue(k).to_dict())

    @classmethod
    def from_inputs(cls, inputs: dict) -> "JiraReader":
        return cls(**inputs)
