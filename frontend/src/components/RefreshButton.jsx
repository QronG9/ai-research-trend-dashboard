import React from 'react'

export default function RefreshButton({ onRefresh, refreshing }) {
  return (
    <button className="refresh" onClick={onRefresh} disabled={refreshing}>
      {refreshing ? 'Refreshing…' : 'Refresh data from OpenAlex'}
    </button>
  )
}
