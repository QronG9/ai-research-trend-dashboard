import React, { useEffect, useState } from 'react'
import ReactECharts from 'echarts-for-react'

const START = 2010
const END = 2025
const GCS_BASE = 'https://storage.googleapis.com/ai-trend-cache'

function slugify(name) {
  return name.toLowerCase().replaceAll(' ', '_').replaceAll('/', '_')
}

export default function TrendChart({ selectedDirection }) {
  const [years, setYears] = useState([])
  const [counts, setCounts] = useState([])

  useEffect(() => {
    let ignore = false
    async function fetchData() {
      if (!selectedDirection) return
      const slug = slugify(selectedDirection)
      const url = `${GCS_BASE}/${encodeURIComponent(slug)}_${START}_${END}.json`
      const res = await fetch(url)
      const json = await res.json()
      const ys = Object.keys(json).map(y => parseInt(y, 10)).sort((a,b)=>a-b)
      const cs = ys.map(y => json[y] || 0)
      if (!ignore) {
        setYears(ys)
        setCounts(cs)
      }
    }
    fetchData()
    return () => { ignore = true }
  }, [selectedDirection])

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
