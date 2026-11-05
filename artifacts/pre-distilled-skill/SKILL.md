# Acme Cloud duplicate-charge refund procedure

Checked-in workshop example for the fresh support agent. Use this procedure when a customer reports a duplicate charge.

1. **Identify the customer and the case.** Call `lookup_account(customer_email)`. Match the selected customer and incident to the charge. Check existing refunds before attempting a new one.
2. **Read the current policy.** Call `fetch_policy("refund")` and read the customer's current no-approval limit from the account lookup. A duplicate charge can be eligible for reimbursement even when its amount requires manager approval.
3. **Act within this turn's authorization.** For a selected and authorized case within the live limit, call `issue_refund(customer_email, amount, reason)`. If the amount exceeds the limit, explain that a manager must approve it. The support agent has no escalation tool.
4. **Report the actual receipt.** For `issued`, report the amount and refund ID. For `already_issued`, identify the existing refund. For a rejection, give the returned reason. An approval requirement is a next step for the operator.

The hosted exercise downloads a versioned procedure with evidence references. This fallback contains the procedure text only. Compare the observed SQL tool calls and business result for Ravi's $49 case with the control run.
