"""Seed the database with realistic Indian-context fake applications.

Run from the `backend/` folder (with venv activated):
    python -m scripts.seed

It's safe to re-run: clears the applications table first, then inserts 20 records.
The dates are spread over the last 60 days so the dashboard charts look real.
"""

from __future__ import annotations

import random
from datetime import date, timedelta

from app.db import Base, SessionLocal, engine
from app.models.application import Application
from app.models.status_history import StatusHistory
from app.schemas.common import Source, Status

# Indian-context tech companies + roles a fresh DS/BDA grad would realistically apply to
COMPANIES_AND_ROLES: list[tuple[str, list[str]]] = [
    ("Razorpay",            ["Data Engineer", "Data Scientist", "Backend Engineer"]),
    ("Swiggy",              ["Data Analyst", "ML Engineer", "Business Analyst"]),
    ("Zomato",              ["Data Scientist", "Data Engineer"]),
    ("Flipkart",            ["Data Engineer", "ML Engineer", "SDE-1"]),
    ("PhonePe",             ["Data Engineer", "Backend Engineer"]),
    ("Freshworks",          ["Data Analyst", "Software Engineer"]),
    ("Zoho",                ["Data Engineer", "Software Engineer"]),
    ("CRED",                ["Data Scientist", "Backend Engineer"]),
    ("Postman",             ["Software Engineer", "Data Engineer"]),
    ("BrowserStack",        ["Software Engineer"]),
    ("Microsoft India",     ["Data Engineer", "Data Scientist"]),
    ("Walmart Global Tech", ["Data Analyst", "Data Engineer"]),
    ("Atlassian India",     ["Software Engineer"]),
    ("Mphasis",             ["Data Analyst", "Software Engineer"]),
    ("Persistent Systems",  ["Data Engineer"]),
    ("Mu Sigma",            ["Business Analyst", "Decision Scientist"]),
    ("TCS",                 ["Data Analyst"]),
    ("Infosys",             ["Data Engineer"]),
    ("Wipro",               ["Data Analyst"]),
    ("Capgemini",           ["Data Engineer"]),
]

LOCATIONS = ["Bengaluru", "Hyderabad", "Pune", "Gurgaon", "Mumbai", "Chennai", "Remote (India)"]
SALARY_RANGES = ["₹6-10 LPA", "₹8-14 LPA", "₹10-18 LPA", "₹12-20 LPA", "₹15-25 LPA", None, None]

SOURCES_WEIGHTED = (
    [Source.LINKEDIN] * 6
    + [Source.NAUKRI] * 4
    + [Source.TELEGRAM] * 4
    + [Source.REFERRAL] * 2
    + [Source.INDEED] * 2
    + [Source.COMPANY_SITE] * 1
    + [Source.FOUNDIT] * 1
)

# Status distribution biased toward Applied/Ghosted/Rejected (realistic for early job hunt)
def _pick_status(days_ago: int) -> Status:
    """Older apps are more likely to have an outcome; newer ones still 'applied'."""
    if days_ago < 7:
        return random.choices(
            [Status.APPLIED, Status.SCREENING],
            weights=[8, 2],
        )[0]
    if days_ago < 21:
        return random.choices(
            [Status.APPLIED, Status.SCREENING, Status.INTERVIEW, Status.REJECTED],
            weights=[5, 3, 2, 2],
        )[0]
    return random.choices(
        [Status.APPLIED, Status.SCREENING, Status.INTERVIEW, Status.OFFER, Status.REJECTED, Status.GHOSTED],
        weights=[2, 1, 2, 1, 4, 5],
    )[0]


SAMPLE_JD = (
    "We are looking for a Data Engineer to join our team. You will design and build "
    "scalable ETL pipelines using Python, SQL, and Spark on AWS. Strong understanding of "
    "data modeling, Airflow, and dbt is required. Experience with Databricks or Snowflake "
    "is a plus."
)


def seed(num: int = 20) -> None:
    random.seed(42)  # reproducible

    # Reset
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        db.query(StatusHistory).delete()
        db.query(Application).delete()
        db.commit()

        today = date.today()
        # Pick 20 (company, role) pairs without replacement when possible
        picks: list[tuple[str, str]] = []
        bag = COMPANIES_AND_ROLES.copy()
        random.shuffle(bag)
        for company, roles in bag:
            picks.append((company, random.choice(roles)))
        # If we need more than the unique companies list, top up with random repeats
        while len(picks) < num:
            company, roles = random.choice(COMPANIES_AND_ROLES)
            picks.append((company, random.choice(roles)))
        picks = picks[:num]

        for company, role in picks:
            days_ago = random.randint(0, 59)
            applied = today - timedelta(days=days_ago)
            status = _pick_status(days_ago)

            app_row = Application(
                company=company,
                role=role,
                source=random.choice(SOURCES_WEIGHTED),
                applied_date=applied,
                status=status,
                link=f"https://example.com/jobs/{company.lower().replace(' ', '-')}-{role.lower().replace(' ', '-')}",
                location=random.choice(LOCATIONS),
                salary_range=random.choice(SALARY_RANGES),
                job_description=SAMPLE_JD if random.random() < 0.6 else None,
                notes=None,
            )
            db.add(app_row)
            db.flush()

            db.add(
                StatusHistory(
                    application_id=app_row.id,
                    old_status=None,
                    new_status=Status.APPLIED,
                    source="seed",
                    note="initial application",
                    changed_at=None,  # uses server_default = now()
                )
            )
            if status != Status.APPLIED:
                db.add(
                    StatusHistory(
                        application_id=app_row.id,
                        old_status=Status.APPLIED,
                        new_status=status,
                        source="seed",
                        note=f"transition to {status.value}",
                    )
                )

        db.commit()
        print(f"Seeded {num} applications.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
