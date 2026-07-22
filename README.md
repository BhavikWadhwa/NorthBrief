# NorthBrief

NorthBrief is a Canada-first news briefing app for people who want to understand the day without opening ten different websites.

It brings together local, provincial, national, financial, and global stories, turns the available source information into a short neutral brief, and always links back to the publisher. The goal is not to replace journalism. It is to help someone decide which original stories are worth their time.

## Try It

- [Open the live NorthBrief app](https://northbrief-web-bhavik.onrender.com)
- [Check the API status](https://northbrief-api-bhavik.onrender.com/api/v1/health)

The demo is hosted on Render's free tier, so the first visit after a quiet period may take a little longer while the service wakes up.

## Why I Built It

News in Canada is often spread across city publications, provincial reporting, national outlets, government updates, and global sources. A Vancouver reader might care about a local transit disruption, a Bank of Canada announcement, and an international conflict, but those stories should not all be treated as equally local or equally urgent.

NorthBrief is my attempt to make that experience calmer. Users choose a province, city, and the topics they care about. The feed then considers location, interests, freshness, and source variety. It does this without following people around the internet or building a detailed behavioural profile.

## What It Can Do Today

- Create an account and choose a Canadian province and city.
- Select interests such as local news, Canada, world news, finance, politics, AI, and humanitarian stories.
- Browse `For You`, `Local`, `Canada`, `World`, `Finance`, and `Trending` feeds.
- Read short summaries and a plain-English "Why this matters" explanation.
- See the publisher, source website, publication time, and original article link on every card.
- Save stories for later.
- Use publisher images when they are included safely in feed metadata, with topic-based fallback images otherwise.
- Ingest stories from a configurable collection of 28 RSS and official public feeds.
- Group repeated coverage so the feed does not show the same story over and over.
- Manage sources and ingestion from a small admin dashboard.

## Tech Stack, In Plain English

NorthBrief is split into a website, an API, a database, and a news-processing pipeline.

| Part | Technology | What it does here |
| --- | --- | --- |
| Website | Next.js 15, React, TypeScript | Builds the pages people see and keeps the interface type-safe. |
| Styling and motion | Tailwind CSS, Framer Motion, Lucide | Handles the responsive design, visual system, animation, and icons. |
| Sign-in | NextAuth plus secure API tokens | Keeps browser sessions connected to the correct backend user. |
| API | FastAPI and Pydantic | Receives requests from the website and checks incoming data. |
| Database access | SQLAlchemy and Alembic | Reads and writes data, and safely applies database changes over time. |
| Database | PostgreSQL | Stores users, preferences, sources, raw feed items, summaries, and bookmarks. |
| News ingestion | Python, Feedparser, RSS/Atom | Fetches permitted feed metadata, then cleans, tags, and deduplicates it. |
| Summaries | Swappable provider layer | Supports OpenAI, with a predictable local fallback for development and the public demo. |
| Local environment | Docker Compose | Starts the website, API, worker, and database together. |
| Hosting | Render | Hosts the live frontend and backend from this repository. |

The live demo currently uses the deterministic fallback summarizer so it can run without sending publisher metadata to a paid AI service. Setting `SUMMARIZATION_PROVIDER=openai` and providing an `OPENAI_API_KEY` enables the OpenAI provider.

## The Parts That Did Not Work the First Time

This project had a few very real bumps on the way to production. I have kept them here because they explain several design decisions in the code and are more useful than pretending the deployment was effortless.

### 1. Account creation failed even though the form looked correct

**What happened:** New users saw a general sign-in error. The backend logs showed that the password library and the installed version of `bcrypt` did not agree with each other. One code path also hit bcrypt's 72-byte password limit.

**How I fixed it:** Passwords now use `PBKDF2-SHA256`, which avoids that compatibility problem and supports the password lengths accepted by the API. Password verification also fails safely when it receives an invalid stored hash instead of crashing the login request.

### 2. The admin page returned "403 Forbidden"

**What happened:** The page loaded, but a normal account could not run ingestion. This looked like a broken button, but the API was correctly refusing an account without admin permission.

**How I fixed it:** Local development remains convenient for testing, while production checks the user's admin flag. Render creates a unique production admin password through the `ADMIN_PASSWORD` environment variable instead of publishing a predictable password in the repository.

### 3. NorthBrief and another project were pointed at the same Render database

**What happened:** The available Render database already belonged to the AutoFlow project. Letting NorthBrief create tables in the default area could have mixed two unrelated applications together.

**How I fixed it:** NorthBrief uses its own PostgreSQL schema named `northbrief`. Think of it as a separate locked room inside the same database building. The startup process creates that room if needed, and every NorthBrief database connection is directed there. AutoFlow's tables are left alone.

### 4. Database setup failed during the first Render deployments

**What happened:** Render could build the container, but the API did not start reliably. The database address contained encoded connection options that the migration tool interpreted incorrectly, and the original startup command did not make the required order obvious.

**How I fixed it:** The backend now has one explicit startup script. It prepares the isolated schema, applies migrations, adds safe seed data, and only then starts the API. The database URL is escaped correctly before Alembic reads it.

### 5. A feed item contained a date that PostgreSQL could not save as JSON

**What happened:** The worker fetched real stories, then stopped with `datetime is not JSON serializable`. The date was valid, but raw JSON cannot store a Python date object directly. After that error, the same database session also needed to be reset before it could continue.

**How I fixed it:** Raw feed values are converted into JSON-safe strings before storage. Source processing is isolated so one failed publisher is recorded and skipped instead of taking down the entire ingestion run.

### 6. One slow or outdated RSS feed could freeze all ingestion

**What happened:** The first 28-source production run appeared to start but did not finish. The feed parser had no network timeout, so a single publisher that never completed its response could hold up every other source.

**How I fixed it:** Every feed request now has a 20-second limit, a 5 MB download limit, and a maximum of 50 entries per source per run. Fetches still happen in parallel, failed sources are retried and logged, and healthy sources continue. After this change, the live feed filled with real publisher-linked stories from regional, national, official, technology, and global sources.

### 7. Render's free tier does not include the always-running worker used locally

**What happened:** Docker Compose could run scheduled ingestion continuously, but duplicating that setup on Render would require another paid service.

**How I fixed it for the MVP:** Production can start a guarded background ingestion after a deployment while the API becomes available normally. It will not repeat if a completed run happened in the previous hour. Local development still includes the regular worker, and a dedicated queue or scheduled worker is the right next step for a larger deployment.

## How News Moves Through NorthBrief

1. The source registry loads active feeds from `backend/config/sources.json`.
2. Feeds are fetched in parallel with timeouts, retries, and size limits.
3. NorthBrief stores the headline, original URL, publisher, date, short feed description, and optional image metadata.
4. Rules add likely region and category labels, along with confidence scores.
5. Similar headlines are clustered so one event does not overwhelm the feed.
6. The summarizer creates a short brief and a "Why this matters" sentence. Weak source material is flagged rather than confidently filled in.
7. Feed ranking considers the user's choices, freshness, regional relevance, category relevance, and source priority.
8. The finished card keeps the original publisher and link visible.

NorthBrief does not intentionally download and republish complete articles. It is designed around headlines, permitted snippets, RSS/Atom metadata, official feeds, and outbound source links.

## Source Coverage

The source registry currently contains 28 entries across:

- Canadian city and provincial reporting, including British Columbia, Alberta, Ottawa, Toronto, Montreal, Winnipeg, and Halifax.
- Canadian national publishers.
- Government of Canada and Statistics Canada updates.
- Canadian and global finance coverage.
- World news.
- Technology and AI reporting.

Adding or removing a source does not require changing application code. Edit `backend/config/sources.json` or use the admin source manager. Each source includes its feed URL, website, default region, default category, ranking priority, and active status.

## Run It Locally With Docker

You will need Docker Desktop.

1. Create local environment files:

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

On Windows PowerShell, use:

```powershell
Copy-Item backend/.env.example backend/.env
Copy-Item frontend/.env.example frontend/.env
```

2. Build and start everything:

```bash
docker compose up --build
```

3. Open the services:

- Website: [http://localhost:3000](http://localhost:3000)
- Interactive API documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

The local seed account is:

```text
Email: admin@northbrief.local
Password: password123
```

These credentials are only the local development defaults. Production uses a generated password.

## Run It Without Docker

Start PostgreSQL first and set the database address in `backend/.env`.

### Backend

```bash
cd backend
pip install -e ".[dev]"
alembic upgrade head
python -m app.seed
uvicorn app.main:app --reload
```

### Background worker

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

## Useful Configuration

| Variable | Purpose |
| --- | --- |
| `DATABASE_URL` | PostgreSQL connection address. |
| `DB_SCHEMA` | Optional isolated PostgreSQL schema, such as `northbrief`. |
| `JWT_SECRET` | Secret used to sign backend login tokens. |
| `NEXTAUTH_SECRET` | Secret used to protect browser sessions. |
| `ADMIN_EMAIL` / `ADMIN_PASSWORD` | Production administrator credentials. |
| `SUMMARIZATION_PROVIDER` | `mock` for the fallback or `openai` for OpenAI. |
| `OPENAI_API_KEY` | Required only when the OpenAI provider is selected. |
| `INGEST_ON_STARTUP` | Allows a guarded ingestion run after deployment. |
| `CORS_ORIGINS` | Website addresses allowed to call the API. |

Example values are available in `backend/.env.example` and `frontend/.env.example`. Never commit real secrets.

## Main API Routes

All API routes begin with `/api/v1`.

- `POST /auth/signup` and `POST /auth/login`
- `GET /preferences` and `PUT /preferences`
- `GET /feed?tab=for-you`
- `GET`, `POST`, and `DELETE /bookmarks`
- `GET /meta/categories` and `GET /meta/regions`
- `POST /admin/ingestion/run`
- `GET /admin/articles`
- `POST /admin/summaries/retry/{raw_article_id}`
- `GET`, `POST`, and `PATCH /sources`
- `GET /health`

The full interactive reference is available at `/docs` while the backend is running.

## Project Layout

```text
.
|-- backend/
|   |-- app/
|   |   |-- api/              Request routes and authentication
|   |   |-- core/             Settings and security
|   |   |-- models/           Database models
|   |   |-- schemas/          Input and output validation
|   |   |-- services/         Ranking, tagging, ingestion, and summaries
|   |   |-- seed.py           Local demo data
|   |   `-- worker.py         Scheduled local ingestion
|   |-- alembic/              Database migrations
|   |-- config/               Sources and summary prompts
|   `-- .env.example
|-- frontend/
|   |-- app/                  Next.js pages
|   |-- components/           Reusable interface components
|   |-- lib/                  API, authentication, and shared types
|   |-- public/               Static and fallback images
|   `-- tests/
|-- docker-compose.yml
|-- render.yaml
`-- README.md
```

## What Comes Next

The current version is a working portfolio and startup MVP, not a finished newsroom product. The most useful next improvements would be:

- A dedicated scheduled worker and job queue for more predictable ingestion.
- Better "More coverage" groups when several publishers report the same event.
- Stronger place-name and organization recognition.
- English and French summaries.
- Better source governance, licensing records, and editorial review tools.
- End-to-end browser tests and production monitoring.
- User controls for hiding stories and adjusting individual source preferences.

## A Note on the Product Philosophy

NorthBrief should help readers reach good reporting, not avoid it. A useful brief gives someone enough context to understand why a story matters, clearly shows where the information came from, and makes the original article the natural next click.
