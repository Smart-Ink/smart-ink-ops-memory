from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

from .interface import MemoryAdapter


class LocalStubMemPalaceAdapter(MemoryAdapter):
    """Local stub adapter for development when MemPalace is not wired."""

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


class MemPalaceHTTPAdapter(MemoryAdapter):
    """HTTP-backed adapter for real MemPalace integration.

    Expected endpoint behavior:
    - POST {base_url}{index_path} with { project_id, chunks }
    - POST {base_url}{search_path} with { project_id, query, limit }
    """

    def __init__(
        self,
        base_url: str,
        api_key: str | None = None,
        index_path: str = "/index",
        search_path: str = "/search",
        timeout_seconds: float = 20.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.index_path = index_path
        self.search_path = search_path
        self.timeout_seconds = timeout_seconds

    def _post_json(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        data = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        request = urllib.request.Request(url=url, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                body = response.read().decode("utf-8")
                return json.loads(body) if body else {}
        except urllib.error.HTTPError as exc:
            error_body = exc.read().decode("utf-8") if exc.fp else ""
            raise RuntimeError(f"MemPalace HTTP {exc.code}: {error_body}") from exc

    def index_conversation_chunks(self, project_id: str, chunks: list[dict[str, Any]]) -> dict[str, Any]:
        return self._post_json(self.index_path, {"project_id": project_id, "chunks": chunks})

    def search_memory(self, query: str, project_id: str, limit: int = 10) -> list[dict[str, Any]]:
        response = self._post_json(self.search_path, {"project_id": project_id, "query": query, "limit": limit})
        return list(response.get("results", []))


def get_memory_adapter(mode: str = "stub") -> MemoryAdapter:
    if mode == "stub":
        return LocalStubMemPalaceAdapter()

    if mode == "mempalace":
        base_url = os.environ.get("MEMPALACE_BASE_URL")
        if not base_url:
            raise ValueError("MEMPALACE_BASE_URL is required when MEMORY_ADAPTER_MODE=mempalace")

        return MemPalaceHTTPAdapter(
            base_url=base_url,
            api_key=os.environ.get("MEMPALACE_API_KEY"),
            index_path=os.environ.get("MEMPALACE_INDEX_PATH", "/index"),
            search_path=os.environ.get("MEMPALACE_SEARCH_PATH", "/search"),
            timeout_seconds=float(os.environ.get("MEMPALACE_TIMEOUT_SECONDS", "20")),
        )

    raise ValueError(f"Unsupported MEMORY_ADAPTER_MODE: {mode}")
