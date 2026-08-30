# Neura AI — Deployment Guide

## Live hosting (free tier)

### Backend — Render
1. Push repo to GitHub
2. [render.com](https://render.com) → **New Blueprint** → connect repo
3. Set env vars: `GOOGLE_API_KEY`, `FRONTEND_URL`, `EXTRA_CORS_ORIGINS`
4. Note API URL (e.g. `https://neura-ai-api.onrender.com`)

### Frontend — Vercel
1. [vercel.com](https://vercel.com) → import repo, root dir `frontend`
2. Set `VITE_API_URL` to Render API URL
3. Deploy and copy Vercel URL back into Render CORS settings

## Demo accounts (seeded on first boot)
| Username | Password | Role |
|----------|----------|------|
| alice.chen | demo12345 | finance |
| admin | admin12345 | admin |
