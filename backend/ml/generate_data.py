# backend/ml/generate_data.py
import pandas as pd
from faker import Faker
from datetime import timedelta
import random
import os

fake = Faker()

def generate_sample_invoices(num_invoices=500):
    data = []
    for i in range(num_invoices):
        invoice_date = fake.date_between(start_date='-2y', end_date='today')
        due_date = invoice_date + timedelta(days=random.choice([15, 30, 45, 60]))
        amount = round(random.uniform(50.0, 5000.0), 2)

        paid_on_time = random.choices([True, False], weights=[0.75, 0.25])[0]
        if not paid_on_time and amount > 2000:
            paid_on_time = random.choices([True, False], weights=[0.4, 0.6])[0]

        payment_date = due_date - timedelta(days=random.randint(0, 5)) if paid_on_time else due_date + timedelta(days=random.randint(1, 40))
        is_late = payment_date > due_date

        data.append({
            'invoice_id': f'INV-{2023000 + i}', 'vendor': fake.company(), 'amount': amount,
            'currency': 'USD', 'invoice_date': invoice_date, 'due_date': due_date,
            'payment_date': payment_date, 'is_late': is_late
        })

    df = pd.DataFrame(data)

    # Save training data inside backend/ml
    training_path = os.path.join('backend', 'ml', 'training_data.csv')
    df.to_csv(training_path, index=False)
    print(f"Generated {training_path}")

    # Save upload-ready data in the project root
    upload_df = df[['invoice_id', 'vendor', 'amount', 'currency', 'invoice_date', 'due_date']]
    upload_path = 'sample_invoices.csv'
    upload_df.to_csv(upload_path, index=False)
    print(f"Generated {upload_path} (for upload)")

if __name__ == '__main__':
    generate_sample_invoices()
