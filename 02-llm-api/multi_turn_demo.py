from llm_client import stream_model
from config import LLM_SYSTEM_PROMPT
from llm_result import LLMResult


def main():
    messages: list[dict[str, str]] = [{"role": "system", "content": LLM_SYSTEM_PROMPT}]
    while True:
        question = input(
            "请输入问题：（输入 exit 或者 quit 退出，输入/history 查询当前消息信息）\n"
        ).strip()

        if not question:
            print("输入不能为空")
            continue

        if question.lower() in {"quit", "exit"}:
            break

        if question == "/history":
            print(f"当前消息数量：{len(messages)}")
            print(f"当前完整轮数：{(len(messages)-1)//2}")
            for index, message in enumerate(messages, start=1):
                content = message["content"]
                preview = content[:50]

                if len(content) > 50:
                    preview += "..."

                print(f"{index}. role={message['role']}, " f"content={preview}")

            continue

        messages.append({"role": "user", "content": question})

        def consume_stream(messages: list[dict[str, str]]) -> LLMResult:

            text_parts: list[str] = []
            actual_model: str | None = None
            finish_reason: str | None = None
            prompt_tokens: int | None = None
            completion_tokens: int | None = None
            total_tokens: int | None = None

            try:
                for event in stream_model(messages=messages):
                    if event.event_type == "content":
                        if event.content is not None:
                            text_parts.append(event.content)
                            print(event.content, end="", flush=True)
                    elif event.event_type == "finish":
                        actual_model = event.model
                        finish_reason = event.finish_reason
                        prompt_tokens = event.prompt_tokens
                        completion_tokens = event.completion_tokens
                        total_tokens = event.total_tokens
            except Exception as exc:
                print(f"\n模型调用失败：{exc}")
                if messages[-1]["role"] == "user":
                    messages.pop()
                continue

            if actual_model is None:
                if messages[-1]["role"] == "user":
                    messages.pop()
                    print("\n模型调用失败：流式响应未返回实际模型")
                    continue

            full_text = "".join(text_parts)
            print()

            if not full_text:
                if messages[-1]["role"] == "user":
                    messages.pop()
                    print("\n模型调用失败：模型回答为空")
                    continue

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
            print("\n调用信息：")
            print(f"实际模型：{llm_result.model}")
            print(f"停止原因：{llm_result.finish_reason}")
            print(f"输入 Token：{llm_result.prompt_tokens}")
            print(f"输出 Token：{llm_result.completion_tokens}")
            print(f"总 Token：{llm_result.total_tokens}")
            return llm_result

        llm_result = consume_stream(messages=messages)
        messages.append({"role": "assistant", "content": llm_result.content})


if __name__ == "__main__":
    main()
