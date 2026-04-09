# Memory Boundary (MemPalace Adapter)

The memory service is the only module aware of external memory engine behavior.

## Public adapter methods
- `index_conversation_chunks(chunks: list[dict]) -> dict`
- `search_memory(query: str, project_id: str, limit: int) -> list[dict]`

## Current implementation
A placeholder in-memory adapter is included for local MVP.

## Environment-specific TODOs
- Replace in-memory store with real MemPalace client initialization.
- Map chunk metadata fields to MemPalace index schema.
- Add auth/tenant token handling if MemPalace deployment requires it.

These TODOs are intentionally isolated to `services/memory/src/adapter.py` and `services/memory/src/main.py`.
