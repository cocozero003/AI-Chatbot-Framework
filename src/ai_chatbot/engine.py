import os
import re
import openai
from typing import Optional, Tuple
from .tools import TOOLS
from .handoff import human_handoff_tool

# Load API key
openai.api_key = os.getenv("OPENAI_API_KEY")

GREETING_PATTERNS = [
    re.compile(r"\bhello\b|\bhi\b|\bhey\b", re.IGNORECASE),
    re.compile(r"\bสวัสดี\b", re.IGNORECASE),
]
FAQ_PATTERNS = {
    re.compile(r"\bhelp\b", re.IGNORECASE): "Sure, how can I assist you today?",
    re.compile(r"\bbye\b|\bfarewell\b", re.IGNORECASE): "Goodbye! Have a great day!",
}
ESCALATION_KEYWORDS = ["urgent", "ด่วน", "เจ้าหน้าที่"]

class ChatbotEngine:
    def detect_intent(self, text: str) -> Tuple[str, Optional[str]]:
        txt = text.strip()
        for pat in GREETING_PATTERNS:
            if pat.search(txt): return "greeting", None
        for pat, resp in FAQ_PATTERNS.items():
            if pat.search(txt): return "faq", resp
        for name in TOOLS:
            if name in txt.lower():
                param = txt.lower().split(name,1)[-1].strip()
                return f"tool:{name}", param
        return "open_ended", None

    def should_escalate(self, user_id: str, text: str) -> bool:
        if any(k in text.lower() for k in ESCALATION_KEYWORDS):
            return True
        return False

    def rag_retrieve(self, query: str) -> Optional[str]:
        # TODO: integrate your vector-store retrieval
        return None

    def llm_generate(self, prompt: str, model: str = "gpt-3.5-turbo") -> str:
        resp = openai.ChatCompletion.create(
            model=model,
            messages=[{"role":"system","content":prompt}],
            temperature=0.2, max_tokens=256
        )
        return resp.choices[0].message.content.strip()

    def process(self, user_id: str, text: str) -> str:
        intent, data = self.detect_intent(text)
        if intent == "greeting":
            return "สวัสดีครับ! มีอะไรให้ช่วยได้บ้าง?"
        if intent == "faq":
            return data  # type: ignore
        if intent.startswith("tool:"):
            _, name = intent.split(":",1)
            return TOOLS[name](data or "")
        if self.should_escalate(user_id, text):
            return human_handoff_tool(user_id, text)
        retrieved = self.rag_retrieve(text)
        if retrieved:
            prompt = (
                "You are an assistant grounded in the following context:\n"
                f"{retrieved}\n\nUser: {text}\nAssistant:"
            )
            return self.llm_generate(prompt, model="gpt-4")
        prompt = f"You are a helpful assistant.\nUser: {text}\nAssistant:"
        return self.llm_generate(prompt)
