// src/App.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import InvoiceUploadForm from './components/InvoiceUploadForm';
import InvoicesTable from './components/InvoicesTable';
import Dashboard from './components/Dashboard';
import './App.css';

function App() {
    const [invoices, setInvoices] = useState([]);
    const [isLoading, setIsLoading] = useState(true);

    const API_URL = 'http://localhost:8000';

    const fetchInvoices = async () => {
        setIsLoading(true);
        try {
            const response = await axios.get(`${API_URL}/invoices/`);
            setInvoices(response.data.sort((a, b) => b.id - a.id)); // Sort by most recent
        } catch (error) {
            console.error("Failed to fetch invoices:", error);
        } finally {
            setIsLoading(false);
        }
    };

    // Fetch initial data when the component loads
    useEffect(() => {
        fetchInvoices();
    }, []);

    const handleUploadSuccess = () => {
        fetchInvoices(); // Refresh the invoice list after a successful upload
    };

    const handlePredictDelay = async (invoiceId) => {
        try {
            await axios.post(`${API_URL}/invoices/${invoiceId}/predict-delay/`);
            fetchInvoices(); // Refresh to show the new prediction
        } catch (error) {
            console.error("Failed to get prediction:", error);
        }
    };

    return (
        <div className="App" style={{ fontFamily: 'sans-serif', padding: '20px', maxWidth: '1200px', margin: 'auto' }}>
            <header style={{ textAlign: 'center', marginBottom: '40px' }}>
                <h1>AI-Powered Invoice Analyzer</h1>
            </header>
            <main>
                <InvoiceUploadForm onUploadSuccess={handleUploadSuccess} />
                <hr style={{ margin: '30px 0' }} />
                {isLoading && invoices.length === 0 ? <p>Loading dashboard...</p> : <Dashboard invoices={invoices} />}
                <hr style={{ margin: '30px 0' }} />
                {isLoading ? <p>Loading invoices...</p> : <InvoicesTable invoices={invoices} onPredict={handlePredictDelay} />}
            </main>
        </div>
    );
}

export default App;
