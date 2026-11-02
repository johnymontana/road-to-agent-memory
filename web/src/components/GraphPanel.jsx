import { useEffect, useMemo, useRef, useState } from 'react'
import { InteractiveNvlWrapper } from '@neo4j-nvl/react'
import { colorForLabels, LAYER_LABELS } from '../palette.js'

const caption = n => String(n.properties?.name || n.properties?.preference || n.properties?.content || n.properties?.task || n.labels?.[0] || n.id).slice(0, 55)

export default function GraphPanel({ refreshKey, onError, ready, module, sessionId }) {
  const [layer, setLayer] = useState('all')
  const [scope, setScope] = useState('current')
  const [graph, setGraph] = useState({ nodes: [], relationships: [] })
  const [runs, setRuns] = useState([])
  const [snapshotInfo, setSnapshotInfo] = useState(null)
  const [loading, setLoading] = useState(false)
  const [selectedId, setSelectedId] = useState(null)
  const [localError, setLocalError] = useState(null)
  const [reload, setReload] = useState(0)
  const [nams, setNams] = useState(false)
  const nvl = useRef(null)

  useEffect(() => {
    if (!ready) return
    let cancelled = false
    fetch('/api/replays').then(r => r.json()).then(d => { if (!cancelled) setRuns(d.runs ?? []) }).catch(() => {})
    return () => { cancelled = true }
  }, [ready, refreshKey, reload])

  useEffect(() => {
    if (!ready) return
    let cancelled = false
    setLoading(true); setLocalError(null)
    const activeSession = scope.startsWith('session:') ? scope.slice(8) : scope === 'current' ? sessionId : null
    const url = nams ? '/api/graph/nams' : scope.startsWith('replay:')
      ? `/api/replays/${encodeURIComponent(scope.slice(7))}`
      : `/api/graph?layer=${layer}${activeSession ? `&session_id=${encodeURIComponent(activeSession)}` : ''}`
    fetch(url).then(r => { if (!r.ok) throw new Error(`Graph request failed (HTTP ${r.status})`); return r.json() })
      .then(data => { if (!cancelled) { setGraph(data.graph ?? data); setSnapshotInfo(data.graph ? data : null); setSelectedId(null) } })
      .catch(e => { if (!cancelled) { setLocalError(e.message); onError?.(e.message) } })
      .finally(() => { if (!cancelled) setLoading(false) })
    return () => { cancelled = true }
  }, [ready, layer, scope, sessionId, refreshKey, reload, nams, onError])

  const nodes = useMemo(() => (graph.nodes ?? []).map(n => ({ id: String(n.id), caption: caption(n), color: colorForLabels(n.labels).fill, size: 32, captionSize: 2 })), [graph])
  const rels = useMemo(() => (graph.relationships ?? []).map(r => ({ id: String(r.id), from: String(r.from), to: String(r.to), caption: r.type })), [graph])
  const selected = graph.nodes?.find(n => String(n.id) === selectedId)
  const selectNode = node => { setSelectedId(String(node.id)); nvl.current?.fit?.([String(node.id)]) }

  return <div className="graph-panel"><div className="panel-header"><span className="panel-title">Memory graph</span><div className="graph-controls">
    <label className="sr-only" htmlFor="graph-view">Graph view</label><select id="graph-view" aria-label="Graph view" value={scope} onChange={e => setScope(e.target.value)}>
      <option value="current">Current conversation</option><option value="all">All stored memory</option>{runs.map(r => <option key={r.id} value={`replay:${r.id}`}>Saved replay · {r.title}</option>)}
      {runs.filter(r => r.module > 1).flatMap(r => (r.session_ids ?? []).map(id => <option key={`${r.id}-${id}`} value={`session:${id}`}>Live memory · {r.title} · {id.slice(-12)}</option>))}
    </select>
    <select aria-label="Memory layer" value={layer} disabled={scope.startsWith('replay:') || nams} onChange={e => setLayer(e.target.value)}>{['all', 'short_term', 'long_term', 'reasoning'].map(l => <option key={l} value={l}>{l.replace('_', ' ')}</option>)}</select>
    <button className="btn" onClick={() => setReload(k => k + 1)}>Refresh graph</button>
    <button className="btn" disabled={!nodes.length} onClick={() => nvl.current?.fit(nodes.map(n => n.id))}>Fit graph</button>
    {module === 5 && <label><input type="checkbox" checked={nams} onChange={e => setNams(e.target.checked)} /> NAMS</label>}
  </div></div>
  <div className="graph-canvas">
    {graph.truncated && <p className="graph-notice">Showing the newest bounded subset. Choose a conversation or replay for a complete lesson view.</p>}
    {scope.startsWith('replay:') && <p className="graph-notice">Recorded replay output · {runs.find(r => scope === `replay:${r.id}`)?.title}. {snapshotInfo?.protocol} This is a saved projection; choose Live memory for persisted message/entity/trace links.</p>}
    {scope.startsWith('session:') && <p className="graph-notice">Live stored memory · {scope.slice(8)}</p>}
    {loading && <div className="graph-loading" role="status">Loading graph…</div>}
    {localError ? <div className="graph-empty">{localError}. Retry with Refresh graph.</div> : nodes.length ? <InteractiveNvlWrapper ref={nvl} nodes={nodes} rels={rels}
      nvlCallbacks={{ onLayoutDone: () => nvl.current?.fit(nodes.map(n => n.id)) }}
      onInitializationError={error => setLocalError(`Graph initialization failed: ${String(error)}`)}
      mouseEventCallbacks={{ onNodeClick: selectNode, onPan: true, onZoom: true, onDrag: true }}
      nvlOptions={{ initialZoom: 1.2, allowDynamicMinZoom: true, disableTelemetry: true }} />
      : !loading && <div className="graph-empty">{module === 1 ? 'Module 1 is stateless. It does not create memory.' : 'No memory in this view. Send a message, select a saved replay, or choose All stored memory.'}</div>}
    {nodes.length > 0 && <details className="graph-accessible-list"><summary>Inspect nodes by keyboard ({nodes.length})</summary>{graph.nodes.map(n => <button key={n.id} onClick={() => selectNode(n)}>{caption(n)}</button>)}</details>}
    <div className="graph-legend">{LAYER_LABELS.filter(l => module === 5 || l.key !== 'skills').map(l => <span key={l.key} className="legend-item"><span className="dot" style={{ backgroundColor: l.fill }} />{l.key.replace('_', ' ')}</span>)}</div>
  </div>
  {selected && <aside className="details-drawer"><div className="details-header"><div><strong>{caption(selected)}</strong><p>{selected.labels?.join(' · ')}</p></div><button aria-label="Close node details" onClick={() => setSelectedId(null)}>×</button></div>
    <table className="details-table"><tbody>{Object.entries(selected.properties ?? {}).map(([key, value]) => <tr key={key}><th>{key}</th><td>{typeof value === 'object' ? JSON.stringify(value) : String(value ?? '—')}</td></tr>)}</tbody></table></aside>}
  </div>
}
