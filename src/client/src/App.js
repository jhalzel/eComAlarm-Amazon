import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [data, setData] = useState(null);

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
      
        <div className='App-status'>
        <h2>Status</h2>
        <p className='App-link'>Last Updated: {data ? data.last_updated : 'N/A'}</p>
        </div>
        
      {data ? (        
        <div className='App-link'>
          <h7>Total FBM Sales: <br/> <span className='App-link-values'>{data.fbm_sales}</span></h7>
          <h7>Total FBA Sales: <br/>  <span className='App-link-values'>{data.fba_sales}</span></h7>
          <h7>Orders Pending: <br/> <span className='App-link-values'>{data.order_pending_count}</span> </h7>
          <h7>Order Count: <br/> <span className='App-link-values'>{data.order_count}</span></h7>
        </div>
      ) : (
        <p className='App'>Loading...</p>
      )}
      
    </div>
  );
}

export default App;
