import litellm

from interop_llm_tools.config import get_config

config = get_config()


def main():
    resp = litellm.completion(
        model=f"openai/{config.openai_default_instruct_model}",
        api_key=config.openai_api_key,
        api_base=config.openai_api_base,
        organization="",
        messages=[
            {
                "content": "You are a duck. You only know how to quack.",
                "role": "system",
            },
            {"content": "Hello, how are you?", "role": "user"},
        ],
    )
    print(resp)


if __name__ == "__main__":
    main()
