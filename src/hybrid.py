def rrf_sections(rankings, k=60):
    """Merge several ranked lists of chunks. Returns section IDs, best first."""
    scores = {}
    for ranking in rankings:
        for rank, chunk in enumerate(ranking, start=1):
            scores[chunk.section] = scores.get(chunk.section, 0.0) + 1.0 / (k + rank)
    return sorted(scores, key=scores.get, reverse=True)
