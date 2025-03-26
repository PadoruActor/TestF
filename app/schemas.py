# app/schemas.py
from pydantic import BaseModel, validator
from typing import List
from datetime import datetime
import re

class TronApiRequest(BaseModel):
    address: str
    visible: bool = True

    @validator('address')
    def validate_address(cls, v):
        if not re.match(r'^T[1-9A-HJ-NP-Za-km-z]{33}$', v):
            raise ValueError('Invalid Tron address format')
        return v

class AddressInfo(TronApiRequest):
    bandwidth: int
    energy: int
    balance: int

class AddressRequestCreate(BaseModel):
    address: str
    bandwidth: int
    energy: int
    balance: int

class AddressRequestOut(AddressRequestCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class PaginatedAddressRequests(BaseModel):
    count: int
    items: List[AddressRequestOut]
    page: int
    pages: int