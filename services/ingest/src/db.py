from __future__ import annotations

import os
import uuid

import psycopg2
from psycopg2.extras import Json


def get_conn():
    return psycopg2.connect(os.environ["DATABASE_URL"])


def _new_id() -> str:
    return uuid.uuid4().hex


def persist_import(project_id: str, source_name: str, parsed_conversations: list[dict], memory_chunks: list[dict]) -> dict:
    conn = get_conn()
    created = {"conversations": 0, "messages": 0, "chunks": 0, "candidates": 0}

    with conn:
        with conn.cursor() as cur:
            chat_source_id = _new_id()
            cur.execute(
                'INSERT INTO "ChatSource" (id, "projectId", "sourceName", "createdAt") VALUES (%s, %s, %s, now())',
                (chat_source_id, project_id, source_name),
            )

            for conv in parsed_conversations:
                conv_id = _new_id()
                cur.execute(
                    'INSERT INTO "ChatConversation" (id, "projectId", "chatSourceId", "externalId", title, "startedAt", "rawPayload", "createdAt") VALUES (%s, %s, %s, %s, %s, %s, %s, now())',
                    (
                        conv_id,
                        project_id,
                        chat_source_id,
                        conv["external_id"],
                        conv["title"],
                        conv.get("started_at"),
                        Json(conv.get("raw_payload", {})),
                    ),
                )
                created["conversations"] += 1

                message_id_map: dict[str, str] = {}
                for msg in conv["messages"]:
                    msg_id = _new_id()
                    message_id_map[msg["external_id"]] = msg_id
                    cur.execute(
                        'INSERT INTO "ChatMessage" (id, "projectId", "conversationId", "externalId", role, content, "sequenceNo", "createdAt") VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                        (
                            msg_id,
                            project_id,
                            conv_id,
                            msg["external_id"],
                            msg["role"],
                            msg["content"],
                            msg["sequence_no"],
                            msg.get("created_at"),
                        ),
                    )
                    created["messages"] += 1

                for pair_chunk in conv.get("pair_chunks", []):
                    source_message_ids = pair_chunk.get("message_external_ids", [])
                    db_message_id = message_id_map.get(source_message_ids[0]) if source_message_ids else None
                    if not db_message_id:
                        continue

                    chunk_id = _new_id()
                    chunk_content = pair_chunk["content"]
                    cur.execute(
                        'INSERT INTO "ChatChunk" (id, "projectId", "conversationId", "messageId", "chunkIndex", content, "tokenEstimate", "embeddingStatus", "createdAt") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, now())',
                        (
                            chunk_id,
                            project_id,
                            conv_id,
                            db_message_id,
                            pair_chunk["chunk_index"],
                            chunk_content,
                            max(1, len(chunk_content.split())),
                            "indexed",
                        ),
                    )
                    created["chunks"] += 1

                    for candidate in pair_chunk.get("candidates", []):
                        inbox_id = _new_id()
                        cur.execute(
                            'INSERT INTO "InboxItem" (id, "projectId", type, title, summary, payload, "confidenceScore", status, "createdAt") VALUES (%s, %s, %s::"InboxType", %s, %s, %s, %s, %s::"InboxStatus", now())',
                            (
                                inbox_id,
                                project_id,
                                candidate["type"],
                                candidate["title"],
                                candidate["summary"],
                                Json(candidate["payload"]),
                                candidate["confidence_score"],
                                "pending",
                            ),
                        )
                        created["candidates"] += 1

                        cur.execute(
                            'INSERT INTO "SourceReference" (id, "projectId", "sourceType", "conversationId", "messageId", "chunkId", "inboxItemId", metadata, "createdAt") VALUES (%s, %s, %s::"SourceRefType", %s, %s, %s, %s, %s, now())',
                            (
                                _new_id(),
                                project_id,
                                "chunk",
                                conv_id,
                                db_message_id,
                                chunk_id,
                                inbox_id,
                                Json(
                                    {
                                        "reason": "extraction",
                                        "source_message_external_ids": source_message_ids,
                                        "pair_index": pair_chunk.get("pair_index"),
                                    }
                                ),
                            ),
                        )

    conn.close()
    return {**created, "memory_chunks": len(memory_chunks)}
