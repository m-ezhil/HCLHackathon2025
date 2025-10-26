import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException
from main import app
from database.core import get_db
import account.routes as account_routes

# Dummy DB object for dependency override
class DummyDB:
    pass

@pytest.fixture()
def client():
    def override_get_db():
        yield DummyDB()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

# Helper fake customer returned by auth dependency
class FakeCustomer:
    def __init__(self, id=1):
        self.id = id

# ---------------------------
# Successful creation tests
# ---------------------------

def test_account_creation_success_creates_account_and_transaction(client, monkeypatch):
    # Arrange
    fake_customer = FakeCustomer(id=42)
    monkeypatch.setattr(account_routes, "verify_access_token", lambda: fake_customer)
    # Simulate no existing account
    monkeypatch.setattr(account_routes, "is_account_exists", lambda db, cid, atype: False)

    created = {"id": 100, "customer_id": 42, "account_type": "SAVINGS", "balance": 0}
    monkeypatch.setattr(account_routes, "create_account", lambda db, cid, atype, amount: created)

    called = {}
    def fake_create_tx(db, account_id, tx_type, amt):
        called["args"] = (account_id, tx_type, amt)
    monkeypatch.setattr(account_routes, "create_transaction_by_account_id", fake_create_tx)

    # Act
    resp = client.post("/account/create", json={"account_type": "savings", "initial_deposit": 250})

    # Assert
    assert resp.status_code == 200
    body = resp.json()
    assert body["id"] == 100
    assert body["customer_id"] == 42
    assert body["account_type"] == "SAVINGS"
    # create_account is called with initial balance 0 (per route) and transaction called with deposit amount
    assert called.get("args") == (100, "DEPOSIT", 250)

# ---------------------------
# Validation and failure tests
# ---------------------------

def test_account_creation_negative_initial_deposit_returns_400(client, monkeypatch):
    # Arrange: authenticated user
    monkeypatch.setattr(account_routes, "verify_access_token", lambda: FakeCustomer(id=1))
    # Act
    resp = client.post("/account/create", json={"account_type": "SAVINGS", "initial_deposit": -10})
    # Assert
    assert resp.status_code == 400
    assert "detail" in resp.json()

def test_account_creation_invalid_account_type_returns_400(client, monkeypatch):
    monkeypatch.setattr(account_routes, "verify_access_token", lambda: FakeCustomer(id=1))
    resp = client.post("/account/create", json={"account_type": "GOLD", "initial_deposit": 50})
    assert resp.status_code == 400
    assert "detail" in resp.json()

def test_account_creation_duplicate_account_returns_400(client, monkeypatch):
    monkeypatch.setattr(account_routes, "verify_access_token", lambda: FakeCustomer(id=7))
    # Simulate existing account for this customer & type
    monkeypatch.setattr(account_routes, "is_account_exists", lambda db, cid, atype: True)
    resp = client.post("/account/create", json={"account_type": "SAVINGS", "initial_deposit": 0})
    assert resp.status_code == 400
    assert "detail" in resp.json()

def test_account_creation_unauthorized_returns_401(client, monkeypatch):
    # Simulate auth dependency raising unauthorized
    def raise_unauth():
        raise HTTPException(status_code=401, detail="Unauthorized")
    monkeypatch.setattr(account_routes, "verify_access_token", raise_unauth)
    resp = client.post("/account/create", json={"account_type": "SAVINGS", "initial_deposit": 10})
    assert resp.status_code == 401

def test_account_creation_missing_fields_returns_422(client, monkeypatch):
    # auth ok
    monkeypatch.setattr(account_routes, "verify_access_token", lambda: FakeCustomer(id=1))
    # missing initial_deposit -> pydantic validation error
    resp = client.post("/account/create", json={"account_type": "SAVINGS"})
    assert resp.status_code == 422
    assert "detail" in resp.json()

# ---------------------------
# Edge / negative scenarios
# ---------------------------

def test_account_creation_account_type_case_insensitive(client, monkeypatch):
    # Ensure lowercase account_type is accepted (route uses .upper())
    fake_customer = FakeCustomer(id=55)
    monkeypatch.setattr(account_routes, "verify_access_token", lambda: fake_customer)
    monkeypatch.setattr(account_routes, "is_account_exists", lambda db, cid, atype: False)
    monkeypatch.setattr(account_routes, "create_account", lambda db, cid, atype, amount: {"id": 1, "customer_id": cid, "account_type": atype.upper(), "balance": 0})
    monkeypatch.setattr(account_routes, "create_transaction_by_account_id", lambda db, aid, t, amt: None)

    resp = client.post("/account/create", json={"account_type": "current", "initial_deposit": 0})
    assert resp.status_code == 200
    assert resp.json()["account_type"] == "CURRENT"
```# filepath: c:\Users\ezhil_qkbzfrn\Desktop\HCL Hackathon\HCLHackathon2025\tests\test_account_routes.py
import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException
from main import app
from database.core import get_db
import account.routes as account_routes

# Dummy DB object for dependency override
class DummyDB:
    pass

@pytest.fixture()
def client():
    def override_get_db():
        yield DummyDB()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

# Helper fake customer returned by auth dependency
class FakeCustomer:
    def __init__(self, id=1):
        self.id = id

# ---------------------------
# Successful creation tests
# ---------------------------

def test_account_creation_success_creates_account_and_transaction(client, monkeypatch):
    # Arrange
    fake_customer = FakeCustomer(id=42)
    monkeypatch.setattr(account_routes, "verify_access_token", lambda: fake_customer)
    # Simulate no existing account
    monkeypatch.setattr(account_routes, "is_account_exists", lambda db, cid, atype: False)

    created = {"id": 100, "customer_id": 42, "account_type": "SAVINGS", "balance": 0}
    monkeypatch.setattr(account_routes, "create_account", lambda db, cid, atype, amount: created)

    called = {}
    def fake_create_tx(db, account_id, tx_type, amt):
        called["args"] = (account_id, tx_type, amt)
    monkeypatch.setattr(account_routes, "create_transaction_by_account_id", fake_create_tx)

    # Act
    resp = client.post("/account/create", json={"account_type": "savings", "initial_deposit": 250})

    # Assert
    assert resp.status_code == 200
    body = resp.json()
    assert body["id"] == 100
    assert body["customer_id"] == 42
    assert body["account_type"] == "SAVINGS"
    # create_account is called with initial balance 0 (per route) and transaction called with deposit amount
    assert called.get("args") == (100, "DEPOSIT", 250)

# ---------------------------
# Validation and failure tests
# ---------------------------

def test_account_creation_negative_initial_deposit_returns_400(client, monkeypatch):
    # Arrange: authenticated user
    monkeypatch.setattr(account_routes, "verify_access_token", lambda: FakeCustomer(id=1))
    # Act
    resp = client.post("/account/create", json={"account_type": "SAVINGS", "initial_deposit": -10})
    # Assert
    assert resp.status_code == 400
    assert "detail" in resp.json()

def test_account_creation_invalid_account_type_returns_400(client, monkeypatch):
    monkeypatch.setattr(account_routes, "verify_access_token", lambda: FakeCustomer(id=1))
    resp = client.post("/account/create", json={"account_type": "GOLD", "initial_deposit": 50})
    assert resp.status_code == 400
    assert "detail" in resp.json()

def test_account_creation_duplicate_account_returns_400(client, monkeypatch):
    monkeypatch.setattr(account_routes, "verify_access_token", lambda: FakeCustomer(id=7))
    # Simulate existing account for this customer & type
    monkeypatch.setattr(account_routes, "is_account_exists", lambda db, cid, atype: True)
    resp = client.post("/account/create", json={"account_type": "SAVINGS", "initial_deposit": 0})
    assert resp.status_code == 400
    assert "detail" in resp.json()

def test_account_creation_unauthorized_returns_401(client, monkeypatch):
    # Simulate auth dependency raising unauthorized
    def raise_unauth():
        raise HTTPException(status_code=401, detail="Unauthorized")
    monkeypatch.setattr(account_routes, "verify_access_token", raise_unauth)
    resp = client.post("/account/create", json={"account_type": "SAVINGS", "initial_deposit": 10})
    assert resp.status_code == 401

def test_account_creation_missing_fields_returns_422(client, monkeypatch):
    # auth ok
    monkeypatch.setattr(account_routes, "verify_access_token", lambda: FakeCustomer(id=1))
    # missing initial_deposit -> pydantic validation error
    resp = client.post("/account/create", json={"account_type": "SAVINGS"})
    assert resp.status_code == 422
    assert "detail" in resp.json()

# ---------------------------
# Edge / negative scenarios
# ---------------------------

def test_account_creation_account_type_case_insensitive(client, monkeypatch):
    # Ensure lowercase account_type is accepted (route uses .upper())
    fake_customer = FakeCustomer(id=55)
    monkeypatch.setattr(account_routes, "verify_access_token", lambda: fake_customer)
    monkeypatch.setattr(account_routes, "is_account_exists", lambda db, cid, atype: False)
    monkeypatch.setattr(account_routes, "create_account", lambda db, cid, atype, amount: {"id": 1, "customer_id": cid, "account_type": atype.upper(), "balance": 0})
    monkeypatch.setattr(account_routes, "create_transaction_by_account_id", lambda db, aid, t, amt: None)

    resp = client.post("/account/create", json={"account_type": "current", "initial_deposit": 0})
    assert resp.status_code == 200
    assert resp.json()["account_type"] == "CURRENT"