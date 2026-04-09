from __future__ import annotations

from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel

from .adapter import MemPalaceAdapter

adapter = MemPalaceAdapter()
app = FastAPI(title="smart-ink memory service")


class IndexRequest(BaseModel):
    project_id: str
    chunks: list[dict[str, Any]]


class SearchRequest(BaseModel):
    project_id: str
    query: str
    limit: int = 10


@app.get('/health')
def health():
    return {'ok': True}


@app.post('/index')
def index(payload: IndexRequest):
    return adapter.index_conversation_chunks(payload.project_id, payload.chunks)


@app.post('/search')
def search(payload: SearchRequest):
    return {'results': adapter.search_memory(payload.query, payload.project_id, payload.limit)}
