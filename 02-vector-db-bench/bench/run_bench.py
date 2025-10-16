import typer
import numpy as np
from bench.dataset import load_dataset
from bench.embed import embed_texts
from bench.groundtruth import build_gt_index, knn

app = typer.Typer()

@app.command()
def run(n_docs: int = 1000, n_queries: int = 500, top_k: int = 10):
    texts, ids = load_dataset(n_docs)
    print(f"Loaded {len(texts)} docs.")
    emb = embed_texts(texts)
    print(f"Embeddings shape: {emb.shape}")

    q_idx = np.random.choice(len(texts), size=n_queries, replace=False)
    queries = emb[q_idx]
    gt = build_gt_index(emb)
    gt_topk = knn(gt, queries, top_k)
    print(f"Ground truth computed, shape={gt_topk.shape}")

    print("Pipeline OK")

if __name__ == "__main__":
    app()
