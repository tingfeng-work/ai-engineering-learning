import json

from app.structured_output.validator import validate_result


JSON_SAMPLES: list[str] = [
    """{
    "intent": "refund",
    "confidence": 0.92
    }""",
    """{
    "intent": "refund"
    }""",
    """{
    "intent": "refund",
    "confidence": "92%"
    }""",
    "{'intent': 'refund', 'confidence': 0.92}",
    """
    ["refund", 0.92]
    """,
    """{
    "intent": "sing",
    "confidence": 0.92
    }""",
    """{
    "intent": "refund",
    "confidence": 1.5
    }""",
    """{
    "intent": "refund",
    "confidence": true
    }""",
    """{}""",
]


def main() -> None:
    for index, sample in enumerate(JSON_SAMPLES, start=1):
        print(f"========== sample {index} ==========")
        try:
            data = json.loads(sample)
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
