# AI Chatbot Framework

**Hybrid pipeline**:  
1. Rule-based shortcuts (greeting, FAQ)  
2. Tool calls (n8n webhook)  
3. Retrieval-Augmented Generation (RAG) stub  
4. LLM fallback (GPT-3.5 / GPT-4)  
5. Human-in-the-loop escalation

## Quickstart

```bash
git clone https://github.com/you/ai-chatbot.git
cd ai-chatbot
cp .env.example .env
pip install -r requirements.txt
uvicorn ai_chatbot.app:app --reload
```

See [docs/architecture.md](docs/architecture.md) and [examples/curl_requests.md](examples/curl_requests.md) for details.
