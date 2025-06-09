import pytest
from ai_chatbot.engine import ChatbotEngine

@pytest.fixture
def bot():
    return ChatbotEngine()

def test_greeting(bot):
    assert bot.process("u1","hello") == "สวัสดีครับ! มีอะไรให้ช่วยได้บ้าง?"

def test_faq(bot):
    resp = bot.process("u1","help")
    assert "assist you" in resp or "ช่วย" in resp

def test_tool_invocation(monkeypatch, bot):
    monkeypatch.setitem(bot.__class__.TOOLS, "fda", lambda p: f"TOOL GOT {p}")
    assert "TOOL GOT 123" in bot.process("u1","fda 123")

def test_escalation(monkeypatch, bot):
    monkeypatch.setattr(bot, "should_escalate", lambda u,t: True)
    os.environ["SLACK_WEBHOOK_URL"] = "https://example.com"
    monkeypatch.setattr("requests.post", lambda *a,**k: type("R",(object,),{"raise_for_status":lambda s:None})())
    reply = bot.process("user","urgent please")
    assert "เชื่อมต่อเจ้าหน้าที่" in reply
