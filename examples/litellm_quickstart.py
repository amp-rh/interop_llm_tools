import litellm

from interop_llm_tools.config import get_config

config = get_config()
model_configs = config.models.instruct_model_params


def main():
    response = litellm.completion(
        **model_configs.as_litellm_dict(),
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
