import { useState, useEffect } from 'react';
import './App.css';
import Chart from './components/Chart'
import axios from 'axios';

function App() {
  const [data, setData] = useState(null);
  const [fbm_threshold, setFbm_threshold] = useState(localStorage.getItem('fbm_threshold') || 999.99);
  const [temp_threshold, setTemp_threshold] = useState(localStorage.getItem('fbm_threshold') || 999.99);
  const [last_updated, setLast_updated] = useState(null);

  const apiUrl = 'https://amazon-ecom-alarm.onrender.com';


// Function to Post the data to the API
const setThreshold = async (newThreshold) => {
  try {
    console.log(newThreshold)
    const response = await fetch(`${apiUrl}/set_threshold`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ fbm_threshold: newThreshold }),
    });

    if (response.ok) {
      console.log('Threshold updated successfully');
      localStorage.setItem('fbm_threshold', newThreshold);
    } else {
      console.error('Failed to update threshold. Response status:', response.status);
    }
  } catch (error) {
    console.error('Error:', error);
  }
};  


// Function to handle changes in the input field
 const handleThresholdChange = (e) => {
  setTemp_threshold(e.target.value);
  setThreshold(e.target.value);
};

// Function to handle the "Enter" key press
const handleKeyPress = (e) => {
  if (e.key === 'Enter') {
    // Update the value of the text box when "Enter" key is pressed
    setFbm_threshold(e.target.value);
    setThreshold(e.target.value)
  }
};


// Function to handle the button click
const handleClick = () => {
  // Update the value of the text box when the button is clicked
  setFbm_threshold(temp_threshold);
};

const handleEdit = () => {
  // Update the value of the text box when the button is clicked
  setFbm_threshold(null);
};

useEffect(() => {
  // Function to fetch the data from the API
  const fetchData = async () => {
      axios.get(`${apiUrl}/get_event`)
          .then((response) => {
              // Parse the JSON data
              const rawData = response.data
              console.log(rawData);
            
          
          setData(rawData);
          console.log('Threshold: ', data[0].threshold)
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
    <div className='App'>
      
      <header>
          <a href='/'>
            <h6>Amazon FBM Revenue Tracker</h6>
          </a>
      </header>
    
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
        data && data.fbm_sales > fbm_threshold ? (
          <>
          <div className="alert">
            <div className="alert-message" >FBM Sales have exceeded the threshold of <span style={{ color: 'rgb(255, 71, 47)' }}>${fbm_threshold}!</span> </div>
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
          <span className="App-link-values">${data.total_sales}</span>
        </div>
        <div className="data-box">
          <div>Total Order Count:</div>
          <span className="App-link-values">{data.total_order_count}</span>
        </div>
        <div className="data-box">
          <div>FBM Sales:</div>
          <span className="App-link-values">${data.fbm_sales}</span>
        </div>
        <div className="data-box">
          <div>FBA Sales:</div>
          <span className="App-link-values">${data.fba_sales}</span>
        </div>
        <div className="data-box">
          <div>FBA Pending Sales:</div>
          <span className="App-link-values">${data.fba_pending_sales}</span>
        </div>
        <div className="data-box">
          <div>FBM Pending Sales:</div>
          <span className="App-link-values">${data.fbm_pending_sales}</span>
        </div>
        <div className="data-box">
          <div>Orders Pending:</div>
          <span className="App-link-values">{data.order_pending_count}</span>
        </div>
        <div className="data-box">
          <div>Shipped Order Count:</div>
          <span className="App-link-values">{data.shipped_order_count}</span>
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
