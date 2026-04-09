from __future__ import annotations


def chunk_message(content: str, max_chars: int = 450) -> list[str]:
    content = content.strip()
    if not content:
        return []
    if len(content) <= max_chars:
        return [content]

    words = content.split()
    chunks = []
    current = ""
    for word in words:
        next_candidate = (current + " " + word).strip()
        if len(next_candidate) > max_chars:
            chunks.append(current)
            current = word
        else:
            current = next_candidate
    if current:
        chunks.append(current)
    return chunks
