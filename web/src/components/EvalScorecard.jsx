import { useEffect, useState } from 'react'

export default function EvalScorecard({ open, onClose, onError }) {
  const [questions, setQuestions] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (!open) return
    let cancelled = false
    setLoading(true)
    setQuestions(null)

    fetch('/api/eval')
      .then((res) => {
        if (!res.ok) throw new Error(`GET /api/eval failed: ${res.status} ${res.statusText}`)
        return res.json()
      })
      .then((data) => {
        if (!cancelled) setQuestions(Array.isArray(data.questions) ? data.questions : [])
      })
      .catch((e) => {
        if (cancelled) return
        onError?.(e.message || 'Eval request failed')
        onClose?.()
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })

    return () => {
      cancelled = true
    }
  }, [open, onClose, onError])

  if (!open) return null

  const answeredCount = questions?.filter((q) => q.answered).length ?? 0

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2 className="modal-title">
            Continuity Eval Scorecard
            {questions && (
              <span className="badge score-badge">
                {answeredCount} / {questions.length} answered
              </span>
            )}
          </h2>
          <button className="error-dismiss" onClick={onClose} aria-label="Close">
            ×
          </button>
        </div>

        <div className="modal-body">
          {loading && (
            <div className="modal-loading">
              <span className="spinner" /> running eval questions against the agent…
            </div>
          )}
          {questions && questions.length === 0 && (
            <div className="trace-empty">No eval questions returned.</div>
          )}
          {questions && questions.length > 0 && (
            <ul className="eval-list">
              {questions.map((q) => (
                <li key={q.id ?? q.question} className="eval-item">
                  <span className="eval-status" aria-label={q.answered ? 'answered' : 'not answered'}>
                    {q.answered ? '✅' : '❌'}
                  </span>
                  <div className="eval-content">
                    <div className="eval-question">{q.question}</div>
                    {q.answer && <div className="eval-answer mono">{q.answer}</div>}
                  </div>
                  <span className="badge eval-module-badge">
                    module {q.expected_from_module ?? '?'}
                  </span>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  )
}
