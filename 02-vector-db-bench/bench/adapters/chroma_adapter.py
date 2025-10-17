import chromadb
from chromadb.config import Settings

class ChromaAdapter:
    def __init__(self, name="bench", persist_dir=".chroma"):
        self.client = chromadb.Client(Settings(
            is_persistent=True,
            persist_directory=persist_dir
        ))
        self.col = self.client.get_or_create_collection(
            name=name,
            metadata={"hnsw:space":"cosine"}
        )

    def reset(self):
        self.client.delete_collection(self.col.name)
        self.col = self.client.get_or_create_collection(
            name=self.col.name,
            metadata={"hnsw:space":"cosine"}
        )

    def upsert(self, ids, vectors, metadatas):
        self.col.add(ids=ids, embeddings=vectors.tolist(), metadatas=metadatas)

    def query(self, query_vectors, top_k):
        res = self.col.query(query_embeddings=query_vectors.tolist(), n_results=top_k)
        return res["ids"]

    def close(self):
        pass
