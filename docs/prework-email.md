# Pre-workshop email — Road to Agent Memory

Send to all registered attendees at least 4–5 days before the session.

---

**Subject:** Pre-work for "Road to Agent Memory" — ≈20 min, due 48h before we start

Hi all!

Ahead of the workshop, please complete the four steps below **at least 48 hours before
the session**. Total time: about 20 minutes. Doing this in advance means we spend the
workshop building agent memory — not waiting for cloud instances to provision.

## Step 1 — Create your free AuraDB instance (~10 min)

1. Go to [console.neo4j.io](https://console.neo4j.io) and sign in (or create a free account).
2. Create a **free instance** (the free tier is all we need). If you can choose a
   region, pick the one closest to you: Codespaces starts in the region nearest you
   (US East/West, Europe West or Southeast Asia). Every memory write is a database
   round trip, so a distant region can make each chat turn take 20+ seconds instead
   of a few. `make check` prints the measured time per query.
3. **Save the credentials immediately** — the connection URI, username, and password are shown only once. Download the credentials file or copy all three into a password manager.
4. Wait for the instance status to show **Running**, and confirm you can open it.

> ⚠️ **Important:** free AuraDB instances **pause after a period of inactivity**.
> Please re-open console.neo4j.io **on the morning of the workshop** and make sure your
> instance is still Running — resume it if it has paused. This takes 30 seconds and
> saves us ten minutes of live debugging.

## Step 2 — Store your OpenAI API key as a Codespaces secret (~5 min)

We use OpenAI for the chat model, embeddings, and entity extraction. Storing the key
as a *personal Codespaces secret* means it appears in your workshop environment
automatically — no pasting keys into files on the day.

1. In GitHub, click your avatar (top right) → **Settings**.
2. In the left sidebar, under "Code, planning, and automation", click **Codespaces**.
3. Under **Codespaces secrets**, click **New secret**.
4. Name: `OPENAI_API_KEY` (exactly this — all caps, with underscores).
5. Value: your OpenAI API key (starts with `sk-...`; create one at platform.openai.com if you don't have one).
6. Under **Repository access**, choose **Selected repositories** and pick *only* the workshop repository.
7. Save.
8. Optional: add `NAMS_API_KEY` (from Step 3) the same way, so module 5 needs no setup on the day.

Create secrets **before** you create the codespace. If you add one later, GitHub offers to
reload the codespace; accept, or the new secret won't be visible.

While you're on the Codespaces settings page, set **Default idle timeout** to **90 minutes**.
The default of 30 minutes can stop your codespace during a talk segment.

## Step 3 — Sign up for NAMS and create an API key (~5 min)

Module 5 can use a hosted NAMS workspace or the workshop’s checked-in procedure.

1. Open the [NAMS console](https://memory.neo4jlabs.com/) and choose **Sign In**. Sign in with your Neo4j account or choose **Sign up** (email or Google). First login provisions a default workspace and key.
2. Open **Dashboard → API Keys**, select your workshop workspace and create a workspace-bound data key. [API Keys dashboard](https://memory.neo4jlabs.com/dashboard/api-keys).
3. Store its `nams_` value privately in a personal Codespaces secret named `NAMS_API_KEY` scoped to the workshop repo, or in the workshop’s private `.env`. The default `NAMS_BASE_URL` is `https://memory.neo4jlabs.com`. Keep the key out of chat, tickets, Git and screenshots.

## Step 4 — Check readiness

1. [Open this workshop in Codespaces](https://github.com/codespaces/new?repo=johnymontana/road-to-agent-memory), or use the local setup in the [workshop README](../README.md). Wait for setup to complete.
2. Set `NEO4J_URI`, `NEO4J_USERNAME` and `NEO4J_PASSWORD` in your private `.env` if your personal secrets do not already supply them.
3. Run `make check` from the repo root. It measures the median of five Bolt queries and checks required services. Record the failing check name if you need help. Share only redacted diagnostics.
4. For the hosted route run `make nams-check`. Read both **workspace reachable** and **distillation enabled**. An unavailable or unconfirmed capability stops the check and prints the fallback command. A successful check reports the hosted publish thresholds, the workspace's active ontology and whether it accepts the workshop seed. If the workspace already carries a custom ontology from another project, create a separate workshop workspace and key.
5. Stop here. Save hosted seeding, generation and publication for class. With a disabled capability or no key, plan to use the supplied procedure for the fresh-agent comparison. When finished, stop the codespace until the workshop.

## What will this cost me?

- **OpenAI:** expected usage for the whole workshop is **under $1**. You need an OpenAI account with billing enabled and a small balance.
- **GitHub Codespaces:** the workshop uses a 4-core machine, ≈ **8 core-hours** for the session. Personal GitHub accounts include **120 core-hours/month free**, so this fits comfortably — as long as you stop or delete the codespace afterward (see the teardown guide).
- **AuraDB free tier** and **NAMS** are free for what we'll do.

## What do I need to know beforehand?

- **Python basics** — reading a short script and running a command should feel familiar.
- **Editing a text file** — you'll add credentials to a `.env` file.

That's it. **No Neo4j, Cypher, graph theory, or PydanticAI experience needed** — we
teach all of it from zero.

## Deadline

Please complete **the core setup and readiness check at least 48 hours before the workshop**. Complete the NAMS check if you plan to follow the hosted route. When you're done — or if you hit any snag — **reply to this email** with
"ready" (or with the failing check name and redacted details), and we'll get you
sorted before the session.

See you soon!
