import { useEffect, useMemo, useRef, useState } from 'react'
import { InteractiveNvlWrapper } from '@neo4j-nvl/react'
import {
  ZoomInteraction,
  PanInteraction,
  DragNodeInteraction,
} from '@neo4j-nvl/interaction-handlers'
import { colorForLabels, LAYER_LABELS } from '../palette.js'

const LAYER_OPTIONS = [
  { value: 'all', label: 'All layers' },
  { value: 'short_term', label: 'Short-term' },
  { value: 'long_term', label: 'Long-term' },
  { value: 'reasoning', label: 'Reasoning' },
]

function truncate(value, max = 40) {
  if (typeof value !== 'string') return undefined
  return value.length > max ? `${value.slice(0, max - 1)}…` : value
}

/** Map an API node to an NVL node. */
function toNvlNode(apiNode) {
  const labels = Array.isArray(apiNode.labels) ? apiNode.labels : []
  const props = apiNode.properties ?? {}
  const caption = props.name ?? truncate(props.content) ?? labels[0] ?? String(apiNode.id)
  const { fill } = colorForLabels(labels)
  return {
    id: String(apiNode.id),
    caption: String(caption),
    color: fill,
    size: 24,
  }
}

/** Map an API relationship to an NVL relationship. */
function toNvlRel(apiRel) {
  return {
    id: String(apiRel.id),
    from: String(apiRel.from),
    to: String(apiRel.to),
    caption: apiRel.type ?? '',
  }
}

function formatValue(value) {
  if (value === null || value === undefined) return '—'
  if (typeof value === 'object') return JSON.stringify(value)
  return String(value)
}

export default function GraphPanel({ refreshKey, onError }) {
  const [layer, setLayer] = useState('all')
  const [namsMode, setNamsMode] = useState(false)
  const [graph, setGraph] = useState({ nodes: [], relationships: [] })
  const [unavailable, setUnavailable] = useState(false)
  const [loading, setLoading] = useState(false)
  const [selectedId, setSelectedId] = useState(null)

  const nvlRef = useRef(null)
  const [interactions, setInteractions] = useState([])

  // NVL interaction handlers need the NVL instance, which only exists
  // after the wrapper has mounted — so build them in a second pass.
  useEffect(() => {
    const nvl = nvlRef.current?.nvl ?? nvlRef.current
    if (nvl) {
      setInteractions([
        new ZoomInteraction(nvl),
        new PanInteraction(nvl),
        new DragNodeInteraction(nvl),
      ])
    }
  }, [])

  useEffect(() => {
    let cancelled = false
    setLoading(true)

    const url = namsMode
      ? '/api/graph/nams'
      : `/api/graph?layer=${encodeURIComponent(layer)}`

    fetch(url)
      .then((res) => {
        if (!res.ok) throw new Error(`GET ${url} failed: ${res.status} ${res.statusText}`)
        return res.json()
      })
      .then((data) => {
        if (cancelled) return
        setGraph({
          nodes: Array.isArray(data.nodes) ? data.nodes : [],
          relationships: Array.isArray(data.relationships) ? data.relationships : [],
        })
        setUnavailable(Boolean(data.unavailable))
        setSelectedId(null)
      })
      .catch((e) => {
        if (!cancelled) onError?.(e.message || 'Graph fetch failed')
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })

    return () => {
      cancelled = true
    }
  }, [layer, namsMode, refreshKey, onError])

  const nvlNodes = useMemo(() => graph.nodes.map(toNvlNode), [graph])
  const nvlRels = useMemo(() => graph.relationships.map(toNvlRel), [graph])

  const selectedNode = useMemo(
    () => graph.nodes.find((n) => String(n.id) === selectedId) ?? null,
    [graph, selectedId],
  )

  function handleNodeClick(node) {
    if (node?.id != null) setSelectedId(String(node.id))
  }

  return (
    <div className="graph-panel">
      <div className="panel-header">
        <span className="panel-title">Memory Graph</span>
        <div className="graph-controls">
          <label className="graph-toggle">
            <input
              type="checkbox"
              checked={namsMode}
              onChange={(e) => setNamsMode(e.target.checked)}
            />
            Module 5 · NAMS
          </label>
          <select
            className="layer-select"
            value={layer}
            onChange={(e) => setLayer(e.target.value)}
            disabled={namsMode}
            title={namsMode ? 'Layer filter applies to /api/graph only' : 'Filter by memory layer'}
          >
            {LAYER_OPTIONS.map((o) => (
              <option key={o.value} value={o.value}>
                {o.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="graph-canvas">
        {unavailable ? (
          <div className="graph-empty">
            NAMS is not configured for this backend. Switch off “Module 5 · NAMS” or run a
            module 5 backend.
          </div>
        ) : nvlNodes.length === 0 && !loading ? (
          <div className="graph-empty">
            The memory graph is empty — send a chat message to create some memories.
          </div>
        ) : (
          <InteractiveNvlWrapper
            ref={nvlRef}
            nodes={nvlNodes}
            rels={nvlRels}
            interaction={interactions}
            mouseEventCallbacks={{ onNodeClick: handleNodeClick }}
            nvlOptions={{ initialZoom: 0.9, allowDynamicMinZoom: true }}
          />
        )}
        {loading && <div className="graph-loading"><span className="spinner" /> loading graph…</div>}

        <div className="graph-legend">
          {LAYER_LABELS.map((l) => (
            <span key={l.key} className="legend-item" title={l.label}>
              <span className="dot" style={{ backgroundColor: l.fill, borderColor: l.stroke }} />
              {l.key.replace(/_/g, ' ')}
            </span>
          ))}
        </div>
      </div>

      {selectedNode && (
        <aside className="details-drawer">
          <div className="details-header">
            <div>
              <div className="details-title">
                {selectedNode.properties?.name ??
                  truncate(selectedNode.properties?.content, 24) ??
                  'Node details'}
              </div>
              <div className="details-labels">
                {(Array.isArray(selectedNode.labels) ? selectedNode.labels : []).map((l) => (
                  <span key={l} className="badge label-badge">{l}</span>
                ))}
              </div>
            </div>
            <button className="error-dismiss" onClick={() => setSelectedId(null)} aria-label="Close">
              ×
            </button>
          </div>
          <table className="details-table">
            <tbody>
              {Object.entries(selectedNode.properties ?? {}).map(([key, value]) => (
                <tr key={key}>
                  <td className="details-key">{key}</td>
                  <td className="details-value mono">{formatValue(value)}</td>
                </tr>
              ))}
              {Object.keys(selectedNode.properties ?? {}).length === 0 && (
                <tr>
                  <td className="details-key">—</td>
                  <td className="details-value">no properties</td>
                </tr>
              )}
            </tbody>
          </table>
        </aside>
      )}
    </div>
  )
}
