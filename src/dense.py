import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "BAAI/bge-small-en-v1.5"
QUERY_PREFIX = "Represent this sentence for searching relevant passages: "


class DenseRetriever:
    def __init__(self, chunks, max_words=200):
        self.chunks = chunks
        self.model = SentenceTransformer(MODEL_NAME)
        self.owners = []  # section index for each passage
        passages = []
        for idx, c in enumerate(chunks):
            words = c.text.split() or [""]
            for start in range(0, len(words), max_words):
                passages.append(c.title + ". " + " ".join(words[start:start + max_words]))
                self.owners.append(idx)
        self.emb = self.model.encode(passages, normalize_embeddings=True)

    def rank_sections(self, query):
        q = self.model.encode(QUERY_PREFIX + query, normalize_embeddings=True)
        order = np.argsort(-(self.emb @ q))
        seen, ranked = set(), []
        for p in order:
            idx = self.owners[p]
            if idx not in seen:
                seen.add(idx)
                ranked.append(self.chunks[idx])
        return ranked
