# Quick CURL Examples

## Greeting
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id":"u123","message":"hello"}'
```

## FDA Lookup Tool
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id":"u123","message":"fda G1234567"}'
```

## Escalation / Human Handoff
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id":"u123","message":"urgent issue"}'
```
