import React, { useEffect, useState, useCallback } from 'react'
import RankingBoard from './components/RankingBoard.jsx'
import HeatmapPanel from './components/HeatmapPanel.jsx'
import RefreshButton from './components/RefreshButton.jsx'
import AllTrends from './pages/AllTrends.jsx'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export default function App() {
  const [latestYear, setLatestYear] = useState(null)
  const [refreshing, setRefreshing] = useState(false)
  const [activeTab, setActiveTab] = useState('rankings') // 'all' | 'heatmap' | 'rankings'
  const [notice, setNotice] = useState('')

  const fetchLatestYear = useCallback(async () => {
    const res = await fetch(`${API_BASE}/api/rankings/latest`)
    const data = await res.json()
    setLatestYear(data.latest_year || null)
  }, [])

  useEffect(() => {
    fetchLatestYear()
  }, [fetchLatestYear])

  const handleRefresh = async () => {
    setRefreshing(true)
    setNotice('Updating…')
    try {
      const res = await fetch(`${API_BASE}/api/refresh`, { method: 'POST' })
      const data = await res.json()
      console.log('Refresh result:', data)
      await fetchLatestYear()
      setNotice('Data updated from OpenAlex successfully')
      setTimeout(() => setNotice(''), 3000)
    } catch (e) {
      console.error('Refresh error', e)
      setNotice('Error updating data')
      setTimeout(() => setNotice(''), 3000)
    } finally {
      setRefreshing(false)
    }
  }

  return (
    <div className="container">
      <header className="header">
        <div>
          <h1>AI Research Trend Dashboard</h1>
          <p>2025 data reflects real-time OpenAlex updates</p>
        </div>
        <div>
          <RefreshButton onRefresh={handleRefresh} refreshing={refreshing} />
        </div>
      </header>

      {notice && <div className="card" style={{ marginBottom: 12 }}>{notice}</div>}

      <nav className="card" style={{ marginBottom: 12, paddingBottom: 12 }}>
        <button className="refresh" onClick={() => setActiveTab('all')} disabled={activeTab==='all'}>All Trends</button>
        <button className="refresh" onClick={() => setActiveTab('heatmap')} disabled={activeTab==='heatmap'} style={{ marginLeft: 8 }}>Heatmap</button>
        <button className="refresh" onClick={() => setActiveTab('rankings')} disabled={activeTab==='rankings'} style={{ marginLeft: 8 }}>Rankings</button>
      </nav>

      {activeTab === 'all' && (
        <>
          <RankingBoard apiBase={API_BASE} latestYear={latestYear} />
          <AllTrends apiBase={API_BASE} />
        </>
      )}

      {activeTab === 'heatmap' && (
        <HeatmapPanel apiBase={API_BASE} />
      )}

      {activeTab === 'rankings' && (
        <>
          <RankingBoard apiBase={API_BASE} latestYear={latestYear} />
          <AllTrends apiBase={API_BASE} />
        </>
      )}
    </div>
  )
}
