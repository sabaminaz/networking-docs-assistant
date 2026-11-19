from src.chunk import chunk_rfc
from src.retrieve import BM25Retriever


def test_bm25_finds_section_by_keyword():
    r = BM25Retriever(chunk_rfc("tests/fixtures/sample_rfc.txt", "9999"))
    top = r.search("time to live", k=1)
    assert top[0].section == "3.1"
