import os
import requests
import logging
from typing import Dict, Callable

logger = logging.getLogger(__name__)
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")

def fda_lookup_tool(param: str) -> str:
    """Call an n8n webhook to look up a registration number or product name."""
    try:
        resp = requests.post(N8N_WEBHOOK_URL, json={"query": param}, timeout=5)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        logger.error("FDA lookup error: %s", e)
        return "ขออภัย เกิดปัญหาในการตรวจสอบทะเบียน"

    status = data.get("status")
    if status == "valid":
        return (
            f"✅ จดทะเบียนแล้วกับ {data.get('holder')} "
            f"หมดอายุ {data.get('expiry')} (หมวด: {data.get('category')})"
        )
    if status in ("invalid", "not_found"):
        return "❌ ไม่พบข้อมูลการจดทะเบียน กรุณาตรวจสอบใหม่"
    return "⚠️ ระบบไม่พร้อมใช้งาน กรุณาลองใหม่ภายหลัง"

TOOLS: Dict[str, Callable[[str], str]] = {
    "fda": fda_lookup_tool,
}
