import React, { useEffect, useMemo, useState } from 'react'
import ReactECharts from 'echarts-for-react'

// Simple in-memory cache to avoid redundant fetches in a session
const seriesCache = new Map()

const START = 2010
const END = 2025
const GCS_BASE = 'https://storage.googleapis.com/ai-trend-cache'

// Keep the list of direction slugs synchronized with the backend directions
// Fetching every JSON to list all slugs would be heavy; instead we embed names here if needed.
// Alternatively, host a small index file in the bucket.
const DIRECTION_SLUGS = [
  'natural_language_processing',
  'large_language_models_(llm)',
  'vision-language_models_(vlm)',
  'video_llm',
  'retrieval-augmented_generation_(rag)',
  'graph_neural_networks_(gnn)',
  'graph_representation_learning',
  'causal_machine_learning',
  'causal_inference',
  'reinforcement_learning',
  'deep_reinforcement_learning',
  'prompt_engineering',
  'instruction_tuning',
  'ai_alignment',
  'rlhf',
  'multimodal_learning',
  'few-shot_learning',
  'self-supervised_learning',
  'contrastive_learning',
  'federated_learning',
  'differential_privacy_in_ml',
  'knowledge_graphs',
  'graph_machine_learning',
  'automatic_speech_recognition',
  'machine_translation',
  'question_answering',
  'information_retrieval',
  'named_entity_recognition',
  'summarization',
  'data_augmentation',
  'domain_adaptation',
  'computer_vision',
  'multimodal_(general)'
]

export default function AllTrends() {
  const [directions, setDirections] = useState(DIRECTION_SLUGS)

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
        {directions.map((slug) => (
          <MiniTrend key={slug} slug={slug} />
        ))}
      </div>
    </div>
  )
}

function MiniTrend({ slug }) {
  const [data, setData] = useState(seriesCache.get(slug) || [])

  useEffect(() => {
    let ignore = false
    async function fetchData() {
      if (seriesCache.has(slug)) {
        setData(seriesCache.get(slug))
        return
      }
      const url = `${GCS_BASE}/${encodeURIComponent(slug)}_${START}_${END}.json`
      const res = await fetch(url)
      const json = await res.json()
      const arr = Object.keys(json)
        .map(y => parseInt(y, 10))
        .sort((a, b) => a - b)
        .map(y => ({ year: y, count: json[y] || 0 }))
      seriesCache.set(slug, arr)
      if (!ignore) setData(arr)
    }
    if (!data || data.length === 0) fetchData()
    return () => { ignore = true }
  }, [slug])

  const years = data.map(d => d.year)
  const counts = data.map(d => d.count)

  const title = slug.replaceAll('_', ' ')

  const option = useMemo(() => ({
    title: {
      text: title.length > 32 ? title.slice(0, 29) + '…' : title,
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
  }), [title, years, counts])

  return (
    <div className="mini-card">
      <ReactECharts option={option} style={{ height: 220 }} />
    </div>
  )
}
