import unittest

from app.llm.result import LLMResult


class TestLLMResult(unittest.TestCase):
    def test_required_fields_and_optional_usage(self) -> None:
        result = LLMResult(
            content="hello",
            model="test-model",
            finish_reason="stop",
            prompt_tokens=12,
            completion_tokens=20,
            total_tokens=32,
        )

        self.assertEqual(result.content, "hello")
        self.assertEqual(result.model, "test-model")
        self.assertEqual(result.finish_reason, "stop")
        self.assertEqual(result.total_tokens, 32)

    def test_optional_fields_default_to_none(self) -> None:
        result = LLMResult(content="hello", model="test-model")

        self.assertIsNone(result.finish_reason)
        self.assertIsNone(result.prompt_tokens)
        self.assertIsNone(result.completion_tokens)
        self.assertIsNone(result.total_tokens)


if __name__ == "__main__":
    unittest.main()
