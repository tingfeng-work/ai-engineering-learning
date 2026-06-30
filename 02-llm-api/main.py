from llm_client import ask_model


def main() -> None:
    question = input("请输入问题：").strip()

    if not question:
        print("问题不能为空")
        return

    try:
        result = ask_model(question)
    except Exception as exc:
        print(f"模型调用失败：{exc}")
        return

    print("\n模型回答：")
    print(result.content)

    print("\n实际模型：")
    print(result.model)

    print("\n停止原因：")
    print(result.finish_reason)

    print("\ntoken 消耗：")
    if result.total_tokens is None:
        print("未知")
    else:
        print(
            f"prompt_tokens: {result.prompt_tokens}",
            f"completion_tokens: {result.completion_tokens}",
            f"total_tokens: {result.total_tokens}",
        )


if __name__ == "__main__":
    main()
