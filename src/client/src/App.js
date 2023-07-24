import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [data, setData] = useState(null);
  const [fbm_threshold, setFbm_threshold] = useState(null);
  const [temp_threshold, setTemp_threshold] = useState(null);

 // Function to handle changes in the input field
 const handleThresholdChange = (e) => {
  setTemp_threshold(e.target.value);
};

// Function to handle the "Enter" key press
const handleKeyPress = (e) => {
  if (e.key === 'Enter') {
    // Update the value of the text box when "Enter" key is pressed
    setFbm_threshold(e.target.value);
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
  const fetchMembersData = async () => {
    try {
      const response = await fetch('/members'); // The API route URL
      const data = await response.json();
      setData(data);
    } catch (error) {
      console.log('Error:', error);
    }
  };

  fetchMembersData(); // Initial fetch

  const interval = setInterval(fetchMembersData, 60000); // Fetch every minute (adjust as needed)

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
        <h4 className='App-status'>Last Updated: {data ? data.last_updated : 'N/A'}</h4>
      </div>

      {/* Input for FBM Sales Threshold */}
      {!fbm_threshold ? (
        <>
        <h7 className='Sales_threshold_title'>FBM Sales Threshold: {" "}{fbm_threshold} {" "}</h7>
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
        <h7 className='Sales_threshold_title'>FBM Sales Threshold: {" "}
        <span className='fbm_threshold'>${fbm_threshold}</span> {" "}</h7>
        <button onClick={handleEdit}>Edit</button>
        </div>
      )}
       
      
        
        {data ? (
      <div className="App-link">
        <div className="data-box">
          <h7>Total Sales:</h7>
          <span className="App-link-values">${data.total_sales}</span>
        </div>
        <div className="data-box">
          <h7>FBM Sales:</h7>
          <span className="App-link-values">${data.fbm_sales}</span>
        </div>
        <div className="data-box">
          <h7>FBA Sales:</h7>
          <span className="App-link-values">${data.fba_sales}</span>
        </div>
        <div className="data-box">
          <h7>FBA Pending Sales:</h7>
          <span className="App-link-values">${data.fba_pending_sales}</span>
        </div>
        <div className="data-box">
          <h7>FBM Pending Sales:</h7>
          <span className="App-link-values">${data.fbm_pending_sales}</span>
        </div>
        <div className="data-box">
          <h7>Orders Pending:</h7>
          <span className="App-link-values">{data.order_pending_count}</span>
        </div>
        <div className="data-box">
          <h7>Total Order Count:</h7>
          <span className="App-link-values">{data.total_order_count}</span>
        </div>
        <div className="data-box">
          <h7>Shipped Order Count:</h7>
          <span className="App-link-values">{data.shipped_order_count}</span>
        </div>
      </div>
    ) : (
      <p className="App">Loading...</p>
    )}
  </div>
  );
}

export default App;
