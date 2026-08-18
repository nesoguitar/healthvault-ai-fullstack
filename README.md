# HealthVault AI

A full-stack, AI-powered Personal Health Record (PHR) application.

- **Frontend**: Next.js 15 (App Router), TypeScript, Tailwind CSS, shadcn/ui-style
  components, React Hook Form + Zod, TanStack Query, Recharts.
- **Backend**: FastAPI, PostgreSQL + pgvector, SQLAlchemy 2.0, Alembic, JWT auth.
- **AI**: Pluggable provider — runs with zero external dependencies in `mock`
  mode, or against Azure OpenAI / OpenAI for real record-grounded answers.
- **Storage**: Pluggable — local disk in dev, Azure Blob Storage in production.

---

## Quick start (Docker — recommended)

Requires Docker and Docker Compose.

```bash
# 1. Start Postgres (with pgvector), the API, and the web app
docker compose up --build

# 2. In another terminal: run migrations and load the demo patient
docker compose exec backend alembic upgrade head
docker compose exec backend python -m app.seed
```

Then open:
- **App**: http://localhost:3000
- **API docs (Swagger)**: http://localhost:8000/api/v1/docs
- **Demo login**: `nathan.mekhaeil@example.com` / `DemoPass123!`

Everything runs in `AI_PROVIDER=mock` and `STORAGE_BACKEND=local` by default —
no Azure account or API key is required to run the full stack locally. See
[Connecting Azure services](#connecting-azure-services) below to switch either on.

---

## Running without Docker

### Backend

Requires Python 3.12+ and a local PostgreSQL 16 with the `pgvector` extension
available (easiest: run just the `db` service from `docker-compose.yml` —
`docker compose up db`).

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# edit .env — at minimum set DATABASE_URL and generate a real JWT_SECRET_KEY:
#   openssl rand -hex 32

alembic upgrade head
python -m app.seed          # optional: loads the demo patient
uvicorn app.main:app --reload
```

API is now at http://localhost:8000 (docs at `/api/v1/docs` while `DEBUG=true`).

### Frontend

Requires Node.js 18.18+.

```bash
npm install
cp .env.local.example .env.local   # NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
npm run dev
```

App is now at http://localhost:3000. Register a new account or sign in with
the seeded demo account.

---

## Architecture

```
app/                     Next.js routes (App Router)
components/               UI components (ui/, dashboard/, timeline/, ...)
contexts/auth-context.tsx  Client-side auth state (JWT in localStorage)
lib/api/                    Typed API client + backend<->frontend mappers
hooks/                        TanStack Query hooks (dashboard, timeline, chat, docs)
mock-data/                     Original static fixtures (now used only for
                                 reference/demo copy, e.g. suggested chat prompts)

backend/
  app/
    core/          Settings, DB engine/session, JWT + password hashing, auth deps
    models/         SQLAlchemy ORM models (one file per resource)
    schemas/         Pydantic request/response models
    api/v1/endpoints/ FastAPI routers — one per resource
    services/          storage.py (local/Azure Blob), ai.py (mock/Azure OpenAI/OpenAI),
                         document_intelligence.py, chat_context.py (RAG grounding), audit.py
    seed.py              Demo data loader
  alembic/               Migrations (0001 creates the full schema + pgvector extension)
```

### How the frontend talks to the backend

`lib/api/client.ts` is a thin `fetch` wrapper that attaches the JWT access
token and silently refreshes it on a 401. `lib/api/resources.ts` calls the
API and maps FastAPI's snake_case responses onto the same camelCase
TypeScript types (`types/index.ts`) the UI components were originally built
against — so the presentational components didn't need to change when the
data source moved from static mocks to a live API.

### Authentication

- `POST /api/v1/auth/register` creates a `User` (identity) and a `Patient`
  (clinical profile) row together.
- `POST /api/v1/auth/login` returns a short-lived access token (30 min) and
  a longer-lived refresh token (7 days). Repeated failed logins lock the
  account for 15 minutes.
- Every patient-data endpoint resolves "the current user's own patient
  record" server-side (`get_current_patient` in `app/core/deps.py`) rather
  than accepting a patient id from the URL — this is the main control
  against one account reading another account's PHI.

### AI Chat

`POST /api/v1/chat/messages` builds a context block from the patient's own
diagnoses, medications, allergies, labs, and timeline (`app/services/chat_context.py`)
and passes it to the configured AI provider as a system message, so answers
are grounded in that patient's real record rather than the model's general
knowledge. In `AI_PROVIDER=mock` (the default), canned responses are
returned instead, with no external API calls.

### File uploads

`POST /api/v1/documents` validates type/size, streams the file to the
configured storage backend, creates a `Document` row with
`status=processing`, and returns immediately. A background task then runs
text extraction (Azure Document Intelligence, or a no-op stub locally),
generates an embedding via the AI provider, and flips the status to
`processed` or `failed`. The frontend polls `GET /documents` every 2.5s
while any document is still processing.

---

## Connecting Azure services

All three integrations are optional and off by default. Set the relevant
env vars (in `backend/.env` or the `docker-compose.yml` environment block)
and restart the backend — no code changes needed.

### Azure Blob Storage

```bash
STORAGE_BACKEND=azure
AZURE_STORAGE_CONNECTION_STRING=<connection string>
# or, for managed-identity auth instead of a connection string:
# AZURE_STORAGE_ACCOUNT_URL=https://<account>.blob.core.windows.net
AZURE_STORAGE_CONTAINER_NAME=medical-records
```

### Azure OpenAI (chat + embeddings)

```bash
AI_PROVIDER=azure
AZURE_OPENAI_ENDPOINT=https://<resource>.openai.azure.com
AZURE_OPENAI_API_KEY=<key>
AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4o
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-small
EMBEDDING_DIMENSIONS=1536   # must match your embedding deployment's output size
```

If you change `EMBEDDING_DIMENSIONS`, update the `Vector(...)` dimension in
`app/models/document.py` / `app/models/chat.py` and generate a new Alembic
migration — pgvector columns have a fixed dimension.

### Azure AI Document Intelligence (OCR / structured extraction)

```bash
DOCUMENT_INTELLIGENCE_ENABLED=true
AZURE_DOCINTEL_ENDPOINT=https://<resource>.cognitiveservices.azure.com
AZURE_DOCINTEL_API_KEY=<key>
```

---

## HIPAA-oriented design notes

This is a demo-grade MVP, not a certified HIPAA-compliant system — going to
production would additionally require a signed BAA with Azure, encryption
key management, a formal risk assessment, and a compliance review. That
said, several controls are built in from the start:

- **Access control**: every PHI endpoint resolves data ownership server-side
  from the JWT subject; there is no patient id parameter to tamper with.
- **Audit logging**: `app/models/audit_log.py` + `app/services/audit.py`
  record login attempts and are wired for use on any PHI read/write. The
  table is append-only from the application's perspective — ship it to a
  write-once sink (Azure Monitor) in production.
- **Least-privilege tokens**: short-lived access tokens (30 min) + separate
  refresh tokens limit the blast radius of a leaked token.
- **Account lockout**: 5 failed logins locks an account for 15 minutes.
- **Generic auth errors**: login/registration failures don't reveal which
  field was wrong, to resist account enumeration.
- **Soft deletes**: medical events and documents are soft-deleted
  (`deleted_at`), preserving continuity-of-care history and auditability
  instead of destroying records.
- **Security headers + no-store caching** on every API response
  (`app/main.py` middleware) — appropriate for responses that may contain PHI.
- **Storage isolation**: uploaded files are keyed by
  `{patient_id}/{uuid}_{filename}`, so a container/bucket listing never
  mixes PHI across patients, and blobs are never public.

For a production deployment, also plan for: encryption at rest (Azure Blob
and Azure Database for PostgreSQL both support this natively), a WAF in
front of the API, secrets in Azure Key Vault rather than `.env` files, MFA
enforcement (the `User.mfa_enabled` field is scaffolded but not yet wired to
an OTP flow), and a data retention / right-to-deletion policy.

---

## Running tests

```bash
cd backend
pytest
```

(Test scaffolding is set up under `backend/tests/` — add cases as you build
out further business logic.)
