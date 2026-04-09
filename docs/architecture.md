# Architecture

`smart-ink-ops-memory` is intentionally lean and split by bounded responsibilities.

## Layers
1. **Web app (`apps/web`)**
   - Operational UI (dashboard, search, inbox, tasks, meetings, prompts, assets, analytics)
   - API routes for import trigger, inbox approvals, memory query proxy
2. **Data layer (`packages/db`)**
   - Prisma schema + client for all canonical operational entities and raw chat ingestion records
3. **Shared contracts (`packages/shared`)**
   - Shared enums/types for inbox and extraction payloads
4. **Extraction utils (`packages/ai`)**
   - deterministic chunking + heuristic extraction helpers used by services
5. **Ingestion service (`services/ingest`)**
   - Parses ChatGPT export JSON
   - Normalizes conversations/messages/chunks
   - Writes to Postgres
   - Creates InboxItem candidates
   - Calls memory adapter index endpoint
6. **Memory service (`services/memory`)**
   - Small adapter boundary around MemPalace-compatible capabilities
7. **Worker service (`services/worker`)**
   - Simple background jobs (analytics snapshots / extraction retries)

## MemPalace boundary
The app never imports MemPalace internals directly. Integration is isolated in `services/memory/src/adapter.py` with:
- `index_conversation_chunks(...)`
- `search_memory(...)`

This boundary allows replacement with a different memory engine later.
