import React, { useState } from 'react'
import RankingBoard from './components/RankingBoard.jsx'
import HeatmapPanel from './components/HeatmapPanel.jsx'
import RefreshButton from './components/RefreshButton.jsx'
import AllTrends from './pages/AllTrends.jsx'

const CLOUD_FUNCTION_URL = import.meta.env.VITE_CLOUD_FUNCTION_URL || ''

export default function App() {
  const [refreshing, setRefreshing] = useState(false)
  const [activeTab, setActiveTab] = useState('rankings') // 'all' | 'heatmap' | 'rankings'
  const [notice, setNotice] = useState('')

  const handleRefresh = async () => {
    if (!CLOUD_FUNCTION_URL) {
      setNotice('Cloud Function URL not configured')
      setTimeout(() => setNotice(''), 3000)
      return
    }
    setRefreshing(true)
    setNotice('Updating…')
    try {
      const res = await fetch(CLOUD_FUNCTION_URL, { method: 'POST' })
      const data = await res.json().catch(() => ({}))
      console.log('Refresh result:', data)
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
          <p>2010–2025 counts from OpenAlex (cached in GCS)</p>
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
          <RankingBoard />
          <AllTrends />
        </>
      )}

      {activeTab === 'heatmap' && (
        <HeatmapPanel />
      )}

      {activeTab === 'rankings' && (
        <>
          <RankingBoard />
          <AllTrends />
        </>
      )}
    </div>
  )
}
