# backend/ml/trainer.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import os

def train_model():
    data_path = os.path.join('backend', 'ml', 'training_data.csv')
    model_path = os.path.join('backend', 'ml', 'delay_prediction_model.pkl')

    df = pd.read_csv(data_path, parse_dates=['invoice_date', 'due_date'])

    df['days_to_due'] = (df['due_date'] - df['invoice_date']).dt.days
    df['month_due'] = df['due_date'].dt.month
    df['vendor_category'] = df['vendor'].apply(lambda x: x.split(' ')[-1])

    features = ['amount', 'days_to_due', 'month_due', 'vendor_category']
    target = 'is_late'
    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    numeric_features = ['amount', 'days_to_due', 'month_due']
    categorical_features = ['vendor_category']

    preprocessor = ColumnTransformer(transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

    model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression(random_state=42, class_weight='balanced'))
    ])

    model_pipeline.fit(X_train, y_train)
    accuracy = model_pipeline.score(X_test, y_test)
    print(f"Model Accuracy: {accuracy:.4f}")

    joblib.dump(model_pipeline, model_path)
    print(f"Model saved to {model_path}")

if __name__ == '__main__':
    train_model()
