import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BarChart,LineChart, Line, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import '../App.css'


export const Chart = () => {
    const [json_data, setJson_data] = useState([]);
    const [originalData, setOriginalData] = useState([]);

    const apiUrl = 'https://amazon-ecom-alarm.onrender.com';

    const filter_dates = (e, data) => {
        // Get current date
        const today = new Date();

        // Get the last 7 days
        const last7Days = new Date(today.getFullYear(), today.getMonth(), today.getDate() - 7);
        // Get the last 30 days
        const last30Days = new Date(today.getFullYear(), today.getMonth(), today.getDate() - 30);
        // Get the last 90 days
        const last90Days = new Date(today.getFullYear(), today.getMonth(), today.getDate() - 90);

        console.log('event: ', e.target.innerText);

         // Create a variable to store the filtered data
        let filteredData = [];

        console.log('data: ', data);
        // case and switch statement to filter data based on button clicked
        switch (e.target.value) {
            case 'Weekly View':
                console.log('Weekly View');
                // Filter data to only show the last 7 days
                filteredData = data.filter((item) => {
                    const itemDate = new Date(item.date);
                    return itemDate >= last7Days;
                });
                break;
            case 'Monthly View':
                console.log('Monthly View');
                // Filter data to only show the last 30 days
                filteredData = data.filter((item) => {
                    const itemDate = new Date(item.date);
                    return itemDate >= last30Days;
                });
                break;
            case '90 Day View':
                console.log('90 Day View');
                // Filter data to only show the last 90 days
                filteredData = data.filter((item) => {
                    const itemDate = new Date(item.date);
                    return itemDate >= last90Days;
                });
                break;
            default:
                console.log('default');
                // Filter data to only show the last 7 days
                filteredData = data.filter((item) => {
                    const itemDate = new Date(item.date);
                    return itemDate >= last7Days;
                });
        }
        
        console.log('filtered data: ', data);
        setJson_data(filteredData);
    };


    useEffect(() => {
        // Function to fetch the data from the API
        const fetchData = async () => {
            axios.get(`${apiUrl}/get_data`)
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
                        date: item.date
                    };

                    // Push the data point into the formattedData array
                    formattedData.push(dataPoint);
                });
                
                // Set both json_data and originalData
                setJson_data(formattedData);
                setOriginalData(formattedData);
                })
                .catch((err) => {
                    console.log(err);
                });  
            };
        
        fetchData(); // Initial fetch

    }, []);

    // useEffect(() => {
    //     // Function to fetch the data from the API
    //     const fetchData = async () => {
    //       try {
    //         const response = await axios.get(`${apiUrl}/get_data`);
            
    //         if (!response.data || !Array.isArray(response.data)) {
    //           throw new Error('Invalid data format received');
    //         }
      
    //         // Parse the JSON data
    //         const formattedData = response.data.forEach((item) => ({
    //           fba_sales: item.fba_sales[0],
    //           fbm_sales: item.fbm_sales[0],
    //           total_order_count: item.total_order_count[0],
    //           order_pending_count: item.order_pending_count[0],
    //           shipped_order_count: item.shipped_order_count[0],
    //           fba_pending_sales: item.fba_pending_sales[0],
    //           fbm_pending_sales: item.fbm_pending_sales[0],
    //           threshold: item.threshold[0],
    //           date: item.date,
    //         }));
      
    //         // Set both json_data and originalData
    //         setJson_data(formattedData);
    //         setOriginalData(formattedData);
      
    //         console.log("formattedData: ", formattedData);
    //       } catch (error) {
    //         console.error('Error:', error);
    //       }
    //     };
      
    //     fetchData(); // Initial fetch
      
    //     const interval = setInterval(fetchData, 60000); // Fetch every minute (adjust as needed)
      
    //     return () => clearInterval(interval); // Cleanup function to clear the interval
    //   }, []);
      

    return (
        <>
        <div className='options-section'>
        <h3>Chart View:</h3>
        <select className='chart-button' onChange={e => filter_dates(e, originalData)}>
            <option value="">Choose Range</option>
            <option value="Weekly View">Weekly View</option>
            <option value="Monthly View">Monthly View</option>
            <option value="90 Day View">90 Day View</option>
        </select>
        </div>
       
        
        <div className='chart-section'>
            <div className='chart-container'>
            <h1>Sales Data</h1>
            <ResponsiveContainer width="100%" height={300}>
                <LineChart data={json_data}>
                    {/* <CartesianGrid strokeDasharray="3 3" /> */}
                    <XAxis dataKey="date"  tick={{ fontSize: 12, fill:'#61dafb' }} tickFormatter={(value) => `${value}`} />
                    <YAxis tick={{ fontSize: 15, fill:'#61dafb' }} tickFormatter={(value) => `$${value}`} />
                    <Tooltip contentStyle={{ backgroundColor: '#282c34' }}/>
                    <Legend  />
                    <Line type="monotone" dataKey="fba_sales" stroke="#8884d8" />
                    <Line type="monotone" dataKey="fbm_sales" stroke="#82ca9d" />
                    <Line type="monotone" dataKey="fba_pending_sales" stroke="#065535" />
                    <Line type="monotone" dataKey="threshold" stroke="red" />
                </LineChart>
            </ResponsiveContainer>
            </div>
            
            <div className='chart-container'>
            <h1>Order Data</h1>
            <ResponsiveContainer width="100%" height={300}>
            <BarChart data={json_data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                {/* <CartesianGrid strokeDasharray="3 3" /> */}
                <XAxis dataKey="date" tick={{ fontSize: 12, fill:'#61dafb' }} tickFormatter={(value) => `${value}`} />
                <YAxis  tick={{ fontSize: 15, fill:'#61dafb' }} />
                <Tooltip contentStyle={{ backgroundColor: '#282c34' }} />
                <Legend />
                <Bar dataKey="total_order_count" stackId="b" fill="#ffc658" />
                <Bar dataKey="order_pending_count" stackId="b" fill="#ffe4e1" />
                <Bar dataKey="shipped_order_count" stackId="b" fill="green" />
            </BarChart>
            </ResponsiveContainer>
            {/* </div> */}
            </div>
        </div>
        </>
    );
};

export default Chart;
