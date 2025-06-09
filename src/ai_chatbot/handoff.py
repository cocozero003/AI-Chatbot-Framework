import os
import logging
import requests

logger = logging.getLogger(__name__)
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def human_handoff_tool(user_id: str, message: str) -> str:
    """
    Notify human agents (e.g. via Slack) and reply with a placeholder.
    """
    payload = {
        "text": f":rotating_light: *Handoff Request*\n• User: `{user_id}`\n• Message: {message}"
    }
    try:
        resp = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=3)
        resp.raise_for_status()
        return "กำลังเชื่อมต่อเจ้าหน้าที่… กรุณารอสักครู่ครับ"
    except Exception as e:
        logger.error("Handoff error: %s", e)
        return "ขออภัย ขณะนี้ไม่สามารถเชื่อมต่อเจ้าหน้าที่ได้ กรุณาลองใหม่ภายหลัง"
