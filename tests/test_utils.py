from types import SimpleNamespace

from app.utils import summarize_changes


def test_summarize_changes_no_api_keys(monkeypatch):
    monkeypatch.delenv("SUMMARIZER_API_KEYS", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    summary, metadata = summarize_changes("example diff")
    assert summary.startswith("Summary:")
    assert metadata["method"] == "fallback"
    assert metadata["tokens_used"] is None
    assert metadata["truncated"] is False


def test_summarize_changes_tries_all_keys(monkeypatch):
    monkeypatch.setenv("SUMMARIZER_API_KEYS", "openai:bad,openai:good")
    attempts = []

    class FakeCompletions:
        def __init__(self, api_key: str):
            self.api_key = api_key

        def create(self, **kwargs):
            if self.api_key == "bad":
                raise RuntimeError("key rejected")
            return SimpleNamespace(
                choices=[
                    SimpleNamespace(message=SimpleNamespace(content=f"summary-{self.api_key}"))
                ]
            )

    class FakeClient:
        def __init__(self, api_key: str):
            attempts.append(api_key)
            self.chat = SimpleNamespace(completions=FakeCompletions(api_key))

    summary, metadata = summarize_changes(
        "example diff",
        client_factory=lambda key: FakeClient(key),
    )

    assert attempts == ["bad", "good"]
    assert summary == "summary-good"
    assert metadata["method"] == "openai"
