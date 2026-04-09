# smart-ink-ops-memory

Lean internal operations memory system for Smart Ink.

## Stack
- Monorepo: pnpm workspaces + turbo
- Web: Next.js + TypeScript (`apps/web`)
- Data: Postgres + Prisma (`packages/db`)
- Ingestion: Python FastAPI (`services/ingest`)
- Memory adapter: Python FastAPI (`services/memory`)
- Worker: Python FastAPI (`services/worker`)

## Quick start
1. Copy environment values:
   ```bash
   cp .env.example .env
   ```
2. Install JS dependencies:
   ```bash
   pnpm install
   ```
3. Start local infra + services:
   ```bash
   docker compose up --build -d
   ```
4. Generate Prisma client and apply migration + seed:
   ```bash
   pnpm db:generate
   pnpm db:migrate
   pnpm db:seed
   ```
5. Run web app:
   ```bash
   pnpm --filter @smart-ink/web dev
   ```

Open `http://localhost:3000`.

## Import ChatGPT export
- POST JSON payload to `apps/web` API route:
  - endpoint: `POST /api/import`
  - body: `{ "projectId": "...", "sourceName": "chatgpt-export", "export": { ... } }`
- Route proxies to ingest service, which stores conversations/messages/chunks + creates inbox candidates.

## Tests
Python ingestion tests:
```bash
cd services/ingest
pip install -r requirements.txt
pytest
```

## Docs
- `docs/implementation-plan.md`
- `docs/architecture.md`
- `docs/ingestion-flow.md`
- `docs/review-queue.md`
- `docs/memory-boundary.md`


## Seed dataset (MVP demo)
- 1 imported conversation with linked source, messages, and chunks
- 3 inbox candidates
- 2 prompts
- 2 tasks
- 1 meeting
- source references linking inbox candidates back to chunk/message/conversation


## MemPalace adapter modes
- `MEMORY_ADAPTER_MODE=stub` (default): local in-memory search/index behavior.
- `MEMORY_ADAPTER_MODE=mempalace`: uses HTTP adapter in `services/memory/src/adapter.py`.
  - required: `MEMPALACE_BASE_URL`
  - optional: `MEMPALACE_API_KEY`, `MEMPALACE_INDEX_PATH`, `MEMPALACE_SEARCH_PATH`, `MEMPALACE_TIMEOUT_SECONDS`

## Memory indexing/search helper scripts
Index normalized chunks:
```bash
python scripts/memory_index_chunks.py --project-id seed-project --chunks-file scripts/sample-memory-chunks.json
```

Run search query:
```bash
python scripts/memory_search_query.py --project-id seed-project --query "onboarding checklist"
```
