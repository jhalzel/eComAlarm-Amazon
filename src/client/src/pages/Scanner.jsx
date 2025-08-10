// import React, { useState } from 'react'
// import Papa from 'papaparse'
// import { AgGridReact } from 'ag-grid-react'
// import 'ag-grid-community/styles/ag-grid.css'
// import 'ag-grid-community/styles/ag-theme-alpine.css'

// function Scanner() {
// 	const [csvData, setCsvData] = useState([])
// 	const [columns, setColumns] = useState([])
// 	const [upcColumn, setUpcColumn] = useState('')
// 	const [costColumn, setCostColumn] = useState('')
// 	const [loading, setLoading] = useState(false)
// 	const [results, setResults] = useState(null)

// 	// Handle CSV upload and parse
// 	const handleFileUpload = (e) => {
// 		const file = e.target.files[0]
// 		Papa.parse(file, {
// 			header: true,
// 			skipEmptyLines: true,
// 			complete: (result) => {
// 				setCsvData(result.data)
// 				setColumns(Object.keys(result.data[0]))
// 			},
// 		})
// 	}

// 	// Handle form submit
// 	const handleSubmit = async (e) => {
// 		e.preventDefault()
// 		if (!upcColumn || !costColumn) return

// 		setLoading(true)
// 		// Extract UPCs and Costs
// 		const upcList = csvData.map((row) => String(row[upcColumn]).padStart(12, '0'))
// 		const costsList = csvData.map((row) => parseFloat(String(row[costColumn]).replace('$', '')))

// 		// Send to Flask endpoint
// 		const response = await fetch('/api/process_upc_batch', {
// 			method: 'POST',
// 			headers: { 'Content-Type': 'application/json' },
// 			body: JSON.stringify({ upc_list: upcList, costs_list: costsList }),
// 		})
// 		const data = await response.json()
// 		setResults(data)
// 		setLoading(false)
// 	}

// 	// Define column definitions based on your keys
// 	const columnDefs =
// 		results && results.length > 0
// 			? Object.keys(results[0]).map((key) => ({
// 					field: key,
// 					// Optional: use valueFormatter to handle null/NaN display here
// 					valueFormatter: (params) => {
// 						const val = params.value
// 						if (val === null || val === undefined || (typeof val === 'number' && isNaN(val))) {
// 							return 'N/A'
// 						}
// 						return val
// 					},
// 			  }))
// 			: []

// 	return (
// 		<div>
// 			<h2>Amazon Batch Processor</h2>
// 			<input type="file" accept=".csv" onChange={handleFileUpload} />
// 			{columns.length > 0 && (
// 				<form onSubmit={handleSubmit}>
// 					<label>
// 						UPC Column:
// 						<select value={upcColumn} onChange={(e) => setUpcColumn(e.target.value)}>
// 							<option value="">Select column</option>
// 							{columns.map((col) => (
// 								<option key={col} value={col}>
// 									{col}
// 								</option>
// 							))}
// 						</select>
// 					</label>
// 					<label>
// 						Cost Column:
// 						<select value={costColumn} onChange={(e) => setCostColumn(e.target.value)}>
// 							<option value="">Select column</option>
// 							{columns.map((col) => (
// 								<option key={col} value={col}>
// 									{col}
// 								</option>
// 							))}
// 						</select>
// 					</label>
// 					<button type="submit">Process Batch</button>
// 				</form>
// 			)}
// 			{results && results.length > 0 && (
// 				// <div>
// 				// 	<h3>Results</h3>
// 				// 	<table className="min-w-full border border-gray-300 rounded shadow">
// 				// 		<thead className="bg-gray-100">
// 				// 			<tr>
// 				// 				{Object.keys(results[0]).map((key) => (
// 				// 					<th key={key} className="px-2 py-1 border-b">
// 				// 						{key}
// 				// 					</th>
// 				// 				))}
// 				// 			</tr>
// 				// 		</thead>
// 				// 		<tbody>
// 				// 			{results.map((row, idx) => (
// 				// 				<tr key={idx} className="hover:bg-gray-50">
// 				// 					{Object.values(row).map((val, i) => {
// 				// 						let displayVal = val
// 				// 						if (
// 				// 							val === null ||
// 				// 							val === undefined ||
// 				// 							(typeof val === 'number' && isNaN(val))
// 				// 						) {
// 				// 							displayVal = 'N/A'
// 				// 						}
// 				// 						return (
// 				// 							<td key={i} className="px-2 py-1 border-b">
// 				// 								{displayVal}
// 				// 							</td>
// 				// 						)
// 				// 					})}
// 				// 				</tr>
// 				// 			))}
// 				// 		</tbody>
// 				// 	</table>
// 				// </div>

// 				<div className="ag-theme-alpine" style={{ height: 400, width: '100%', marginTop: 20 }}>
// 					<AgGridReact
// 						rowData={results}
// 						columnDefs={columnDefs}
// 						defaultColDef={{
// 							flex: 1,
// 							minWidth: 100,
// 							sortable: true,
// 							filter: true,
// 							resizable: true,
// 						}}
// 					/>
// 				</div>
// 			)}

// 			{loading && (
// 				<div className="flex justify-center items-center my-4">
// 					<div className="animate-spin rounded-full h-8 w-8 border-t-4 border-b-4 border-white-500"></div>
// 					<span className="ml-2 font-medium">Processing...</span>
// 				</div>
// 			)}
// 		</div>
// 	)
// }

// export default Scanner
