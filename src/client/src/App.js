import { useState, useEffect } from 'react';
import './App.css';
import Login from './pages/auth/login'
import Register from './pages/auth/register'
import Home from './pages/Home'
import { AuthProvider } from './context/authContext'
import { useRoutes } from 'react-router-dom'
import NavBar from './components/NavBar'
// import axios from 'axios'
import { useAuth } from './context/authContext'
import { getDatabase, ref, get } from 'firebase/database'
import { app } from './firebase/firebase'

function App() {
	// const apiUrl = 'https://amazon-ecom-alarm.onrender.com'

	const { currentUser, userLoggedIn } = useAuth()
	const [data, setData] = useState(null)
	const [threshold, set_Threshold] = useState(null)
	const [temp_threshold, setTemp_threshold] = useState(
		localStorage.getItem('threshold') || 999.99
	)
	const [last_updated, setLast_updated] = useState('')

	// // Function to handle changes in the input field
	// const handleThresholdChange = (e) => {
	// 	setTemp_threshold(e.target.value)
	// }

	// // Function to handle the "Enter" key press
	// const handleKeyPress = (e) => {
	// 	if (e.key === 'Enter') {
	// 		// Update the value of the text box when "Enter" key is pressed
	// 		set_Threshold(e.target.value)
	// 	}
	// }

	// // Function to handle the button click
	// const handleClick = () => {
	// 	// Update the value of the text box when the button is clicked
	// 	set_Threshold(temp_threshold)
	// }

	// const handleEdit = () => {
	// 	// Update the value of the text box when the button is clicked
	// 	set_Threshold(null)
	// }

	// const updateFirebaseThreshold = (newThreshold) => {
	// 	// Make a POST request to the API
	// 	axios
	// 		.post(`${apiUrl}/set_firebase_data`, { threshold: newThreshold })
	// 		.then((response) => {
	// 			// Handle the response if needed
	// 			console.log('Threshold updated successfully')
	// 		})
	// 		.catch((error) => {
	// 			// Handle errors
	// 			console.error('Failed to update threshold:', error)
	// 		})
	// }

	const fetchData = () => {
		const db = getDatabase(app)
		const dbRef = ref(db, '/')

		get(dbRef)
			.then((snapshot) => {
				if (snapshot.exists()) {
					const rawData = snapshot.val()
					console.log('raw data', rawData)
					const formattedData = []

					Object.keys(rawData).forEach((key) => {
						const dataPoint = {
							date: rawData[key].date,
							fba_pending_sales: rawData[key].fba_pending_sales,
							fba_sales: rawData[key].fba_sales,
							fbm_pending_sales: rawData[key].fbm_pending_sales,
							fbm_sales: rawData[key].fbm_sales,
							shipped_order_count: rawData[key].shipped_order_count,
							order_pending_count: rawData[key].order_pending_count,
							total_order_count: rawData[key].total_order_count,
						}

						formattedData.push(dataPoint)
					})

					const last_row = rawData[Object.keys(rawData).pop()]
					setLast_updated(last_row.last_updated)

					console.log('formattedData_App.js: ', formattedData)
					setData(formattedData)
				} else {
					console.log('No data available')
				}
			})
			.catch((error) => {
				console.error('Failed to retrieve data:', error)
			})
	}

	useEffect(() => {
		if (userLoggedIn) {
			const db = getDatabase(app)
			const dbRef = ref(db, `data/${currentUser.uid}`)

			fetchData() // Initial fetch

			const interval = setInterval(fetchData, 300000) // Fetch every 5 minutes (adjust as needed)

			return () => clearInterval(interval) // Cleanup function to clear the interval
		} else {
			console.log('User is not authenticated')
		}
	}, [threshold, userLoggedIn])

	const routes = [
		{
			path: '*',
			element: <Login />,
		},
		{
			path: '/',
			element: <Login />,
		},
		{
			path: '/login',
			element: <Login />,
		},
		{
			path: '/home',
			element: (
				<Home data={data} last_updated={last_updated} threshold={threshold} />
			),
		},
		{
			path: '/register',
			element: <Register />,
		},
	]

	let routesElement = useRoutes(routes)

	return (
		<AuthProvider>
			<NavBar name={'Seller Metrics Monitor'} />
			<div className="w-full h-screen flex flex-col">{routesElement}</div>
		</AuthProvider>
	)
}

export default App