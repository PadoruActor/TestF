from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import math
import logging
from app import schemas, services
from app.database import get_db

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Tron Address Info API",
    description="API for retrieving and storing Tron blockchain address information",
    version="1.0.0"
)

# Initialize services
tron_service = services.TronService()
db_service = services.DatabaseService()


@app.post("/address-info/", response_model=schemas.AddressInfo)
async def get_address_info(
        request: schemas.TronApiRequest,
        db: Session = Depends(get_db)
):
    """
    Retrieve information about a Tron blockchain address.

    Args:
        request: TronApiRequest containing address and visibility flag
        db: Database session dependency

    Returns:
        Address information including balance, bandwidth, and energy

    Raises:
        HTTPException: 400 for invalid requests, 500 for server errors
    """
    try:
        request_data = {
            "address": request.address,
            "visible": request.visible
        }

        # Get data from Tron API
        address_info = tron_service.get_address_info(request_data)

        # Save to database
        db_request = schemas.AddressRequestCreate(
            address=address_info["address"],
            bandwidth=address_info["bandwidth"],
            energy=address_info["energy"],
            balance=address_info["balance"]
        )
        db_service.create_address_request(db, db_request)

        return address_info
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/address-requests/", response_model=schemas.PaginatedAddressRequests)
async def get_address_requests(
        page: int = Query(1, ge=1, description="Page number"),
        limit: int = Query(10, ge=1, le=100, description="Items per page"),
        db: Session = Depends(get_db)
):
    """
    Retrieve paginated history of address requests.

    Args:
        page: Page number to retrieve
        limit: Number of items per page
        db: Database session dependency

    Returns:
        Paginated list of address requests with metadata
    """
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