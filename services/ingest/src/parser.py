from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ParsedMessage:
    external_id: str
    role: str
    content: str
    created_at: str | None


@dataclass
class ParsedConversation:
    external_id: str
    title: str
    started_at: str | None
    messages: list[ParsedMessage]
    raw_payload: dict[str, Any]


def _as_text(content_obj: Any) -> str:
    if isinstance(content_obj, str):
        return content_obj
    if isinstance(content_obj, dict):
        parts = content_obj.get("parts")
        if isinstance(parts, list):
            return " ".join(str(part) for part in parts if part is not None).strip()
        text = content_obj.get("text")
        if isinstance(text, str):
            return text
    return ""


def _parse_mapping_messages(conv: dict[str, Any]) -> list[ParsedMessage]:
    mapping = conv.get("mapping")
    if not isinstance(mapping, dict):
        return []

    rows: list[tuple[float, int, ParsedMessage]] = []
    fallback = 0
    for node_id, node in mapping.items():
        if not isinstance(node, dict):
            continue
        message = node.get("message")
        if not isinstance(message, dict):
            continue

        author = message.get("author") if isinstance(message.get("author"), dict) else {}
        role = str(author.get("role", "")).strip().lower() or "user"
        content = _as_text(message.get("content"))
        if not content:
            continue

        external_id = str(message.get("id") or node_id or f"msg-{fallback}")
        created_raw = message.get("create_time") or node.get("create_time")
        try:
            sort_time = float(created_raw) if created_raw is not None else float("inf")
        except (TypeError, ValueError):
            sort_time = float("inf")

        rows.append(
            (
                sort_time,
                fallback,
                ParsedMessage(
                    external_id=external_id,
                    role=role,
                    content=content,
                    created_at=str(created_raw) if created_raw is not None else None,
                ),
            )
        )
        fallback += 1

    rows.sort(key=lambda row: (row[0], row[1]))
    return [row[2] for row in rows]


def _parse_legacy_messages(conv: dict[str, Any]) -> list[ParsedMessage]:
    messages = conv.get("messages", [])
    parsed: list[ParsedMessage] = []
    for idx, msg in enumerate(messages):
        if not isinstance(msg, dict):
            continue
        content = _as_text(msg.get("content"))
        if not content:
            continue
        parsed.append(
            ParsedMessage(
                external_id=str(msg.get("id", f"msg-{idx}")),
                role=str(msg.get("role", "user")).strip().lower(),
                content=content,
                created_at=str(msg.get("created_at")) if msg.get("created_at") is not None else None,
            )
        )
    return parsed


def parse_chatgpt_export(payload: dict[str, Any]) -> list[ParsedConversation]:
    source = payload.get("conversations", payload)
    conversations = source if isinstance(source, list) else []
    parsed: list[ParsedConversation] = []

    for idx, conv in enumerate(conversations):
        if not isinstance(conv, dict):
            continue
        messages = _parse_mapping_messages(conv) or _parse_legacy_messages(conv)
        parsed.append(
            ParsedConversation(
                external_id=str(conv.get("id", f"conv-{idx}")),
                title=str(conv.get("title", "Untitled")),
                started_at=str(conv.get("create_time") or conv.get("started_at") or "") or None,
                messages=messages,
                raw_payload=conv,
            )
        )

    return parsed
