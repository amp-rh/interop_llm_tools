from llama_index.core.base.llms.types import ChatMessage, MessageRole
from llama_index.llms.litellm import LiteLLM

from interop_llm_tools.config import get_config

config = get_config()
print(config.models.instruct_model_params.as_litellm_dict())


def main():
    response = LiteLLM(
        **config.models.instruct_model_params.as_litellm_dict(), temperature=0.0
    ).chat(
        messages=[
            ChatMessage.from_str(
                content="You are a duck. You only know how to quack.",
                role=MessageRole.SYSTEM,
            ),
            ChatMessage.from_str(content="Hello, how are you", role=MessageRole.USER),
        ]
    )
    print(response)


if __name__ == "__main__":
    main()
