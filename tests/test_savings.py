from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_saving():
    response = client.post("/savings/", json={
        "date": "2024-05-24",
        "amount": 12.5,
        "category": "test",
        "notes": "Unit test record"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == 12.5
    assert data["category"] == "test"

def test_get_savings():
    response = client.get("/savings/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_by_id():
    post = client.post("/savings/", json={
        "date": "2024-05-24",
        "amount": 99.9,
        "category": "lookup",
        "notes": "for ID test"
    })
    saving_id = post.json()["id"]

    get = client.get(f"/savings/{saving_id}")
    assert get.status_code == 200
    assert get.json()["id"] == saving_id

def test_update_saving():
    post = client.post("/savings/", json={
        "date": "2024-05-24",
        "amount": 50.0,
        "category": "update",
        "notes": "to update"
    })
    saving_id = post.json()["id"]

    update = client.put(f"/savings/{saving_id}", json={
        "date": "2024-05-25",
        "amount": 75.0,
        "category": "updated",
        "notes": "updated notes"
    })
    assert update.status_code == 200
    updated = update.json()
    assert updated["amount"] == 75.0
    assert updated["category"] == "updated"

def test_delete_saving():
    post = client.post("/savings/", json={
        "date": "2024-05-24",
        "amount": 88.8,
        "category": "temp",
        "notes": "delete me"
    })
    saving_id = post.json()["id"]

    delete = client.delete(f"/savings/{saving_id}")
    assert delete.status_code == 200
    assert "deleted" in delete.json()["message"]

def test_get_nonexistent():
    response = client.get("/savings/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Saving not found"

def test_delete_nonexistent():
    response = client.delete("/savings/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Saving not found"
    
def test_create_missing_date():
    response = client.post("/savings/", json={
        "amount": 10.0,
        "category": "test",
        "notes": "missing date"
    })
    assert response.status_code == 422
    assert "detail" in response.json()

def test_create_missing_amount():
    response = client.post("/savings/", json={
        "date": "2024-05-24",
        "category": "test",
        "notes": "missing amount"
    })
    assert response.status_code == 422
    assert "detail" in response.json()

def test_create_invalid_amount():
    response = client.post("/savings/", json={
        "date": "2024-05-24",
        "amount": "not_a_number",
        "category": "test",
        "notes": "invalid amount"
    })
    assert response.status_code == 422
    assert "detail" in response.json()

def test_create_bad_date_format():
    response = client.post("/savings/", json={
        "date": "24-05-2024",  # Invalid format, should be YYYY-MM-DD
        "amount": 100.0,
        "category": "test",
        "notes": "bad date"
    })
    assert response.status_code == 422
    assert "detail" in response.json()


def test_summary_endpoint():
    # Create 3 entries in different months
    entries = [
        {"date": "2024-01-15", "amount": 100.0, "category": "test", "notes": "Jan"},
        {"date": "2024-02-15", "amount": 200.0, "category": "test", "notes": "Feb"},
        {"date": "2024-03-15", "amount": 300.0, "category": "test", "notes": "Mar"},
    ]

    for entry in entries:
        client.post("/savings/", json=entry)

    response = client.get("/summary/")
    assert response.status_code == 200

    data = response.json()
    assert data["total_savings"] == 600.0
    assert data["average_monthly"] == 200.0
    assert "2024-01" in data["monthly_breakdown"]
    assert data["highest_month"]["month"] == "2024-03"
    assert data["highest_month"]["amount"] == 300.0
