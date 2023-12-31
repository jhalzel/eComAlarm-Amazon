import { useState, useEffect } from 'react';
import './App.css';
import Chart from './components/Chart'
import axios from 'axios';

function App() {
  const [data, setData] = useState(null);
  const [fbm_threshold, setFbm_threshold] = useState(localStorage.getItem('fbm_threshold') || 999.99);
  const [temp_threshold, setTemp_threshold] = useState(localStorage.getItem('fbm_threshold') || 999.99);
  const [last_updated, setLast_updated] = useState("");
  const [fbm_sales, setFbm_sales] = useState(null);

  const apiUrl = 'https://amazon-ecom-alarm.onrender.com';
  // const apiUrl = 'http://127.0.0.1:5000/';


const updateFirebaseThreshold = (newThreshold) => {
  axios.post(`${apiUrl}/set_firebase_data`, { fbm_threshold: newThreshold })
    .then((response) => {
      // Handle the response if needed
      console.log('Threshold updated successfully');
    })
    .catch((error) => {
      // Handle errors
      console.error('Failed to update threshold:', error);
    });
};

// Function to handle changes in the input field
 const handleThresholdChange = (e) => {
  setTemp_threshold(e.target.value);
};

// Function to handle the "Enter" key press
const handleKeyPress = (e) => {
  if (e.key === 'Enter') {
    // Update the value of the text box when "Enter" key is pressed
    console.log('temp_threshold: ', e.target.value);
    setFbm_threshold(e.target.value);
    console.log('fbm_threshold: ', fbm_threshold)
    updateFirebaseThreshold(e.target.value); // Call the function to update the Firebase database
    console.log('Enter key pressed');
    updateFirebaseThreshold(fbm_threshold);
  }
};

// Function to handle the button click
const handleClick = () => {
  // Update the value of the text box when the button is clicked
  setFbm_threshold(temp_threshold);
  updateFirebaseThreshold(temp_threshold); // Call the function to update the Firebase database
};

// Function to handle the 'edit' button click
const handleEdit = () => {
  // Update the value of the text box when the button is clicked
  setFbm_threshold(null);
};


const retrieveLastUpdated = () => {
  axios.get(`${apiUrl}/get_firebase_data`)
  .then((response) => {
    // Parse the Object  
    const keys = Object.keys(response.data);
    // Get the last key in the object
    const lastKey = keys[keys.length - 1];
    // Get the value of the last key in the object
    const lastValue = response.data[lastKey];
    // Get the last updated date's value
    const last_updated = lastValue.last_updated[0];
    // Set the last_updated state to the last updated value in the data
    setLast_updated(last_updated);
  })

  .catch((err) => {
      console.log(err);
  });  
}


useEffect(() => {
  // Function to fetch the data from the API
  const fetchData = async () => {
    // Check current threshold value
    if (fbm_threshold) {
      console.log('fbm_threshold: ', fbm_threshold);
    }
      // Make a GET request to the API
      axios.get(`${apiUrl}/get_firebase_data`)
          .then((response) => {
            // Parse the JSON data
            const rawData = response.data;
            
            // Initialize an empty array to store the formatted data
            const formattedData = [];

            var dataPoint = {};
            Object.keys(rawData).forEach(key => {
              // Create a new object for each data point
              dataPoint = rawData[key];
              // Print the data point to the console
              // console.log('dataPoint: ', dataPoint);
            });
            // Push the data point into the formattedData array
            formattedData.push(dataPoint);
            console.log("formattedData: ", formattedData);

            // Find the last entry in formattedData
            const lastEntry = formattedData[formattedData.length - 1];
            // Print the value in 'fbm_sales'[0]
            console.log("fbm_sales[0]: ", lastEntry.fbm_sales[0]);
            // Set the fbm_sales state to the value in 'fbm_sales'[0]
            setFbm_sales(lastEntry.fbm_sales[0]);

            setData(formattedData);
          })
        
        .catch((err) => {
          console.log(err);
        });  
      };

      
  // call function to retrieve last updated value
  retrieveLastUpdated();
  
  fetchData(); // Initial fetch

  const interval = setInterval(fetchData, 300000); // Fetch every 5 minutes (adjust as needed)

  updateFirebaseThreshold(fbm_threshold);
  localStorage.setItem('fbm_threshold', fbm_threshold);

  return () => clearInterval(interval); // Cleanup function to clear the interval
  // Call the function to update the Firebase database
}, [fbm_threshold]);


  return (
    <div className='App'>
      
      <header>
          <a href='/'>
            <h6>Amazon FBM Revenue Tracker</h6>
          </a>
      </header>

      <div>

        <p>Revenue data of the last 12 hour period on Amazon:</p>

      </div>

      <div>
        <h4 className='status-update'>Last Updated: {data ? last_updated : 'N/A'}</h4>
      </div>

      <div className="sales-container">
        {/* Input for FBM Sales Threshold */}
        {!fbm_threshold ? (
          <>
          <div className='Sales_threshold_title'>FBM Sales Threshold: {fbm_threshold} </div>
          <div  className='Sales_threshold1'>
          {/* Use the value prop to bind the input field to the state */}
          <input
            type="text"
            id="fbm_threshold"
            name="fbm_threshold"
            placeholder="FBM Sales Threshold"
            value={temp_threshold}
            onChange={handleThresholdChange}
            onKeyDown={handleKeyPress}
          />
            <button onClick={handleClick}>Update</button>
          </div>
          </>) : (
          <div className='Sales_threshold2'>
          <div className='Sales_threshold_title'>FBM Sales Threshold: {" "}
          <span className='fbm_threshold'>${fbm_threshold}</span><span><button onClick={handleEdit}>Set Threshold</button></span></div>
          </div>
        )
        }
      
      {
        data && fbm_sales > fbm_threshold ? (
          <>
          <div className="alert">
            <div style={{color:'red'}} className="alert-message" >FBM Sales have exceeded the threshold of <span style={{ color: 'rgb(255, 71, 47)' }}>${fbm_threshold}!</span> </div>
          </div>
          </>
        ) : (
          <>
          <div className="alert">
          <div className='alert-title'>FBM Alert:</div>
            <div className="alert-message">FBM Sales have not exceeded the threshold of <span style={{ color: 'greenyellow' }}>${fbm_threshold}</span> </div>
          </div>
          </>
        )
      }
      </div>
      
        
      {data ? (
      <div className="App-link">
        <div className="data-box">
          <div>Total Sales:</div>
          <span className="App-link-values">${data[0].total_sales}</span>
        </div>
        <div className="data-box">
          <div>Total Order Count:</div>
          <span className="App-link-values">{data[0].total_order_count}</span>
        </div>
        <div className="data-box">
          <div>FBM Sales:</div>
          <span className="App-link-values">${data[0].fbm_sales}</span>
        </div>
        <div className="data-box">
          <div>FBA Sales:</div>
          <span className="App-link-values">${data[0].fba_sales}</span>
        </div>
        <div className="data-box">
          <div>FBA Pending Sales:</div>
          <span className="App-link-values">${data[0].fba_pending_sales}</span>
        </div>
        <div className="data-box">
          <div>FBM Pending Sales:</div>
          <span className="App-link-values">${data[0].fbm_pending_sales}</span>
        </div>
        <div className="data-box">
          <div>Orders Pending:</div>
          <span className="App-link-values">{data[0].order_pending_count}</span>
        </div>
        <div className="data-box">
          <div>Shipped Order Count:</div>
          <span className="App-link-values">{data[0].shipped_order_count}</span>
        </div>
      </div>
    ) : (
      <p className="App">Loading...</p>
    )}
    
    <section>
      <div className="chart">
        <Chart threshold={fbm_threshold} />
      </div>
    </section>

  </div>
  );
}

export default App;
