"""
Database models for Tron Address Info API.
"""

from sqlalchemy import Column, Integer, String, DateTime, BigInteger
from sqlalchemy.sql import func
from app.database import Base


class AddressRequest(Base):
    """
    Database model for storing address request information.

    Attributes:
        id: Primary key
        address: Tron blockchain address
        bandwidth: Address bandwidth
        energy: Address energy
        balance: TRX balance in sun
        created_at: Timestamp of record creation
    """
    __tablename__ = "address_requests"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True)
    bandwidth = Column(Integer)
    energy = Column(Integer)
    balance = Column(BigInteger)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<AddressRequest {self.address}>"