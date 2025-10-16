import requests
from app.config import OLLAMA_URL

def generate(prompt: str, model: str = "mistral") -> str:
    resp = requests.post(f"{OLLAMA_URL}/api/generate", json={"prompt": prompt, "model": model}, timeout=60)
    resp.raise_for_status()
    return resp.json().get("response", "")