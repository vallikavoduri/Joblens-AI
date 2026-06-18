# Notes from the kickoff conversation (June 16, 2026)

Captured here so you have a permanent reference for the *why* behind every decision in this project. Especially useful for:
- Interview storytelling ("walk me through this project")
- Picking back up after a break
- Explaining your choices in your README / LinkedIn post

---

## The core insight

> The job-tracker space is crowded with US-focused, Gmail-only tools. The real gap is **Telegram channels + Indian portals (Naukri, Foundit) + consistency analytics**. That's where this project differentiates.

---

## Why JobLens won over the facial-recognition idea

| Criterion | JobLens (chosen) | Facial Recognition |
|---|---|---|
| Aligns with your B.Tech (Data Science / Big Data Analytics) | ✅ Strong — data product | ⚠️ Tangential — it's CV |
| Saturation in fresher portfolios | Medium (Telegram angle is fresh) | **Very high** — most overdone project |
| ML breadth in one project | NLP, embeddings, NER, time-series | One narrow domain (CNN) |
| You understand the user (yourself) | ✅ Living the problem | ⚠️ No real user |
| Storytelling for interviews | "I built this because I needed it" — gold | "It detects faces" — generic |
| Open-source potential / GitHub stars | Genuine (Telegram + Naukri gap) | Crowded space |
| Production deploy is realistic in 2 weeks | ✅ Yes | ⚠️ ML serving + GPU cost |

---

## Existing players (so you can position against them in your README)

| Tool | What they do | What they DON'T do |
|---|---|---|
| Huntr | Kanban + Chrome extension + CRM | No Telegram, no Naukri, no consistency dashboard |
| Teal HQ | Resume builder + ATS keyword match | No auto-update from email, no Indian portals |
| Simplify | Auto-fill 100+ ATS forms | Tracker is secondary |
| Applyra | Gmail OAuth + AI email parsing | US-Gmail-only |
| G-Track | Gmail sync + Kanban + AI scoring | No Telegram, no Indian portals |
| Resumly | Auto-update pipeline from email | Same blind spot |
| Jobless | Real-time push notifications | Same blind spot |

**Your README pitch (when you write it):**

> "I evaluated Huntr, Teal, Simplify, Applyra, and G-Track. All five solve US-centric Gmail tracking. None handle Telegram channels (a major source for Indian and remote-first job seekers) or Naukri/Foundit. JobLens fills that gap and adds a consistency dashboard because outcomes follow effort."

That paragraph alone signals product thinking — rare in fresher portfolios.

---

## Architecture decisions (and the *why* for each — interview ammo)

| Decision | Why |
|---|---|
| **FastAPI** (not Flask, not Django) | Python-first (so you stay in ML ecosystem); async-ready; auto-docs; lightweight |
| **SQLite first, Postgres later** | Zero-config for Day 2 dev; SQLAlchemy makes the swap one line |
| **Vite + React** (not Next.js) | Faster dev loop for a solo SPA; no SSR overhead you don't need |
| **Tailwind** (not MUI / Chakra) | Smaller bundle; fewer "looks like every other portal" vibes |
| **sentence-transformers `all-MiniLM-L6-v2`** | 80MB, runs on CPU, near-state-of-the-art for sentence similarity |
| **DistilBERT (or zero-shot BART) for email classification** | DistilBERT = 66M params, trains fast on CPU; BART zero-shot needs no training data |
| **Render free tier** | Free 750hrs/month, supports Docker, no credit card |
| **MLflow for experiment tracking** | Industry-standard MLOps tool; tiny effort to add, huge resume signal |
| **OAuth2 read-only Gmail scope** | Security signal — recruiters look for this kind of detail |

When an interviewer asks "Why did you pick X?", every answer above is a **30-second story**. Memorise three of these by interview day.

---

## ML concepts you'll cover (and the resume bullet points they unlock)

By June 29, you can legitimately put these on your resume:

- "Fine-tuned DistilBERT for 5-class email classification (precision: 0.XX, recall: 0.XX) on 100 hand-labelled examples"
- "Built semantic resume↔JD matching using sentence-transformers embeddings + cosine similarity"
- "Designed an OAuth2 + Gmail API ingestion pipeline with read-only scope and token rotation"
- "Used MLflow to track experiments across 8 classifier configurations and selected the model with best F1-on-rejection-class"
- "Deployed full-stack ML application on Render with Dockerised FastAPI backend and Vite-React frontend"
- "Reduced manual job-tracking time by ~95% in personal use, applied to 60+ roles using the platform"

**Notice:** every bullet has a number. **Numbers > adjectives** in resumes.

---

## Things you SHOULD NOT do (anti-patterns I'll catch you on)

1. **Don't try to use GPT-4 / OpenAI API for classification.** Free tier is paywalled; recruiters want to see *your* model. Use HuggingFace open models.
2. **Don't add features mid-build.** Anything new goes in the README "Roadmap" section.
3. **Don't skip Phase 5 (deploy + README + demo).** A great unfinished project < a decent finished one.
4. **Don't commit `.env` files.** `.gitignore` already protects you, but always `git status` before commit.
5. **Don't keep coding past midnight.** Tired commits = bug commits. Push, sleep, resume tomorrow.

---

## Personal email for git config

> **TODO:** fill this in once you decide which email to use for personal commits.
>
> Recommended: a Gmail like `vallikavoduri@gmail.com` (whatever you already use for personal GitHub login). It must match the email on your personal GitHub account, otherwise commits won't link to your profile.

```
[entered on Day 1]: __________________________
```

---

## Post-internship plan (after June 30)

1. **Week of June 30:** rest 2–3 days, then deep clean the JobLens codebase, write a Medium / Hashnode blog post about building it.
2. **July:** start Track B of the learning roadmap (Andrew Ng + 3Blue1Brown).
3. **August onwards:** weekly LinkedIn post, daily 1 SQL/Python question, apply to roles using JobLens itself (very meta — recruiters love this story).

---

## When you doubt yourself

You're a fresher. You're using AI tools to learn faster than someone six months ago could have. That's not cheating — that's what every productive engineer in 2026 does. The recruiters worth working for know this.

You'll forget half the ML concepts you "learn" during this build. That's normal. The *project* is the artifact that proves you can build, debug, and ship. The concepts come back faster the second time.

Keep going.
