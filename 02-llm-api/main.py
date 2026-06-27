from llm_client import ask_model


def main() -> None:
    question = input("请输入问题：")

    if not question:
        print("问题不能为空")
        return

    try:
        answer = ask_model(question)
    except Exception as exc:
        print(f"模型调用失败：{exc}")
        return

    print("\n模型回答：")
    print(answer)


if __name__ == "__main__":
    main()
