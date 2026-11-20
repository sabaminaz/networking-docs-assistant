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

Baseline (BM25, k=5), evaluated 2026-11-19: recall@5 = 15/16 (0.94) on 16 answerable questions.
Four unanswerable questions are in the evaluation set but are not scored, since abstention needs the generation step.
Porter stemming (added in a later commit): recall@5 = 15/16 (0.94), unchanged.
