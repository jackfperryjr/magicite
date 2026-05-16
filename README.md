# Magicite

> The processing core of the Magiloom ecosystem. Raw web clips enter; structured, embedded knowledge exits.

Part of the **Magiloom** second-brain ecosystem alongside [Aetherneedle](https://github.com/jackfperryjr/aetherneedle) and [Crystarium](https://github.com/jackfperryjr/crystarium).

<p align="center">
  <img src="https://github.com/jackfperryjr/magicite/actions/workflows/deploy.yml/badge.svg" alt="Build Status" height="20">
  <img src="https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=ffdd54" />
  <img src="https://img.shields.io/badge/FastAPI-005571?style=flat-square&logo=fastapi" />
  <img src="https://img.shields.io/badge/Supabase-3FC085?style=flat-square&logo=supabase&logoColor=white" alt="Supabase">
  <img src="https://img.shields.io/badge/Claude_4.6-D97706?style=flat-square&logo=anthropic&logoColor=white" alt="Claude 4.6">
  <img src="https://img.shields.io/badge/Voyage_AI-008080?style=flat-square&logo=vlc&logoColor=white" alt="Voyage AI">
</p>

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
