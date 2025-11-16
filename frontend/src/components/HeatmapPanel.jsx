import React, { useEffect, useState } from 'react'
import ReactECharts from 'echarts-for-react'

const START = 2010
const END = 2025
const GCS_BASE = 'https://storage.googleapis.com/ai-trend-cache'

const SLUGS = [
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

export default function HeatmapPanel() {
  const [years, setYears] = useState([])
  const [directions, setDirections] = useState([])
  const [matrix, setMatrix] = useState([])
  const [useLog, setUseLog] = useState(true)

  useEffect(() => {
    let ignore = false
    async function fetchAll() {
      const yearsArr = Array.from({ length: END - START + 1 }, (_, i) => START + i)
      const results = await Promise.all(
        SLUGS.map(async (slug) => {
          const url = `${GCS_BASE}/${encodeURIComponent(slug)}_${START}_${END}.json`
          const res = await fetch(url)
          const json = await res.json()
          return yearsArr.map(y => json[y] || 0)
        })
      )
      if (ignore) return
      setYears(yearsArr)
      setDirections(SLUGS)
      // transpose results to matrix[yearIndex][dirIndex]
      const matrixByYear = yearsArr.map((_, i) => SLUGS.map((_, j) => results[j][i]))
      setMatrix(matrixByYear)
    }
    fetchAll()
    return () => { ignore = true }
  }, [])

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
