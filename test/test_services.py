from app.services import DatabaseService
from app.schemas import AddressRequestCreate
from app.models import AddressRequest
from datetime import datetime


def test_create_address_request(db):
    db_service = DatabaseService()

    request_data = AddressRequestCreate(
        address="TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t",
        bandwidth=1000,
        energy=2000,
        balance=3000
    )

    created_request = db_service.create_address_request(db, request_data)

    assert created_request.id is not None
    assert created_request.address == request_data.address
    assert created_request.bandwidth == request_data.bandwidth
    assert created_request.energy == request_data.energy
    assert created_request.balance == request_data.balance

    # Проверяем запись в БД
    db_request = db.query(AddressRequest).filter(AddressRequest.id == created_request.id).first()
    assert db_request is not None