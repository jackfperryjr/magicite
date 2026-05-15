# Magicite

> The processing core of the Magiloom ecosystem. Raw web clips enter; structured, embedded knowledge exits.

Part of the **[Magiloom](https://github.com/jackfperryjr)** second-brain ecosystem alongside [Aetherneedle](#) and [Crystarium](#).

---

## What it does

Magicite is a FastAPI service that acts as the refinement engine between the browser and the knowledge graph. When a clip arrives from the Aetherneedle extension, Magicite:

1. **Validates** the request against a Supabase-issued JWT
2. **Synthesizes** — sends the raw content to Claude for entity extraction and summarization via structured tool use
3. **Embeds** — converts the content into a 1024-dimensional vector via Voyage AI (`voyage-3`)
4. **Persists** — writes the enriched clip and its embedding to Supabase

The result is a piece of "crystallized" knowledge ready to be surfaced and connected in Crystarium.

---

## Stack

| Layer | Technology |
|---|---|
| Runtime | Python 3.12 |
| Framework | FastAPI |
| LLM | Claude (Anthropic) |
| Embeddings | Voyage AI — `voyage-3` |
| Database | Supabase (Postgres + pgvector) |
| Auth | Supabase JWT (HS256) |
| Deploy | Railway |

---

## API

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/clips` | Ingest, process, and store a web clip |

All routes except `/health` require a `Bearer` token issued by Supabase.
