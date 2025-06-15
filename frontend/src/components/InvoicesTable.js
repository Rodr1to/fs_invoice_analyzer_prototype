// frontend/src/components/InvoicesTable.js
import React from 'react';

const InvoicesTable = ({ invoices, onPredict }) => {
    if (!invoices.length) {
        return <p>No invoices found. Upload a file to get started.</p>;
    }

    return (
        <div>
            <h2>Invoices</h2>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                <thead>
                    <tr style={{ borderBottom: '2px solid #333' }}>
                        <th style={{ padding: '8px' }}>Invoice ID</th>
                        <th style={{ padding: '8px' }}>Vendor</th>
                        <th style={{ padding: '8px' }}>Amount</th>
                        <th style={{ padding: '8px' }}>Due Date</th>
                        <th style={{ padding: '8px' }}>Duplicate?</th>
                        <th style={{ padding: '8px' }}>Late Risk?</th>
                        <th style={{ padding: '8px' }}>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {invoices.map((invoice) => (
                        <tr key={invoice.id} style={{ borderBottom: '1px solid #ccc' }}>
                            <td style={{ padding: '8px' }}>{invoice.invoice_id}</td>
                            <td style={{ padding: '8px' }}>{invoice.vendor}</td>
                            <td style={{ padding: '8px' }}>{invoice.amount.toFixed(2)} {invoice.currency}</td>
                            <td style={{ padding: '8px' }}>{invoice.due_date}</td>
                            <td style={{ padding: '8px' }}>{invoice.duplicate_flag ? '🚩 Yes' : 'No'}</td>
                            <td style={{ padding: '8px' }}>
                                {invoice.is_late_prediction === null
                                    ? 'N/A'
                                    : invoice.is_late_prediction
                                    ? '⚠️ High'
                                    : '✅ Low'}
                            </td>
                            <td style={{ padding: '8px' }}>
                                {invoice.is_late_prediction === null && (
                                    <button onClick={() => onPredict(invoice.id)}>Predict Delay</button>
                                )}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default InvoicesTable;
