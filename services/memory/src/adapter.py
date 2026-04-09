from __future__ import annotations

from typing import Any

from .interface import MemoryAdapter


class LocalStubMemPalaceAdapter(MemoryAdapter):
    """Local stub adapter for development when MemPalace is not wired.

    TODO(environment-specific): replace this with actual MemPalace client calls.
    """

    def __init__(self) -> None:
        self._store: dict[str, list[dict[str, Any]]] = {}

    def index_conversation_chunks(self, project_id: str, chunks: list[dict[str, Any]]) -> dict[str, Any]:
        self._store.setdefault(project_id, []).extend(chunks)
        return {"indexed": len(chunks), "adapter": "local-stub"}

    def search_memory(self, query: str, project_id: str, limit: int = 10) -> list[dict[str, Any]]:
        haystack = self._store.get(project_id, [])
        q = query.lower().strip()
        scored: list[dict[str, Any]] = []

        for idx, item in enumerate(haystack):
            text = str(item.get("content", ""))
            if not text:
                continue

            text_lower = text.lower()
            occurrences = text_lower.count(q) if q else 0
            lexical_score = (1.0 + occurrences * 0.1) if q and q in text_lower else 0.15

            scored.append(
                {
                    "id": str(item.get("id") or f"mem-{idx}"),
                    "score": round(lexical_score, 3),
                    "snippet": text[:280],
                    "metadata": {
                        "conversation_external_id": str(item.get("conversation_external_id", "")),
                        "message_external_ids": item.get("message_external_ids", []),
                        "chunk_index": str(item.get("chunk_index", "")),
                        "adapter": "local-stub",
                    },
                }
            )

        scored.sort(key=lambda row: row["score"], reverse=True)
        return scored[:limit]


def get_memory_adapter(mode: str = "stub") -> MemoryAdapter:
    if mode == "stub":
        return LocalStubMemPalaceAdapter()

    # TODO(environment-specific): instantiate real MemPalace adapter when runtime is configured.
    raise ValueError(f"Unsupported MEMORY_ADAPTER_MODE: {mode}")
