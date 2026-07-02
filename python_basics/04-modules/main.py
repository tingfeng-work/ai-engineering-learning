import prompt_builder
from config import DEFAULT_MODEL, DEFAULT_SYSTEM_PROMPT, DEFAULT_TEMPERATURE

# print(DEFAULT_MODEL)
# print(DEFAULT_SYSTEM_PROMPT)
# print(DEFAULT_TEMPERATURE)

# message = prompt_builder.build_message(
#     system_prompt="你是一名 AI 应用开发助手", user_prompt="什么是 RAG ?"
# )

# print(message)
request = prompt_builder.build_chat_request(
    question="什么是 Function Calling",
    model=DEFAULT_MODEL,
    temperature=DEFAULT_TEMPERATURE,
    system_prompt=DEFAULT_SYSTEM_PROMPT,
)
print(request)

messages = request["messages"]

for i, message in enumerate(messages, start=1):
    print(f"第{i}条消息：role:{message["role"]},content: {message["content"]}")
