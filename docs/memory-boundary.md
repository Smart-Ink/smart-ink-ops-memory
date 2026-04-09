# Memory Boundary (MemPalace Adapter)

The memory service is the only module aware of external memory engine behavior.

## Adapter contract
`services/memory/src/interface.py` defines the required adapter interface:
- `index_conversation_chunks(chunks: list[dict]) -> dict`
- `search_memory(query: str, project_id: str, limit: int) -> list[dict]`

## Adapter implementations
- `LocalStubMemPalaceAdapter` (default, local development)
- `MemPalaceHTTPAdapter` (real integration via HTTP)

Set mode with:
- `MEMORY_ADAPTER_MODE=stub`
- `MEMORY_ADAPTER_MODE=mempalace` (requires `MEMPALACE_BASE_URL`)

## MemPalace integration env
- `MEMPALACE_BASE_URL` (required in `mempalace` mode)
- `MEMPALACE_API_KEY` (optional bearer token)
- `MEMPALACE_INDEX_PATH` (default `/index`)
- `MEMPALACE_SEARCH_PATH` (default `/search`)
- `MEMPALACE_TIMEOUT_SECONDS` (default `20`)

## Local command helpers
Index sample chunks:
```bash
python scripts/memory_index_chunks.py --project-id seed-project --chunks-file scripts/sample-memory-chunks.json
```

Search sample memory:
```bash
python scripts/memory_search_query.py --project-id seed-project --query "onboarding checklist"
```
