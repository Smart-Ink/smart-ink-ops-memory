from src.adapter import LocalStubMemPalaceAdapter


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
