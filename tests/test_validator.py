import unittest

from app.structured_output.validator import validate_result


class TestValidator(unittest.TestCase):
    def test_valid_result_has_no_errors(self) -> None:
        errors = validate_result({"intent": "refund", "confidence": 0.92})

        self.assertEqual(errors, [])

    def test_rejects_invalid_top_level_type(self) -> None:
        errors = validate_result(["refund", 0.92])

        self.assertEqual(len(errors), 1)

    def test_rejects_bool_confidence(self) -> None:
        errors = validate_result({"intent": "refund", "confidence": True})

        self.assertEqual(len(errors), 1)


if __name__ == "__main__":
    unittest.main()
