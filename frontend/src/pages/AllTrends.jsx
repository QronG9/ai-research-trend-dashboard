import React, { useEffect, useMemo, useState } from 'react'
import ReactECharts from 'echarts-for-react'

// Simple in-memory cache to avoid redundant fetches in a session
const seriesCache = new Map()

export default function AllTrends({ apiBase }) {
  const [directions, setDirections] = useState([])
  const [seriesMap, setSeriesMap] = useState({})

  useEffect(() => {
    let ignore = false
    async function fetchBulk() {
      // Prefer bulk endpoint to minimize requests
      const res = await fetch(`${apiBase}/api/all-directions`)
      const data = await res.json()
      if (ignore) return
      const dirs = data.directions || []
      setDirections(dirs)
      const ser = data.series || {}
      // Fill cache
      Object.entries(ser).forEach(([name, arr]) => {
        seriesCache.set(name, arr)
      })
      setSeriesMap(ser)
    }
    fetchBulk()
    return () => { ignore = true }
  }, [apiBase])

  const gridCols = 4

  return (
    <div className="card" style={{ paddingBottom: 12 }}>
      <h3 style={{ marginTop: 0 }}>All Trends</h3>
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: `repeat(${gridCols}, 1fr)`,
          gap: 12
        }}
      >
        {directions.map((name) => (
          <MiniTrend key={name} name={name} apiBase={apiBase} />
        ))}
      </div>
    </div>
  )
}

function MiniTrend({ name, apiBase }) {
  const [data, setData] = useState(seriesCache.get(name) || [])

  useEffect(() => {
    let ignore = false
    async function fetchData() {
      if (seriesCache.has(name)) {
        setData(seriesCache.get(name))
        return
      }
      const res = await fetch(`${apiBase}/api/direction/${encodeURIComponent(name)}`)
      const json = await res.json()
      const arr = (json.years || []).map((y, idx) => ({ year: y, count: (json.counts || [])[idx] || 0 }))
      seriesCache.set(name, arr)
      if (!ignore) setData(arr)
    }
    if (!data || data.length === 0) fetchData()
    return () => { ignore = true }
  }, [apiBase, name])

  const years = data.map(d => d.year)
  const counts = data.map(d => d.count)

  const option = useMemo(() => ({
    title: {
      text: name.length > 32 ? name.slice(0, 29) + '…' : name,
      left: 'center',
      top: 6,
      textStyle: { fontSize: 12 }
    },
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: years,
      axisLabel: {
        interval: function (index) { return index % 3 === 0 },
      }
    },
    yAxis: { type: 'value', splitLine: { show: true } },
    series: [{ type: 'line', data: counts, smooth: true, symbol: 'none' }],
    grid: { left: 40, right: 10, top: 30, bottom: 30 }
  }), [name, years, counts])

  return (
    <div className="mini-card">
      <ReactECharts option={option} style={{ height: 220 }} />
    </div>
  )
}
