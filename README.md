# Use Case: Personalized Consumer Memory

**Author fingerprint:** `DBHATT-Debashis2007-SystemDesignPOC-2026` — Debashis Bhattacharjee ([@Debashis2007](https://github.com/Debashis2007))

**YouTube walkthrough:** [Personalized Consumer Memory — System Design #Shorts](https://youtu.be/A7SJFImj4JM)

**Design doc:** [docs/DESIGN.md](./docs/DESIGN.md) — architecture, patterns, and why.


**Parent system design:** [04 — RAG / Document Retrieval](https://github.com/Debashis2007/personalized-consumer-memory/blob/main/04-rag-embedding-pipeline.md)

## Users & problem

Consumers upload notes/files or opt into memory so the assistant remembers preferences. Isolation and delete/forget are product-critical.

## Requirements & SLOs

| Requirement | Target |
|-------------|--------|
| Isolation | Per-user indexes or strict partitions |
| Forget | Hard delete within policy SLA |
| Latency | Fast personal retrieve |
| Consent | Explicit opt-in controls |

## Design (from parent)

```
User memory events / uploads → per-user chunk+embed
  → user-scoped vector+meta store
  → query only with user_id key
  → delete path: tombstone + async purge
```

Reuse versioned chunks from **04**; **never** share ANN postings across users.

## Specializations

| Concern | Consumer memory choice |
|---------|------------------------|
| Scale | Millions of tiny indexes → pack users in shards with hard filters |
| UX | Memory inspector UI; per-item delete |
| Safety | Memory content untrusted for tool privilege ([07](https://github.com/Debashis2007/personalized-consumer-memory/blob/main/07-agent-runtime-containment.md)) |
| Retention | TTL tiers; export/download |

## Failure modes

- Cache key missing user_id → force ACL key in every cache layer.
- Soft delete only → purge job SLO + verify absence in ANN.
- Prompt injection via “remember this” → policy engine ignores memory for privilege.




## Design walkthrough (opens on GitHub)

> **Watch on YouTube:** [Personalized Consumer Memory — System Design #Shorts](https://youtu.be/A7SJFImj4JM)


![Design overview](docs/video/design-overview.gif)

Full narrated video (download): [docs/video/design-overview.mp4](docs/video/design-overview.mp4)

## Run (self-contained POC)

This folder is a **standalone** project (safe to split into its own GitHub repo).

```bash
cd personalized-consumer-memory
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
PYTHONPATH=. python -m uvicorn app.main:app --reload --port 8000
```

```bash
curl -s http://127.0.0.1:8000/health | jq
```

curl -s -X POST http://127.0.0.1:8000/memory -H 'Content-Type: application/json' -d '{"user_id":"u1","text":"I like dark mode"}' | jq

---

**Copyright (c) 2026 Debashis Bhattacharjee. All Rights Reserved.**  
Unauthorized copying or redistribution of this material is prohibited.  
GitHub: [Debashis2007](https://github.com/Debashis2007)

