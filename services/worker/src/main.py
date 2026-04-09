from __future__ import annotations

import os

import psycopg2
from fastapi import FastAPI

app = FastAPI(title="smart-ink worker service")


@app.get('/health')
def health():
    return {'ok': True}


@app.post('/jobs/analytics-snapshot')
def analytics_snapshot(project_id: str):
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    with conn:
        with conn.cursor() as cur:
            cur.execute('SELECT count(*) FROM "ChatConversation" WHERE "projectId"=%s', (project_id,))
            imported_conversations = cur.fetchone()[0]
            cur.execute('SELECT count(*) FROM "ChatChunk" WHERE "projectId"=%s AND "embeddingStatus"=%s', (project_id, 'indexed'))
            indexed_chunks = cur.fetchone()[0]
            cur.execute('SELECT count(*) FROM "InboxItem" WHERE "projectId"=%s AND status=%s::"InboxStatus"', (project_id, 'pending'))
            pending = cur.fetchone()[0]
            cur.execute('INSERT INTO "AnalyticsSnapshot" (id, "projectId", "snapshotDate", "importedConversations", "indexedChunks", "pendingInbox", "approvedPrompts", "approvedTasks", "approvedMeetings", "overdueTasks", "repeatedUnresolvedIdeas") VALUES (gen_random_uuid()::text, %s, now(), %s, %s, %s, 0, 0, 0, 0, 0)', (project_id, imported_conversations, indexed_chunks, pending))
    conn.close()
    return {'ok': True, 'project_id': project_id}
