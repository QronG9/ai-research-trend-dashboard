import React from 'react'

export default function DirectionSelector({ directions, selected, onChange }) {
  return (
    <div className="card">
      <label htmlFor="direction">Direction</label>
      <select id="direction" value={selected} onChange={e => onChange(e.target.value)}>
        {directions.map((d) => (
          <option key={d} value={d}>{d}</option>
        ))}
      </select>
    </div>
  )
}
