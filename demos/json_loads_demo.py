import json


JSON_SAMPLES: list[str] = [
    """{
    "intent": "refund",
    "confidence": 0.92
    }""",
    """
    result:
    {"intent": "refund", "confidence": 0.92}
    """,
    """
    ```json
    {"intent": "refund", "confidence": 0.92}
    ```
    """,
    "{'intent': 'refund', 'confidence': 0.92}",
    """
    ["refund", 0.92]
    """,
]


def main() -> None:
    for index, sample in enumerate(JSON_SAMPLES, start=1):
        print(f"========== sample {index} ==========")
        try:
            print(json.loads(sample))
        except json.JSONDecodeError as exc:
            print(f"json decode failed: {exc}")


if __name__ == "__main__":
    main()
