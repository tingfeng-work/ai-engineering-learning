from dataclasses import dataclass


@dataclass
class StreamEvent:
    event_type: str
    content: str | None = None
    model: str | None = None
    finish_reason: str | None = None
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None


if __name__ == "__main__":
    event1 = StreamEvent(event_type="content", content="Hello")
    event2 = StreamEvent(
        event_type="finish",
        model="test-model",
        finish_reason="stop",
        prompt_tokens=10,
        completion_tokens=20,
        total_tokens=30,
    )

    print(event1)
    print(event2)
