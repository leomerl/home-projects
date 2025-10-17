import numpy as np
import faiss

def build_gt_index(emb: np.ndarray):
    emb = emb / (np.linalg.norm(emb, axis=1, keepdims=True) + 1e-12)
    index = faiss.IndexFlatIP(emb.shape[1])
    index.add(emb)
    return index

def knn(index, queries: np.ndarray, k: int):
    q = queries / (np.linalg.norm(queries, axis=1, keepdims=True) + 1e-12)
    D, I = index.search(q.astype(np.float32), k)
    return I

def compute_groundtruth(doc_embs: np.ndarray, query_embs: np.ndarray, k: int):
    index = build_gt_index(doc_embs)
    q = query_embs / (np.linalg.norm(query_embs, axis=1, keepdims=True) + 1e-12)
    D, I = index.search(q.astype(np.float32), k)
    return D, I
