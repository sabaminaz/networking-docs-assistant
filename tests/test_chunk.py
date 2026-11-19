from src.chunk import chunk_rfc


def test_fixture_sections_parsed():
    chunks = chunk_rfc("tests/fixtures/sample_rfc.txt", "9999")
    by_section = {c.section: c for c in chunks}
    assert set(by_section) == {"1", "3", "3.1"}  # TOC lines ignored
    assert "Header" in by_section["3.1"].title
    assert "time to live" in by_section["3.1"].text
    assert "[Page" not in by_section["3.1"].text
