# Implementation Plan: smart-ink-ops-memory MVP

## 1) Monorepo foundation
- Initialize a pnpm + turbo style monorepo structure with `apps`, `packages`, `services`, and `docs`.
- Add root workspace, TypeScript base config, docker compose, env example, and repo-level README.

## 2) Data layer with Prisma + Postgres
- Implement full Prisma schema in `packages/db/prisma/schema.prisma` covering all required MVP entities.
- Create DB client package and seed script for realistic demo data.

## 3) Shared contracts + AI extraction utilities
- Add shared TypeScript domain enums/types in `packages/shared`.
- Add lightweight extraction/chunking helpers in `packages/ai` for candidate generation.

## 4) Python services
- Build `services/ingest` FastAPI service for ChatGPT export import pipeline:
  - parse exports
  - normalize transcript
  - chunk messages
  - persist to Postgres
  - create inbox candidates with source references
  - call memory service adapter indexing endpoint
- Build `services/memory` FastAPI service exposing adapter boundary:
  - `index_conversation_chunks(...)`
  - `search_memory(...)`
- Build `services/worker` placeholder for periodic analytics snapshots/extraction jobs.

## 5) Next.js web app MVP modules
- Build left-sidebar app shell and pages for dashboard, memory search, prompt library, tasks, meetings, inbox, assets, analytics.
- Implement API routes:
  - import trigger endpoint
  - inbox approval endpoint
  - memory search proxy endpoint
- Implement dashboard cards + basic tables/lists and source traceability sections.

## 6) Tests + docs
- Add automated tests for parsing, normalization, chunking, candidate creation, approval flow (Python pytest).
- Write docs: architecture, ingestion flow, review queue, memory boundary.

## 7) Final validation
- Ensure local run path with docker compose + app instructions.
- Keep MemPalace integration behind explicit adapter TODO markers only where environment-specific.
