# Handoff & Next Steps — JobLens

> **For Vallika (continuing on a new machine) AND for the next AI agent session.**
> This file captures *exactly* where the project is, how to set it up fresh, and what to build next.
> Last updated: **2026-06-26**, end of Phase 1.1.

---

## 🟢 TL;DR — start here

1. Clone the repo on the new machine.
2. Run the **"Fresh-machine setup"** section below (5 commands).
3. Open this file + `docs/PROJECT_PLAN.md` side-by-side.
4. Resume from **Phase 1.2** (Frontend pages — sidebar, Applications list, Add form).

---

## What is done ✅

### Phase 0 — Setup (complete)

- ✅ Personal project folder outside Nokia OneDrive (`C:\Users\vallika\projects\job-tracker`)
- ✅ Python 3.12.10 + Node 22.22 + Git 2.51 verified
- ✅ Per-repo git config (`vallikavoduri@gmail.com`) — global Nokia config untouched
- ✅ GitHub repo: **<https://github.com/vallikavoduri/Joblens-AI>**
- ✅ Folder scaffold: `backend/`, `frontend/`, `ml/`, `ingestion/`, `docs/`
- ✅ Python venv with FastAPI + SQLAlchemy + Pydantic + pytest installed
- ✅ Vite + React 19 + Tailwind v4 frontend
- ✅ JobLens landing page renders with **live `/health` poll → green "Backend online" pill**
- ✅ Vite proxy at `/api/*` → forwards to `http://127.0.0.1:8000`

### Phase 1.1 — Backend models + API (complete)

- ✅ SQLAlchemy 2.0 ORM models: `Application`, `Email`, `StatusHistory`
- ✅ Enums: `Source`, `Status`, `EmailClassification` (in `app/schemas/common.py`)
- ✅ Pydantic schemas: `ApplicationCreate`, `ApplicationUpdate`, `ApplicationOut`, `ApplicationListOut`, `StatusHistoryOut`
- ✅ CRUD endpoints under `/applications`:
  - `POST /applications`
  - `GET /applications` (filters: `q`, `status`, `source`, `applied_from`, `applied_to`, `limit`, `offset`)
  - `GET /applications/{id}`
  - `PATCH /applications/{id}` (auto-logs StatusHistory on status change)
  - `DELETE /applications/{id}` (cascades emails + history)
  - `GET /applications/{id}/history`
- ✅ Dashboard endpoint `GET /dashboard/stats?days=30` (KPIs, daily counts, by-status, by-source, current + longest streak)
- ✅ Seed script: `python -m scripts.seed` — 20 realistic Indian-context fake applications
- ✅ 7 passing pytest tests (`backend/tests/test_applications.py`)
- ✅ pytest config + isolated in-memory SQLite test DB

---

## Fresh-machine setup (do this first on any new computer)

Assumes a Windows machine with PowerShell. Adjust paths for macOS / Linux.

### 1. Install prerequisites

```powershell
# Python 3.12 (NOT 3.13 or 3.14 — ML libs trail behind. 3.12 is the sweet spot.)
winget install Python.Python.3.12

# Node.js 22+
winget install OpenJS.NodeJS.LTS

# Git
winget install Git.Git
```

Close + reopen PowerShell so PATH refreshes.

### 2. Clone the repo

```powershell
cd C:\Users\<your-username>\projects   # or any folder you like
git clone https://github.com/vallikavoduri/Joblens-AI.git
cd Joblens-AI
```

### 3. Per-repo git identity (one-time)

```powershell
git config user.name "Vallika Voduri"
git config user.email "vallikavoduri@gmail.com"
```

If on a personal laptop with only this email globally, this is optional — but doing it per-repo is safe + future-proof.

### 4. Backend setup

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m scripts.seed          # seeds 20 applications
python -m pytest -v             # should show 7 passed
uvicorn app.main:app --reload   # leave this running
```

If activation fails with *"running scripts is disabled"*: run once
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### 5. Frontend setup

In a **new** PowerShell window:

```powershell
cd C:\Users\<you>\projects\Joblens-AI\frontend
npm install
npm run dev
```

Open <http://localhost:5173> — you should see the JobLens landing page with a green **"Backend online"** pill.

If the pill is red, the backend isn't running — check terminal 1.

---

## Daily workflow (you already know this, here as a refresher)

| When | Command(s) | Why |
|---|---|---|
| Start of session | `git pull` | Sync any commits you made elsewhere |
| Every meaningful chunk | `git add . && git commit -m "feat: ..."` | Never lose work + green squares |
| End of session | `git push` | Backup + recruiters see your activity |

Commit message format (Conventional Commits):

- `feat:` new feature
- `fix:` bug fix
- `refactor:` no behaviour change
- `docs:` documentation only
- `test:` adding tests
- `chore:` setup, deps, config

---

## What's NEXT — phase-by-phase

Pick up from **Phase 1.2**. The detailed plan is in `docs/PROJECT_PLAN.md`. Below is a quick checklist version.

### Phase 1.2 — Frontend pages (next up)

Goal: a working frontend where you can manually add applications and see them in a table.

**Install:**
```powershell
cd frontend
npm install react-router-dom
```

**Files to create / edit:**

| File | Purpose |
|---|---|
| `frontend/src/api/client.js` | Single `fetch` wrapper hitting `/api/*`, JSON handling, error normalising |
| `frontend/src/components/Sidebar.jsx` | Left nav with links: Dashboard, Applications, Add, Settings |
| `frontend/src/components/Layout.jsx` | Sidebar + main content area shell |
| `frontend/src/components/StatusBadge.jsx` | Coloured pill (applied/interview/offer/rejected/ghosted) |
| `frontend/src/components/SourceBadge.jsx` | Small chip showing LinkedIn / Naukri / Telegram / etc |
| `frontend/src/pages/Dashboard.jsx` | KPI cards (charts come in Phase 1.3) |
| `frontend/src/pages/Applications.jsx` | Table with all applications + basic filters |
| `frontend/src/pages/AddApplication.jsx` | Form: company, role, source, status, applied_date, link, location, salary, notes |
| `frontend/src/pages/ApplicationDetail.jsx` | Single application view + edit + history timeline |
| `frontend/src/App.jsx` | Replace landing with `<BrowserRouter>` + routes |
| `frontend/src/main.jsx` | Already fine |

**Acceptance criteria for Phase 1.2:**

- Sidebar nav works (4 routes resolve)
- You can add an application via the form and see it appear in the Applications table
- You can click an application → see its detail page → edit status → see the history grow
- All 20 seeded applications render with correct status badges

### Phase 1.3 — Dashboard analytics (charts)

```powershell
cd frontend
npm install recharts date-fns
```

Build on the `/dashboard/stats` endpoint that already exists.

**Files:**
- `frontend/src/components/KpiCard.jsx` — Total / Active / Offers / Response Rate / Streak
- `frontend/src/components/DailyApplicationsChart.jsx` — bar chart of last 30 days
- `frontend/src/components/StatusFunnelChart.jsx` — applied → screening → interview → offer / rejected
- `frontend/src/components/SourceDonut.jsx` — donut chart by source
- `frontend/src/components/StreakRing.jsx` — current streak with a ring graphic

The backend already returns everything in one call (`GET /dashboard/stats`). Just feed it into Recharts.

### Phase 1.4 — Polish + filters

- Search box on Applications page (calls `/applications?q=...`)
- Status + source + date range filters in a sticky toolbar
- Sort by applied_date, company, status
- **Dark mode toggle** — Tailwind v4 dark variant + a `<ThemeToggle>` button storing state in `localStorage`
- Mobile responsive (test sidebar collapse below 768px)

### Phase 2 — Email parsing with ML

**Files to create:**
- `ingestion/gmail/auth.py` — OAuth2 flow
- `ingestion/gmail/fetch.py` — pull last 90 days emails
- `ml/notebooks/01_email_classifier.ipynb` — train DistilBERT or zero-shot BART
- `backend/app/services/email_classifier.py` — load saved model, classify
- `backend/app/routes/gmail.py` — `POST /gmail/sync`, `GET /emails`
- `backend/app/services/entity_matching.py` — link classified emails to applications

**Setup:**
1. Google Cloud Console → new project → enable Gmail API → OAuth credentials (Desktop type) → download `credentials.json` to `backend/secrets/` (gitignored)
2. Add to `requirements.txt`: `google-auth`, `google-auth-oauthlib`, `google-api-python-client`, `transformers`, `torch` (CPU build), `datasets`, `scikit-learn`, `mlflow`

**Concepts to learn alongside** — see `docs/LEARNING_ROADMAP.md` § Phase 2.

### Phase 3 — Resume ↔ JD semantic matching

**Files:**
- `ml/notebooks/02_resume_jd_match.ipynb` — explore sentence-transformers, cosine similarity
- `backend/app/services/resume_matcher.py` — load `all-MiniLM-L6-v2`, encode resume + JD, compute score
- `backend/app/routes/resume.py` — `POST /resume/upload`, `GET /applications/{id}/match`
- `frontend/src/pages/Resume.jsx` — upload PDF, see scores against all jobs

**Setup:**
- `pip install sentence-transformers pdfplumber pypdf`

### Phase 4.5 — Smart Apply assistant (high-differentiator)

Two sub-features (skip A, do B+C):

**B. Tailored cover letter generator**
- `backend/app/services/cover_letter_gen.py` — HF Inference API or local `flan-t5-base`
- Endpoint: `POST /applications/{id}/cover-letter`
- UI: button on each application card → editable textbox → copy to clipboard

**C. One-click apply Chrome extension** (Manifest V3) — separate folder `extension/`
- `extension/manifest.json`
- `extension/content.js` — detect form, fill from profile, show "Apply with JobLens" button
- `extension/popup.html` + `popup.js` — profile editor + login

### Phase 4 — Telegram ingestion (stretch)

- `ingestion/telegram/client.py` — Telethon connection
- `ml/notebooks/03_telegram_ner.ipynb` — spaCy NER for job-post extraction
- `backend/app/routes/telegram.py` — `POST /telegram/sync`, `GET /discovered-jobs`

### Phase 5 — Ship + polish [DO NOT SKIP]

- `docker/Dockerfile` for backend
- Optional `docker/docker-compose.yml` for local one-command boot
- Deploy to Render free tier (Docker template)
- `.env.example` already exists — make sure it's complete
- README: hero GIF (ScreenToGif), screenshots, architecture diagram (Excalidraw), demo-video link
- LinkedIn post + pin repo

---

## Critical gotchas (read these before debugging)

1. **Python 3.12 required.** Phase 2's `transformers` and Phase 3's `torch` do NOT have stable wheels for Python 3.13/3.14 yet (as of June 2026). Stick with 3.12.
2. **Never commit `.env`.** Already gitignored. If you accidentally do, **rotate the secrets immediately** and `git rm --cached .env`.
3. **`.gitignore` had a bug** that ignored `backend/app/models/` because of the loose `models/` pattern. Fixed on 2026-06-26 — now uses `ml/models/`. If you see ORM model files going missing from git, check this.
4. **CORS** — backend allows `http://localhost:5173` only. If you change the Vite port, update `FRONTEND_ORIGIN` in `backend/.env`.
5. **Vite proxy** — frontend calls `/api/*` which Vite forwards to `http://127.0.0.1:8000`. Use `127.0.0.1` not `localhost` (IPv6 vs IPv4 nonsense on Windows).
6. **Two terminals always** — one for `uvicorn`, one for `npm run dev`. Both run forever (Ctrl+C to stop).
7. **Conventional Commits** — keep using `feat:` / `fix:` / `docs:` prefixes. Recruiters notice this.
8. **Phase 5 (deploy + README + demo) is non-negotiable.** A great unfinished project < a decent finished one. Cut Phase 4 (Telegram) before cutting Phase 5.

---

## How to talk to the next AI agent (priming prompt)

When you open a fresh chat in Cursor on the new machine, paste this as your first message:

```
You are continuing the JobLens project. Before doing anything else:

1. Read these files in order:
   - docs/HANDOFF_NEXT_STEPS.md  (this file — the current source of truth)
   - docs/PROJECT_PLAN.md
   - docs/LEARNING_ROADMAP.md
   - docs/NOTES.md
   - docs/KICKOFF_CONTEXT.md
   - README.md
   - backend/app/main.py
   - backend/app/models/application.py
   - backend/app/routes/applications.py
   - frontend/src/App.jsx

2. Then summarise back to me:
   - Where the project is right now (which phases are done)
   - What Phase 1.2 needs (files to create)
   - Any gotchas I should remember from past chats

3. Wait for my go-ahead before generating code. Confirm Python 3.12 is
   available locally (`py --list`) before any pip work.

I want to continue from Phase 1.2 — frontend pages (sidebar, Applications
table, Add form, ApplicationDetail page). Build that next.
```

That gets a fresh agent fully oriented in one prompt.

---

## Project stats snapshot (2026-06-26)

- Total commits: **4** (will grow)
- Files tracked by git: ~40
- Backend endpoints live: **9**
- Tests passing: **7/7**
- Frontend pages: 1 (landing) — will grow to 4+ in Phase 1.2
- Phases done: **0, 1.1**
- Phases remaining: 1.2, 1.3, 1.4, 2, 3, 4.5, 4, 5
- Repo: <https://github.com/vallikavoduri/Joblens-AI>

---

## When in doubt

> The point of this project is to **stand out on your resume**, not to be perfect.
> Done > Perfect. Every committed phase is a recruiter-visible artifact.
> Keep shipping.
