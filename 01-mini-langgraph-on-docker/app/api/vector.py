import time
import requests
from fastapi import APIRouter, Body, Query, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from app.config import OLLAMA_URL
from app.metrics import prompt_count, req_latency, vec_upserts_total, vec_queries_total, vec_query_latency
from app.services.vector_index import ensure_index, upsert_doc, knn_search
from app.services.ollama_client import generate

router = APIRouter(prefix="/vector", tags=["vector"])

@router.post("/index/init")
def init_index():
    ensure_index()
    return {"ok": True}

@router.post("/embed")
def embed_document(
    id: str = Query(..., description="Document ID (stored as doc:<id>)"),
    text: str = Body(..., embed=True, description="Plain text content")
):
    upsert_doc(id, text)
    vec_upserts_total.inc()
    return {"ok": True, "id": id, "len": len(text)}

@router.get("/search")
def search(q: str, k: int = 5):
    start = time.perf_counter()
    res = knn_search(q, k=k)
    elapsed = time.perf_counter() - start
    vec_queries_total.inc()
    vec_query_latency.observe(elapsed)
    res["latency_seconds"] = elapsed
    return res

@router.get("/ollama")
def ask_ollama(q: str):
    answer = generate(q)
    return {"answer": answer}

@router.get("/ask")
@req_latency.time()
def ask(q: str):
    prompt_count.inc()
    response = requests.post(OLLAMA_URL, json={"model": "mistral", "prompt": q, "stream": False})
    return {"answer": response.json()["response"]}

@router.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)