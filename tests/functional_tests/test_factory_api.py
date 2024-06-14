import llama_index.core as lmx
import phoenix as px
import pytest

from interop_llm_tools.api import get_factory_api


@pytest.fixture(autouse=True)
def init_tracing():
    px.launch_app()
    lmx.set_global_handler("arize_phoenix")


class TestFactoryApi:
    @pytest.mark.asyncio
    async def test_doc_agent_from_factory(self, secret_numbers):
        secret_number = secret_numbers.pop()
        api = get_factory_api()
        agent = await api.aget_document_agent(document_path=secret_number.path)
        resp = await agent.aquery("what is the secret number?")
        assert secret_number.str in resp

    @pytest.mark.asyncio
    async def test_multi_doc_agent_from_factory(self, secret_numbers):
        api = get_factory_api()
        secret_number_1, secret_number_2 = secret_numbers.pop(), secret_numbers.pop()
        agent = await api.aget_multi_document_agent(
            document_paths=[secret_number_1.path, secret_number_2.path]
        )
        resp = await agent.aquery("what are the two secret numbers?")
        assert secret_number_1.str in resp
        assert secret_number_2.str in resp

    @pytest.mark.asyncio
    async def test_get_summary_pipeline(self):
        api = get_factory_api()
        pipeline = api.get_summary_pipeline()

        verbose_context = """In the vast expanse of the universe, there exists an infinitesimally tiny speck of dust by 
        the name of Earth, which is inhabited by numerous creatures, both great and small, including humans who 
        possess the remarkable ability to communicate intricately through a medium known as language. This complex 
        system of words and sentences allows them to convey thoughts, emotions, and ideas with precision and 
        efficiency. However, at times, some individuals may indulge in the use of superfluous words or phrases, 
        adding unnecessary length and complexity to their utterances, which, when summarized, may be encapsulated in 
        a concise and straightforward statement."""

        summary = await pipeline.arun(context=verbose_context)

        original_length = len(verbose_context)
        summary_length = len(summary)

        assert summary_length < original_length

        important_words = ["Earth", "human", "language"]
        for word in important_words:
            assert word in summary

    @pytest.mark.asyncio
    async def test_get_jira_issue_summary_pipeline(self, jira_issue_keys):
        api = get_factory_api()
        pipeline = api.get_jira_issue_summary_pipeline()
        resp = await pipeline.arun(jira_issue_key=jira_issue_keys.pop())
        print(resp)
        # TODO Add assertions

    @pytest.mark.asyncio
    async def test_get_summary_aggregation_pipeline(self):
        api = get_factory_api()
        pipeline = api.get_summary_aggregation_pipeline()

        verbose_contexts = [
            """In the vast expanse of the universe, there exists an infinitesimally tiny speck of dust by 
        the name of Earth, which is inhabited by numerous creatures, both great and small, including humans who 
        possess the remarkable ability to communicate intricately through a medium known as language. This complex 
        system of words and sentences allows them to convey thoughts, emotions, and ideas with precision and 
        efficiency. However, at times, some individuals may indulge in the use of superfluous words or phrases, 
        adding unnecessary length and complexity to their utterances, which, when summarized, may be encapsulated in 
        a concise and straightforward statement.""",
            """Amidst the grandiose symphony of nature, where myriad creatures harmoniously coexist in a breathtaking 
        tapestry of life, lies a minute fraction of this spectacle, an insignificant morsel in the grand scheme 
        of things, known as our planet. This seemingly ordinary orb is home to a myriad of beings, 
        each possessing unique characteristics and complexities. Among these inhabitants are humans, 
        who have been blessed with the extraordinary faculty of articulate expression through the eloquent 
        language. Yet, occasionally, some humans embellish their speech with surplus words, creating intricately 
        woven sentences that, when boiled down to their essence, can be succinctly summarized as "There's a 
        minute fraction of nature called our planet, inhabited by humans who sometimes use excessive words""",
        ]

        summary = await pipeline.arun(contexts=verbose_contexts)

        original_length = sum(len(_) for _ in verbose_contexts)
        summary_length = len(summary)

        assert summary_length < original_length

        important_words = ["Earth", "human", "language"]
        for word in important_words:
            assert word in summary

    @pytest.mark.asyncio
    async def test_get_jira_issue_summary_aggregation_pipeline(self, jira_issue_keys):
        api = get_factory_api()
        pipeline = api.get_jira_issue_summary_aggregation_pipeline()
        resp = await pipeline.arun(jira_issue_keys=jira_issue_keys)
        print(resp)
        # TODO Add assertions
