import { useEffect, useState } from 'react'
import ChatPanel from './components/ChatPanel.jsx'
import GraphPanel from './components/GraphPanel.jsx'
import TracePanel from './components/TracePanel.jsx'
import EvalScorecard from './components/EvalScorecard.jsx'

export default function App() {
  const [health, setHealth] = useState(null)
  const [messages, setMessages] = useState([])
  const [sessionId, setSessionId] = useState(null)
  const [toolCalls, setToolCalls] = useState([])
  const [sending, setSending] = useState(false)
  const [error, setError] = useState(null)
  const [graphRefreshKey, setGraphRefreshKey] = useState(0)
  const [evalOpen, setEvalOpen] = useState(false)

  useEffect(() => {
    fetch('/api/health')
      .then((res) => {
        if (!res.ok) throw new Error(`GET /api/health failed: ${res.status} ${res.statusText}`)
        return res.json()
      })
      .then(setHealth)
      .catch((e) => setError(`Could not reach backend — is it running on :8000? (${e.message})`))
  }, [])

  async function handleSend(text) {
    const message = text.trim()
    if (!message || sending) return

    setMessages((prev) => [...prev, { role: 'user', content: message }])
    setSending(true)
    setError(null)
    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message, session_id: sessionId }),
      })
      if (!res.ok) throw new Error(`POST /api/chat failed: ${res.status} ${res.statusText}`)
      const data = await res.json()

      if (data.session_id) setSessionId(data.session_id)
      setToolCalls(Array.isArray(data.tool_calls) ? data.tool_calls : [])
      setMessages((prev) => [...prev, { role: 'assistant', content: data.reply ?? '' }])
      // Make the new memory layer(s) appear in the graph after each reply.
      setGraphRefreshKey((k) => k + 1)
    } catch (e) {
      setError(e.message || 'Chat request failed')
    } finally {
      setSending(false)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1 className="header-title">Road to Agent Memory — Acme Cloud SupportBot</h1>
        <button className="btn btn-eval" onClick={() => setEvalOpen(true)}>
          Run Eval
        </button>
      </header>

      {error && (
        <div className="error-banner" role="alert">
          <span>{error}</span>
          <button className="error-dismiss" onClick={() => setError(null)} aria-label="Dismiss">
            ×
          </button>
        </div>
      )}

      <main className="main">
        <section className="panel chat-panel-container">
          <ChatPanel
            messages={messages}
            onSend={handleSend}
            sending={sending}
            health={health}
          />
        </section>

        <div className="right-column">
          <section className="panel graph-panel-container">
            <GraphPanel refreshKey={graphRefreshKey} onError={setError} />
          </section>
          <section className="panel trace-panel-container">
            <TracePanel toolCalls={toolCalls} />
          </section>
        </div>
      </main>

      <EvalScorecard open={evalOpen} onClose={() => setEvalOpen(false)} onError={setError} />
    </div>
  )
}
