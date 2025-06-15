# backend/schemas.py
from pydantic import BaseModel
from datetime import date
from typing import Optional

class InvoiceBase(BaseModel):
    invoice_id: str
    vendor: str
    amount: float
    currency: str
    invoice_date: date
    due_date: date

class InvoiceCreate(InvoiceBase):
    pass

class Invoice(InvoiceBase):
    id: int
    status: str
    is_late_prediction: Optional[bool]
    duplicate_flag: bool

    class Config:
        orm_mode = True # Allows Pydantic to read data from ORM models
