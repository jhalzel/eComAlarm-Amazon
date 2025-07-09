import { useEffect, useState } from 'react'
import Chart from './Chart'
import { filter_dates } from '../utils/actions'

export default function Metrics({ data, threshold }) {
	const [filteredData, setFilteredData] = useState(0)
	const [summedData, setSummedData] = useState({})
	const [selectedView, setSelectedView] = useState('Weekly View') // default view

	const handleSelectChange = (e) => {
		setSelectedView(e.target.value)
	}

	useEffect(() => {
		const { filteredData, summedData } = filter_dates(selectedView, data)
		setFilteredData(filteredData)
		setSummedData(summedData)
	}, [selectedView, data])

	return (
		<>
			<div className="flex justify-center py-2 shadow">
				<h3 className="flex self-center pr-4 font-semibold text-center px-4">Adjust Timeline:</h3>
				<select
					value={selectedView}
					className="bg-custom-bg rounded-lg px-2 py-1 cursor-pointer"
					onChange={handleSelectChange}>
					{/* <option value="">Choose Range</option> */}
					<option value="default">Weekly Sales</option>
					<option value="Monthly View">Monthly Sales</option>
					<option value="90 Day View">90 Day Sales</option>
					<option value="Year View">1 Year Sales History</option>
					<option value="2 Year View">2 Year Sales History</option>
				</select>
			</div>

			<div className="stats grid sm:grid-rows-4 md:grid-rows-2 lg:grid-rows-2 gap-2 shadow max-w-[100vw]">
				<div className="stat gap-1 text-center shadow max-w-100px">
					<div className="stat-title text-center">Total Sales</div>
					{/* <div className="stat-value">
						{Number(summedData['fba_sales']) + Number(summedData['fbm_sales'])}
					</div> */}
					<div className="stat-value">
						{(Number(summedData['fba_sales']) + Number(summedData['fbm_sales'])).toLocaleString(
							'en-US',
							{
								style: 'currency',
								currency: 'USD',
								minimumFractionDigits: 2,
							}
						)}
					</div>

					{/* <div className="stat-desc">21% more than last month</div> */}
				</div>

				<div className="stat gap-1 text-center shadow">
					<div className="stat-title text-center">Total Order Count</div>
					<div className="stat-value">{summedData.total_order_count}</div>
					{/* <div className="stat-desc">21% more than last month</div> */}
				</div>

				<div className="stat gap-1 text-center shadow">
					<div className="stat-title text-center">Merchant Fulfilled Sales</div>
					<div className="stat-value">
						{Number(summedData.fbm_sales).toLocaleString('en-US', {
							style: 'currency',
							currency: 'USD',
							minimumFractionDigits: 2,
						})}
					</div>

					{/* <div className="stat-desc">21% more than last month</div> */}
				</div>

				<div className="stat gap-1 text-center shadow">
					<div className="stat-title text-center">Amazon Fulfilled Sales</div>
					<div className="stat-value">
						{Number(summedData.fba_sales).toLocaleString('en-US', {
							style: 'currency',
							currency: 'USD',
							minimumFractionDigits: 2,
						})}
					</div>

					{/* <div className="stat-desc">21% more than last month</div> */}
				</div>

				<div className="stat gap-1 text-center shadow">
					<div className="stat-title text-center">FBA Pending Sales</div>
					<div className="stat-value">
						{Number(summedData['fba_pending_sales']).toLocaleString('en-US', {
							style: 'currency',
							currency: 'USD',
							minimumFractionDigits: 2,
						})}
					</div>

					{/* <div className="stat-desc">21% more than last month</div> */}
				</div>

				<div className="stat gap-1 text-center shadow">
					<div className="stat-title text-center">FBM Pending Sales</div>
					<div className="stat-value">
						{Number(summedData.fbm_pending_sales).toLocaleString('en-US', {
							style: 'currency',
							currency: 'USD',
							minimumFractionDigits: 2,
						})}
					</div>

					{/* <div className="stat-desc">21% more than last month</div> */}
				</div>

				<div className="stat gap-1 text-center shadow">
					<div className="stat-title text-center">Total Pending Sales</div>
					<div className="stat-value">{summedData.order_pending_count}</div>
					{/* <div className="stat-desc">21% more than last month</div> */}
				</div>

				<div className="stat gap-1 text-center shadow">
					<div className="stat-title text-center">Shipped Orders</div>
					<div className="stat-value">{summedData.shipped_order_count}</div>
					{/* <div className="stat-desc">21% more than last month</div> */}
				</div>
			</div>
			<Chart data={filteredData} threshold={threshold} selectedView={selectedView} />
		</>
	)
}
