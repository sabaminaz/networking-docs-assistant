import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.chunk import chunk_rfc
from src.retrieve import BM25Retriever

chunks = chunk_rfc("data/raw/rfc791.txt", "791")
retriever = BM25Retriever(chunks)

with open("eval/questions.jsonl") as f:
    questions = [json.loads(line) for line in f if line.strip()]

answerable = [q for q in questions if q["section"]]
hits = 0
for q in answerable:
    top = retriever.search(q["question"], k=5)
    if any(c.section == q["section"] for c in top):
        hits += 1

print(f"recall@5: {hits}/{len(answerable)} = {hits / len(answerable):.2f}")
