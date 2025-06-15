// frontend/src/components/InvoiceUploadForm.js
import React, { useState } from 'react';
import axios from 'axios';

const InvoiceUploadForm = ({ onUploadSuccess }) => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [isUploading, setIsUploading] = useState(false);
    const [error, setError] = useState('');

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
        setError(''); // Clear previous errors
    };

    const handleUpload = async () => {
        if (!selectedFile) {
            setError('Please select a file first.');
            return;
        }
        setIsUploading(true);
        setError('');
        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            // Post the file to the backend
            await axios.post('http://localhost:8000/upload-invoice/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            // Notify the parent component of success
            onUploadSuccess();
        } catch (err) {
            const errorMsg = err.response?.data?.detail || "Upload failed. Please use a valid CSV file.";
            setError(errorMsg);
            console.error(err);
        } finally {
            setIsUploading(false);
        }
    };

    return (
        <div style={{ border: '1px solid #ccc', padding: '20px', borderRadius: '8px' }}>
            <h2>Upload New Invoice File</h2>
            <input type="file" onChange={handleFileChange} accept=".csv" />
            <button onClick={handleUpload} disabled={isUploading} style={{ marginLeft: '10px' }}>
                {isUploading ? 'Uploading...' : 'Upload'}
            </button>
            {error && <p style={{ color: 'red', marginTop: '10px' }}>{error}</p>}
        </div>
    );
};

export default InvoiceUploadForm;
