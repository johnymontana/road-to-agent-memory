# Teardown — cleaning up after the workshop

Decide after the final capstone exercise and take-home discussion. To run the [Monday example](../scripts/monday_memory.py) later, retain your workshop environment and credentials and stop the codespace between sessions. When you finish, save any artifacts you plan to keep, verify the database/workspace names, then clean up the workshop resources below. Deleting a codespace removes its local uncommitted files, generated package and receipts.

## 1. Delete your codespace

1. Go to [github.com/codespaces](https://github.com/codespaces).
2. Find the workshop codespace, open the `···` menu, and choose **Delete**.

Stopping is not enough if you want the storage back — deleting removes both the
running machine (core-hours) and its disk. Your personal `OPENAI_API_KEY` Codespaces
secret is *not* deleted with the codespace; remove it under **GitHub Settings →
Codespaces → Codespaces secrets** if you created it only for the workshop.

## 2. Delete (or pause) your AuraDB instance

1. Go to [console.neo4j.io](https://console.neo4j.io).
2. Open your instance and choose **Delete** — or **Pause** if you'd like to keep
   exploring the graph you built.

The free tier is generous, but an idle instance you forgot about is the classic way to
be surprised by it later. Note that free instances also auto-pause after inactivity.

## 3. Revoke your NAMS API key

1. Open the [NAMS API Keys dashboard](https://memory.neo4jlabs.com/dashboard/api-keys) in the workshop workspace.
2. Find the `nams_` key you created for the workshop and revoke (or delete) it.

## 4. Rotate your OpenAI key (if you created one for the workshop)

If you minted an API key specifically for this session, delete it at
[platform.openai.com](https://platform.openai.com) under **API keys**. If it was a
pre-existing key you also use elsewhere, there's nothing to do — but never commit it
anywhere; the workshop only ever read it from environment variables.

## A note on what you used

**NAMS** (the Neo4j Agent Memory Service) and the **`neo4j-agent-memory`** Python
package are **Neo4j Labs experimental projects**: community-supported, with **no
SLAs** and interfaces that may change between releases. They're perfect for learning
and prototyping — evaluate carefully before betting a production workload on them.
Your AuraDB instance and the Neo4j database itself are, of course, fully supported
products.

## Keep going

- **Docs:** [neo4j.com/labs/agent-memory](https://neo4j.com/labs/agent-memory) — the
  `neo4j-agent-memory` package and NAMS.
- **Course:** the **Context Graphs** course on
  [GraphAcademy](https://graphacademy.neo4j.com) — the natural next step.
- **This repo** includes a [module reading map](../README.md#read-and-compare-the-agents) and [participant exercises](modules/). To revisit a previous hosted result, inspect the downloaded package directly. Running `make module-5` starts a full hosted replay with new seed records and a new generation/publication.
