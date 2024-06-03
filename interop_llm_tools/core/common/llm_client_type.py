from enum import Enum, auto


class LlmClientType(Enum):
    OLLAMA = auto()

    @classmethod
    def from_str(cls, s: str) -> "LlmClientType":
        for k, v in cls.__members__.items():
            if k.lower() == s.lower():
                return cls(value=v)
