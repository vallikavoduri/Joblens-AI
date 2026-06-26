"""End-to-end CRUD tests for /applications."""

from __future__ import annotations

from datetime import date

from fastapi.testclient import TestClient


def _make_payload(**overrides: object) -> dict:
    base = {
        "company": "Razorpay",
        "role": "Data Engineer",
        "source": "linkedin",
        "status": "applied",
        "applied_date": str(date.today()),
        "location": "Bengaluru",
    }
    base.update(overrides)
    return base


def test_health(client: TestClient) -> None:
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_create_and_get_application(client: TestClient) -> None:
    res = client.post("/applications", json=_make_payload())
    assert res.status_code == 201, res.text
    data = res.json()
    assert data["id"] > 0
    assert data["company"] == "Razorpay"
    assert data["status"] == "applied"

    app_id = data["id"]
    fetched = client.get(f"/applications/{app_id}")
    assert fetched.status_code == 200
    assert fetched.json()["id"] == app_id


def test_list_applications_filters(client: TestClient) -> None:
    client.post("/applications", json=_make_payload(company="Razorpay", source="linkedin"))
    client.post("/applications", json=_make_payload(company="Swiggy", source="naukri"))
    client.post("/applications", json=_make_payload(company="Zomato", source="telegram"))

    res = client.get("/applications")
    assert res.status_code == 200
    body = res.json()
    assert body["total"] == 3
    assert len(body["items"]) == 3

    # Filter by source
    res = client.get("/applications?source=naukri")
    assert res.json()["total"] == 1

    # Free-text search on company name
    res = client.get("/applications?q=swig")
    assert res.json()["total"] == 1
    assert res.json()["items"][0]["company"] == "Swiggy"


def test_patch_updates_status_and_logs_history(client: TestClient) -> None:
    created = client.post("/applications", json=_make_payload()).json()
    app_id = created["id"]

    res = client.patch(f"/applications/{app_id}", json={"status": "interview", "notes": "round 1 scheduled"})
    assert res.status_code == 200
    assert res.json()["status"] == "interview"
    assert res.json()["notes"] == "round 1 scheduled"

    history = client.get(f"/applications/{app_id}/history").json()
    # Should have: initial "applied" on create + transition to "interview"
    assert len(history) == 2
    assert history[-1]["new_status"] == "interview"
    assert history[-1]["old_status"] == "applied"


def test_delete_application(client: TestClient) -> None:
    created = client.post("/applications", json=_make_payload()).json()
    app_id = created["id"]

    res = client.delete(f"/applications/{app_id}")
    assert res.status_code == 204

    res = client.get(f"/applications/{app_id}")
    assert res.status_code == 404


def test_validation_rejects_blank_company(client: TestClient) -> None:
    res = client.post("/applications", json=_make_payload(company=""))
    assert res.status_code == 422  # Pydantic validation


def test_dashboard_stats_smoke(client: TestClient) -> None:
    # Empty DB → all zeros
    res = client.get("/dashboard/stats")
    assert res.status_code == 200
    body = res.json()
    assert body["total"] == 0
    assert body["response_rate"] == 0.0
    assert isinstance(body["daily_counts"], list)
    assert isinstance(body["by_status"], list)

    # After adding a few
    client.post("/applications", json=_make_payload(status="applied"))
    client.post("/applications", json=_make_payload(company="Swiggy", status="interview"))
    client.post("/applications", json=_make_payload(company="Zomato", status="rejected"))

    res = client.get("/dashboard/stats")
    body = res.json()
    assert body["total"] == 3
    assert body["active"] == 2  # applied + interview
    assert body["rejections"] == 1
