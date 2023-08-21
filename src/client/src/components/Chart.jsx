import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BarChart,LineChart, Line, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import '../App.css'


export const Chart = () => {
    const [json_data, setJson_data] = useState([]);

    useEffect(() => {
        axios.get('/get_json_data')
            .then((response) => {
                // Parse the JSON data
                const rawData = response.data.map(JSON.parse);
                console.log(rawData);
                // Initialize an empty array to store the formatted data
                const formattedData = [];

                // Loop through the rawData
                rawData.forEach(item => {
                // Create a new object for each data point
                const dataPoint = {
                    fba_sales: item.fba_sales[0],
                    fbm_sales: item.fbm_sales[0],
                    total_order_count: item.total_order_count[0],
                    order_pending_count: item.order_pending_count[0],
                    shipped_order_count: item.shipped_order_count[0],
                    fba_pending_sales: item.fba_pending_sales[0],
                    fbm_pending_sales: item.fbm_pending_sales[0],
                    threshold: item.threshold[0],
                };

                // Push the data point into the formattedData array
                formattedData.push(dataPoint);
            });
            
            console.log("formattedData: ", formattedData);
            setJson_data(formattedData);
            })
            .catch((err) => {
                console.log(err);
            });  
    }, []);


    return (
        <div className='chart-section'>
            <div className='chart-container'>
            <h1>Sales Data</h1>
            <ResponsiveContainer width="100%" height={300}>
                <LineChart data={json_data}>
                    {/* <CartesianGrid strokeDasharray="3 3" /> */}
                    <XAxis dataKey="name" />
                    <YAxis tick={{ fontSize: 17, fill:'#61dafb' }} tickFormatter={(value) => `$${value}`} />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="fba_sales" stroke="#8884d8" />
                    <Line type="monotone" dataKey="fbm_sales" stroke="#82ca9d" />
                    <Line type="monotone" dataKey="fba_pending_sales" stroke="#065535" />
                    <Line type="monotone" dataKey="threshold" stroke="maroon" />
                </LineChart>
            </ResponsiveContainer>
            </div>
            
            <div className='chart-container'>
            <h1>Order Data</h1>
            <ResponsiveContainer width="100%" height={300}>
            <BarChart data={json_data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                {/* <CartesianGrid strokeDasharray="3 3" /> */}
                <XAxis dataKey="name" />
                <YAxis  tick={{ fontSize: 17, fill:'#61dafb' }} />
                <Tooltip />
                <Legend />
                <Bar dataKey="total_order_count" stackId="b" fill="#ffc658" />
                <Bar dataKey="order_pending_count" stackId="b" fill="#ffe4e1" />
                <Bar dataKey="shipped_order_count" stackId="b" fill="green" />
            </BarChart>
            </ResponsiveContainer>
            {/* </div> */}
            </div>
        </div>
    );
};

export default Chart;
