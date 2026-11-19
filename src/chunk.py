import re
from dataclasses import dataclass

HEADING = re.compile(r"^(\d+(?:\.\d+)*)\.\s+(\S.*)$")
APPENDIX = re.compile(r"^APPENDIX\s+[A-Z]:")


@dataclass
class Chunk:
    rfc: str
    section: str
    title: str
    text: str


def chunk_rfc(path, rfc_number):
    chunks = []
    current = None  # (section, title)
    body = []

    def flush():
        if current:
            chunks.append(Chunk(rfc_number, current[0], current[1],
                                "\n".join(body).strip()))

    with open(path, encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.rstrip("\n")
            if "[Page" in line:  # skip page furniture
                continue
            if APPENDIX.match(line) and "..." not in line:
                flush()
                current = None 
                body = []
                continue
            m = HEADING.match(line)
            if m and "..." not in line:  # skip table-of-contents lines
                flush()
                current = (m.group(1), m.group(2).strip())
                body = []
            elif current:
                body.append(line)
    flush()
    return chunks

