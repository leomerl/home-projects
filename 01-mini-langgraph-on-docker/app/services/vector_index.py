import redis
from typing import Dict, Any
from app.config import INDEX_NAME, DOC_PREFIX, DIM, DIST
from app.services.redis_client import rbin
from app.services.embeddings import fake_embed, pack_f32

def index_exists() -> bool:
    try:
        rbin.execute_command("FT.INFO", INDEX_NAME)
        return True
    except redis.exceptions.ResponseError:
        return False
    
def ensure_index() -> None:
    if index_exists():
        return
    cmd = [
        "FT.CREATE", INDEX_NAME,
        "ON", "HASH",
        "PREFIX", "1", DOC_PREFIX,
        "SCHEMA",
        "text", "TEXT",
        "embedding", "VECTOR", "FLAT",
        "TYPE", "FLOAT32",
        "DIM", str(DIM),
        "DISTANCE_METRIC", DIST
    ]
    rbin.execute_command(*cmd)

def upsert_doc(doc_id: str, text: str) -> None:
    ensure_index()
    vec = fake_embed(text)
    payload = {
        b"text": text.encode("utf-8"),
        b"embedding": pack_f32(vec)
    }
    rbin.hset(f"{DOC_PREFIX}{doc_id}", mapping=payload)

def knn_search(query: str, k: int = 5) -> Dict[str, Any]:
    ensure_index()
    qvec = fake_embed(query)
    qvec_bytes = pack_f32(qvec)
    cmd = [
        "FT.SEARCH", INDEX_NAME,
        f"*=>[KNN {k} @embedding $vec]",
        "PARAMS", "2", "vec", qvec_bytes,
        "RETURN", "2", "text", "__score__",
        "DIALECT", "2"
    ]
    raw = rbin.execute_command(*cmd)
    total = raw[0] if raw else 0
    results = []
    for i in range(1, len(raw), 2):
        key = raw[i].decode()
        fields = raw[i+1]
        item = {"key": key}
        for j in range(0, len(fields), 2):
            fname = fields[j].decode()
            val = fields[j+1]
            if fname == "text":
                item["text"] = val.decode(errors='ignore')
            elif fname == "__score__":
                try:
                    item["score"] = float(val.decode())
                except Exception:
                    item["score"] = None
        results.append(item)
    return {"total": total, "results": results}