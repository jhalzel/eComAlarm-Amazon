import { useEffect, useState } from 'react'
import Chart from './Chart'
import { filter_dates } from '../utils/actions'
import DateSlider from './DateSlider'

export default function Metrics({ data, threshold }) {
	const [filteredData, setFilteredData] = useState(0)
	const [summedData, setSummedData] = useState({})
	const [selectedView, setSelectedView] = useState('Custom Range') // default view

	const [daysBack, setDaysBack] = useState(234) // default to 30 days

	const handleSelectChange = (e) => {
		setSelectedView(e.target.value)
	}

	useEffect(() => {
		let result

		if (selectedView === 'Custom Range') {
			const today = new Date()
			const startDate = new Date(today)
			startDate.setDate(today.getDate() - daysBack)

			result = filter_dates('Custom Range', data, {
				start: startDate.toISOString().slice(0, 10),
				end: today.toISOString().slice(0, 10),
			})
		} else {
			result = filter_dates(selectedView, data)
		}

		setFilteredData(result.filteredData)
		setSummedData(result.summedData)
	}, [selectedView, daysBack, data])

	return (
		<>
			<div className="flex flex-col items-center py-2 shadow">
				<div className="flex items-center gap-4">
					<h3 className="font-semibold">Adjust Timeline:</h3>
					<select
						value={selectedView}
						className="bg-custom-bg rounded-lg px-2 py-1 cursor-pointer"
						onChange={handleSelectChange}>
						<option value="Custom Range">Custom Range</option>
						<option value="Year View">1 Year Sales History</option>
						<option value="2 Year View">2 Year Sales History</option>
					</select>

					{/* Slider below, only when Custom Range is selected */}
					{selectedView === 'Custom Range' && (
						<div className="mt-3 w-full max-w-md">
							<DateSlider
								daysBack={daysBack}
								onChange={(val) => {
									setDaysBack(val)
									setSelectedView('Custom Range')
								}}
							/>
						</div>
					)}
				</div>
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
