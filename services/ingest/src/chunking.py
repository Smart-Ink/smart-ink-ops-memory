from __future__ import annotations

from typing import Any


def _split_text(content: str, max_chars: int) -> list[str]:
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
        if len(next_candidate) > max_chars and current:
            chunks.append(current)
            current = word
        else:
            current = next_candidate
    if current:
        chunks.append(current)
    return chunks


def build_exchange_pairs(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    pairs: list[dict[str, Any]] = []
    pending_user: dict[str, Any] | None = None

    for message in messages:
        role = str(message.get("role", "")).lower().strip()
        if role == "user":
            if pending_user is not None:
                pairs.append(
                    {
                        "pair_index": len(pairs),
                        "message_external_ids": [pending_user["external_id"]],
                        "content": f"User: {pending_user['content']}",
                    }
                )
            pending_user = message
            continue

        if role == "assistant" and pending_user is not None:
            pairs.append(
                {
                    "pair_index": len(pairs),
                    "message_external_ids": [pending_user["external_id"], message["external_id"]],
                    "content": f"User: {pending_user['content']}\nAssistant: {message['content']}",
                }
            )
            pending_user = None
            continue

        pairs.append(
            {
                "pair_index": len(pairs),
                "message_external_ids": [message["external_id"]],
                "content": f"{role.title() or 'Message'}: {message['content']}",
            }
        )

    if pending_user is not None:
        pairs.append(
            {
                "pair_index": len(pairs),
                "message_external_ids": [pending_user["external_id"]],
                "content": f"User: {pending_user['content']}",
            }
        )

    return pairs


def chunk_exchange_pairs(pairs: list[dict[str, Any]], max_chars: int = 450) -> list[dict[str, Any]]:
    chunks: list[dict[str, Any]] = []
    for pair in pairs:
        split_chunks = _split_text(str(pair["content"]), max_chars=max_chars)
        for split_index, content in enumerate(split_chunks):
            chunks.append(
                {
                    "pair_index": pair["pair_index"],
                    "split_index": split_index,
                    "message_external_ids": list(pair["message_external_ids"]),
                    "content": content,
                }
            )
    return chunks
