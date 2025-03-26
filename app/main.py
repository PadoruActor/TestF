# app/main.py
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import math
from app import schemas, services
from app.database import get_db
import logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Инициализация сервисов
tron_service = services.TronService()
db_service = services.DatabaseService()


@app.post("/address-info/", response_model=schemas.AddressInfo)
async def get_address_info(request: schemas.TronApiRequest, db: Session = Depends(get_db)):
    try:
        # Получаем данные из Tron API
        address_info = tron_service.get_address_info(request.dict())

        # Сохраняем в базу данных
        db_service.create_address_request(db, schemas.AddressRequestCreate(
            address=address_info.address,
            bandwidth=address_info.bandwidth,
            energy=address_info.energy,
            balance=address_info.balance
        ))

        return address_info

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/address-requests/", response_model=schemas.PaginatedAddressRequests)
async def get_address_requests(
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1, le=100),
        db: Session = Depends(get_db)
):
    skip = (page - 1) * limit
    total = db_service.count_address_requests(db)
    pages = math.ceil(total / limit) if total else 1

    items = db_service.get_address_requests(db, skip=skip, limit=limit)

    return {
        "count": total,
        "items": items,
        "page": page,
        "pages": pages
    }