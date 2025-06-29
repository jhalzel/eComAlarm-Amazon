export const filter_dates = (e, data) => {
	// Get current date
	const today = new Date('2024-09-01')

	// Get the last 7 days
	const last7Days = new Date(today.getFullYear(), today.getMonth(), today.getDate() - 7)
	// Get the last 30 days
	const last30Days = new Date(today.getFullYear(), today.getMonth(), today.getDate() - 30)
	// Get the last 90 days
	const last90Days = new Date(today.getFullYear(), today.getMonth(), today.getDate() - 90)
	// Get the last year days
	const last365Days = new Date(today.getFullYear(), today.getMonth(), today.getDate() - 365)
	// Get the last two years days
	// const last730Days = new Date(today.getFullYear(), today.getMonth(), today.getDate() - 730)

	// Create a variable to store the filtered data
	let filteredData = []

	// case and switch statement to filter data based on button clicked
	switch (e) {
		case 'Weekly View':
			console.log('Weekly View')
			filteredData = data.filter((item) => {
				const itemDate = new Date(item.date)
				return itemDate >= last7Days && itemDate <= today
			})
			break
		case 'Monthly View':
			console.log('Monthly View')
			filteredData = data.filter((item) => {
				const itemDate = new Date(item.date)
				return itemDate >= last30Days && itemDate <= today
			})
			break

		case '90 Day View':
			console.log('90 Day View')
			filteredData = data.filter((item) => {
				const itemDate = new Date(item.date)
				return itemDate >= last90Days && itemDate <= today
			})
			break

		case 'Year View':
			console.log('Year View')
			filteredData = data.filter((item) => {
				const itemDate = new Date(item.date)
				return itemDate >= last365Days && itemDate <= today
			})
			break

		default:
			console.log('default (Weekly View fallback)')
			filteredData = data.filter((item) => {
				const itemDate = new Date(item.date)
				return itemDate >= last7Days && itemDate <= today
			})
			break
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
