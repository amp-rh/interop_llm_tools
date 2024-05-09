import litellm

from interop_llm_tools.config import get_config

config = get_config()


def main():
    response = litellm.completion(
        model="ollama/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
        api_base=config.default_llm_api_base_url,
        temperature=0.0,
        messages=[
            {
                "content": "You are a duck. You only know how to quack.",
                "role": "system",
            },
            {"content": "Hello, how are you?", "role": "user"},
        ],
    )
    print(response)


if __name__ == "__main__":
    main()
