from context_manager import build_context

# messages = [
#     {"role": "system", "content": "system"},
#     {"role": "user", "content": "user-1"},
#     {"role": "assistant", "content": "assistant-1"},
#     {"role": "user", "content": "user-2"},
#     {"role": "assistant", "content": "assistant-2"},
#     {"role": "user", "content": "user-3"},
# ]

# context = build_context(messages=messages, max_history_rounds=0)

# print("完整历史：")
# print(messages)

# print("发送上下文：")
# print(context)

# invalid_messages = [
#     {"role": "user", "content": "user-1"},
#     {"role": "user", "content": "user-2"},
# ]
# invalid_messages = [
#     {"role": "system", "content": "system"},
#     {"role": "user", "content": "user-1"},
#     {"role": "assistant", "content": "assistant-1"},
# ]
# invalid_messages = [
#     {"role": "system", "content": "system"},
#     {"role": "user", "content": "user-1"},
#     {"role": "assistant", "content": "assistant-1"},
#     {"role": "assistant", "content": "orphan-assistant"},
#     {"role": "user", "content": "current-user"},
# ]
# invalid_messages = [
#     {"role": "system", "content": "system"},
#     {"role": "assistant", "content": "wrong-1"},
#     {"role": "user", "content": "wrong-2"},
#     {"role": "user", "content": "current-user"},
# ]
# try:
#     context = build_context(messages=invalid_messages, max_history_rounds=1)
# except Exception as exc:
#     print(f"错误信息：{exc}")

messages = [
    {"role": "system", "content": "system"},
    {"role": "user", "content": "user-1"},
    {"role": "assistant", "content": "assistant-1"},
    {"role": "user", "content": "user-2"},
    {"role": "assistant", "content": "assistant-2"},
    {"role": "user", "content": "user-3"},
]

request_messages = build_context(messages, 1)

assert len(messages) == 6
assert len(request_messages) == 4
