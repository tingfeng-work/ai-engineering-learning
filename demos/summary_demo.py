from app.conversation.summary_manager import summarize_history


def main() -> None:
    history = [
        {
            "role": "user",
            "content": "My name is Jianfeng, and I am learning AI application development.",
        },
        {
            "role": "assistant",
            "content": "Start with the native OpenAI SDK, then add context management.",
        },
    ]
    summary = summarize_history(summary_messages=history)
    print(summary)


if __name__ == "__main__":
    main()
