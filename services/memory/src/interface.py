from __future__ import annotations

from typing import Any, Protocol


class MemoryAdapter(Protocol):
    def index_conversation_chunks(self, project_id: str, chunks: list[dict[str, Any]]) -> dict[str, Any]:
        ...

    def search_memory(self, query: str, project_id: str, limit: int = 10) -> list[dict[str, Any]]:
        ...
