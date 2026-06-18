# Kickoff Context — Read this first if you're a new agent session

> **For the next AI agent that opens this project:** This file exists so you can pick up exactly where the previous session left off. Read this in full, then read `PROJECT_PLAN.md`, `LEARNING_ROADMAP.md`, `GIT_GUIDE.md`, and `NOTES.md`. After that, ask the user "I'm caught up — what step do you want to do next?"

---

## Who is the user?

- **Name:** Vallika Voduri
- **Personal email:** vallikavoduri@gmail.com
- **Current situation:** B.Tech in Data Science / Big Data Analytics. Currently interning at Nokia. **Internship ends June 30, 2026.**
- **ML/AI background:** Self-described as none yet — wants to learn fundamentals while building.
- **Goal:** A standout resume project + a structured learning path for future interviews.
- **Personality signals from kickoff chat:** thoughtful, asks the right cautious questions (e.g., "won't this affect my Nokia OneDrive?", "won't I lose my chats?"), wants reassurance when uncertain. Treat her with patience, walk through unfamiliar things step-by-step.

## Why this project (JobLens)

She compared two ideas:

1. **Job application tracker with AI/ML** — chosen
2. Facial recognition project — rejected (over-saturated in fresher portfolios)

The deciding factors:
- Aligns with her data-science B.Tech.
- She lives the problem (applies via LinkedIn, Naukri, Indeed, Telegram).
- Real market gap: existing tools (Huntr, Teal, Simplify, Applyra, G-Track, Resumly, Jobless) all skip Telegram channels and Indian job portals.
- Lets her layer ML in *gradually* as she learns.

## Hard constraints

| Constraint | Detail |
|---|---|
| **Timeline** | June 16 → June 29, 2026 (14 days). No slipping past June 29. |
| **Internship overlap** | She's still working at Nokia until June 30 — productive hours/day are limited. |
| **Location of code** | `C:\Users\vallika\projects\job-tracker` — **outside** Nokia OneDrive. Critical: never write personal-project files into `C:\Users\vallika\OneDrive - Nokia\...`. That's company tenant. |
| **Free only** | All learning resources, all deploy targets, all ML models must be free / free-tier. No OpenAI API. |
| **Per-repo git identity** | This repo uses `vallikavoduri@gmail.com` (per-repo). Global config remains `voduri.vallika@nokia.com`. Don't ever change global. |

## Tech decisions already made (don't relitigate)

| Layer | Choice |
|---|---|
| Backend | FastAPI + SQLAlchemy + SQLite (→ Postgres later) |
| Frontend | React + Vite + Tailwind + Recharts |
| ML — text classification | Hugging Face Transformers (DistilBERT or BART zero-shot) |
| ML — semantic search | sentence-transformers `all-MiniLM-L6-v2` + FAISS |
| Email | Gmail API, OAuth2 read-only |
| Telegram | Telethon (stretch goal only) |
| Deploy | Render free tier, Docker |
| MLOps signal | MLflow for experiment tracking |

## Where we are right now (as of end of kickoff session)

**Phase 0 progress (Day 1, June 16):**

- [x] 0.1 Personal project folder created at `C:\Users\vallika\projects\job-tracker` (outside OneDrive)
- [x] 0.2 Tools verified: Python 3.14, Node v22.22, npm 11.6, Git 2.51
- [ ] 0.3 Initialize git repo with per-repo personal email — **next step (was about to run when session ended)**
- [ ] 0.4 Create personal GitHub repo + push first commit — needs her GitHub username + chosen repo name
- [ ] 0.5 Scaffold folder structure (backend/, frontend/, ml/, ingestion/)
- [ ] 0.6 Python venv + base packages
- [ ] 0.7 Vite + React + Tailwind bootstrap
- [ ] 0.8 Hello-world both servers running

**Files already created** (all under `C:\Users\vallika\projects\job-tracker\`):
- `.gitignore` — Python + Node + secrets-safe
- `README.md` — project overview
- `docs/PROJECT_PLAN.md` — 14-day day-by-day build plan
- `docs/LEARNING_ROADMAP.md` — free-only AI/ML learning path (just-in-time + long-term + interview prep)
- `docs/GIT_GUIDE.md` — daily git workflow + GitHub setup walkthrough
- `docs/NOTES.md` — design decisions + interview ammo
- `docs/KICKOFF_CONTEXT.md` — this file
- `docs/CHAT_HISTORY_2026-06-16.md` — actual exchanges from kickoff

## What to do as the next agent

1. Greet her warmly — she just switched workspaces and may still be a little anxious about losing context.
2. Confirm you've read `docs/` and understand where we are.
3. Ask: *"Ready to do step 0.3 — git init with personal email and first commit? I just need your personal GitHub username and the repo name you want."*
4. Once she shares those, run the commands in `GIT_GUIDE.md` § "GitHub setup walkthrough", verify, push.
5. Move to step 0.5 (folder scaffold) → 0.6 (Python venv) → 0.7 (Vite/React) → 0.8 (hello world).
6. Aim to wrap Phase 0 today so Day 2 (June 17) starts with backend models.

## Behaviour rules for the agent

1. **Never write to `C:\Users\vallika\OneDrive - Nokia\...`** — that's her work tenant.
2. **Never modify global git config.** Per-repo only.
3. **Bias toward Done > Perfect.** Phase 5 (deploy + README + demo) is non-negotiable on June 28-29. Cut Phase 4 (Telegram) before cutting Phase 5.
4. **Teach as you go.** When introducing an ML concept, give a 30-second intuition before code.
5. **Keep PRs/commits small and frequent.** Conventional Commits style (`feat:`, `fix:`, `docs:`).
6. **Don't suggest paid tools or APIs.** Free-only.
7. **If she asks "won't this affect X?"** — pause, verify, give concrete proof. She values reassurance.
8. **Update `PROJECT_PLAN.md` checkboxes** as phases complete, so she has a visible progress signal.

## How to talk about this project to recruiters (her future use)

> "I built JobLens because every existing job tracker assumes you're applying through US Gmail. As an Indian job-seeker, I was applying through Naukri, LinkedIn, Indeed, *and* Telegram channels. None of the existing tools handled all four. I built JobLens to unify them, classify recruiter emails with a fine-tuned DistilBERT model, score resume-vs-JD fit using sentence-transformers embeddings, and visualise my own consistency over time. It's deployed at [URL], and I've used it myself to apply to 60+ roles."

That's her interview pitch. Keep reinforcing it.
