def build_chat_request(
    question: str,
    model: str = "qwen-plus",
    temperature: float = 0.2,
    system_prompt: str | None = None,
) -> dict[str, object]:
    # 推荐使用 if system_prompt is None:
    if system_prompt == None:
        system_prompt = "你是一名 AI 应用开发助手"
    result: dict = {}
    result["model"] = model
    result["temperature"] = temperature
    result["messages"] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question},
    ]
    return result


request = build_chat_request(question="什么是 RAG ?")
print(request)

print(request["model"])

print(request["messages"][1]["content"])

request2 = build_chat_request(
    question="什么是 RAG ?", temperature=0.5, system_prompt="辅助我完成 AI 开发学习"
)

messages = request2["messages"]

for i, message in enumerate(messages, start=1):
    print(
        f"第{i}条消息，" f'role = {message["role"]},' f'content = {message["content"]}'
    )
