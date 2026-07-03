import hashlib
import math
import re
from collections import Counter


TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9+#.-]{1,}")


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text or "")]


def local_embedding(text: str, dimensions: int = 96) -> list[float]:
    vector = [0.0] * dimensions
    for token, count in Counter(tokenize(text)).items():
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        index = int.from_bytes(digest[:4], "big") % dimensions
        vector[index] += 1.0 + math.log(count)
    norm = math.sqrt(sum(value * value for value in vector)) or 1.0
    return [round(value / norm, 6) for value in vector]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    if not a or not b:
        return 0.0
    width = min(len(a), len(b))
    dot = sum(a[i] * b[i] for i in range(width))
    an = math.sqrt(sum(value * value for value in a[:width]))
    bn = math.sqrt(sum(value * value for value in b[:width]))
    if not an or not bn:
        return 0.0
    return dot / (an * bn)
