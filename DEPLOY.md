# Neura AI — Deployment Guide

## Quick links

| Service | URL |
|---------|-----|
| Frontend (GitHub Pages) | https://carloskipkoech.github.io/neura-ai/ |
| Backend (Render) | Set up once — see below |

## One-click backend (Render, free tier)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/CarlosKipkoech/neura-ai)

On the Render Blueprint screen, connect your GitHub repo and apply the spec. The free tier does **not** support persistent disks — the app uses `/tmp` for SQLite and Qdrant. Demo users and the knowledge base are re-seeded on each cold start; signups are lost after redeploys or long idle spin-downs.

After deploy, set these env vars in the Render dashboard:

| Variable | Value |
|----------|-------|
| `GOOGLE_API_KEY` | Your Gemini API key |
| `FRONTEND_URL` | `https://carloskipkoech.github.io/neura-ai` |
| `EXTRA_CORS_ORIGINS` | Same as `FRONTEND_URL` |

Copy the Render service URL (e.g. `https://neura-ai-api.onrender.com`).

## Frontend (GitHub Pages — automatic)

Pushes to `main` deploy via GitHub Actions. Set this repository secret:

| Secret | Value |
|--------|-------|
| `VITE_API_URL` | Your Render API URL (no trailing slash) |

```bash
gh secret set VITE_API_URL --body "https://neura-ai-api.onrender.com"
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
