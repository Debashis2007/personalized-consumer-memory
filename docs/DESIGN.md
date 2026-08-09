# Design: Personalized Consumer Memory

**Project:** `personalized-consumer-memory`  
**Parent system design:** `04-rag-embedding-pipeline.md`

## 1. What this POC demonstrates

Per-user memory indexes with hard isolation and forget/delete.

## 2. Architecture (POC)

```text
POST /memory (user_id) → per-user MockVectorIndex
POST /memory/query → search only with user ACL
DELETE /memory/{user_id}
```

## 3. Patterns used (and why)

| Pattern | Why used | Where in code |
|---------|----------|---------------|
| Per-user index map | Prevents accidental cross-user ANN hits. | `memories[user_id]`. |
| ACL keyed by user_id | Defense in depth on search. | `search(..., {user_id})`. |
| Hard forget | Privacy requirement. | `DELETE` drops index. |

## 4. Key endpoints

`GET /health`, `POST /memory`, `POST /memory/query`, `DELETE /memory/{user_id}`

## 5. Tradeoffs / POC limits

No async purge verification against a durable ANN store.

## 6. How to run

See the **Run (self-contained POC)** section in [`../README.md`](../README.md).

This folder is self-contained and can be published as its own GitHub repository.

## 7. Design walkthrough video

> **Watch on YouTube:** [Personalized Consumer Memory — System Design #Shorts](https://youtu.be/A7SJFImj4JM)
>
> Direct link: **https://youtu.be/A7SJFImj4JM**

Also available in-repo:
- GIF preview: [`video/design-overview.gif`](./video/design-overview.gif)
- MP4 download: [`video/design-overview.mp4`](./video/design-overview.mp4)
- Narration script: [`video/narration.txt`](./video/narration.txt)

---

**Copyright (c) 2026 Debashis Bhattacharjee. All Rights Reserved.**  
Unauthorized copying or redistribution of this material is prohibited.  
GitHub: [Debashis2007](https://github.com/Debashis2007)

