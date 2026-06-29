# app2.py — call Ollama Cloud via HTTP API

import os  # Read environment variables safely
import requests  # HTTP client

# Read API key from environment (set with export OLLAMA_API_KEY=...)
api_key = os.environ.get("OLLAMA_API_KEY")

# Fail fast if the key is missing
if not api_key:
    raise ValueError("OLLAMA_API_KEY is not set. Run: export OLLAMA_API_KEY='your-key'")

# Cloud host + path (not localhost)
url = "https://ollama.com/api/chat"

# Same style of body as local — model must be a cloud-capable name you pulled/registered
payload = {
    "model": "gpt-oss:120b-cloud",  # Example from class; use a tag from the Ollama library
    "messages": [
        {
            "role": "user",
            "content": "Explain REST API in a beginner friendly way.",
        }
    ],
    "stream": False,
}

# Bearer token in header — standard way to send API keys
headers = {
    "Authorization": f"Bearer {api_key}",
}

response = requests.post(
    url,
    json=payload,
    headers=headers,
    timeout=120,
)

data = response.json()
print(data["message"]["content"])
