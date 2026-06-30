from openai import OpenAI

from config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL, LLM_SYSTEM_PROMPT

from llm_result import LLMResult

from stream_event import StreamEvent

from collections.abc import Iterator

client = OpenAI(
    api_key=LLM_API_KEY,
    base_url=LLM_BASE_URL,
)


def ask_model(question: str) -> LLMResult:
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": LLM_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": question,
            },
        ],
    )
    choice = response.choices[0]
    content = choice.message.content

    if content is None:
        raise ValueError("模型没有返回文本内容")

    if response.usage is None:
        result = LLMResult(
            content=content,
            model=response.model,
            finish_reason=choice.finish_reason,
        )
    else:
        result = LLMResult(
            content=content,
            model=response.model,
            finish_reason=choice.finish_reason,
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens,
            total_tokens=response.usage.total_tokens,
        )

    return result


def stream_model(messages: list[dict[str, str]]) -> Iterator[StreamEvent]:
    stream = client.chat.completions.create(
        model=LLM_MODEL,
        stream=True,
        stream_options={"include_usage": True},
        messages=messages,
    )
    actual_model: str | None = None
    finish_reason: str | None = None
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None
    for chunk in stream:
        # print(chunk)
        if chunk.choices:
            choices = chunk.choices[0]
            text = choices.delta.content
            if text:
                yield StreamEvent(
                    event_type="content",
                    content=text,
                )
            if choices.finish_reason is not None:
                finish_reason = choices.finish_reason
            if chunk.model is not None:
                actual_model = chunk.model

        if chunk.usage is not None:
            usage = chunk.usage
            completion_tokens = usage.completion_tokens
            prompt_tokens = usage.prompt_tokens
            total_tokens = usage.total_tokens
    finish_event = StreamEvent(
        event_type="finish",
        model=actual_model,
        finish_reason=finish_reason,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=total_tokens,
    )
    yield finish_event
