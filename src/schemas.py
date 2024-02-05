from _decimal import Decimal
from typing import List

from pydantic import BaseModel


class AZSAllMainInfoModel(BaseModel):
    id: int
    tel_number: str
    coords: str
    address: str
    images: List[str]
    services: List[str]

    class Config:
        from_attributes = True


class FuelInfo(BaseModel):
    type: str
    price: Decimal
    currency: str

    class Config:
        from_attributes = True


class AZSFuelInfoModel(BaseModel):
    id: int
    fuels: List

    class Config:
        from_attributes = True
