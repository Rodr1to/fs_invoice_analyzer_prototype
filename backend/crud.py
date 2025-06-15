# backend/crud.py
from sqlalchemy.orm import Session
from . import models, schemas
from thefuzz import fuzz

def get_invoice_by_invoice_id(db: Session, invoice_id: str):
    return db.query(models.Invoice).filter(models.Invoice.invoice_id == invoice_id).first()

def create_invoice(db: Session, invoice: schemas.InvoiceCreate):
    db_invoice = models.Invoice(**invoice.dict())
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

def get_invoices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Invoice).offset(skip).limit(limit).all()

def check_for_duplicates(db: Session, new_invoice: schemas.InvoiceCreate, threshold=85):
    """Checks for likely duplicates based on vendor, amount, and dates."""
    all_invoices = db.query(models.Invoice).all()
    for existing_invoice in all_invoices:
        # Check for same amount within a small tolerance
        amount_match = abs(existing_invoice.amount - new_invoice.amount) < 0.01 
        # Check for similar vendor name
        vendor_similarity = fuzz.ratio(existing_invoice.vendor.lower(), new_invoice.vendor.lower())

        if amount_match and vendor_similarity > threshold:
            return True # Found a likely duplicate
    return False
