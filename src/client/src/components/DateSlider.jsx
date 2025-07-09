import React from 'react'

function DateSlider({ daysBack, onChange }) {
	const maxDays = Math.floor((new Date() - new Date('2023-07-01')) / (1000 * 60 * 60 * 24))

	return (
		<div className="p-5">
			<label className="mb-1 block font-medium">Show data from the last {daysBack} days</label>
			<input
				type="range"
				min="1"
				max={maxDays}
				value={daysBack}
				onChange={(e) => onChange(Number(e.target.value))}
				className="range w-full"
			/>
		</div>
	)
}

export default DateSlider
