import os

from src.adapter import LocalStubMemPalaceAdapter, MemPalaceHTTPAdapter, get_memory_adapter


def test_local_stub_index_and_search():
    adapter = LocalStubMemPalaceAdapter()

    out = adapter.index_conversation_chunks(
        "proj-1",
        [
            {"id": "c1", "content": "Weekly planning prompt template", "conversation_external_id": "conv-1", "message_external_ids": ["m1"], "chunk_index": 0},
            {"id": "c2", "content": "Meeting agenda and task follow up", "conversation_external_id": "conv-1", "message_external_ids": ["m2"], "chunk_index": 1},
        ],
    )
    assert out["indexed"] == 2

    results = adapter.search_memory("prompt", "proj-1", limit=5)
    assert len(results) == 2
    assert results[0]["metadata"]["adapter"] == "local-stub"
    assert results[0]["id"] == "c1"


def test_mempalace_http_adapter_methods(monkeypatch):
    adapter = MemPalaceHTTPAdapter(base_url="http://mempalace.local", api_key="x")

    def fake_post_json(path, payload):
        if path == "/index":
            return {"indexed": len(payload["chunks"]), "adapter": "mempalace-http"}
        if path == "/search":
            return {"results": [{"id": "hit-1", "score": 0.9, "snippet": "demo", "metadata": {}}]}
        raise AssertionError("unexpected path")

    monkeypatch.setattr(adapter, "_post_json", fake_post_json)

    indexed = adapter.index_conversation_chunks("proj-1", [{"content": "x"}])
    assert indexed["indexed"] == 1

    results = adapter.search_memory("demo", "proj-1", 5)
    assert results[0]["id"] == "hit-1"


def test_adapter_factory_requires_base_url_for_mempalace(monkeypatch):
    monkeypatch.delenv("MEMPALACE_BASE_URL", raising=False)
    try:
        get_memory_adapter("mempalace")
        assert False, "Expected ValueError when MEMPALACE_BASE_URL is missing"
    except ValueError:
        assert True

    monkeypatch.setenv("MEMPALACE_BASE_URL", "http://mempalace.local")
    adapter = get_memory_adapter("mempalace")
    assert isinstance(adapter, MemPalaceHTTPAdapter)

    # Avoid leaking env changes across tests
    if "MEMPALACE_BASE_URL" in os.environ:
        del os.environ["MEMPALACE_BASE_URL"]
