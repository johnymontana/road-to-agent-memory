function JsonBlock({ label, value }) {
  return (
    <details className="trace-details">
      <summary>{label}</summary>
      <pre className="mono trace-json">
        {value === undefined ? 'undefined' : JSON.stringify(value, null, 2)}
      </pre>
    </details>
  )
}

export default function TracePanel({ toolCalls }) {
  const calls = Array.isArray(toolCalls) ? toolCalls : []

  return (
    <div className="trace-panel">
      <div className="panel-header">
        <span className="panel-title">Tool Trace</span>
        {calls.length > 0 && (
          <span className="badge">{calls.length} call{calls.length === 1 ? '' : 's'}</span>
        )}
      </div>

      <div className="trace-body">
        {calls.length === 0 ? (
          <div className="trace-empty">No tool calls yet — ask the agent something.</div>
        ) : (
          <ol className="trace-timeline">
            {calls.map((tc, i) => (
              <li key={i} className="trace-item">
                <div className="trace-head">
                  <span className="trace-index">{i + 1}</span>
                  <span className="trace-tool">{tc.name ?? 'tool'}</span>
                  {typeof tc.duration_ms === 'number' && (
                    <span className="trace-duration">{tc.duration_ms} ms</span>
                  )}
                </div>
                <JsonBlock label="input" value={tc.input} />
                <JsonBlock label="output" value={tc.output} />
                {tc.sql && <pre className="mono trace-sql">{tc.sql}</pre>}
              </li>
            ))}
          </ol>
        )}
      </div>
    </div>
  )
}
