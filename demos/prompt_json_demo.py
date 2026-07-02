import json

from app.conversation.context_manager import build_context
from app.streaming.consumer import consume_stream
from app.structured_output.prompts import JSON_SYSTEM_PROMPT
from app.structured_output.validator import validate_result


def main() -> None:
    messages: list[dict[str, str]] = [{"role": "system", "content": JSON_SYSTEM_PROMPT}]
    question = input("question: ").strip()
    if not question:
        print("input cannot be empty")
        return

    messages.append({"role": "user", "content": question})
    request_messages = build_context(
        messages=messages,
        max_history_rounds=2,
    )
    response = consume_stream(request_messages=request_messages)
    if response is None:
        return

    try:
        data = json.loads(response.content)
        errors = validate_result(data=data)
        if len(errors) == 0:
            print("validation passed")
        else:
            for error in errors:
                print(error)
    except json.JSONDecodeError as exc:
        print(f"json decode failed: {exc}")


if __name__ == "__main__":
    main()
