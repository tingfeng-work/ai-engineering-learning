from llm_result import LLMResult

result1 = LLMResult(
    content="你好",
    model="openai/gpt-oss-20b:free",
    finish_reason="stop",
    prompt_tokens=12,
    completion_tokens=20,
    total_tokens=32,
)

result2 = LLMResult(content="你好", model="free")

print(result1)
print(result2)

print(
    f"content: {result1.content}",
    f"finish_reason: {result1.finish_reason}",
    f"total_tokens: {result1.total_tokens}",
)

print(
    f"content: {result2.content}",
    f"finish_reason: {result2.finish_reason}",
    f"total_tokens: {result2.total_tokens}",
)
