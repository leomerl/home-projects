import os

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434/api/generate")

REDIS_HOST = os.getenv("REDIS_HOST", "redis-vector")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

INDEX_NAME = "docs"
DOC_PREFIX = "doc:"
DIM = int(os.getenv("EMBED_DIM", "1536"))
DIST = os.getenv("EMBED_DIST", "cosine")