import React, { useEffect, useState } from 'react'
import ReactECharts from 'echarts-for-react'

export default function HeatmapPanel({ apiBase }) {
  const [years, setYears] = useState([])
  const [directions, setDirections] = useState([])
  const [matrix, setMatrix] = useState([])
  const [useLog, setUseLog] = useState(true)

  useEffect(() => {
    let ignore = false
    async function fetchData() {
      const res = await fetch(`${apiBase}/api/heatmap`)
      const data = await res.json()
      if (!ignore) {
        setYears(data.years || [])
        setDirections(data.directions || [])
        setMatrix(data.matrix || [])
      }
    }
    fetchData()
    return () => { ignore = true }
  }, [apiBase])

  const transformed = matrix.map(row => row.map(v => useLog ? Math.log1p(v) : v))
  const data = []
  for (let i = 0; i < years.length; i++) {
    for (let j = 0; j < directions.length; j++) {
      data.push([j, i, transformed[i]?.[j] ?? 0])
    }
  }

  const option = {
    title: { text: 'Heatmap' },
    tooltip: { position: 'top' },
    grid: { left: 100, bottom: 80, right: 20, top: 40 },
    xAxis: { type: 'category', data: directions, splitArea: { show: true }, axisLabel: { rotate: 40 } },
    yAxis: { type: 'category', data: years, splitArea: { show: true } },
    visualMap: {
      min: 0,
      max: Math.max(1, ...data.map(d => d[2])),
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: 10
    },
    series: [{
      name: useLog ? 'log1p(count)' : 'count',
      type: 'heatmap',
      data,
      label: { show: false },
      emphasis: { itemStyle: { shadowBlur: 5, shadowColor: 'rgba(0, 0, 0, 0.6)' } }
    }]
  }

  return (
    <div className="card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h3 style={{ margin: 0 }}>Heatmap</h3>
        <label><input type="checkbox" checked={useLog} onChange={e => setUseLog(e.target.checked)} /> log1p scale</label>
      </div>
      <ReactECharts option={option} style={{ height: 520 }} />
    </div>
  )
}
