# Neura AI — Deployment Guide

## Quick links

| Service | URL |
|---------|-----|
| Frontend (GitHub Pages) | https://carloskipkoech.github.io/neura-ai/ |
| Backend (Fly) | https://neura-ai-api.fly.dev |

## Backend (Fly)

The API is deployed from `backend/` with `fly.toml`.

```bash
cd backend
fly deploy --remote-only --app neura-ai-api
```

Secrets already set on the app: `GOOGLE_API_KEY`, `JWT_SECRET`. SQLite and Qdrant live in `/tmp` and are rebuilt on each machine start (about 1–2 minutes for embeddings).

## Frontend (GitHub Pages — automatic)

Pushes to `main` deploy via GitHub Actions. The Pages secret is:

| Secret | Value |
|--------|-------|
| `VITE_API_URL` | `https://neura-ai-api.fly.dev` |

```bash
gh secret set VITE_API_URL --body "https://neura-ai-api.fly.dev"
gh workflow run deploy-frontend.yml
```

## Local development

```bash
# Backend
cd backend && source .venv/bin/activate
uvicorn app:app --reload --port 8000

# Frontend
cd frontend && npm run dev   # http://localhost:5174
```

Create `frontend/.env.local`:
```
VITE_API_URL=http://127.0.0.1:8000
```

## Demo accounts (seeded on first boot)

| Username | Password | Role |
|----------|----------|------|
| alice.chen | demo12345 | finance |
| bob.martinez | demo12345 | hr |
| carol.williams | demo12345 | marketing |
| david.kim | demo12345 | engineering |
| elena.rodriguez | demo12345 | executive |
| frank.johnson | demo12345 | employee |
| admin | admin12345 | admin |

## Auth API

- `POST /auth/signup` — `username`, `name`, `password`, `role` (all roles except `admin`)
- `POST /auth/login` — `username`, `password` (role loaded from account)
- `GET /auth/me` — Bearer JWT
- `POST /chat` — Bearer JWT + `{ "question": "..." }`
