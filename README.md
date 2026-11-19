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

Baseline (BM25, k=5): pending the evaluation set.
