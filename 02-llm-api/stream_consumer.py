from llm_result import LLMResult
from llm_client import stream_model


def consume_stream(
    request_messages: list[dict[str, str]], display: bool = True
) -> LLMResult | None:

    text_parts: list[str] = []
    actual_model: str | None = None
    finish_reason: str | None = None
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None

    try:
        for event in stream_model(messages=request_messages):
            if event.event_type == "content":
                if event.content is not None:
                    text_parts.append(event.content)
                    if display:
                        print(event.content, end="", flush=True)
            elif event.event_type == "finish":
                actual_model = event.model
                finish_reason = event.finish_reason
                prompt_tokens = event.prompt_tokens
                completion_tokens = event.completion_tokens
                total_tokens = event.total_tokens
    except Exception as exc:

        print(f"\n模型调用失败：{exc}")
        return None

    if actual_model is None:

        print("\n模型调用失败：流式响应未返回实际模型")
        return None

    full_text = "".join(text_parts)
    if display:
        print()

    if not full_text:

        print("\n模型调用失败：模型回答为空")
        return None

    llm_result = LLMResult(
        content=full_text,
        model=actual_model,
        finish_reason=finish_reason,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=total_tokens,
    )

    # print(llm_result)
    # print(messages)
    if display:
        print("\n调用信息：")
        print(f"实际模型：{llm_result.model}")
        print(f"停止原因：{llm_result.finish_reason}")
        print(f"输入 Token：{llm_result.prompt_tokens}")
        print(f"输出 Token：{llm_result.completion_tokens}")
        print(f"总 Token：{llm_result.total_tokens}")
    return llm_result
