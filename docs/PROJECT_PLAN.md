# Project Plan — JobLens

**Window:** Started June 16, 2026 — finishing when it's *good*, not when the calendar says so.
**Working assumption:** Variable hours/day depending on internship load (ends June 30). No hard daily targets — phase-based progress instead.
**North star:** a deployed, demo-ready project on personal GitHub with a 60-second demo video and a polished README — that **stands out** in a fresher portfolio because of four differentiators (see below).

---

## What makes JobLens stand out (keep these front of mind)

1. **Telegram channel ingestion** — every existing tracker (Huntr/Teal/Simplify/Applyra) is Gmail-only. We cover Telegram + Naukri/Foundit too.
2. **Real ML metrics** — not "I used ChatGPT", but "I fine-tuned DistilBERT, achieved F1 = 0.XX on rejection class, used MLflow to track 8 experiments."
3. **Semantic resume↔JD matching** — sentence-transformers + cosine similarity. Same tech LinkedIn/Indeed use internally. Senior-level signal.
4. **Consistency dashboard** — streaks, weekly goals, application funnel. Shows data-product thinking. Recruiters love it.

If a feature doesn't reinforce one of these four, it goes in the README "Roadmap" section, not the build.

---

## Scope philosophy

> Done > Perfect. Anything not built before we ship goes into a "Roadmap / Future Work" section in the README. Recruiters love seeing a roadmap — it shows product thinking.

**MVP (must ship):** Phases 0–3
**Stretch (only if time permits):** Phase 4
**Polish (final 2 days are reserved for this — DO NOT skip):** Phase 5

---

## Phase 0 — Setup

| # | Task | Done? |
|---|---|---|
| 0.1 | Create personal project folder outside OneDrive | ✅ |
| 0.2 | Install / verify Python, Node, Git | ✅ |
| 0.3 | Initialize git repo with **per-repo personal email** (not Nokia email) | ✅ |
| 0.4 | Create personal GitHub repo + push first commit | ✅ |
| 0.5 | Scaffold folder structure (backend/, frontend/, ml/, ingestion/, docs/) | ⬜ |
| 0.6 | Create Python venv + install base packages (fastapi, uvicorn, sqlalchemy, pydantic) | ⬜ |
| 0.7 | Bootstrap Vite + React + Tailwind in `frontend/` | ⬜ |
| 0.8 | "Hello world" — backend serves `/health`, frontend shows a styled landing page | ⬜ |

**Definition of done:** `git push` works, both servers start cleanly, you can hit `localhost:8000/health` and see the React landing page at `localhost:5173`.

---

## Phase 1 — Core CRUD + Dashboard

This phase has **no ML**. Get the bones working first.

### 1.1 — Backend models + API ✅ DONE

- ✅ SQLAlchemy models: `Application`, `Email`, `StatusHistory`
- ✅ Pydantic schemas (Create / Update / Out / List)
- ✅ CRUD endpoints: `POST / GET / GET-by-id / PATCH / DELETE /applications` + `GET /applications/{id}/history`
- ✅ Dashboard stats endpoint `GET /dashboard/stats` (KPIs, daily counts, by-status, by-source, streaks)
- ✅ Seed script with 20 realistic Indian-context applications (`python -m scripts.seed`)
- ✅ pytest fixtures + 7 passing tests covering CRUD + validation + dashboard smoke
- ✅ Auto-creates StatusHistory rows on status change (audit trail)

### 1.2 — Frontend core pages

- Layout + sidebar navigation (Dashboard / Applications / Add / Settings)
- "Add Application" form (company, role, source, applied_date, status, link, notes)
- "Applications" list page — table view with sort/filter

### 1.3 — Dashboard analytics

This is the **resume-differentiating** part. Show off your data-analytics chops:

- KPI cards: Total Applied, Active (Applied + Interview), Offers, Response Rate
- **Daily applications chart** (last 30 days, line/bar) — Recharts
- **Status funnel** (Applied → Interview → Offer / Rejected) — Recharts
- **Streak counter** — "🔥 5 days in a row of applying"
- **Source breakdown** (LinkedIn vs Naukri vs Telegram vs Referral) — donut chart

### 1.4 — Polish + filters

- Search by company/role
- Filter by status, source, date range
- Sort by applied_date, status
- Mobile-responsive (Tailwind breakpoints)
- Dark mode toggle (small detail, big perceived polish)

**Definition of done:** You can manually add 20 applications, the dashboard updates live, and it looks good on phone + desktop.

---

## Phase 2 — Email parsing with ML

**This is where the ML starts.** Each task includes the concept you'll learn alongside.

### 2.1 — Gmail OAuth + email fetch

- Set up Google Cloud project, enable Gmail API
- OAuth2 flow (read-only scope: `gmail.readonly`)
- Backend endpoint: `POST /gmail/sync` — fetches last 90 days of emails, stores raw subject + sender + snippet in DB
- **Concept learned:** OAuth2 flows, scope security, never storing user passwords

### 2.2 — Email classifier (the ML part)

- Notebook in `ml/01_email_classifier.ipynb`
- Build a small labelled dataset (~100 emails labelled by you = enough for fine-tuning a small model OR for prompt engineering)
- **Two approaches, pick whichever clicks faster:**
  - **A. Zero-shot (fastest, no training):** `transformers.pipeline("zero-shot-classification")` with `facebook/bart-large-mnli`
  - **B. Fine-tune DistilBERT:** small dataset, train for 3 epochs on CPU
- Evaluate on a held-out 20% — confusion matrix, precision/recall per class
- Save model to `ml/models/email_classifier/`
- **Concepts learned:** train/test split, supervised classification, precision/recall/F1, confusion matrix, transformers (high level), zero-shot vs fine-tuning trade-off

### 2.3 — Wire it up + entity matching

- Backend service: classify each new Gmail email, extract company name (regex on signature + simple NER), match to an existing application
- Auto-update application status when email is classified as `interview` / `rejection` / `offer`
- UI: "Inbox" page showing classified emails with confidence scores
- **Concept learned:** entity linking, threshold tuning (precision-vs-recall trade-off in production)

**Definition of done:** Sync your real Gmail, see emails classified, watch one application's status flip from "Applied" to "Interview" automatically.

---

## Phase 3 — Resume ↔ JD semantic matching

### 3.1 — Embeddings core

- Notebook `ml/02_resume_jd_match.ipynb`
- Use `sentence-transformers` (`all-MiniLM-L6-v2` — small, fast, free, no GPU)
- Encode resume → vector. Encode each JD → vector. Cosine similarity = match score (0–100)
- Sub-skill scoring: split resume into bullet points → encode each → match each JD-required-skill against best-matching bullet
- **Concepts learned:** word vs sentence embeddings, cosine similarity, semantic vs lexical search, why embeddings beat keywords

### 3.2 — UI integration

- Upload resume (PDF — use `pdfplumber` or `pypdf` to extract text)
- For each application, compute and store match score
- Show on application card: "Match: 78% • Missing: Kubernetes, Airflow"
- Sort applications by match score (helps prioritise follow-ups)

**Definition of done:** Upload your real resume, see scores against the JDs you've added.

---

## Phase 4 — Telegram ingestion [STRETCH but high-differentiator]

> This is one of our four standout features. Try hard to include it. Skip ONLY if Phases 0–3 ran way long AND we're squeezed for time.

### 4.1 — Telethon connector

- Telegram API + Telethon
- User configures 3–5 channels (e.g. `@bigDataJobs`, `@RemoteJobsIndia`)
- Backend cron: fetch last 100 messages from each channel daily
- Store raw messages

### 4.2 — Job-post extraction

- Notebook `ml/03_telegram_ner.ipynb`
- For each message, classify "is this a job post?" (zero-shot again, or rules)
- If yes, extract `{role, company, location, salary, apply_link}` using a mix of regex + spaCy NER
- Surface as "Discovered Jobs" feed in UI — user can promote one to an "Applied" status with one click

---

## Phase 4.5 — Smart Apply assistant [HIGH-DIFFERENTIATOR FEATURE]

> Added based on user request: "I want this is apply for all jobs also". Approach: a **safe, ToS-respecting** version of auto-apply that's actually a stronger resume signal than a bot. Two parts:

### 4.5.1 — Tailored cover letter generator

For any application (or discovered job), generate a 150-word cover letter that:

- References the **specific company** and **role** from the JD
- Pulls 2–3 most relevant bullets from your resume (using the same sentence-transformers similarity from Phase 3)
- Highlights the JD's top required skills you actually have
- Free LLM backend: Hugging Face Inference API free tier (e.g. `meta-llama/Llama-3.2-3B-Instruct`) or local `flan-t5-base` via transformers

UI: "Generate cover letter" button on each application card → editable textbox → copy to clipboard.

**Concepts learned:** prompt engineering, retrieval-augmented generation (RAG) intuition, free LLM inference, output post-processing.

### 4.5.2 — One-click apply Chrome extension (Simplify-style, for Indian portals)

A small Manifest V3 Chrome extension that:

- On Naukri/LinkedIn/Indeed/Foundit job-application pages, detects the form
- Auto-fills your stored profile (name, email, phone, education, experience, links) into matched form fields using DOM heuristics
- Shows a floating "Apply with JobLens" button that records the application in your tracker automatically (calls your FastAPI backend)
- **You still hit Submit** — no ToS violation, no account-ban risk, no spammy applications

**Why this is the right version:** Auto-apply BOTS (LazyApply, Sonara) violate LinkedIn/Naukri ToS and can get a personal account shadow-banned — terrible for someone actively job-hunting. This Simplify-style approach gives 90% of the time-saving with zero risk, and *no* existing tool does it well for Indian portals — true product gap.

**Concepts learned:** Chrome extension Manifest V3, content scripts, DOM querying, message passing between extension and backend, CORS handling.

**Resume bullet this unlocks:** *"Built a Chrome extension that auto-fills profile data on 4 major Indian job portals (Naukri, LinkedIn, Indeed, Foundit), reducing per-application time by ~70%, and automatically syncs each application to a FastAPI tracker."*

---

## Phase 5 — Ship + polish [DO NOT SKIP]

This phase is what turns a project into a *resume* project. Always reserve a final 2 sessions for this — don't let it get squeezed out by feature work.

### 5.1 — Deploy

- Dockerize backend (single Dockerfile)
- Build frontend → static files served by FastAPI (or separate Vercel deploy)
- Deploy to **Render free tier** (or Railway / Fly.io)
- Set up `.env.example`, document env vars
- Smoke test the live URL

### 5.2 — README + demo + LinkedIn

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

## Session ritual (every time you sit down to code)

| When | What | Why |
|---|---|---|
| Start of session (5 min) | Read current phase, pick 1–3 tasks to do | Forces focus |
| Every meaningful chunk of work | `git add -A && git commit -m "..."` | You'll never lose work + your contribution graph fills up |
| End of session (5 min) | What worked / what blocked / what next | Builds an interview-ready story |
| End of session | `git push` | Backup + green squares |

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

## What "good enough" looks like when we ship

A recruiter clicks the GitHub link from your resume. Within 30 seconds they should see:

1. A **clear problem statement** in the README
2. A **GIF or screenshot** that shows what it does
3. A **live URL** they can click
4. A **tech stack section** with badges
5. A **demo video** (linked, embedded thumbnail)
6. A **roadmap** showing it's an active project, not abandoned

If those six things exist, you have a project that gets you interviews.
