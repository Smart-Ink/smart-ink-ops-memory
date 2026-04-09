from __future__ import annotations

from typing import Any


class MemPalaceAdapter:
    def __init__(self) -> None:
        self._store: dict[str, list[dict[str, Any]]] = {}

    def index_conversation_chunks(self, project_id: str, chunks: list[dict[str, Any]]) -> dict[str, Any]:
        """Index chunks for a project.

        TODO(environment-specific): wire this method to actual MemPalace runtime/client.
        """
        self._store.setdefault(project_id, []).extend(chunks)
        return {"indexed": len(chunks)}

    def search_memory(self, query: str, project_id: str, limit: int = 10) -> list[dict[str, Any]]:
        """Search indexed memory.

        TODO(environment-specific): replace lexical scoring with MemPalace vector retrieval.
        """
        haystack = self._store.get(project_id, [])
        scored = []
        q = query.lower().strip()
        for idx, item in enumerate(haystack):
            text = str(item.get("content", ""))
            score = 1.0 if q and q in text.lower() else 0.1
            if score > 0:
                scored.append(
                    {
                        "id": f"mem-{idx}",
                        "score": score,
                        "snippet": text[:240],
                        "metadata": {
                            "conversation_external_id": item.get("conversation_external_id", ""),
                            "message_external_id": item.get("message_external_id", ""),
                            "chunk_index": str(item.get("chunk_index", "")),
                        },
                    }
                )
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:limit]
