// frontend/src/components/Dashboard.js
import React from 'react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const Dashboard = ({ invoices }) => {
    if (!invoices.length) return null;

    // Data for Delay Risk Ratio Pie Chart
    const overdueCount = invoices.filter(inv => inv.is_late_prediction === true).length;
    const onTimeCount = invoices.filter(inv => inv.is_late_prediction === false).length;
    const pieData = [
        { name: 'Predicted On-Time', value: onTimeCount },
        { name: 'Predicted Late', value: overdueCount },
    ];
    const COLORS = ['#0088FE', '#FF8042'];

    // Data for Top Vendors by Amount Bar Chart
    const vendorSpend = invoices.reduce((acc, inv) => {
        acc[inv.vendor] = (acc[inv.vendor] || 0) + inv.amount;
        return acc;
    }, {});

    const barData = Object.entries(vendorSpend)
        .sort(([, a], [, b]) => b - a)
        .slice(0, 5)
        .map(([name, value]) => ({ name: name.split(' ')[0], value: value.toFixed(2) }));

    return (
        <div>
            <h2>Dashboard</h2>
            <div style={{ display: 'flex', justifyContent: 'space-around', flexWrap: 'wrap', width: '100%' }}>
                <div style={{ width: '100%', maxWidth: '400px', marginBottom: '20px' }}>
                    <h3>Delay Risk Ratio</h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <PieChart>
                            <Pie data={pieData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={100} fill="#8884d8" label>
                                {pieData.map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                ))}
                            </Pie>
                            <Tooltip />
                            <Legend />
                        </PieChart>
                    </ResponsiveContainer>
                </div>
                <div style={{ width: '100%', maxWidth: '500px' }}>
                    <h3>Top 5 Vendors by Spend</h3>
                    <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={barData} margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
                            <XAxis dataKey="name" />
                            <YAxis />
                            <Tooltip />
                            <Legend />
                            <Bar dataKey="value" fill="#82ca9d" />
                        </BarChart>
                    </ResponsiveContainer>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;

