import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.chunk import chunk_rfc
from src.retrieve import BM25Retriever
from src.dense import DenseRetriever
from src.hybrid import rrf_sections

chunks = chunk_rfc("data/raw/rfc791.txt", "791")
n = len(chunks)
bm25 = BM25Retriever(chunks)
dense = DenseRetriever(chunks)

with open("eval/questions.jsonl") as f:
    qs = [json.loads(line) for line in f if line.strip()]
qs = [q for q in qs if q["section"]]

methods = {
    "bm25": lambda s: [c.section for c in bm25.search(s, k=n)],
    "dense": lambda s: [c.section for c in dense.rank_sections(s)],
    "hybrid": lambda s: rrf_sections([bm25.search(s, k=n), dense.rank_sections(s)]),
}

for name, rank_fn in methods.items():
    hits = sum(q["section"] in rank_fn(q["question"])[:5] for q in qs)
    print(f"{name}: recall@5 = {hits}/{len(qs)}")

