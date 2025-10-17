import numpy as np

def percentile(latencies_ms, p):
    return float(np.percentile(latencies_ms, p)) if latencies_ms else 0.0

def recall_at_k(pred_ids, gt_ids):
    hits = 0
    total = 0
    for pred, gt in zip(pred_ids, gt_ids):
        total += min(len(gt), len(pred))
        hits += len(set(pred) & set(gt))
    return hits / total if total else 0.0
