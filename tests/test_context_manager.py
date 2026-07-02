import unittest

from app.conversation.context_manager import build_context


class TestContextManager(unittest.TestCase):
    def test_build_context_keeps_recent_rounds_without_mutating_source(self) -> None:
        messages = [
            {"role": "system", "content": "system"},
            {"role": "user", "content": "user-1"},
            {"role": "assistant", "content": "assistant-1"},
            {"role": "user", "content": "user-2"},
            {"role": "assistant", "content": "assistant-2"},
            {"role": "user", "content": "user-3"},
        ]

        request_messages = build_context(messages, 1)

        self.assertEqual(len(messages), 6)
        self.assertEqual(
            request_messages,
            [
                {"role": "system", "content": "system"},
                {"role": "user", "content": "user-2"},
                {"role": "assistant", "content": "assistant-2"},
                {"role": "user", "content": "user-3"},
            ],
        )

    def test_build_context_rejects_invalid_message_order(self) -> None:
        invalid_messages = [
            {"role": "system", "content": "system"},
            {"role": "assistant", "content": "wrong-1"},
            {"role": "user", "content": "wrong-2"},
            {"role": "user", "content": "current-user"},
        ]

        with self.assertRaises(ValueError):
            build_context(invalid_messages, 1)


if __name__ == "__main__":
    unittest.main()
