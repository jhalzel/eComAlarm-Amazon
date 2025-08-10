import React, { useState, useEffect } from 'react'
import Papa from 'papaparse'
import { AgGridReact } from 'ag-grid-react'
import { useTheme } from '../context/themeContext'

// import 'ag-grid-community/styles/ag-grid.css'
// import 'ag-grid-community/styles/ag-theme-alpine.css'

import { colorSchemeDark } from 'ag-grid-community'

import {
	AllCommunityModule,
	ModuleRegistry,
	colorSchemeDarkBlue,
	colorSchemeDarkWarm,
	colorSchemeLightCold,
	colorSchemeLightWarm,
	themeQuartz,
} from 'ag-grid-community'

ModuleRegistry.registerModules([AllCommunityModule])

// const themeLightWarm = themeQuartz.withPart(colorSchemeLightWarm)
// const themeDarkWarm = themeQuartz.withPart(colorSchemeDarkWarm)
const themeLightCold = themeQuartz.withPart(colorSchemeLightCold)
const themeDarkBlue = themeQuartz.withPart(colorSchemeDarkBlue)

const myTheme = themeQuartz.withPart(colorSchemeDark)

function Scanner2() {
	const [csvData, setCsvData] = useState([])
	const [columns, setColumns] = useState([])
	const [upcColumn, setUpcColumn] = useState('')
	const [costColumn, setCostColumn] = useState('')
	const [loading, setLoading] = useState(false)
	const [results, setResults] = useState(null)
	const { isdark } = useTheme()

	const tableTheme = isdark ? themeDarkBlue : themeLightCold

	// Column defs state for AgGrid, starts empty
	const [columnDefs, setColumnDefs] = useState([])

	// Handle CSV upload and parse
	const handleFileUpload = (e) => {
		const file = e.target.files[0]
		Papa.parse(file, {
			header: true,
			skipEmptyLines: true,
			complete: (result) => {
				setCsvData(result.data)
				setColumns(Object.keys(result.data[0]))
			},
		})
	}

	// Handle form submit
	const handleSubmit = async (e) => {
		e.preventDefault()
		if (!upcColumn || !costColumn) return

		setLoading(true)
		// Extract UPCs and Costs
		const upcList = csvData.map((row) => String(row[upcColumn]).padStart(12, '0'))
		const costsList = csvData.map((row) => parseFloat(String(row[costColumn]).replace('$', '')))

		// Send to Flask endpoint
		const response = await fetch('https://amazon-ecom-alarm.onrender.com/api/process_upc_batch', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ upc_list: upcList, costs_list: costsList }),
		})
		const data = await response.json()
		setResults(data)

		// Define columnDefs explicitly here based on expected keys (example below)
		setColumnDefs([
			{ field: 'UPC' },
			{ field: 'ASIN' },
			{ field: 'Item Name' },
			{
				field: 'Cost',
				valueFormatter: (params) => {
					const val = Number(params.value)
					if (!isNaN(val)) {
						return `$${val.toFixed(2)}`
					}
					return 'N/A'
				},
			},
			{ field: 'Manufacturer' },
			{ field: 'Sales Rank' },
			{
				field: 'Listing Price',
				valueFormatter: (params) => {
					const val = Number(params.value)
					if (!isNaN(val)) {
						return `$${val.toFixed(2)}`
					}
					return 'N/A'
				},
			},
			{ field: 'New Offer Count' },
			{
				field: 'FBA Fees',
				valueFormatter: (params) => {
					const val = Number(params.value)
					if (!isNaN(val)) {
						return `$${val.toFixed(2)}`
					}
					return 'N/A'
				},
			},
			{
				field: 'FBM Fees',
				valueFormatter: (params) => {
					const val = Number(params.value)
					if (!isNaN(val)) {
						return `$${val.toFixed(2)}`
					}
					return 'N/A'
				},
			},
			{
				field: 'Total Costs',
				valueFormatter: (params) => {
					const val = Number(params.value)
					if (!isNaN(val)) {
						return `$${val.toFixed(2)}`
					}
					return 'N/A'
				},
			},
			{
				field: 'Net Profit',
				valueFormatter: (params) => {
					const val = Number(params.value)
					if (!isNaN(val)) {
						return `$${val.toFixed(2)}`
					}
					return 'N/A'
				},
			},
			{ field: 'ROI (%)' },
		])

		setLoading(false)
	}

	return (
		<div>
			<div className="max-w-3xl mx-auto p-4">
				<h2 className="text-3xl font-bold text-center mb-6">Amazon Batch Processor</h2>

				<div className="mb-4 flex flex-col items-center">
					<label
						htmlFor="file-upload"
						className="bg-custom-bg cursor-pointer px-6 py-3 text-white rounded shadow hover:bg-gray-700 transition">
						Choose CSV File
					</label>
					<input
						id="file-upload"
						type="file"
						accept=".csv"
						onChange={handleFileUpload}
						className="hidden"
					/>
					{csvData.length > 0 && (
						<p className="mt-2 text-gray-600">File loaded: {csvData.length} rows</p>
					)}
				</div>

				{columns.length > 0 && (
					<form onSubmit={handleSubmit} className="flex gap-6 justify-center mb-6 flex-wrap">
						<label className="flex flex-col text-sm font-semibold">
							UPC Column:
							<select
								value={upcColumn}
								onChange={(e) => setUpcColumn(e.target.value)}
								className="mt-1 p-2 border rounded-md w-48"
								required>
								<option value="" disabled>
									Select UPC Column
								</option>
								{columns.map((col) => (
									<option key={col} value={col}>
										{col}
									</option>
								))}
							</select>
						</label>

						<label className="flex flex-col text-sm font-semibold">
							Cost Column:
							<select
								value={costColumn}
								onChange={(e) => setCostColumn(e.target.value)}
								className="mt-1 p-2 border rounded-md w-48"
								required>
								<option value="" disabled>
									Select Cost Column
								</option>
								{columns.map((col) => (
									<option key={col} value={col}>
										{col}
									</option>
								))}
							</select>
						</label>

						<div className="flex items-end justify-end gap-4">
							<button
								type="submit"
								className="bg-orange-400 hover:bg-amber-400 text-white font-semibold px-6 py-2 rounded shadow transition">
								Process Batch
							</button>
							<div className="flex flex-row items-start gap-3 mb-2">
								{loading && (
									<div className="flex items-center">
										<div className="animate-spin rounded-full h-6 w-6 border-t-4 border-b-4 border-black-500"></div>
										<span className="ml-2 font-medium">Processing...</span>
									</div>
								)}
							</div>
						</div>
					</form>
				)}

				{/* AgGrid and Loading remains unchanged */}
			</div>

			{results && results.length > 0 && (
				<div className={`ag-theme-alpine`} style={{ height: '90vh', width: '100%' }}>
					<AgGridReact
						theme={tableTheme}
						rowData={results}
						columnDefs={columnDefs}
						defaultColDef={{ sortable: true, filter: true, resizable: true }}
					/>
				</div>
			)}
		</div>
	)
}

export default Scanner2
