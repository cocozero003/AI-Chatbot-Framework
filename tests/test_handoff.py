import pytest
from ai_chatbot.handoff import human_handoff_tool

@pytest.fixture(autouse=True)
def env(monkeypatch):
    monkeypatch.setenv("SLACK_WEBHOOK_URL", "https://example.com/webhook")

def test_handoff(monkeypatch):
    class FakeResp:
        def raise_for_status(self): pass
    monkeypatch.setattr("requests.post", lambda *a,**k: FakeResp())
    msg = human_handoff_tool("u1","test")
    assert "เชื่อมต่อเจ้าหน้าที่" in msg
