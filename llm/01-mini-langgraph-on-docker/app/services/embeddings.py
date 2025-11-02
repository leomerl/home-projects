import hashlib, struct
import numpy as np
from app.config import DIM

def pack_f32(vec: np.ndarray) -> bytes:
    if vec.dtype != np.float32:
        vec = vec.astype(np.float32)
    return vec.tobytes(order="C")

def fake_embed(text: str, dim: int = DIM) -> np.ndarray:
    # not a real embedder
    h = hashlib.sha256(text.encode("utf-8")).digest()
    seed = struct.unpack("!Q", h[:8])[0] & 0x7FFFFFFFFFFFFFFF
    rng = np.random.default_rng(seed)
    v = rng.normal(size=dim).astype(np.float32)
    v /= np.linalg.norm(v) + 1e-12
    return v