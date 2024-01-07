import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BarChart,LineChart, Line, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import '../App.css'


export const Chart = ({threshold}) => {
    const [json_data, setJson_data] = useState([]);
    const [original_data, setOriginal_data] = useState([]);
    const [temp, setTemp] = useState([]);

    const apiUrl = 'https://amazon-ecom-alarm.onrender.com';
    // const apiUrl = 'http://127.0.0.1:5000/';


    const filter_dates = (e, data) => {
        console.log(e.target.value);
        // Set the selectedView state

        // Get current date
        const today = new Date();

        // Get the last 7 days
        const last7Days = new Date(today.getFullYear(), today.getMonth(), today.getDate() - 7);
        // Get the last 30 days
        const last30Days = new Date(today.getFullYear(), today.getMonth(), today.getDate() - 30);
        // Get the last 90 days
        const last90Days = new Date(today.getFullYear(), today.getMonth(), today.getDate() - 90);

        console.log("event-value: ", e.target.value);   

         // Create a variable to store the filtered data
        let filteredData = [];

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
                    return itemDate >= last90Days;
                });
        }
        
        console.log('filtered data: ', data);
        setJson_data(filteredData);
    };

    // Fetch the data from the API
    useEffect(() => {
        console.log('useEffect is running...');
        // Function to fetch the data from the API
        const fetchData = async () => {
            axios.get(`${apiUrl}/get_firebase_data`)
                .then((response) => {
                    console.log("response: ", response.data)
                    // Parse the JSON data
                    const rawData = response.data;
                    
                    console.log(rawData);
                    // Initialize an empty array to store the formatted data
                    const formattedData = [];

                    // Loop through the rawData
                    Object.keys(rawData).forEach((key) => {
                        const dataPoint = {
                            date: rawData[key].date,
                            fba_sales: [rawData[key].fba_sales],
                            fbm_sales: [rawData[key].fbm_sales],
                            fba_pending_sales: [rawData[key].fba_pending_sales],
                            total_order_count: [rawData[key].total_order_count],
                            order_pending_count: [rawData[key].order_pending_count],
                            shipped_order_count: [rawData[key].shipped_order_count],
                            threshold: [rawData[key].threshold]
                        };      

                        console.log('dataPoint: ', dataPoint)

                        // Push the data point into the formattedData array
                        formattedData.push(dataPoint);
                        console.log('formattedData: ', formattedData)
                    });

                // Set json_data
                setTemp(filter_dates({target: {value: 'Weekly View'}}, formattedData));
                setOriginal_data(formattedData);

                })
                .catch((err) => {
                    console.log(err);
                });  
            };
    
        fetchData(); // Initial fetch

        const interval = setInterval(fetchData, 300000); // Fetch every 5 minutes (adjust as needed)

        return () => clearInterval(interval); // Cleanup function to clear the interval

    }, []);



    return (
        <>
        <div className='options-section'>
        <h3>Chart View:</h3>
        <select className='chart-button' onChangeCapture={e => filter_dates(e, original_data)}>
            <option value="default" selected>Choose Range</option>
            <option value="Weekly View">Weekly View</option>
            <option value="Monthly View">Monthly View</option>
            <option value="90 Day View">90 Day View</option>
            {/* default to weekly */}
        </select>
        </div>
       
        
        <div className='chart-section'>
            <div className='chart-container'>
            <h1>Sales Data</h1>
            <ResponsiveContainer width="100%" height={300}>
                <LineChart data={json_data ? json_data : temp}> 
                    {/* <CartesianGrid strokeDasharray="3 3" /> */}
                    <XAxis dataKey="date"  tick={{ fontSize: 12, fill:'#61dafb' }} tickFormatter={(value) => `${value}`} />
                    <YAxis tick={{ fontSize: 15, fill:'#61dafb' }} tickFormatter={(value) => `$${value}`} />
                    <Tooltip contentStyle={{ backgroundColor: '#282c34' }} formatter={(value, name) => [value, `${name}`]}/>
                    <Legend />
      
                    <Line type="monotone"  dataKey="fba_sales" stroke="#8884d8" />
                    <Line type="monotone" dataKey="fbm_sales" stroke="#82ca9d" />
                    <Line type="monotone" dataKey="fba_pending_sales" stroke="#065535" />
                    <Line
                        type="monotone"
                        dataKey="threshold"
                        stroke="red"
                        dot={false} // Remove dots if you don't want them on the threshold line
                    />
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
                <Tooltip contentStyle={{ backgroundColor: '#282c34' }} formatter={(value, name) => [value, `${name}`]}/>
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
