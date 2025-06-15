# backend/models.py
from sqlalchemy import Column, Integer, String, Float, Date, Boolean
from .database import Base

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(String, unique=True, index=True)
    vendor = Column(String, index=True)
    amount = Column(Float)
    currency = Column(String)
    invoice_date = Column(Date)
    due_date = Column(Date)
    status = Column(String, default="PENDING")
    is_late_prediction = Column(Boolean, nullable=True)
    duplicate_flag = Column(Boolean, default=False)
