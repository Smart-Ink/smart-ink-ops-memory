from __future__ import annotations

import os
from typing import Any

import requests
from fastapi import FastAPI
from pydantic import BaseModel

from .chunking import build_exchange_pairs, chunk_exchange_pairs
from .db import persist_import
from .extract import extract_candidates
from .normalize import normalize_transcript
from .parser import parse_chatgpt_export


class ImportRequest(BaseModel):
    projectId: str
    sourceName: str = "chatgpt-export"
    export: dict[str, Any]


app = FastAPI(title="smart-ink ingest service")


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/import/chatgpt")
def import_chatgpt(payload: ImportRequest):
    parsed = parse_chatgpt_export(payload.export)
    prepared: list[dict[str, Any]] = []
    memory_chunks: list[dict[str, Any]] = []

    for conversation in parsed:
        normalized_messages = normalize_transcript(conversation)
        exchange_pairs = build_exchange_pairs(normalized_messages)
        pair_chunks = chunk_exchange_pairs(exchange_pairs)

        conv_dict: dict[str, Any] = {
            "external_id": conversation.external_id,
            "title": conversation.title,
            "started_at": conversation.started_at,
            "raw_payload": conversation.raw_payload,
            "messages": normalized_messages,
            "pair_chunks": [],
        }

        for idx, chunk in enumerate(pair_chunks):
            chunk_candidates = extract_candidates(
                chunk["content"],
                conversation_external_id=conversation.external_id,
                message_external_ids=chunk["message_external_ids"],
            )
            chunk_record = {
                **chunk,
                "chunk_index": idx,
                "candidates": chunk_candidates,
            }
            conv_dict["pair_chunks"].append(chunk_record)
            memory_chunks.append(
                {
                    "project_id": payload.projectId,
                    "conversation_external_id": conversation.external_id,
                    "message_external_ids": chunk["message_external_ids"],
                    "chunk_index": idx,
                    "content": chunk["content"],
                }
            )

        prepared.append(conv_dict)

    stats = persist_import(payload.projectId, payload.sourceName, prepared, memory_chunks)

    memory_url = os.environ.get("MEMORY_SERVICE_URL", "http://localhost:8102")
    requests.post(f"{memory_url}/index", json={"project_id": payload.projectId, "chunks": memory_chunks}, timeout=10)

    return {"ok": True, "stats": stats}
