from fastapi.testclient import TestClient


def test_get_address_info(client: TestClient):
    # Используем валидный тестовый адрес
    test_address = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"

    response = client.post(
        "/address-info/",
        json={"address": test_address}
    )

    assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"
    data = response.json()
    assert data["address"] == test_address
    assert isinstance(data["bandwidth"], int)
    assert isinstance(data["energy"], int)
    assert isinstance(data["balance"], int)


def test_invalid_address(client: TestClient):
    # Тест на невалидный адрес
    response = client.post(
        "/address-info/",
        json={"address": "INVALID_ADDRESS"}
    )
    # FastAPI возвращает 422 при ошибках валидации
    assert response.status_code == 422
    assert "Invalid Tron address format" in response.text

def test_get_address_requests(client: TestClient, db):
    # Создаем тестовые данные
    from app.models import AddressRequest
    from datetime import datetime

    test_data = AddressRequest(
        address="TEST_ADDRESS_DB",
        bandwidth=1500,
        energy=2500,
        balance=3500,
        created_at=datetime.now()
    )
    db.add(test_data)
    db.commit()

    # Тестируем endpoint
    response = client.get("/address-requests/?page=1&limit=1")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] >= 1
    assert len(data["items"]) == 1
    assert data["items"][0]["address"] == "TEST_ADDRESS_DB"