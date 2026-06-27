# def build_message(system_prompt: str, user_prompt: str) -> list[dict[str, str]]:
#     return [
#         {"role": "system", "content": system_prompt},
#         {"role": "user", "content": user_prompt},
#     ]


# # print(111111)

# if __name__ == "__main__":
#     message = build_message("系统 prompt 测试", "用户 prompt 测试")
#     print(message)


def build_chat_request(
    question: str, model: str, temperature: float, system_prompt: str
) -> dict[str, object]:
    return {
        "model": model,
        "temperature": temperature,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
    }
