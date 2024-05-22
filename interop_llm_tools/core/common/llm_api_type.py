from enum import Enum, auto


class LlmApiType(Enum):
    OLLAMA = auto()

    @classmethod
    def from_str(cls, s: str) -> "LlmApiType":
        for k, v in cls.__members__.items():
            if k.lower() == s.lower():
                return cls(value=v)
