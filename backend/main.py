# backend/main.py
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import pandas as pd
import io
import pdfplumber
from datetime import datetime

from . import crud, models, schemas, predictor # Added predictor
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload-invoice/", response_model=list[schemas.Invoice])
async def upload_invoice(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    df = None
    if file.filename.endswith('.csv'):
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
    elif file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="PDF parsing is a bonus feature. Use CSV.")
    else:
        raise HTTPException(status_code=400, detail="Invalid file format.")

    df.columns = df.columns.str.lower().str.replace(' ', '_')
    created_invoices = []
    for _, row in df.iterrows():
        try:
            invoice_data = schemas.InvoiceCreate(
                invoice_id=str(row['invoice_id']), vendor=row['vendor'], amount=float(row['amount']),
                currency=row['currency'], invoice_date=datetime.strptime(row['invoice_date'], '%Y-%m-%d').date(),
                due_date=datetime.strptime(row['due_date'], '%Y-%m-%d').date()
            )
        except (KeyError, TypeError): continue
        if crud.get_invoice_by_invoice_id(db, invoice_id=invoice_data.invoice_id): continue

        is_duplicate = crud.check_for_duplicates(db, new_invoice=invoice_data)
        db_invoice = crud.create_invoice(db=db, invoice=invoice_data)
        db_invoice.duplicate_flag = is_duplicate
        db.commit()
        db.refresh(db_invoice)
        created_invoices.append(db_invoice)
    return created_invoices

@app.get("/invoices/", response_model=list[schemas.Invoice])
def read_invoices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_invoices(db, skip=skip, limit=limit)

# NEW ENDPOINT
@app.post("/invoices/{invoice_id}/predict-delay/", response_model=schemas.Invoice)
def predict_invoice_delay(invoice_id: int, db: Session = Depends(get_db)):
    db_invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if not db_invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    is_late = predictor.predict_delay(
        amount=db_invoice.amount, invoice_date=db_invoice.invoice_date,
        due_date=db_invoice.due_date, vendor=db_invoice.vendor
    )

    db_invoice.is_late_prediction = is_late
    db.commit()
    db.refresh(db_invoice)
    return db_invoice
