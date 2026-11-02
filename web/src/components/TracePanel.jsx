export default function TracePanel({ turns = [] }) {
  return <div className="trace-panel"><div className="panel-header"><span className="panel-title">Execution evidence · all turns</span></div><div className="trace-body">
    {!turns.length && <p className="trace-empty">Send a browser message to inspect its execution. Terminal replays are available in Saved replay.</p>}
    {turns.map((turn, index) => <details key={turn.request_id ?? index} className="trace-details" open={index === turns.length - 1}>
      <summary>Turn {index + 1} · {turn.status || 'completed'} · {turn.tool_calls?.length || 0} calls · {turn.timing?.total_seconds ?? '—'}s</summary>
      <p className="mono">Operation: {turn.request_id} · Business result: {turn.business_status || 'no action'}</p>
      {turn.warnings?.length > 0 && <p role="status">Partial completion: {turn.warnings.map(w => `${w.phase}: ${w.error}`).join('; ')}. The operation receipt retains the reply.</p>}
      <details><summary>Retrieved evidence and memory writes</summary><pre>{JSON.stringify(turn.context, null, 2)}</pre></details>
      {!turn.tool_calls?.length && <p>No tools in this turn. Earlier executions remain above.</p>}
      {turn.tool_calls?.map((call, i) => <details key={i}><summary>{call.name} · {call.duration_ms}ms {call.origin && `· ${call.origin}`}</summary><pre>{JSON.stringify({ input: call.input, output: call.output }, null, 2)}</pre>{call.sql && <pre aria-label="Executed SQL">{call.sql}</pre>}</details>)}
    </details>)}
  </div></div>
}
