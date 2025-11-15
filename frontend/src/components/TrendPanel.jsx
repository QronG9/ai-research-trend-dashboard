import React, { useEffect, useState } from 'react'
import ReactECharts from 'echarts-for-react'

const CACHE_BASE = "https://qrong9.github.io/ai-research-trend-dashboard/cache/";

function normalize(name) {
  return name
    .toLowerCase()
    .replaceAll(" ", "_")
    .replaceAll("-", "_")
    .replaceAll("(", "")
    .replaceAll(")", "")
    .replaceAll("/", "_");
}

async function loadData(direction) {
  const key = normalize(direction);
  const url = `${CACHE_BASE}${key}_2010_2025.json`;
  console.log("Fetching static JSON:", url);
  const res = await fetch(url);
  if (!res.ok) throw new Error("Failed to load JSON: " + url);
  return await res.json();
}

export default function TrendPanel({ direction }) {
  const [years, setYears] = useState([])
  const [counts, setCounts] = useState([])

  useEffect(() => {
    let ignore = false
    async function run() {
      if (!direction) return
      try {
        const dict = await loadData(direction)
        const ys = Object.keys(dict).map(Number).sort((a,b)=>a-b)
        const cs = ys.map(y => Number(dict[String(y)] || 0))
        if (!ignore) {
          setYears(ys)
          setCounts(cs)
        }
      } catch (e) {
        console.error(e)
      }
    }
    run()
    return () => { ignore = true }
  }, [direction])

  const option = {
    title: { text: direction || 'Trend' },
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: years },
    yAxis: { type: 'value' },
    series: [{ type: 'line', data: counts, smooth: true, symbol: 'none' }],
    grid: { left: 50, right: 20, top: 40, bottom: 40 }
  }

  return (
    <div className="card">
      <ReactECharts option={option} style={{ height: 320 }} />
    </div>
  )
}
