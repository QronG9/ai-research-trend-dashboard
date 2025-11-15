import React, { useEffect, useState } from 'react'
import ReactECharts from 'echarts-for-react'

export default function TrendChart({ apiBase, selectedDirection }) {
  const [years, setYears] = useState([])
  const [counts, setCounts] = useState([])

  useEffect(() => {
    let ignore = false
    async function fetchData() {
      if (!selectedDirection) return
      const res = await fetch(`${apiBase}/api/direction/${encodeURIComponent(selectedDirection)}`)
      const data = await res.json()
      if (!ignore) {
        setYears(data.years || [])
        setCounts(data.counts || [])
      }
    }
    fetchData()
    return () => { ignore = true }
  }, [apiBase, selectedDirection])

  const option = {
    title: { text: selectedDirection || 'Trend' },
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: years },
    yAxis: { type: 'value', name: 'Count' },
    series: [{ type: 'line', smooth: true, data: counts }],
    grid: { left: 50, right: 20, top: 40, bottom: 40 }
  }

  return (
    <div className="card">
      <ReactECharts option={option} style={{ height: 320 }} />
    </div>
  )
}
