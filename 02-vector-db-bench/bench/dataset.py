import random

def load_dataset(n_docs: int = 1000):
    topics = ["sports", "politics", "tech", "science", "finance"]
    texts, ids = [], []
    for i in range(n_docs):
        topic = random.choice(topics)
        text = f"{topic} article about {random.choice(['AI','markets','elections','research','teams'])}"
        texts.append(text)
        ids.append(f"id-{i}")
    return texts, ids