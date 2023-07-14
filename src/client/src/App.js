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
      <nav className='App-header'>
        <ul>
          <li>
            <a href='/'>
              <h6>Amazon FBM Revenue Tracker</h6>
            </a>
          </li>
        </ul>
      </nav>
      {data ? (
        <div>
          <h3 className='App-link'>Total Sales: {data.total_sales}</h3>
          <h3 className='App-link'>Order Count: {data.order_count}</h3>
        </div>
      ) : (
        <p className='App'>Loading...</p>
      )}
      
      <div className='App-status'>
        <h2>Status</h2>
        <p className='App-link'>Last Updated: {data ? data.last_updated : 'N/A'}</p>
      </div>

    </div>
  );
}

export default App;
