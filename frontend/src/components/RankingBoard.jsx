import React, { useEffect, useState } from 'react'
import ReactECharts from 'echarts-for-react'

export default function RankingBoard() {
  const [items, setItems] = useState([])
  const [year, setYear] = useState(null)
  const [years, setYears] = useState([])

  const RANK_URL = "https://qrong9.github.io/ai-research-trend-dashboard/data/ai_rankings.json"

  useEffect(() => {
    let ignore = false
    async function fetchAll() {
      const res = await fetch(RANK_URL)
      const data = await res.json()
      const ys = (data?.years || []).map(Number).sort((a,b)=>a-b)
      const latest = ys.length ? ys[ys.length-1] : null
      if (!ignore) {
        setYears(ys)
        setYear(latest)
        const selected = (data?.rankings || {})[String(latest)] || []
        setItems(selected)
      }
    }
    fetchAll()
    return () => { ignore = true }
  }, [])

  useEffect(() => {
    let ignore = false
    async function loadYear() {
      if (!year) return
      const res = await fetch(RANK_URL)
      const data = await res.json()
      const selected = (data?.rankings || {})[String(year)] || []
      if (!ignore) setItems(selected)
    }
    loadYear()
    return () => { ignore = true }
  }, [year])

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
          <select value={year || ''} onChange={e => setYear(parseInt(e.target.value))}>
            {years.map(y => (
              <option key={y} value={y}>{y}</option>
            ))}
          </select>
        </div>
      </div>
      <ReactECharts option={option} style={{ height: 360 }} />
    </div>
  )
}
