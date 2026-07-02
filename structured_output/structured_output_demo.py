import json
from structured_output.manual_validation_demo import validate_result
from app.conversation.context_manager import build_context
from app.streaming.stream_consumer import consume_stream

# json_samples: list[str] = [
#     """{
#     "intent": "refund",
#     "confidence": 0.92
#     }""",
#     """
#     识别结果如下：
#     {"intent": "refund", "confidence": 0.92}
#     """,
#     """
#     ```json
#     {"intent": "refund", "confidence": 0.92}
#     ```
#     """,
#     """{
#     "intent": "refund"
#     }""",
#     """{
#     "intent": "refund",
#     "confidence": "92%"
#     }""",
#     "{'intent': 'refund', 'confidence': 0.92}",
#     """
#     ["refund", 0.92]
#     """,
#     """{
#     "intent": "sing",
#     "confidence": 0.92
#     }""",
#     """{
#     "intent": "refund",
#     "confidence": 1.5
#     }""",
#     """{
#     "intent": "refund",
#     "confidence": -0.1
#     }""",
#     """{
#     "intent": "refund",
#     "confidence": true
#     }""",
#     """{
#     "intent": "unknown_intent",
#     "confidence": 2.5
#     }""",
#     """{}""",
# ]

# for index, string in enumerate(json_samples, start=1):
#     # is_valid = True
#     print(f"========== 第 {index} 条 ==========")
#     try:
#         data = json.loads(string)
#         errors = validate_result(data=data)
#         if len(errors) == 0:
#             print("业务校验成功")
#         else:
#             for error in errors:
#                 print(error)
#     except json.JSONDecodeError as exc:
#         print(f"第 {index} 条数据解析失败：{exc}")
JSON_SYSTEM_PROMPT = """请用 json 的形式输出，不输出markdown和解释，遵循这个结构：{"intent":refun,"confidence":0.25};其中 intent 的内容是字符串，只能是refund或consult或complaint或other；confidence的内容是int或float，值只能在0~1之间"""


def main():
    messages: list[dict[str, str]] = [{"role": "system", "content": JSON_SYSTEM_PROMPT}]
    question = input("请输入问题：").strip()
    if not question:
        print("输入不能为空")
        return
    messages.append({"role": "user", "content": question})
    request_messages = build_context(
        messages=messages,
        max_history_rounds=2,
    )
    response = consume_stream(request_messages=request_messages)
    try:
        data = json.loads(response.content)
        errors = validate_result(data=data)
        if len(errors) == 0:
            print("业务校验成功")
        else:
            for error in errors:
                print(error)
    except json.JSONDecodeError as exc:
        print(f"数据解析失败：{exc}")
