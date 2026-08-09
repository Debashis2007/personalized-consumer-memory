# Copyright (c) 2026 Debashis Bhattacharjee. All Rights Reserved.
# Unauthorized copying, modification, or distribution is prohibited.
# https://github.com/Debashis2007

"""Personalized Consumer Memory — thin self-contained FastAPI POC."""

from __future__ import annotations

from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

from poc_core import MockLLM, TokenBucket, health_payload, AUTHOR_NAME, AUTHOR_FINGERPRINT, AUTHOR_GITHUB
from poc_core.safety import SafetyPlane
from poc_core.stores import InMemoryStore, MockVectorIndex

USE_CASE = "Personalized Consumer Memory"
app = FastAPI(title=USE_CASE)
llm = MockLLM()
store = InMemoryStore()
safety = SafetyPlane()

@app.get("/health")
def health():
    return health_payload(
        USE_CASE,
        {
            "author": AUTHOR_NAME,
            "author_github": AUTHOR_GITHUB,
            "fingerprint": AUTHOR_FINGERPRINT,
        },
    )

@app.get("/author")
def author():
    return {
        "author": AUTHOR_NAME,
        "github": AUTHOR_GITHUB,
        "fingerprint": AUTHOR_FINGERPRINT,
        "notice": "Copyright (c) 2026 Debashis Bhattacharjee. All Rights Reserved.",
    }


memories: dict[str, MockVectorIndex] = {}

class MemIn(BaseModel):
    user_id: str
    text: str

class QIn(BaseModel):
    user_id: str
    query: str

@app.post("/memory")
def add_memory(body: MemIn):
    memories.setdefault(body.user_id, MockVectorIndex())
    ch = memories[body.user_id].upsert(f"{body.user_id}-{len(memories[body.user_id].chunks)}", body.user_id, body.text, {body.user_id})
    return {"stored": ch.chunk_id}

@app.post("/memory/query")
def query_memory(body: QIn):
    idx = memories.get(body.user_id) or MockVectorIndex()
    # hard isolation: search only with user acl
    return {"hits": idx.search(body.query, {body.user_id})}

@app.delete("/memory/{user_id}")
def forget(user_id: str):
    memories.pop(user_id, None)
    return {"forgotten": user_id}
