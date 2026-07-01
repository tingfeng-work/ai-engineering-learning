import math


def build_context(
    messages: list[dict[str, str]],
    max_history_rounds: int,
    conversation_summary: str | None = None,
) -> list[dict[str, str]]:
    """
    根据最大历史轮数构造本次发送给模型的上下文。
    """
    # 防御性校验
    # 1. max_history_rounds 是否小于 0
    if max_history_rounds < 0:
        raise ValueError("最大历史轮数不能小于0")
    # 2. messages 数量是否少于 2
    if len(messages) < 2:
        raise ValueError("messages 至少应该包含 system 和当前 user 消息")
    # 3. 第一条是否为 system
    if messages[0]["role"] != "system":
        raise ValueError("messages 的第一条消息必须是 system 消息")
    # 4. 最后一条是否为 user
    if messages[-1]["role"] != "user":
        raise ValueError("messages 的最后一条消息必须是 user 消息")
    # 5. 执行上下文截断

    #  取出 system
    system_message = messages[0]
    #  取出中间的完整历史
    completed_history_messages = messages[1:-1]
    length = len(completed_history_messages)
    if length % 2 != 0:
        raise ValueError("user 消息与 assistant 消息应该成对出现")
    for index in range(0, length, 2):
        if (
            completed_history_messages[index]["role"] != "user"
            or completed_history_messages[index + 1]["role"] != "assistant"
        ):
            raise ValueError(
                f"第 {index//2+1} 轮历史消息角色顺序错误，应为 user -> assistant"
            )

    #  取出当前 user
    current_message = messages[-1]
    #  根据 max_history_rounds 截取完整历史
    if max_history_rounds == 0:
        history_messages = []
    else:
        history_messages = completed_history_messages[-max_history_rounds * 2 :]
    #  组合成一个新列表并返回
    request_messages = [system_message]

    if conversation_summary and conversation_summary.strip():
        request_messages.append(
            {
                "role": "system",
                "content": (
                    "以下是此前对话的历史摘要，仅作为背景信息：\n"
                    f"{conversation_summary}"
                ),
            }
        )

    request_messages.extend(history_messages)
    request_messages.append(current_message)

    return request_messages


def estimate_message_tokens(message: dict[str, str]) -> int:
    return estimate_text_tokens(message["content"]) + 4


def build_context_by_token_budget(
    messages: list[dict[str, str]],
    max_input_tokens: int,
) -> list[dict[str, str]]:
    # 防御性校验
    # 1. max_history_rounds 是否小于 0
    if max_input_tokens <= 0:
        raise ValueError("最大输入 tokens 不能小于0")
    # 2. messages 数量是否少于 2
    if len(messages) < 2:
        raise ValueError("messages 至少应该包含 system 和当前 user 消息")
    # 3. 第一条是否为 system
    if messages[0]["role"] != "system":
        raise ValueError("messages 的第一条消息必须是 system 消息")
    # 4. 最后一条是否为 user
    if messages[-1]["role"] != "user":
        raise ValueError("messages 的最后一条消息必须是 user 消息")
    # 获取系统消息
    system_message = messages[0]
    # 完整历史消息
    completed_history_messages = messages[1:-1]
    # 最新用户提问
    current_message = messages[-1]
    # 构造的符合要求的历史消息
    history_messages = []

    used_tokens = estimate_message_tokens(system_message) + estimate_message_tokens(
        current_message
    )
    if used_tokens > max_input_tokens:
        raise ValueError("system + 当前 user 已经超过最大输入 tokens 数")
    for index in range(len(completed_history_messages) - 2, -1, -2):
        user_message = completed_history_messages[index]
        assistant_message = completed_history_messages[index + 1]
        tokens = estimate_message_tokens(
            message=user_message
        ) + estimate_message_tokens(message=assistant_message)
        if used_tokens + tokens <= max_input_tokens:
            used_tokens = used_tokens + tokens
            history_messages.append(assistant_message)
            history_messages.append(user_message)
        else:
            break

    history_messages.reverse()
    return [system_message] + history_messages + [current_message]


def estimate_text_tokens(text: str) -> int:
    token: int = 0
    cnt: int = 0
    for char in text:
        if "\u4e00" <= char <= "\u9fff":
            token = token + 1
        else:
            cnt = cnt + 1
    return token + math.ceil(cnt / 4)


def estimate_messages_tokens(
    messages: list[dict[str, str]],
) -> int:
    return sum(estimate_message_tokens(message=message) for message in messages)


# if __name__ == "__main__":
# messages = [
#     {"role": "system", "content": "SS"},
#     {"role": "user", "content": "111"},
#     {"role": "assistant", "content": "aaaa"},
#     {"role": "user", "content": "22"},
#     {"role": "assistant", "content": "bbbbbb"},
#     {"role": "user", "content": "CCC"},
# ]

# request_message = build_context_by_token_budget(
#     messages=messages, max_input_tokens=13
# )

# assert request_message == [
#     {"role": "system", "content": "SS"},
#     {"role": "user", "content": "22"},
#     {"role": "assistant", "content": "bbbbbb"},
#     {"role": "user", "content": "CCC"},
# ]
# assert estimate_text_tokens("你好abcde") == 4
# assert estimate_text_tokens("abcdefgh") == 2
# assert estimate_text_tokens("你好世界") == 4
# assert estimate_text_tokens("") == 0

# messages = [
#     {"role": "system", "content": "SS"},
#     {"role": "user", "content": "111"},
#     {"role": "assistant", "content": "aaaa"},
#     {"role": "user", "content": "22"},
#     {"role": "assistant", "content": "bbbbbb"},
#     {"role": "user", "content": "你好a"},
#     {"role": "assistant", "content": "333333"},
#     {"role": "user", "content": "你好4"},
#     {"role": "assistant", "content": "444444"},
# ]
# for message in messages:
#     print(estimate_message_tokens(message=message))
# result = split_history_for_summary(messages=messages, keep_recent_rounds=2)
# print(result[0])
# print(result[1])
# print(format_messages_for_summary(messages=messages))
# messages = [
#     {"role": "user", "content": "我叫廷风"},
#     {"role": "assistant", "content": "很高兴认识你"},
#     {"role": "user", "content": "我正在学习 AI 应用开发"},
#     {"role": "assistant", "content": "你可以从原生 SDK 开始学习"},
# ]
# history_text = format_messages_for_summary(messages=messages)
# print(history_text)
# summary_request = build_summary_request(history_text=history_text)
# print(summary_request)
# assert len(summary_request) == 2
