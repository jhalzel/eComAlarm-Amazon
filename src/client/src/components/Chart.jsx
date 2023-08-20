import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';



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
        <>
            <h1>Chart</h1>
            <BarChart width={600} height={400} data={json_data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="fba_sales" stackId="a" fill="#8884d8" />
                <Bar dataKey="fbm_sales" stackId="a" fill="#82ca9d" />
                
                <Bar dataKey="fba_pending_sales" stackId="c" fill="beige" />
                <Bar dataKey="fbm_pending_sales" stackId="c" fill="maroon" />
            </BarChart>
            {" "}
            <BarChart width={600} height={400} data={json_data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="total_order_count" stackId="b" fill="#ffc658" />
                <Bar dataKey="order_pending_count" stackId="b" fill="#3fwe8f" />
                <Bar dataKey="shipped_order_count" stackId="b" fill="green" />
            </BarChart>
        </>
    );
};

export default Chart;
