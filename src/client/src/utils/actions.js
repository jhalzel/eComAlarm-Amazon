export const filter_dates = (e, data) => {
	// Get current date
	const today = new Date()

	// Get the last 7 days
	const last7Days = new Date(today.getFullYear(), today.getMonth(), today.getDate() - 7)
	// Get the last 30 days
	const last30Days = new Date(today.getFullYear(), today.getMonth(), today.getDate() - 30)
	// Get the last two years days
	const last90Days = new Date(today.getFullYear(), today.getMonth(), today.getDate() - 730)

	// Create a variable to store the filtered data
	let filteredData = []

	// case and switch statement to filter data based on button clicked
	switch (e) {
		case 'Weekly View':
			console.log('Weekly View')
			filteredData = data.filter((item) => new Date(item.date) >= last7Days)
			break
		case 'Monthly View':
			console.log('Monthly View')
			filteredData = data.filter((item) => new Date(item.date) >= last30Days)
			break
		case '90 Day View':
			console.log('90 Day View')
			// Filter data to only show the last 90 days
			filteredData = data.filter((item) => new Date(item.date) >= last90Days)
			break
		default:
			console.log('default')
			// Filter data to only show the last 7 days
			filteredData = data.filter((item) => new Date(item.date) >= last7Days)
	}

	const summedData = {
		fba_pending_sales: 0,
		fbm_pending_sales: 0,
		fba_sales: 0,
		fbm_sales: 0,
		order_pending_count: 0,
		shipped_order_count: 0,
		total_order_count: 0,
	}

	filteredData.forEach((i) => {
		summedData['fba_pending_sales'] += Number.parseInt(i['fba_pending_sales'][0])
		summedData['fba_sales'] += Number.parseInt(i['fba_sales'][0])
		summedData['fbm_sales'] += Number.parseInt(i['fbm_sales'][0])
		summedData['order_pending_count'] += Number.parseInt(i['order_pending_count'][0])
		summedData['shipped_order_count'] += Number.parseInt(i['shipped_order_count'][0])
		summedData['total_order_count'] += Number.parseInt(i['total_order_count'][0])
		summedData['fbm_pending_sales'] += Number.parseInt(i['fbm_pending_sales'][0])
	})

	// console.log('summedData: ', summedData)
	// setFilteredData(summedData)
	// console.log('filtered data (App.js): ', summedData)
	return { filteredData, summedData }
}
