# ingestion/ — External data sources

Modules that pull in jobs / emails from outside JobLens. Each source is a self-contained sub-package, callable from the backend or runnable as a CLI.

## Sources (filled in across phases)

| Module | Source | Phase |
|---|---|---|
| `gmail/`     | Gmail API (OAuth2 read-only) — recruiter emails | Phase 2 |
| `telegram/`  | Telethon — public Telegram job channels | Phase 4 (stretch) |
| `scrapers/`  | Naukri / LinkedIn / Foundit — public job listings | Optional |

## Design rules

1. **Read-only.** Ingestion never logs into anything that requires write access. No bots, no auto-apply (that's Phase 4.5).
2. **Idempotent.** Running an ingestion twice never creates duplicates — dedupe by source+external-id at insert time.
3. **Async-safe.** Long ingestions run as background tasks, not inside HTTP request handlers.
