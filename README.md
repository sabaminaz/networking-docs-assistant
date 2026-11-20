# Networking Documentation Assistant

A retrieval-augmented assistant that answers networking questions from IETF RFCs and
Linux man pages, with answers grounded in cited sections.

## Status

- [x] Section-aware chunker for RFC plain-text files
- [x] BM25 keyword retriever
- [ ] Evaluation set (20+ questions, including unanswerable ones)
- [ ] Dense retrieval and hybrid merge
- [ ] Citation-grounded generation

## Setup

    python -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    curl -o data/raw/rfc791.txt https://www.rfc-editor.org/rfc/rfc791.txt

## Tests

    python -m pytest -q

## Results

Retrieval comparison, 16 answerable questions, recall@5 (evaluated 2026-11-19):
- BM25 with Porter stemming: 15/16
- Dense (bge-small-en-v1.5, 200-word passages): 14/16
- Hybrid (reciprocal rank fusion of BM25 and dense): 16/16

A 16-question set is small, so one question changes the score by about 6 points.
Hybrid covered the misses of both methods: dense caught the gateway question that BM25 missed, while BM25 caught the Protocol field and Flags questions that dense missed.
