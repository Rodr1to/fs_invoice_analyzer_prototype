# backend/predictor.py
import pandas as pd
import joblib
from datetime import date
import os

model_path = os.path.join('backend', 'ml', 'delay_prediction_model.pkl')
model = joblib.load(model_path)

def predict_delay(amount: float, invoice_date: date, due_date: date, vendor: str) -> bool:
    """Predicts if an invoice payment will be late."""
    days_to_due = (due_date - invoice_date).days
    month_due = due_date.month
    vendor_category = vendor.split(' ')[-1]

    input_data = pd.DataFrame([{'amount': amount, 'days_to_due': days_to_due, 'month_due': month_due, 'vendor_category': vendor_category}])

    prediction = model.predict(input_data)
    return bool(prediction[0])
