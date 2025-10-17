import typer
import numpy as np
import time
from bench.dataset import load_dataset
from bench.embed import embed_texts
from bench.groundtruth import build_gt_index, knn, compute_groundtruth
from bench.adapters.chroma_adapter import ChromaAdapter
from bench.metrics import percentile, recall_at_k

app = typer.Typer()

@app.command()
def run(n_docs: int = 1000, n_queries: int = 500, top_k: int = 10):
    texts, ids = load_dataset(n_docs)
    emb = embed_texts(texts)
    q_idx = np.random.choice(len(texts), size=n_queries, replace=False)
    queries = emb[q_idx]
    gt = build_gt_index(emb)
    gt_topk = knn(gt, queries, top_k)

@app.command()
def bench(n_docs: int = 5000, n_queries: int = 200, top_k: int = 10):
    """Benchmark Chroma performance"""
    print("=" * 60)
    print("PHASE 1: Dataset + Embeddings")
    print("=" * 60)
    docs, _ = load_dataset(n_docs)
    print(f"Generated {len(docs)} docs")

    # Select random subset as queries
    q_idx = np.random.choice(len(docs), size=n_queries, replace=False)
    queries = [docs[i] for i in q_idx]
    print(f"Selected {len(queries)} queries")

    doc_embs = embed_texts(docs)
    query_embs = embed_texts(queries)
    print(f"Doc embeddings shape: {doc_embs.shape}")
    print(f"Query embeddings shape: {query_embs.shape}")

    print("\n" + "=" * 60)
    print("PHASE 1: FAISS Ground Truth")
    print("=" * 60)
    _, gt_topk = compute_groundtruth(doc_embs, query_embs, k=top_k)
    print(f"Ground truth shape: {gt_topk.shape}")
    id_by_idx = np.array(range(len(docs)))

    print("\n" + "=" * 60)
    print("PHASE 2: Chroma Benchmark")
    print("=" * 60)
    chroma = ChromaAdapter()
    print("Resetting Chroma...")
    t0 = time.time()
    chroma.reset()
    chroma.upsert(list(id_by_idx), doc_embs, [{}]*len(docs))
    build_time = time.time() - t0
    print(f"Chroma index build time: {build_time:.2f}s")

    print("\n" + "=" * 60)
    print("PHASE 3: Query and Measure Latency")
    print("=" * 60)
    latencies = []
    pred = []
    for i, q in enumerate(query_embs):
        if i % 50 == 0:
            print(f"Processing query {i}/{len(query_embs)}...")
        q0 = time.time()
        res_ids = chroma.query([q], top_k=top_k)[0]
        latencies.append((time.time() - q0) * 1000)
        pred.append(res_ids)

    recall = recall_at_k([set(p) for p in pred],
                        [set(id_by_idx[g]) for g in gt_topk])
    p50, p95 = percentile(latencies, 50), percentile(latencies, 95)

    print("\n" + "=" * 60)
    print("CHROMA BENCHMARK RESULTS")
    print("=" * 60)
    print(f"Build time: {build_time:.2f}s")
    print(f"p50 latency: {p50:.2f}ms")
    print(f"p95 latency: {p95:.2f}ms")
    print(f"Recall@{top_k}: {recall:.3f}")
    print("=" * 60)

if __name__ == "__main__":
    app()
