from llama_index.core.base.llms.types import ChatMessage, MessageRole
from llama_index.llms.litellm import LiteLLM

from interop_llm_tools.config import get_config

config = get_config()


def main():
    resp = LiteLLM(
        model=f"openai/{config.openai_default_instruct_model}",
        temperature=0.0,
        api_base=config.openai_api_base,
        api_key=config.openai_api_key,
        organization="",
    ).chat(
        messages=[
            ChatMessage.from_str(
                content="You are a duck. You only know how to quack.",
                role=MessageRole.SYSTEM,
            ),
            ChatMessage.from_str(content="Hello, how are you", role=MessageRole.USER),
        ]
    )
    print(resp)


if __name__ == "__main__":
    main()
