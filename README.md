# AI Invoice Analyzer

Full-stack application that allows users to upload invoice data (CSVs), view the records, and get AI-driven insights.

## Tech Stack

* **Backend:** Python, FastAPI, SQLAlchemy, SQLite
* **Frontend:** React.js, Axios, Recharts
* **Machine Learning:** Scikit-learn, Pandas, Faker

## Features

* Upload invoices via CSV file.
* View all uploaded invoices in a clean table.
* Detect likely duplicate invoices upon upload.
* Predict the risk of a payment being late using a trained machine learning model.
* Dashboard with visualizations for "Delay Risk Ratio" and "Top Vendors by Spend".

## Setup and Installation

### Prerequisites

* Python 3.9+
* Node.js and npm
* Git

### Backend Setup

1.  `git clone https://github.com/Rodr1to/fs_invoice_analyzer_prototype`
2.  `cd invoice-analyzer/backend`
3.  virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
4.  backend server: `uvicorn main:app --reload`
    *(`http://localhost:8000`)*

### Frontend Setup

1.  `cd invoice-analyzer/frontend`
2.  `npm install`
3.  `npm start`
    *(`http://localhost:3000`)*

## How to Use

1.  Start both the backend and frontend servers.
2.  `python backend/ml/generate_data.py` from the root directory.
3.  web interface, select and upload the `sample_invoices.csv`.
4.  View the uploaded invoices and click "Predict Delay" on any invoice to get an AI-driven prediction.
