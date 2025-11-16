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

export default function RankingBoard() {
  const DEFAULT_YEAR = END
  const [year, setYear] = useState(DEFAULT_YEAR)
  const [items, setItems] = useState([])

  useEffect(() => {
    let ignore = false
    async function fetchRankings() {
      const yearsArr = Array.from({ length: END - START + 1 }, (_, i) => START + i)
      const perDirection = await Promise.all(
        SLUGS.map(async (slug) => {
          const url = `${GCS_BASE}/${encodeURIComponent(slug)}_${START}_${END}.json`
          const res = await fetch(url)
          const json = await res.json()
          const counts = yearsArr.map(y => json[y] || 0)
          const idx = Math.max(0, Math.min(yearsArr.length - 1, year - START))
          return { direction: slug, count: counts[idx] }
        })
      )
      const sorted = perDirection.sort((a, b) => b.count - a.count)
      if (!ignore) setItems(sorted)
    }
    fetchRankings()
    return () => { ignore = true }
  }, [year])

  const top = items.slice(0, 15)
  const dirs = top.map(d => d.direction)
  const counts = top.map(d => d.count)

  const option = {
    title: { text: `Top AI Directions in ${year || ''}` },
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'value' },
    yAxis: { type: 'category', data: dirs.slice().reverse() },
    series: [{ type: 'bar', data: counts.slice().reverse() }],
    grid: { left: 150, right: 20, top: 40, bottom: 40 }
  }

  return (
    <div className="card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h3 style={{ margin: 0 }}>Rankings</h3>
        <div>
          <label>Year: </label>
          <input type="number" value={year || ''} onChange={e => setYear(parseInt(e.target.value) || END)} />
        </div>
      </div>
      <ReactECharts option={option} style={{ height: 360 }} />
    </div>
  )
}
