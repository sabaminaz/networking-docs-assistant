import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.chunk import chunk_rfc
from src.retrieve import BM25Retriever
from src.dense import DenseRetriever
from src.hybrid import rrf_sections
from src.answer import answer

chunks = chunk_rfc("data/raw/rfc791.txt", "791")
n = len(chunks)
by_section = {c.section: c for c in chunks}
bm25 = BM25Retriever(chunks)
dense = DenseRetriever(chunks)


def top3(query):
    fused = rrf_sections([bm25.search(query, k=n), dense.rank_sections(query)])
    return [by_section[s] for s in fused[:3]]


with open("eval/questions.jsonl") as f:
    qs = [json.loads(line) for line in f if line.strip()]
answerable = [q for q in qs if q["section"]]
unanswerable = [q for q in qs if not q["section"]]

abstained = 0
for q in unanswerable:
    out = answer(q["question"], top3(q["question"]))
    abstained += "NOT FOUND" in out.upper()
    print("UNANSWERABLE:", q["question"], "->", out[:150])

valid = 0
for q in answerable:
    top = top3(q["question"])
    out = answer(q["question"], top)
    cited = set(re.findall(r"\[(\d+(?:\.\d+)*)\]", out))
    ok = bool(cited) and cited <= {c.section for c in top}
    valid += ok
    print("ANSWER:", q["question"], "->", out, "| valid citations:", ok)

print(f"abstention: {abstained}/{len(unanswerable)}")
print(f"valid citations: {valid}/{len(answerable)}")
print("Read each answer yourself. A valid citation doesn't prove the answer is correct.")
