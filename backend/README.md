# backend/ — FastAPI service

The Python backend for JobLens. Owns the database, REST API, ML inference, and ingestion jobs.

## Layout

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app + routers
│   ├── models/           # SQLAlchemy ORM models  (added Phase 1)
│   ├── schemas/          # Pydantic request/response schemas  (added Phase 1)
│   ├── routes/           # API endpoint modules  (added Phase 1)
│   └── services/         # Business logic (classifier, matcher)  (added Phase 2+)
├── tests/                # pytest tests  (added Phase 1)
├── requirements.txt
└── .env.example
```

## Run locally

From repo root:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Server runs at `http://localhost:8000`. API docs at `http://localhost:8000/docs`.

## Environment

Copy `.env.example` to `.env` and fill in real values. Never commit `.env` (it's gitignored).
