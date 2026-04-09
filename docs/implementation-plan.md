# Implementation Plan (Schema + Migrations + Seed Refresh)

1. **Reconfirm Prisma schema coverage**
   - Verify every required MVP entity exists in `packages/db/prisma/schema.prisma` and keep relations/enums consistent.

2. **Add explicit Prisma migration artifacts**
   - Create `packages/db/prisma/migrations/` with an initial SQL migration that creates enums, tables, indexes, and foreign keys for all schema models.
   - Add `migration_lock.toml` for PostgreSQL provider.

3. **Upgrade seed data realism**
   - Rewrite `packages/db/prisma/seed.ts` to seed one realistic imported conversation pipeline record set (`ChatSource`, `ChatConversation`, `ChatMessage`, `ChatChunk`, `SourceReference`).
   - Seed exactly: 3 inbox items, 2 tasks, 2 prompts, and 1 meeting, plus supporting entities.

4. **Validate**
   - Run Prisma format and TypeScript seed compile check.
   - Run ingestion tests to ensure surrounding behavior still passes.
