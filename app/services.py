"""
Service layer for Tron Address Info API.

Contains business logic for interacting with Tron blockchain
and database operations.
"""

import logging
from urllib.parse import urljoin
import requests
from sqlalchemy.orm import Session
from app.config import settings
from app.models import AddressRequest as AddressRequestModel
from app.schemas import AddressRequestCreate

logger = logging.getLogger(__name__)


class TronService:
    """Service for interacting with Tron blockchain API."""

    def __init__(self):
        """Initialize TronService with network configuration."""
        self.base_url = settings.TRON_NETWORK_URL.rstrip('/')
        self.headers = {
            'accept': 'application/json',
            'content-type': 'application/json'
        }
        logger.info(f"Initialized TronService with base URL: {self.base_url}")

    def _make_tron_request(self, endpoint: str, payload: dict) -> dict:
        """
        Make a request to Tron API.

        Args:
            endpoint: API endpoint (e.g., 'wallet/getaccount')
            payload: Request payload

        Returns:
            JSON response from API

        Raises:
            ValueError: If request fails
        """
        full_url = urljoin(f"{self.base_url}/", endpoint)
        logger.debug(f"Making request to: {full_url}")

        try:
            response = requests.post(
                full_url,
                headers=self.headers,
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Request to {full_url} failed: {str(e)}")
            raise ValueError(f"Tron API request failed: {str(e)}")

    def get_address_info(self, payload: dict) -> dict:
        """
        Get comprehensive address information from Tron API.

        Args:
            payload: Must contain 'address' field

        Returns:
            Dictionary with address information

        Raises:
            ValueError: If address is missing or API fails
        """
        if not payload.get("address"):
            raise ValueError("Address is required")

        account_data = self._make_tron_request("wallet/getaccount", payload)
        balance_data = self._make_tron_request("wallet/getaccountbalance", payload)

        return {
            "address": payload["address"],
            "bandwidth": account_data.get("free_net_limit", 0),
            "energy": account_data.get("energy_limit", 0),
            "balance": balance_data.get("balance", 0),
            "visible": payload.get("visible", True)
        }


class DatabaseService:
    """Service for database operations."""

    def create_address_request(
            self,
            db: Session,
            request: AddressRequestCreate
    ) -> AddressRequestModel:
        """
        Create a new address request record.

        Args:
            db: Database session
            request: Address request data

        Returns:
            Created AddressRequest model instance
        """
        db_request = AddressRequestModel(**request.dict())
        db.add(db_request)
        db.commit()
        db.refresh(db_request)
        return db_request

    def get_address_requests(
            self,
            db: Session,
            skip: int = 0,
            limit: int = 10
    ) -> list[AddressRequestModel]:
        """
        Get paginated list of address requests.

        Args:
            db: Database session
            skip: Number of items to skip
            limit: Maximum number of items to return

        Returns:
            List of AddressRequest instances
        """
        return db.query(AddressRequestModel) \
            .order_by(AddressRequestModel.created_at.desc()) \
            .offset(skip) \
            .limit(limit) \
            .all()

    def count_address_requests(self, db: Session) -> int:
        """
        Count total number of address requests.

        Args:
            db: Database session

        Returns:
            Total count of address requests
        """
        return db.query(AddressRequestModel).count()