import React, { useEffect, useState } from 'react'
import ReactECharts from 'echarts-for-react'

export default function RankingBoard({ apiBase, latestYear }) {
  const [items, setItems] = useState([])
  const DEFAULT_YEAR = 2025
  const [year, setYear] = useState(DEFAULT_YEAR)

  useEffect(() => {
    if (latestYear && latestYear > DEFAULT_YEAR) {
      setYear(latestYear)
    } else {
      setYear(DEFAULT_YEAR)
    }
  }, [latestYear])

  useEffect(() => {
    let ignore = false
    async function fetchData() {
      if (!year) return
      const res = await fetch(`${apiBase}/api/rankings/${year}`)
      const data = await res.json()
      if (!ignore) setItems(data || [])
    }
    fetchData()
    return () => { ignore = true }
  }, [apiBase, year])

  const dirs = items.slice(0, 15).map(d => d.direction)
  const counts = items.slice(0, 15).map(d => d.count)

  const option = {
    title: { text: `Top AI Directions in ${year || ''}` },
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'value' },
    yAxis: { type: 'category', data: dirs.reverse() },
    series: [{ type: 'bar', data: counts.reverse() }],
    grid: { left: 150, right: 20, top: 40, bottom: 40 }
  }

  return (
    <div className="card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h3 style={{ margin: 0 }}>Rankings</h3>
        <div>
          <label>Year: </label>
          <input type="number" value={year || ''} onChange={e => setYear(parseInt(e.target.value) || latestYear)} />
        </div>
      </div>
      <ReactECharts option={option} style={{ height: 360 }} />
    </div>
  )
}
