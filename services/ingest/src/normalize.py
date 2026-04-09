from __future__ import annotations

from .parser import ParsedConversation


def normalize_transcript(conversation: ParsedConversation) -> list[dict]:
    normalized = []
    for i, message in enumerate(conversation.messages):
        normalized.append(
            {
                "sequence_no": i,
                "external_id": message.external_id,
                "role": message.role.lower(),
                "content": " ".join(message.content.split()),
                "created_at": message.created_at,
            }
        )
    return normalized
