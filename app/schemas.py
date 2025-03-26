"""
Pydantic schemas for Tron Address Info API.

Defines request/response models and validation logic.
"""

from pydantic import BaseModel, validator
from typing import List
from datetime import datetime
import re


class TronApiRequest(BaseModel):
    """
    Request model for Tron address information.

    Attributes:
        address: Tron blockchain address (T... format)
        visible: Whether to include visibility info (default True)
    """
    address: str
    visible: bool = True

    @validator('address')
    def validate_address(cls, v):
        """Validate Tron address format."""
        if not re.match(r'^T[1-9A-HJ-NP-Za-km-z]{33}$', v):
            raise ValueError('Invalid Tron address format')
        return v


class AddressInfo(TronApiRequest):
    """Extended address information response model."""
    bandwidth: int
    energy: int
    balance: int


class AddressRequestCreate(BaseModel):
    """Model for creating address request records."""
    address: str
    bandwidth: int
    energy: int
    balance: int


class AddressRequestOut(AddressRequestCreate):
    """Output model for address requests with metadata."""
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class PaginatedAddressRequests(BaseModel):
    """Paginated list of address requests."""
    count: int
    items: List[AddressRequestOut]
    page: int
    pages: int