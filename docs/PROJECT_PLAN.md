# Project Plan — JobLens

**Window:** June 16 → June 29, 2026 (14 days)
**Working assumption:** ~3–5 productive hours/day on average. Less on weekdays during internship, more on weekends.
**North star:** by June 29, you have a deployed, demo-ready project on your personal GitHub with a 60-second demo video and a polished README.

---

## Scope philosophy

> Done > Perfect. Anything not built by June 29 goes into a "Roadmap / Future Work" section in the README. Recruiters love seeing a roadmap — it shows product thinking.

**MVP (must ship):** Phases 0–3
**Stretch (only if time permits):** Phase 4
**Polish (final 2 days are reserved for this — DO NOT skip):** Phase 5

---

## Phase 0 — Setup (Day 1: June 16)

| # | Task | Done? |
|---|---|---|
| 0.1 | Create personal project folder outside OneDrive | ✅ |
| 0.2 | Install / verify Python, Node, Git | ✅ |
| 0.3 | Initialize git repo with **per-repo personal email** (not Nokia email) | ⬜ |
| 0.4 | Create personal GitHub repo + push first commit | ⬜ |
| 0.5 | Scaffold folder structure (backend/, frontend/, ml/, ingestion/, docs/) | ⬜ |
| 0.6 | Create Python venv + install base packages (fastapi, uvicorn, sqlalchemy, pydantic) | ⬜ |
| 0.7 | Bootstrap Vite + React + Tailwind in `frontend/` | ⬜ |
| 0.8 | "Hello world" — backend serves `/health`, frontend shows a styled landing page | ⬜ |

**Definition of done:** `git push` works, both servers start cleanly, you can hit `localhost:8000/health` and see the React landing page at `localhost:5173`.

---

## Phase 1 — Core CRUD + Dashboard (Days 2–5: June 17–20)

This phase has **no ML**. Get the bones working first.

### Day 2 (Jun 17) — Backend models + API

- SQLAlchemy models: `Application`, `Email`, `StatusHistory`
- Pydantic schemas
- CRUD endpoints: `POST /applications`, `GET /applications`, `PATCH /applications/{id}`, `DELETE`
- Seed script with 20 fake applications
- One pytest test per endpoint

### Day 3 (Jun 18) — Frontend core pages

- Layout + sidebar navigation (Dashboard / Applications / Add / Settings)
- "Add Application" form (company, role, source, applied_date, status, link, notes)
- "Applications" list page — table view with sort/filter

### Day 4 (Jun 19) — Dashboard analytics

This is the **resume-differentiating** part. Show off your data-analytics chops:

- KPI cards: Total Applied, Active (Applied + Interview), Offers, Response Rate
- **Daily applications chart** (last 30 days, line/bar) — Recharts
- **Status funnel** (Applied → Interview → Offer / Rejected) — Recharts
- **Streak counter** — "🔥 5 days in a row of applying"
- **Source breakdown** (LinkedIn vs Naukri vs Telegram vs Referral) — donut chart

### Day 5 (Jun 20) — Polish + filters

- Search by company/role
- Filter by status, source, date range
- Sort by applied_date, status
- Mobile-responsive (Tailwind breakpoints)
- Dark mode toggle (small detail, big perceived polish)

**Definition of done:** You can manually add 20 applications, the dashboard updates live, and it looks good on phone + desktop.

---

## Phase 2 — Email parsing with ML (Days 6–8: June 21–23)

**This is where the ML starts.** Each task includes the concept you'll learn alongside.

### Day 6 (Jun 21) — Gmail OAuth + email fetch

- Set up Google Cloud project, enable Gmail API
- OAuth2 flow (read-only scope: `gmail.readonly`)
- Backend endpoint: `POST /gmail/sync` — fetches last 90 days of emails, stores raw subject + sender + snippet in DB
- **Concept learned:** OAuth2 flows, scope security, never storing user passwords

### Day 7 (Jun 22) — Email classifier (the ML part)

- Notebook in `ml/01_email_classifier.ipynb`
- Build a small labelled dataset (~100 emails labelled by you = enough for fine-tuning a small model OR for prompt engineering)
- **Two approaches, pick whichever clicks faster:**
  - **A. Zero-shot (fastest, no training):** `transformers.pipeline("zero-shot-classification")` with `facebook/bart-large-mnli`
  - **B. Fine-tune DistilBERT:** small dataset, train for 3 epochs on CPU
- Evaluate on a held-out 20% — confusion matrix, precision/recall per class
- Save model to `ml/models/email_classifier/`
- **Concepts learned:** train/test split, supervised classification, precision/recall/F1, confusion matrix, transformers (high level), zero-shot vs fine-tuning trade-off

### Day 8 (Jun 23) — Wire it up + entity matching

- Backend service: classify each new Gmail email, extract company name (regex on signature + simple NER), match to an existing application
- Auto-update application status when email is classified as `interview` / `rejection` / `offer`
- UI: "Inbox" page showing classified emails with confidence scores
- **Concept learned:** entity linking, threshold tuning (precision-vs-recall trade-off in production)

**Definition of done:** Sync your real Gmail, see emails classified, watch one application's status flip from "Applied" to "Interview" automatically.

---

## Phase 3 — Resume ↔ JD semantic matching (Days 9–10: June 24–25)

### Day 9 (Jun 24) — Embeddings core

- Notebook `ml/02_resume_jd_match.ipynb`
- Use `sentence-transformers` (`all-MiniLM-L6-v2` — small, fast, free, no GPU)
- Encode resume → vector. Encode each JD → vector. Cosine similarity = match score (0–100)
- Sub-skill scoring: split resume into bullet points → encode each → match each JD-required-skill against best-matching bullet
- **Concepts learned:** word vs sentence embeddings, cosine similarity, semantic vs lexical search, why embeddings beat keywords

### Day 10 (Jun 25) — UI integration

- Upload resume (PDF — use `pdfplumber` or `pypdf` to extract text)
- For each application, compute and store match score
- Show on application card: "Match: 78% • Missing: Kubernetes, Airflow"
- Sort applications by match score (helps prioritise follow-ups)

**Definition of done:** Upload your real resume, see scores against the JDs you've added.

---

## Phase 4 — Telegram ingestion (Days 11–12: June 26–27) [STRETCH]

> Skip without guilt if Phases 0–3 ran long. The MVP is already strong.

### Day 11 — Telethon connector

- Telegram API + Telethon
- User configures 3–5 channels (e.g. `@bigDataJobs`, `@RemoteJobsIndia`)
- Backend cron: fetch last 100 messages from each channel daily
- Store raw messages

### Day 12 — Job-post extraction

- Notebook `ml/03_telegram_ner.ipynb`
- For each message, classify "is this a job post?" (zero-shot again, or rules)
- If yes, extract `{role, company, location, salary, apply_link}` using a mix of regex + spaCy NER
- Surface as "Discovered Jobs" feed in UI — user can promote one to an "Applied" status with one click

---

## Phase 5 — Ship + polish (Days 13–14: June 28–29) [DO NOT SKIP]

This phase is what turns a project into a *resume* project.

### Day 13 (Jun 28) — Deploy

- Dockerize backend (single Dockerfile)
- Build frontend → static files served by FastAPI (or separate Vercel deploy)
- Deploy to **Render free tier** (or Railway / Fly.io)
- Set up `.env.example`, document env vars
- Smoke test the live URL

### Day 14 (Jun 29) — README + demo + LinkedIn

- **README:**
  - Hero GIF (use ScreenToGif — free, Windows)
  - Problem → solution → screenshots
  - Architecture diagram (use [Excalidraw](https://excalidraw.com) — free)
  - "Tech I learned building this" section (huge resume signal)
  - Roadmap section (anything skipped from Phase 4 goes here)
- **Demo video:** 60 seconds, OBS or Loom (free), narrated
- **LinkedIn post:** announce the project, tag people who'd be interested, link the GitHub
- **Pin the repo** on your GitHub profile

---

## Daily ritual (every day)

| When | What | Why |
|---|---|---|
| Start of day (10 min) | Read today's plan, write 3 specific tasks in a `daily.md` | Forces focus |
| Every 30 min of coding | `git add -A && git commit -m "..."` | You'll never lose work + your contribution graph fills up |
| End of day (10 min) | What worked / what blocked / what tomorrow | Builds an interview-ready story |
| End of day | Push to GitHub | Backup + green squares |

---

## Risk register

| Risk | Likelihood | Mitigation |
|---|---|---|
| Python 3.14 has package incompatibilities | Medium | Switch to Python 3.12 venv (`py -3.12 -m venv .venv`) — install Python 3.12 from python.org if needed |
| Gmail API setup takes a full day | Medium | Have a `MOCK_EMAILS` mode that reads from a JSON file — develop everything else without OAuth |
| ML classifier accuracy is bad | Low | Zero-shot fallback always works; rules fallback always works. Pipeline > accuracy on Day 1 |
| Deployment on Render fails | Medium | Have a `docker-compose up` local-demo path as backup. Recruiters can clone+run |
| Internship work spikes, no time | High | Phase 4 is fully optional. Phase 5 is non-negotiable. Cut Phase 4 first |

---

## What "good enough" looks like by June 29

A recruiter clicks the GitHub link from your resume. Within 30 seconds they should see:

1. A **clear problem statement** in the README
2. A **GIF or screenshot** that shows what it does
3. A **live URL** they can click
4. A **tech stack section** with badges
5. A **demo video** (linked, embedded thumbnail)
6. A **roadmap** showing it's an active project, not abandoned

If those six things exist, you have a project that gets you interviews.
