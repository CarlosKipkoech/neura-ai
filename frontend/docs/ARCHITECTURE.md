# FinSolve AI — UI Architecture

> Enterprise RBAC RAG Chatbot for FinSolve Technologies

---

## 1. UI Architecture Plan

### Overview

FinSolve AI is a feature-based React SPA built with Vite, Tailwind CSS v4, and Framer Motion. The application follows a **layered architecture** with clear separation between presentation, state management, and data layers.

```
┌─────────────────────────────────────────────────────────┐
│                    Presentation Layer                    │
│  Pages → Feature Components → UI Primitives             │
├─────────────────────────────────────────────────────────┤
│                    State Layer                           │
│  AuthContext │ ChatContext │ ThemeContext                │
├─────────────────────────────────────────────────────────┤
│                    Data Layer                            │
│  Mock Data (dev) → API Client (prod) → Backend RAG      │
└─────────────────────────────────────────────────────────┘
```

### Core Principles

| Principle | Implementation |
|-----------|---------------|
| Feature isolation | Each domain (auth, chat, admin) owns its components |
| Composition over inheritance | Small UI primitives composed into features |
| Context for global state | Auth, theme, and chat state via React Context |
| CSS variables for theming | Dark/light mode via CSS custom properties |
| Progressive enhancement | Mock data now, API integration later |

### Routing Strategy

| Route | Page | Access |
|-------|------|--------|
| `/login` | Login Page | Public |
| `/chat` | Chat Dashboard | Authenticated |
| `/admin` | Analytics Dashboard | Admin role only |

---

## 2. Component Hierarchy

```
App
├── ThemeProvider
├── AuthProvider
└── BrowserRouter
    └── AppRoutes
        ├── LoginPage
        │   ├── PageTransition
        │   ├── Input
        │   ├── Select
        │   └── Button
        │
        ├── ChatDashboard [ProtectedRoute]
        │   └── ChatProvider
        │       ├── Sidebar
        │       │   ├── Avatar
        │       │   ├── Badge
        │       │   ├── Button
        │       │   └── ThemeToggle
        │       ├── ChatInterface
        │       │   ├── MessageBubble
        │       │   │   └── ReactMarkdown
        │       │   ├── TypingIndicator
        │       │   └── ChatInput
        │       └── SourcePanel
        │           └── SourceCard
        │
        └── AnalyticsDashboard [ProtectedRoute, adminOnly]
            ├── PageTransition
            ├── MetricCard (×4)
            ├── BarChart (Recharts)
            ├── PieChart (Recharts)
            ├── DepartmentBreakdown
            └── SecurityAlerts
```

---

## 3. Folder Structure

```
finsolve-ai-ui/
├── docs/
│   └── ARCHITECTURE.md
├── public/
│   └── favicon.svg
├── src/
│   ├── app/
│   │   └── App.tsx
│   ├── components/
│   │   ├── layout/
│   │   └── ui/
│   ├── context/
│   ├── data/
│   ├── features/
│   │   ├── admin/
│   │   ├── auth/
│   │   └── chat/
│   ├── hooks/
│   ├── lib/
│   ├── types/
│   ├── index.css
│   └── main.tsx
├── index.html
├── vite.config.ts
└── package.json
```

---

## 4. Page Wireframes

See full wireframe diagrams in the repository docs for Login, Chat Dashboard, and Admin Analytics layouts.

---

## 5. Design System Specification

### Typography

| Token | Value | Usage |
|-------|-------|-------|
| Font Sans | Inter | Body, UI elements |
| Font Mono | JetBrains Mono | Code blocks |
| Heading 1 | 2xl / bold | Page titles |
| Body | sm / regular | Messages, content |
| Caption | xs / medium | Labels, metadata |

### Color Palette

| Token | Dark | Usage |
|-------|------|-------|
| `--bg-primary` | #09090b | Page background |
| `--bg-secondary` | #0f0f12 | Sidebar, header |
| Brand 500 | #3b82f6 | Primary actions |
| Accent Cyan | #06b6d4 | Gradients |

### Effects

- Glassmorphism: `backdrop-filter: blur(20px)`
- Gradient mesh: Radial gradients on dark background
- Shadow glow: Blue glow on focused inputs

---

## 6. Tailwind Design Tokens

Defined in `src/index.css` via `@theme` and CSS custom properties for dark/light theme switching.

Utility classes: `.glass`, `.gradient-brand`, `.gradient-mesh`, `.text-gradient`, `.prose-chat`

---

## 7. Implementation Roadmap

### Phase 1 — Foundation ✅
- Vite + React + TypeScript scaffold
- Tailwind CSS v4 with design tokens
- Framer Motion animations
- Theme system (dark/light)
- UI component library

### Phase 2 — Core Features ✅
- Login page with RBAC role selection
- Chat dashboard with collapsible sidebar
- AI chat interface with streaming simulation
- Source panel with expand/collapse
- Admin analytics dashboard with charts

### Phase 3 — Backend Integration
- Connect to enterprise-rag-assistant Python API
- Real SSE streaming from RAG pipeline
- JWT/session auth with backend

### Phase 4 — Production Hardening
- Error boundaries, E2E tests, CI/CD

### Phase 5 — Enterprise Features
- SSO (Azure AD / Okta), audit logs, multi-tenant branding

---

## Running the Application

```bash
cd finsolve-ai-ui
npm install
npm run dev
```

Open http://localhost:5173 — sign in with any username and select a role.
