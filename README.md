# NorthBrief MVP

NorthBrief is a Canada-first, region-aware, source-linked news briefing MVP.  
It surfaces short AI summaries with clear attribution and outbound links to original publishers.

## Problem Statement

Canadian readers often need to check several national, provincial, city, finance, and global publishers to understand what matters locally. Traditional aggregators can overwhelm readers with duplicate stories, weak regional relevance, and unclear source attribution.

NorthBrief solves this by combining preference-based regional and category relevance, concise neutral summaries, duplicate clustering, and prominent links to original publishers. The product is designed to help busy readers discover important reporting quickly without replacing or republishing the journalism itself.

## Tech Stack
- Frontend: Next.js 14 App Router, React, TypeScript, Tailwind CSS, Framer Motion
- Authentication: NextAuth credentials flow backed by FastAPI JWT authentication
- Backend: FastAPI, Pydantic, SQLAlchemy, Alembic
- Database: PostgreSQL
- Ingestion: Python RSS pipeline with parallel fetching, retries, source health tracking, region/category tagging, and duplicate clustering
- Background jobs: Python worker loop with cron-friendly execution
- AI: provider abstraction with deterministic local fallback and OpenAI-ready summarization
- Infrastructure: Docker and Docker Compose

## Deployment
The repository includes a Render Blueprint for deploying the Next.js frontend, FastAPI backend, and PostgreSQL database. The free deployment uses on-demand web services; the continuous ingestion worker remains available through Docker Compose or can be added as a paid Render worker.

[Deploy to Render](https://render.com/deploy?repo=https://github.com/BhavikWadhwa/NorthBrief)

## Project Structure
```text
.
├─ backend/
│  ├─ app/
│  │  ├─ api/                # FastAPI routes and auth deps
│  │  ├─ core/               # config + security helpers
│  │  ├─ db/                 # SQLAlchemy base/session
│  │  ├─ models/             # DB models
│  │  ├─ schemas/            # Pydantic schemas
│  │  ├─ services/
│  │  │  ├─ ingestion/       # source registry + fetch + dedupe + taggers + pipeline
│  │  │  └─ summarization/   # provider abstraction and guardrails
│  │  ├─ seed.py             # dev seed data
│  │  └─ worker.py           # scheduled ingestion worker
│  ├─ alembic/               # migrations
│  ├─ config/
│  │  ├─ sources.json        # feed registry
│  │  └─ prompt_templates.md # summarization templates
│  ├─ .env.example
│  └─ pyproject.toml
├─ frontend/
│  ├─ app/                   # App Router pages
│  ├─ components/            # reusable UI + app shell
│  ├─ lib/                   # API client + auth + types
│  ├─ tests/                 # lightweight component tests
│  └─ .env.example
├─ docker-compose.yml
└─ README.md
```

## Core MVP Scope Implemented
- User auth (signup/signin) with NextAuth credentials + backend JWT
- Onboarding preferences:
  - country default Canada
  - province/city selection with province-aware city dropdowns
  - category-only interests (no sliders)
  - skip personalization option
- Personalized feed tabs: `For You`, `Local`, `Canada`, `World`, `Finance`, `Trending`
- News card UX:
  - headline
  - concise summary
  - “Why this matters”
  - category/region context
  - source attribution and domain
  - publish-relative time
  - external “Read full story”
  - bookmark action
- Source transparency and canonical URL preservation
- Admin/dev dashboard:
  - trigger ingestion
  - inspect processed article status/confidence
  - retry summarization endpoint on backend
  - manage source registry (view/add/enable/disable)
- Ingestion pipeline:
  - configurable source registry
  - source bootstrap from config + DB-managed source operations
  - parallel multi-source fetch with retry
  - per-source ingestion run tracking
  - RSS metadata ingest
  - dedupe and clustering (store duplicates, show one primary in feed)
  - category and region inference with confidence
  - summarization + guardrails + review flags
  - traceability via `raw_articles` and `summarization_runs`
- Seed/demo data for immediate local demo
- Backend unit tests + frontend component test

## Database Schema
Primary tables included:
- `users`
- `user_preferences`
- `news_sources`
- `raw_articles`
- `processed_articles`
- `categories`
- `regions`
- `article_category_links`
- `article_region_links`
- `ingestion_runs`
- `source_ingestion_runs`
- `summarization_runs`
- `bookmarks`
- `hidden_articles`

Initial migration: `backend/alembic/versions/20260403_01_initial_schema.py`

## Local Run (Docker)
1. Copy env files:
```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```
2. Start stack:
```bash
docker compose up --build
```
3. Open:
- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend docs: [http://localhost:8000/docs](http://localhost:8000/docs)

Seeded admin account:
- email: `admin@northbrief.local`
- password: `password123`

Note:
- In Docker, NextAuth server-side calls use `INTERNAL_API_URL=http://backend:8000/api/v1`.

## Local Run (Without Docker)
### Backend
```bash
cd backend
pip install -e ".[dev]"
alembic upgrade head
python -m app.seed
uvicorn app.main:app --reload
```

### Worker
```bash
cd backend
python -m app.worker
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## API Overview
Base prefix: `/api/v1`
- `GET /health`
- `POST /auth/signup`
- `POST /auth/login`
- `GET /auth/me`
- `GET /preferences`
- `PUT /preferences`
- `GET /feed?tab=for-you|local|canada|world|finance|trending`
- `GET /bookmarks`
- `POST /bookmarks`
- `DELETE /bookmarks/{processed_article_id}`
- `GET /meta/categories`
- `GET /meta/regions`
- `POST /admin/ingestion/run` (admin)
- `GET /admin/articles` (admin)
- `POST /admin/summaries/retry/{raw_article_id}` (admin)
- `GET /sources` (admin)
- `POST /sources` (admin)
- `PATCH /sources/{source_id}` (admin)

## Summarization Providers
Config: `SUMMARIZATION_PROVIDER`
- `mock` (default): deterministic fallback for local/dev
- `openai`: uses OpenAI Responses API (requires `OPENAI_API_KEY`)

Guardrails:
- trims overly long summary output
- flags low-context/low-quality outputs for review
- keeps wording neutral and factual by design

## Integrating Real News Sources
Real news ingestion is configured in:
- `backend/config/sources.json`

How to add a source:
1. Add a new object in `sources.json` with `name`, `source_type`, `feed_url`, `site_url`, default category/region.
   Required fields supported: `priority` (0-1), `is_active` (bool).
2. Use RSS or other metadata-only feeds (headline/snippet/link/image metadata), not full-article republishing.
3. Restart backend/worker or run admin ingestion.

How to trigger ingestion:
- In app: open `/admin` and click `Run ingestion now`.
- Or API: `POST /api/v1/admin/ingestion/run` with an admin token.
- In local development (`ENVIRONMENT=development`), admin endpoints are accessible to authenticated users for faster testing.
- Optional: promote a user to admin manually:
  - `docker compose exec backend python -m app.make_admin you@example.com`

Image support:
- If a feed provides image metadata (`media_content`, `media_thumbnail`, or image links), it is stored as `image_url` and shown at the top of each news card.
- If a feed item has no image metadata, topic-based fallback images are used from `frontend/public/images/fallback`.

## MVP Complete vs Next
MVP complete:
- preference-based personalization
- region/category inference with confidence
- source-linked card feed and admin ingestion controls

Future improvements:
- story clustering and “More coverage”
- stronger geo/entity NLP
- richer source governance and legal policy controls
- queue-backed workers (Celery/RQ) and observability
- deeper automated tests (E2E, contract tests)
- multilingual summaries (EN/FR)
