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

## Generation (cited answers)

Model: llama3.2 via Ollama. Retrieval: hybrid (BM25 + dense, reciprocal rank fusion), top 3 sections.

- Version 1 (first 3,000 characters of each section): abstention 4/4, valid citations 9/16
- Version 2 (best-matching 250-word window per section, current code): abstention 4/4, valid citations 11/16

Diagnosis: the Protocol field question was missed at retrieval (section 3.1 not in the top 3).
The Source Address question received an Options passage, because word-count scoring favors repeated words like "source" and "address."

Next step (not yet tested): rank windows with BM25 and pass the top two per section.

Caveats: the abstention test uses off-topic questions, so 4/4 is an easy bar. A valid citation shows the model cited a retrieved section, not that the answer is correct. Read the answers before trusting them.
