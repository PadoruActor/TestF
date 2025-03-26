# app/services.py
import logging
from urllib.parse import urljoin

import requests
from requests import Session
from tronpy import Tron
from tronpy.providers import HTTPProvider
from app.config import settings
from app.models import AddressRequest as AddressRequestModel
from app.schemas import AddressRequestCreate

logger = logging.getLogger(__name__)


class TronService:
    def __init__(self):
        self.base_url = settings.TRON_NETWORK_URL.rstrip('/')
        self.headers = {
            'accept': 'application/json',
            'content-type': 'application/json'
        }

        # Для отладки
        logger.info(f"Initializing TronService with base URL: {self.base_url}")

    def _make_tron_request(self, endpoint: str, payload: dict):
        """Универсальный метод для запросов к Tron API"""
        full_url = urljoin(f"{self.base_url}/", endpoint)
        logger.info(f"Making request to: {full_url}")

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

    def get_address_info(self, payload: dict):
        """Получение информации об адресе"""
        try:
            # Получаем данные аккаунта
            account_data = self._make_tron_request("wallet/getaccount", payload)

            # Получаем баланс
            balance_data = self._make_tron_request("wallet/getaccountbalance", payload)

            return {
                "address": payload['address'],
                "bandwidth": account_data.get("free_net_limit", 0),
                "energy": account_data.get("energy_limit", 0),
                "balance": balance_data.get("balance", 0),
                "visible": payload.get('visible', True)
            }
        except Exception as e:
            logger.error(f"Failed to get address info: {str(e)}")
            raise


class DatabaseService:
    def create_address_request(self, db: Session, request: AddressRequestCreate) -> AddressRequestModel:
        db_request = AddressRequestModel(**request.dict())
        db.add(db_request)
        db.commit()
        db.refresh(db_request)
        return db_request

    def get_address_requests(self, db: Session, skip: int = 0, limit: int = 10) -> list[AddressRequestModel]:
        return db.query(AddressRequestModel) \
            .order_by(AddressRequestModel.created_at.desc()) \
            .offset(skip) \
            .limit(limit) \
            .all()

    def count_address_requests(self, db: Session) -> int:
        return db.query(AddressRequestModel).count()