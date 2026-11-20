import json
import re
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"
WINDOW_WORDS = 250
STEP_WORDS = 125
STOPWORDS = {"the", "a", "an", "of", "is", "in", "what", "does", "do", "how",
             "which", "on", "to", "and", "for", "by", "its", "it", "be"}

PROMPT = """You answer questions about IETF RFC 791 using ONLY the sources below.
Cite the section number for every claim, like [3.1].
If the sources do not contain the answer, reply exactly: NOT FOUND.

Sources:
{sources}

Question: {question}
Answer:"""


def tokens(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def best_window(text, question):
    """Return the window of the section that shares the most content words with the question."""
    words = text.split()
    if len(words) <= WINDOW_WORDS:
        return text
    q = {t for t in tokens(question) if t not in STOPWORDS}
    best, best_score = words[:WINDOW_WORDS], -1
    for start in range(0, len(words), STEP_WORDS):
        window = words[start:start + WINDOW_WORDS]
        score = sum(1 for t in tokens(" ".join(window)) if t in q)
        if score > best_score:
            best, best_score = window, score
    return " ".join(best)


def answer(question, retrieved):
    sources = "\n\n".join(
        f"[{c.section}] {c.title}\n{best_window(c.text, question)}" for c in retrieved
    )
    body = json.dumps({
        "model": MODEL,
        "prompt": PROMPT.format(sources=sources, question=question),
        "stream": False,
    }).encode()
    req = urllib.request.Request(OLLAMA_URL, data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())["response"].strip()
