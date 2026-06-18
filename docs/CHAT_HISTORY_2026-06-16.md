# Chat history — kickoff session, 2026-06-16

> Captured here for permanence. The previous AI session lived in the Nokia workspace; this file is the bridge so any future session in the JobLens workspace has full context.

---

## User's opening message (paraphrased)

She has been applying to jobs through LinkedIn, Indeed, Naukri, and Telegram channels. She's frustrated by the fragmentation and was thinking about building a tracker that:

- Auto-captures applied jobs.
- Reads emails from recruiters and shows results (accepted / rejected / no response).
- Has a dashboard showing daily applications so she can see how consistent she's being.
- Stands out on her resume (B.Tech in Data Science / Big Data Analytics).

She also shared two Instagram reels about facial-recognition projects (couldn't be opened — Instagram blocks fetches) and asked which idea would help her resume more.

**Important context she added:**
- She doesn't know any AI/ML yet — wants to learn the core concepts that interviewers ask about.
- She's using a Cursor tool from her Nokia internship — internship ends June 30.
- Wants to push the project to her **personal** GitHub, not Nokia's.
- Wants to use this project to learn git better.

---

## Decision matrix the agent walked her through

| Criterion | Job Tracker | Facial Recognition |
|---|---|---|
| Aligns with her DS/BDA background | Strong — data product | Tangential — pure CV |
| Saturation in fresher portfolios | Medium (Telegram angle is fresh) | Very high — extremely overdone |
| ML breadth in one project | NLP, embeddings, NER, time-series | Narrow (CNN) |
| She lives the problem | Yes | No |
| Deployable in 2 weeks | Yes | Risky (GPU, model serving) |
| Storytelling for interviews | "I built it because I needed it" | "It detects faces" |

→ **Decision: Job Tracker (JobLens).**

---

## Existing competitors the agent surveyed for her

Confirmed via web search (June 2026 results):

- **Huntr** — Kanban + Chrome extension + CRM
- **Teal HQ** — Resume builder + ATS keyword match (no auto email update)
- **Simplify** — Auto-fill 100+ ATS forms (tracker is secondary)
- **Applyra** — Gmail OAuth + AI email parsing (US-Gmail-only)
- **G-Track** — Gmail sync + Kanban + AI scoring (no Telegram)
- **Resumly** — Auto-update pipeline from email (US-Gmail-only)
- **Jobless** — Real-time push notifications (US-Gmail-only)
- **Prentus** — All-in-one with mock interviews (US-focused)

**The gap none of them fill:** Telegram channel ingestion + Indian portals (Naukri, Foundit) + a *consistency* dashboard (streaks, weekly goals).

---

## Questions she answered (the form-style choices)

1. **Direction:** "Tracker" (recommended option)
2. **Starting point:** wants comprehensive roadmap + free learning resources + personal-GitHub workflow + better git understanding; project to be done June 16-29 because internship ends June 30
3. **Workspace path:** `C:\Users\vallika\projects\job-tracker` (outside OneDrive)
4. **GitHub:** has account, no repo yet, wanted walkthrough
5. **Tooling:** confirmed git, python, node installed (Python 3.14, Node 22.22, npm 11.6, git 2.51)
6. **Personal email for git:** `vallikavoduri@gmail.com`
7. **GitHub username:** **(not yet shared)** — will share when ready
8. **Action:** wanted to open new folder in a separate Cursor window, then realized Cursor's per-workspace chat scoping made her think she'd lost chats — she had not lost anything, all 24 Nokia chats and 5.44 MB of transcripts were verified safely on disk.

---

## Critical reassurances given to her

1. **Files only go to `C:\Users\vallika\projects\job-tracker`.** Nothing personal touches Nokia OneDrive.
2. **Per-repo git config used** — global Nokia git identity untouched, project commits will use her personal email.
3. **Cursor chat history is preserved on disk** — workspace switching only filters the sidebar, never deletes chats.
4. **Python 3.14 may have ML library issues** — fallback plan: install Python 3.12 in a venv.

---

## Files created during the kickoff session

```
C:\Users\vallika\projects\job-tracker\
├── .gitignore
├── README.md
└── docs\
    ├── PROJECT_PLAN.md       (14-day day-by-day build plan)
    ├── LEARNING_ROADMAP.md   (free-only AI/ML learning path)
    ├── GIT_GUIDE.md          (daily git + GitHub walkthrough)
    ├── NOTES.md              (decisions + interview ammo)
    ├── KICKOFF_CONTEXT.md    (instructions for the next agent session)
    └── CHAT_HISTORY_2026-06-16.md  (this file)
```

No code yet — that's Phase 0.5 onwards. The agent paused at Phase 0 step 0.3 (git init) when the session was interrupted by the workspace switch.

---

## What the next session should resume with

1. Greet her — she may still be a little anxious about chat continuity. Reassure briefly.
2. Confirm: *"I've read all of `docs/`. We're at Phase 0 step 0.3 — git init with personal email. Ready when you share your GitHub username and the repo name."*
3. Once she shares: run `git init`, set per-repo config, first commit, create remote, push.
4. Then move to Phase 0.5 → 0.8: scaffold folders, set up Python venv, bootstrap Vite/React/Tailwind, hello-world both servers.
5. Aim to wrap Phase 0 today (June 16) so Day 2 starts with backend modeling per `PROJECT_PLAN.md`.
