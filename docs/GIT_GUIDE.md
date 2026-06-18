# Practical Git Guide for JobLens

This guide covers ONLY the git you'll actually use during this project. No `rebase --onto` rabbit holes.

---

## Why per-repo identity matters for YOU

Your **global** git config is set to:
```
user.name  = Vallika
user.email = voduri.vallika@nokia.com
```

That's fine for Nokia work. But this project is personal — every commit you make in JobLens should show your **personal** email so:

1. Commits link to your **personal** GitHub profile
2. Your green-square contribution graph fills up correctly
3. You don't accidentally leak Nokia email into a public repo

**Solution:** set git identity *per-repo* (only for this folder), without changing global config.

```powershell
cd C:\Users\vallika\projects\job-tracker
git init
git config user.name "Vallika Voduri"
git config user.email "your-personal-email@gmail.com"
```

Notice: no `--global` flag → applies only to this repo.

Verify:
```powershell
git config user.email      # should show personal email
git config --global user.email   # should still show Nokia email — UNTOUCHED
```

---

## The 6 commands you'll use 95% of the time

| Command | What it does | When |
|---|---|---|
| `git status` | What's changed, what's staged | Constantly. Like `ls` for git. |
| `git add .` | Stage all changes | Before every commit |
| `git commit -m "..."` | Save a snapshot with a message | After every meaningful chunk of work |
| `git push` | Upload commits to GitHub | End of every coding session, minimum |
| `git pull` | Download remote commits | Start of every session (paranoia is good) |
| `git log --oneline` | See history | When debugging "what did I change yesterday" |

That's it. That's the entire daily flow.

---

## Daily flow — copy-paste this

**Start of session:**
```powershell
cd C:\Users\vallika\projects\job-tracker
git pull
git status
```

**After each meaningful chunk of work (every 30–60 minutes):**
```powershell
git status
git add .
git commit -m "feat: add streak counter to dashboard"
```

**End of session:**
```powershell
git push
```

---

## Commit message style (Conventional Commits — recruiter-friendly)

Format: `<type>: <short description>`

| Type | Use for | Example |
|---|---|---|
| `feat` | New feature | `feat: add Gmail OAuth flow` |
| `fix` | Bug fix | `fix: prevent duplicate applications on form resubmit` |
| `refactor` | Code cleanup, no behaviour change | `refactor: extract email parser into service module` |
| `docs` | Documentation only | `docs: add architecture diagram to README` |
| `chore` | Setup, deps, config | `chore: bump fastapi to 0.115` |
| `test` | Adding tests | `test: add unit tests for status transitions` |
| `style` | Formatting, no logic change | `style: format with black` |

**Why this matters:** when a recruiter scrolls your GitHub commit history, "Conventional Commits" instantly signals "this person follows industry conventions." Tiny detail, big perception shift.

---

## What if you mess up?

### "I committed but forgot to add a file"
```powershell
git add forgotten-file.py
git commit --amend --no-edit
```
(Only do this if you haven't pushed yet.)

### "I committed wrong files / wrong message and haven't pushed"
```powershell
git reset --soft HEAD~1   # undo commit, keep changes staged
# fix the issue, then re-commit
```

### "I want to undo all my uncommitted changes" (DANGEROUS — work is lost)
```powershell
git checkout .            # discard unstaged changes
git reset --hard HEAD     # discard everything to last commit
```
Pause and ask before running these. They cannot be undone.

### "I accidentally committed `.env` with my API key"
```powershell
# 1. Rotate the leaked key IMMEDIATELY (assume it's compromised)
# 2. Remove from history:
git rm --cached .env
git commit -m "chore: remove .env from tracking"
# Add .env to .gitignore (already done in this repo)
# If you've ALREADY pushed: tell me and we'll do a force-push removal
```

---

## GitHub setup walkthrough (one-time)

You said you have an account but no repo yet. Here's what to do:

### 1. On github.com (in browser)

1. Go to [github.com/new](https://github.com/new)
2. **Repository name:** `joblens` (or `job-tracker` — your choice; `joblens` sounds better on a resume)
3. **Description:** `AI-powered job application tracker with Gmail + Telegram ingestion, ML email classification, and resume↔JD semantic matching.`
4. **Public** ✓ (recruiters need to see it)
5. **DO NOT** check "Add a README file" — you already have one locally
6. **DO NOT** add `.gitignore` or license here — you have them locally
7. Click **Create repository**

### 2. GitHub will show you a "push existing repo" snippet — copy your URL

It'll look like:
```
https://github.com/<your-username>/joblens.git
```

### 3. In the project folder

(I'll run these for you once you tell me your personal email + GitHub username + new repo URL.)

```powershell
cd C:\Users\vallika\projects\job-tracker
git init -b main
git config user.name "Vallika Voduri"
git config user.email "<personal-email>"
git add .
git commit -m "chore: initial scaffold + planning docs"
git remote add origin https://github.com/<username>/joblens.git
git push -u origin main
```

### 4. Authentication on first push

Windows will pop up a Git Credential Manager window. Sign in with your **personal** GitHub account. After this, future pushes are silent.

⚠️ **If it tries to use Nokia SSO / your work GitHub:** click "use a different account" and pick personal. If you've never linked your personal GitHub to Credential Manager on this machine, it'll ask cleanly.

---

## Branching (you don't need it for solo work, but interview-relevant)

For JobLens, just commit to `main`. It's your project, you're solo.

But know this for interviews:

```powershell
git checkout -b feature/email-classifier   # create + switch to branch
# ... work, commit ...
git push -u origin feature/email-classifier
# Open a PR on GitHub, merge to main
```

If you want to *practice* PRs (and have them visible on your profile), branch every Phase. That's actually a nice resume-flex: "I treated my solo project like a team project."

---

## What NOT to commit (already handled by `.gitignore`)

| File / folder | Why |
|---|---|
| `.env`, `credentials.json`, `token.json` | API keys, OAuth tokens — credential leak |
| `node_modules/`, `.venv/` | Huge, regeneratable from `package.json` / `requirements.txt` |
| `*.db`, `*.sqlite` | Personal data |
| `data/raw/`, `models/`, `mlruns/` | Big binaries — use DVC or just gitignore |
| `__pycache__/`, `.pytest_cache/` | Build artifacts |

If you ever wonder "should this be committed?" — ask yourself: "would I be happy if a stranger read this on the internet?"

---

## Pro tips that make a public GitHub profile look professional

1. **Pin JobLens** on your profile (top of page).
2. **Write a great repo description** (1 sentence) and add **topics** (`ai`, `nlp`, `fastapi`, `react`, `huggingface`, `mlops`).
3. **Set a repo social preview image** in repo Settings → social preview. Use [og-image.vercel.app](https://og-image.vercel.app/) free.
4. **Profile README** — create a repo named exactly your username; the README there shows on your profile. Mention JobLens.
5. **Star repos in your stack** — recruiters do glance at what you star.
