# CLAUDE.md

## MCP Tool Usage

When calling MCP tools (e.g. `mcp__amp-github-mcp__create_pull_request`), string parameters must use actual newlines for multiline content — NOT literal `\n` escape sequences. Escape sequences are passed verbatim and render as broken text in GitHub.

## Running Tests

```bash
PYTHONPATH=interop_llm_tools poetry run pytest tests/ -v --ignore=tests/functional_tests
```

- Unit tests use `MockGenericLlm` and `MockEmbedding` fixtures (no live Ollama needed)
- Functional tests in `tests/functional_tests/` require a live Ollama instance
- 3 pre-existing test failures exist due to missing `llama-index-llms-ollama` dependency
