from __future__ import annotations

import os
from typing import Any

import requests
from fastapi import FastAPI
from pydantic import BaseModel

from .chunking import chunk_message
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
    prepared = []
    memory_chunks = []

    for conversation in parsed:
        normalized_messages = normalize_transcript(conversation)
        conv_dict = {
            "external_id": conversation.external_id,
            "title": conversation.title,
            "started_at": conversation.started_at,
            "raw_payload": conversation.raw_payload,
            "messages": [],
        }
        for message in normalized_messages:
            chunks = chunk_message(message["content"])
            candidates = extract_candidates(message["content"])
            conv_dict["messages"].append({**message, "chunks": chunks, "candidates": candidates})
            for idx, chunk in enumerate(chunks):
                memory_chunks.append(
                    {
                        "project_id": payload.projectId,
                        "conversation_external_id": conversation.external_id,
                        "message_external_id": message["external_id"],
                        "chunk_index": idx,
                        "content": chunk,
                    }
                )
        prepared.append(conv_dict)

    stats = persist_import(payload.projectId, payload.sourceName, prepared, memory_chunks)

    memory_url = os.environ.get("MEMORY_SERVICE_URL", "http://localhost:8102")
    requests.post(f"{memory_url}/index", json={"project_id": payload.projectId, "chunks": memory_chunks}, timeout=10)

    return {"ok": True, "stats": stats}
