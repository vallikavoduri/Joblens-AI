# JobLens — AI-powered Job Application Tracker

> A unified job-application tracker that auto-ingests applications from Gmail, LinkedIn, Naukri, and Telegram channels, classifies recruiter emails with ML, scores resume↔JD fit using embeddings, and visualises consistency analytics across your job-search journey.

**Status:** in active development (June 16–29, 2026)
**Author:** Vallika Voduri
**Background:** B.Tech — Data Science / Big Data Analytics

---

## Why this exists

Every existing tracker (Huntr, Teal, Simplify, Applyra, G-Track, Resumly) focuses on US-centric Gmail-only ingestion. They miss two huge sources for Indian and remote-first job seekers:

1. **Telegram job channels** — large, fast-moving, completely unstructured.
2. **Indian portals** — Naukri, Foundit, Internshala, hirist.

JobLens bridges that gap and adds a **consistency dashboard** (streaks + weekly targets) because outcomes follow effort.

---

## Features (target by June 29)

- [ ] Manual + Chrome-extension job capture (LinkedIn, Naukri, Indeed)
- [ ] Gmail OAuth + ML-based email classification (`confirmation / interview / rejection / offer / irrelevant`)
- [ ] Auto-link emails back to specific applications
- [ ] Telegram channel ingestion with NER-based job-post parsing
- [ ] Resume↔JD semantic match scoring with sentence-transformers
- [ ] Consistency analytics — daily streak, weekly goal, application funnel, response rate
- [ ] Deployed live (Render / Railway free tier)

---

## Tech stack

| Layer | Choice | Why |
|---|---|---|
| Backend | FastAPI + SQLAlchemy + SQLite (→ Postgres) | Python = stays in ML ecosystem |
| Frontend | React + Vite + Tailwind + Recharts | Modern, fast, easy charts |
| ML — text classification | Hugging Face Transformers (DistilBERT, zero-shot) | Strong baselines, no GPU needed |
| ML — semantic search | sentence-transformers + FAISS | Industry standard for embeddings |
| Email | Gmail API (OAuth2 read-only) | Secure, official |
| Telegram | Telethon | Read-only ingestion of public channels |
| Deploy | Docker + Render free tier | Free, simple |
| MLOps (light) | MLflow for experiment tracking | Resume signal |

---

## Repo layout

```
job-tracker/
├── backend/            # FastAPI app, DB models, API routes
├── frontend/           # React + Vite app, dashboard pages
├── ml/                 # Notebooks + scripts: classifier, embeddings
├── ingestion/          # Gmail + Telegram + scrapers
├── docs/               # Plan, learning roadmap, architecture
├── docker/             # Dockerfiles, compose
├── .github/workflows/  # CI
└── README.md
```

---

## See also

- [`docs/HANDOFF_NEXT_STEPS.md`](docs/HANDOFF_NEXT_STEPS.md) — **start here if resuming on a new machine** (setup + current state + next phases)
- [`docs/PROJECT_PLAN.md`](docs/PROJECT_PLAN.md) — phase-by-phase build plan
- [`docs/LEARNING_ROADMAP.md`](docs/LEARNING_ROADMAP.md) — AI/ML free-resource learning path
- [`docs/GIT_GUIDE.md`](docs/GIT_GUIDE.md) — practical git workflow
- [`docs/NOTES.md`](docs/NOTES.md) — design decisions + interview talking points
