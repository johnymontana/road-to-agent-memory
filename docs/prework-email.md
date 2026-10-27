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
2. Create a **free instance** (the free tier is all we need).
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

## Step 3 — Sign up for NAMS and create an API key (~5 min)

Module 5 uses the hosted Neo4j Agent Memory Service.

1. Go to [memory.neo4jlabs.com](https://memory.neo4jlabs.com) and sign up.
2. Create an API key — it will have the prefix `nams_`.
3. Save it somewhere safe alongside your AuraDB credentials.

## Step 4 (optional but appreciated) — Smoke-test your environment (~5 min)

1. Open the workshop repository and click the **"Open in GitHub Codespaces"** badge in the README.
2. Wait for the codespace to finish starting (the first open takes a couple of minutes).
3. In the terminal, run `make check`.
4. If every line is green — you're done. **If anything is red, reply to this email and paste the full output.**

When you're finished, stop the codespace (it also auto-stops on idle) so it doesn't
consume your free quota.

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

Please complete **steps 1–3 at least 48 hours before the workshop** (step 4 is
optional). When you're done — or if you hit any snag — **reply to this email** with
"ready" (or with your `make check` output if anything was red), and we'll get you
sorted before the session.

See you soon!
