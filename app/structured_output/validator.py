ALLOWED_INTENTS = {"refund", "consult", "complaint", "other"}


def validate_result(data: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        errors.append(f"顶层结构非法，预期为 dict，实际是：{type(data).__name__}")
        return errors
    if "intent" not in data:
        errors.append("缺少 intent 字段")
    else:
        intent = data["intent"]
        if not isinstance(intent, str):
            errors.append(
                f"intent 字段类型非法，预期为 str，实际是：{type(intent).__name__}"
            )
        elif intent not in ALLOWED_INTENTS:
            errors.append("intent 字段内容非法")
    if "confidence" not in data:
        errors.append("缺少 confidence 字段")
    else:
        confidence = data["confidence"]
        if isinstance(confidence, (int, float)) and not isinstance(confidence, bool):
            if not 0 <= confidence <= 1:
                errors.append("confidence 字段值非法，应该在 0~1 之间")
        else:
            errors.append(
                f"confidence 字段类型非法，预期为 int or float，实际是：{type(confidence).__name__}"
            )
    return errors
