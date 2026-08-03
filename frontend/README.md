# FinSolve AI — Enterprise RBAC RAG Assistant

Premium enterprise-grade AI assistant web application UI for **FinSolve Technologies**. A role-based access control (RBAC) RAG chatbot with admin analytics, built for FinTech compliance workflows.

## Tech Stack

- **React 19** + TypeScript
- **Vite 6** — build tooling
- **Tailwind CSS v4** — styling with design tokens
- **Framer Motion** — animations and micro-interactions
- **React Router v7** — client-side routing
- **Recharts** — admin analytics charts
- **React Markdown** — rich AI response rendering

## Quick Start

```bash
cd finsolve-ai-ui
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173)

### Demo Login

1. Enter any username (e.g. `alice.chen`)
2. Select a department role
3. Click **Continue to Dashboard**

| Role | Destination |
|------|-------------|
| Admin | Analytics Dashboard (`/admin`) |
| All others | Chat Dashboard (`/chat`) |

## Pages

| Page | Route | Description |
|------|-------|-------------|
| Login | `/login` | Glassmorphism card, role selection, RBAC notice |
| Chat Dashboard | `/chat` | Sidebar, AI chat, source panel |
| Admin Analytics | `/admin` | Metrics, charts, security alerts |

## Features

- Dark theme default with light mode toggle
- Collapsible sidebar with conversation history
- Streaming AI response simulation
- Source document citations with confidence scores
- Role badges (Finance, HR, Marketing, Engineering, Executive, Employee, Admin)
- Admin dashboard with bar/pie charts and security alerts
- Responsive layout (desktop, tablet, mobile)
- Framer Motion page transitions and message animations

## Architecture

See [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) for:

- UI architecture plan
- Component hierarchy
- Folder structure
- Page wireframes
- Design system specification
- Tailwind design tokens
- Implementation roadmap

## Project Structure

```
src/
├── app/           # Root app + routing
├── components/    # Shared UI primitives + layout
├── context/       # Auth, Chat, Theme providers
├── data/          # Mock data (dev)
├── features/      # auth/, chat/, admin/
├── hooks/         # Custom hooks
├── lib/           # Utilities
└── types/         # TypeScript definitions
```

## Backend Integration

This UI is designed to connect to the Python RAG backend in `../enterprise-rag-assistant/`. Phase 3 of the roadmap covers API integration with SSE streaming and JWT auth.

## Scripts

```bash
npm run dev      # Development server
npm run build    # Production build
npm run preview  # Preview production build
```
