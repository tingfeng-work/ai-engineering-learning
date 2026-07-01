from stream_consumer import consume_stream
from config import LLM_SYSTEM_PROMPT
from context_manager import build_context, estimate_messages_tokens
from summarize_manager import (
    split_history_for_summary,
    summarize_history,
)

MAX_HISTORY_ROUNDS = 2
SUMMARY_TRIGGER_ROUNDS = 4
KEEP_RECENT_ROUNDS = 2


def main():
    messages: list[dict[str, str]] = [{"role": "system", "content": LLM_SYSTEM_PROMPT}]
    conversation_summary: str | None = None
    summarized_rounds: int = 0
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

        request_messages = build_context(
            messages=messages,
            max_history_rounds=MAX_HISTORY_ROUNDS,
            conversation_summary=conversation_summary,
        )
        estimated_prompt_tokens = estimate_messages_tokens(messages=request_messages)

        print("\n本次发送给模型的上下文：")
        for message in request_messages:
            print(message)

        llm_result = consume_stream(request_messages=request_messages)
        if llm_result is None:
            if messages[-1]["role"] == "user":
                messages.pop()
                continue

        messages.append({"role": "assistant", "content": llm_result.content})

        total_rounds = (len(messages) - 1) // 2
        if total_rounds >= SUMMARY_TRIGGER_ROUNDS:
            target_summary_round = total_rounds - KEEP_RECENT_ROUNDS
            new_rounds_to_summarize = target_summary_round - summarized_rounds
            if new_rounds_to_summarize > 0:
                summary_messages, _ = split_history_for_summary(
                    messages=messages, keep_recent_rounds=KEEP_RECENT_ROUNDS
                )
                new_summary_messages = summary_messages[
                    summarized_rounds * 2 : target_summary_round * 2
                ]
                new_summary = summarize_history(
                    summary_messages=new_summary_messages,
                    previous_summary=conversation_summary,
                )
                if new_summary is not None:
                    conversation_summary = new_summary
                    summarized_rounds = target_summary_round
                    print(f"\n本次新增摘要轮数：{new_rounds_to_summarize}")
                    print(f"当前累计摘要轮数：{summarized_rounds}")
                    print("当前滚动摘要：")
                    print(conversation_summary)

        print(f"客户端估计输入 Token: {estimated_prompt_tokens}")
        print(f"服务端实际输入 Token: {llm_result.prompt_tokens}")
        print(f"估计差值: {estimated_prompt_tokens-llm_result.prompt_tokens}")


if __name__ == "__main__":
    main()
