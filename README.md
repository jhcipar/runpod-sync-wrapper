# runpod-sync-wrapper

Tiny demo of a sync-style RunPod worker wrapper.

## Files

- `wrapper.py` - tiny wrapper that exposes:
  - `GET /ping`
  - `POST /__runpod/invoke`
- `wrapper_demo.py` - example handler using the wrapper

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 wrapper_demo.py
```

Default port is `8888`. Override with `PORT`.

## Test

```bash
curl -i http://localhost:8888/ping

curl -i -X POST http://localhost:8888/__runpod/invoke \
  -H 'content-type: application/json' \
  -d '{"prompt":"hello","max_tokens":32,"temperature":0.5}'
```
