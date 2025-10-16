import requests
from app.config import MODEL_ENDPOINT

def generate(prompt: str, model: str = "mistral") -> str:
    resp = requests.post(f"{MODEL_ENDPOINT}/api/generate", json={"prompt": prompt, "model": model}, timeout=60)
    resp.raise_for_status()
    return resp.json().get("response", "")