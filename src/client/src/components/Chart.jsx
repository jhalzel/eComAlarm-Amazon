import React, { useState, useEffect } from 'react'

import {
	BarChart,
	LineChart,
	Line,
	Bar,
	Area,
	AreaChart,
	CartesianGrid,
	XAxis,
	YAxis,
	Tooltip,
	Legend,
	ResponsiveContainer,
} from 'recharts'
import Badge from './Badge'
import '../App.css'

export const Chart = ({ threshold, selectedView, data }) => {
	// Initialize the Y-axis range state
	const [yMax, setYMax] = useState(500)

	const handleRangeChange = (e) => {
		setYMax(Number(e.target.value))
	}

	// const threshold = useSelector((state) => state.target.fbm_threshold)
	// const [json_data, setJson_data] = useState([])
	const [original_data, setOriginal_data] = useState([])
	const [selectedChart, setSelectedChart] = useState('Bar Chart (Orders)')

	const apiUrl = 'https://amazon-ecom-alarm.onrender.com'
	// const apiUrl = 'http://127.0.0.1:5000/';

	const handleChartChange = (event) => {
		const selectedValue = event.target.value
		console.log('Selected Chart:', selectedValue)
		setSelectedChart(selectedValue)
	}

	// Fetch the data from the API
	useEffect(() => {
		console.log(selectedView)
		console.log('data: ', data)
	}, [selectedView, data])

	return (
		<>
			<div className="flex justify-center p-4 py-8 shadow">
				<h3 className="flex self-center pr-4 font-semibold text-center px-4">
					Chart View:
				</h3>
				<select
					value={selectedChart}
					className="bg-custom-bg rounded-lg px-2 py-1 cursor-pointer"
					onChangeCapture={(e) => handleChartChange(e)}>
					<option value="default">Choose Chart</option>
					<option value="Line Chart (Sales)">Line Chart</option>
					<option value="Bar Chart (Orders)">Bar Chart</option>
					<option value="Area Chart (Sales)">Area Chart</option>
					{/* default to weekly */}
				</select>
			</div>

			<>
				<div className="mx-8 my-6">
					{(selectedChart === 'Area Chart (Sales)' && (
						<>
							<ResponsiveContainer width="100%" height={400}>
								<AreaChart
									data={data}
									width="100%"
									height={400}
									margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
									<CartesianGrid strokeDasharray="3 3" />
									<XAxis dataKey="date" />
									<YAxis />
									<Tooltip />
									<Legend />
									<Area
										type="monotone"
										dataKey="fbm_sales"
										stackId="1"
										stroke="#8884d8"
										fill="#8884d8"
									/>
									<Area
										type="monotone"
										dataKey="fba_sales"
										stackId="2"
										stroke="#82ca9d"
										fill="#82ca9d"
									/>
									<Area
										type="monotone"
										dataKey="fba_pending_sales"
										stackId="3"
										stroke="#ffc658"
										fill="#ffc658"
									/>
								</AreaChart>
							</ResponsiveContainer>
						</>
					)) ||
						(selectedChart === 'Line Chart (Sales)' && (
							<>
								<div className="relative flex justify-center">
									<div className="min-w-full">
										<ResponsiveContainer
											width="100%"
											height={400}
											className="my-6">
											<LineChart
												data={data}
												width="100%"
												height={400}
												margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
												<CartesianGrid strokeDasharray="3 3" />

												<XAxis
													dataKey="date"
													tick={{ fontSize: 12, fill: '#61dafb' }}
													tickFormatter={(value) => `${value}`}
												/>
												<YAxis
													// domain={[0, 'dataMax']}
													domain={[0, yMax]}
													tick={{ fontSize: 15, fill: '#61dafb' }}
													tickFormatter={(value) => `$${value}`}
												/>
												<Tooltip
													contentStyle={{ backgroundColor: '#282c34' }}
													formatter={(value, name) => [value, `${name}`]}
												/>
												<Legend />
												<Line
													type="monotone"
													dataKey="fbm_sales"
													stroke="#82ca9d"
												/>
												<Line
													type="monotone"
													dataKey="threshold"
													stroke="red"
													dot={false} // Remove dots if you don't want them on the threshold line
												/>
												<Line
													type="monotone"
													dataKey="fba_sales"
													stroke="#8884d8"
												/>
												<Line
													type="monotone"
													dataKey="fba_pending_sales"
													stroke="#065535"
												/>
											</LineChart>
										</ResponsiveContainer>
									</div>
									<div className="absolute top-36 -left-32 -ml-2 -rotate-90 text-center">
										{/* Slider to adjust yMax */}
										<Badge
											name={`Adjust Y-Axis Max: ${yMax}`}
											className="font-bold hover:bg-amber-100"
										/>
										<input
											type="range"
											min={100}
											max="1000"
											value={yMax}
											className="range range-xs "
											onChange={handleRangeChange}
										/>
									</div>
								</div>
							</>
						)) ||
						(selectedChart === 'Bar Chart (Orders)' && (
							<>
								{/* <h1 className="flex justify-center text-xl font-semibold">
									Order Count Chart
								</h1> */}
								<ResponsiveContainer width="100%" height={400}>
									<BarChart
										data={data}
										margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
										<XAxis
											dataKey="date"
											tick={{ fontSize: 12, fill: '#61dafb' }}
											tickFormatter={(value) => `${value}`}
										/>
										<YAxis tick={{ fontSize: 15, fill: '#61dafb' }} />
										<Tooltip
											contentStyle={{ backgroundColor: '#282c34' }}
											formatter={(value, name) => [value, `${name}`]}
										/>
										<Legend />
										<Bar
											dataKey="total_order_count"
											stackId="b"
											fill="#ffc658"
										/>
										<Bar
											dataKey="order_pending_count"
											stackId="b"
											fill="#ffe4e1"
										/>
										<Bar
											dataKey="shipped_order_count"
											stackId="b"
											fill="green"
										/>
									</BarChart>
								</ResponsiveContainer>
							</>
						)) ||
						(selectedChart === 'default' && (
							<div className="bg-custom-bg flex justify-center p-20 rounded-xl">
								<h2 className="text-2xl font-semibold ">
									Select a Chart View...
								</h2>
							</div>
						))}
				</div>
			</>
		</>
	)
}

export default Chart
