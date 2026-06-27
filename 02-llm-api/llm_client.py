from openai import OpenAI

from config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL, LLM_SYSTEM_PROMPT

client = OpenAI(
    api_key=LLM_API_KEY,
    base_url=LLM_BASE_URL,
)


def ask_model(question: str) -> str:
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": LLM_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": question,
            },
        ],
    )

    content = response.choices[0].message.content

    if content is None:
        raise ValueError("模型没有返回文本内容")

    print(response)

    print(response.model)
    print(response.choices[0].finish_reason)
    print(response.usage)

    return content
