from __future__ import annotations

import os
import psycopg2
from psycopg2.extras import Json


def get_conn():
    return psycopg2.connect(os.environ["DATABASE_URL"])


def persist_import(project_id: str, source_name: str, parsed_conversations: list[dict], memory_chunks: list[dict]) -> dict:
    conn = get_conn()
    created = {"conversations": 0, "messages": 0, "chunks": 0, "candidates": 0}
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO \"ChatSource\" (id, \"projectId\", \"sourceName\", \"createdAt\") VALUES (gen_random_uuid()::text, %s, %s, now()) RETURNING id",
                (project_id, source_name),
            )
            chat_source_id = cur.fetchone()[0]
            for conv in parsed_conversations:
                cur.execute(
                    "INSERT INTO \"ChatConversation\" (id, \"projectId\", \"chatSourceId\", \"externalId\", title, \"startedAt\", \"rawPayload\", \"createdAt\") VALUES (gen_random_uuid()::text, %s, %s, %s, %s, %s, %s, now()) RETURNING id",
                    (project_id, chat_source_id, conv["external_id"], conv["title"], conv.get("started_at"), Json(conv.get("raw_payload", {}))),
                )
                conv_id = cur.fetchone()[0]
                created["conversations"] += 1
                for msg in conv["messages"]:
                    cur.execute(
                        "INSERT INTO \"ChatMessage\" (id, \"projectId\", \"conversationId\", \"externalId\", role, content, \"sequenceNo\", \"createdAt\") VALUES (gen_random_uuid()::text, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
                        (project_id, conv_id, msg["external_id"], msg["role"], msg["content"], msg["sequence_no"], msg.get("created_at")),
                    )
                    msg_id = cur.fetchone()[0]
                    created["messages"] += 1
                    for c_idx, chunk in enumerate(msg["chunks"]):
                        cur.execute(
                            "INSERT INTO \"ChatChunk\" (id, \"projectId\", \"conversationId\", \"messageId\", \"chunkIndex\", content, \"tokenEstimate\", \"embeddingStatus\", \"createdAt\") VALUES (gen_random_uuid()::text, %s, %s, %s, %s, %s, %s, 'indexed', now()) RETURNING id",
                            (project_id, conv_id, msg_id, c_idx, chunk, max(1, len(chunk.split()))),
                        )
                        chunk_id = cur.fetchone()[0]
                        created["chunks"] += 1
                        for candidate in msg.get("candidates", []):
                            cur.execute(
                                "INSERT INTO \"InboxItem\" (id, \"projectId\", type, title, summary, payload, \"confidenceScore\", status, \"createdAt\") VALUES (gen_random_uuid()::text, %s, %s::\"InboxType\", %s, %s, %s, %s, 'pending', now()) RETURNING id",
                                (project_id, candidate["type"], candidate["title"], candidate["summary"], Json(candidate["payload"]), candidate["confidence_score"]),
                            )
                            inbox_id = cur.fetchone()[0]
                            created["candidates"] += 1
                            cur.execute(
                                "INSERT INTO \"SourceReference\" (id, \"projectId\", \"sourceType\", \"conversationId\", \"messageId\", \"chunkId\", \"inboxItemId\", metadata, \"createdAt\") VALUES (gen_random_uuid()::text, %s, 'chunk'::\"SourceRefType\", %s, %s, %s, %s, %s, now())",
                                (project_id, conv_id, msg_id, chunk_id, inbox_id, Json({"reason": "extraction"})),
                            )
    conn.close()
    return {**created, "memory_chunks": len(memory_chunks)}
