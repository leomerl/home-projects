import numpy as np
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

_model = None

def embed_texts(texts: list[str], model_name: str = "all-MiniLM-L6-v2") -> np.ndarray:
    global _model
    if _model is None:
        _model = SentenceTransformer(model_name)
    emb = _model.encode(texts, batch_size=64, show_progress_bar=True, convert_to_numpy=True)
    return emb.astype(np.float32)
