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


def parse_chatgpt_export(payload: dict[str, Any]) -> list[ParsedConversation]:
    conversations = payload.get("conversations", [])
    parsed: list[ParsedConversation] = []
    for conv in conversations:
      msgs: list[ParsedMessage] = []
      for idx, msg in enumerate(conv.get("messages", [])):
          msgs.append(
              ParsedMessage(
                  external_id=str(msg.get("id", f"msg-{idx}")),
                  role=str(msg.get("role", "user")),
                  content=str(msg.get("content", "")).strip(),
                  created_at=msg.get("created_at"),
              )
          )
      parsed.append(
          ParsedConversation(
              external_id=str(conv.get("id", "")),
              title=str(conv.get("title", "Untitled")),
              started_at=conv.get("started_at"),
              messages=[m for m in msgs if m.content],
              raw_payload=conv,
          )
      )
    return parsed
