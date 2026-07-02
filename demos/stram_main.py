from app.llm.llm_client import stream_model
from app.llm.llm_result import LLMResult


def main() -> None:
    question = input("请输入问题:").strip()

    if not question:
        print("问题不能为空！")
        return

    text_parts: list[str] = []

    actual_model: str | None = None
    finish_reason: str | None = None
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None
    try:
        for event in stream_model(question):
            if event.event_type == "content":
                if event.content is not None:
                    print(event.content, end="", flush=True)
                    text_parts.append(event.content)
            elif event.event_type == "finish":
                actual_model = event.model
                finish_reason = event.finish_reason
                prompt_tokens = event.prompt_tokens
                completion_tokens = event.completion_tokens
                total_tokens = event.total_tokens

    except Exception as exc:
        print(f"\n模型调用失败：{exc}")
        return

    if actual_model is None:
        raise ValueError("流式响应未返回实际模型")

    print()

    full_text = "".join(text_parts)
    llm_result = LLMResult(
        content=full_text,
        model=actual_model,
        finish_reason=finish_reason,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=total_tokens,
    )
    print(f"完整回答长度：{len(full_text)}")

    print(f"完整的LLMResult:{llm_result}")


if __name__ == "__main__":
    main()
