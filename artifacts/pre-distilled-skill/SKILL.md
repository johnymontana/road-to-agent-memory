# Acme Cloud Refund Procedure (pre-distilled fallback)

> Fallback artifact (review B2): checked into the repo so the module 5 payoff
> survives a NAMS outage. Regenerate with `make nams-distill` against a healthy
> workspace and diff before committing.

**When a customer requests a refund for a duplicate charge:**

1. **Identify the customer and plan first.** Call `lookup_account(customer_email)`
   before touching money. Note the plan's no-approval refund limit.
2. **Check the refund policy.** Call `fetch_policy("refund")`. Duplicate charges
   are always refundable; amounts within the plan's no-approval limit
   (Pro: $250, Enterprise: $500) need no escalation.
3. **Issue within the limit; escalate above it.** Call
   `issue_refund(customer_email, amount, reason)` when the amount is within the
   limit. If the tool reports `rejected_over_limit`, explain the escalation path
   (engineering-manager approval) instead of retrying.
4. **Confirm in writing.** State the amount, the reason, and the refund id.

*Grounding: distilled from 2 recorded refund traces (6 tool calls) in the Acme
Cloud workspace memory. Grounding score and per-claim provenance: see the skill
subgraph (`GROUNDED_IN` edges) in the NAMS console.*
