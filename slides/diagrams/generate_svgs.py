#!/usr/bin/env python3
"""Render the workshop's diagram inventory to SVG with the fixed palette.

Every color is paired with a text label (accessibility: never color-only meaning).
Sources for the five committed Excalidraw diagrams live alongside; these SVGs are
the render artifacts the deck references.
"""

from __future__ import annotations

import runpy
from pathlib import Path

OUT = Path(__file__).resolve().parent

PALETTE = {
    "short": ("#B2F2BB", "#2F9E44"),
    "long": ("#FFEC99", "#F08C00"),
    "reasoning": ("#D0BFFF", "#9C36B5"),
    "store": ("#A5D8FF", "#1971C2"),
    "labs": ("#E5DBFF", "#6366F1"),
    "neutral": ("#F1F3F5", "#495057"),
    "alert": ("#FFE3E3", "#C92A2A"),
}


def esc(t: str) -> str:
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class Svg:
    def __init__(self, w: int = 960, h: int = 420):
        self.w, self.h, self.el = w, h, []
        self.el.append(f'<rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff" rx="12"/>')
        self.el.append(
            '<defs><marker id="arr" markerWidth="10" markerHeight="10" refX="8" refY="3" '
            'orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#495057"/></marker>'
            '<marker id="arr-red" markerWidth="10" markerHeight="10" refX="8" refY="3" '
            'orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#C92A2A"/></marker></defs>'
        )

    def box(self, x, y, w, h, label, color="neutral", sub=None, stroke_dash=None):
        fill, stroke = PALETTE[color]
        dash = ' stroke-dasharray="6 4"' if stroke_dash else ""
        self.el.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="2.5"{dash}/>'
        )
        cx = x + w / 2
        lines = label.split("\n")
        ty = y + h / 2 - (len(lines) - 1) * 12 - (10 if sub else 0)
        for i, line in enumerate(lines):
            self.el.append(
                f'<text x="{cx}" y="{ty + i * 24}" text-anchor="middle" '
                f'font-family="sans-serif" font-size="17" font-weight="600" '
                f'fill="#1e1e1e">{esc(line)}</text>'
            )
        if sub:
            self.el.append(
                f'<text x="{cx}" y="{y + h - 14}" text-anchor="middle" '
                f'font-family="sans-serif" font-size="13" fill="#495057">{esc(sub)}</text>'
            )

    def arrow(self, x1, y1, x2, y2, label="", red=False, dashed=False):
        dash = ' stroke-dasharray="6 4"' if dashed else ""
        color = "#C92A2A" if red else "#495057"
        marker = "arr-red" if red else "arr"
        self.el.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
            f'stroke-width="2.5"{dash} marker-end="url(#{marker})"/>'
        )
        if label:
            self.el.append(
                f'<text x="{(x1 + x2) / 2}" y="{(y1 + y2) / 2 - 8}" text-anchor="middle" '
                f'font-family="sans-serif" font-size="13" fill="{color}">{esc(label)}</text>'
            )

    def text(self, x, y, t, size=14, color="#495057", bold=False, anchor="middle"):
        weight = ' font-weight="700"' if bold else ""
        self.el.append(
            f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="sans-serif" '
            f'font-size="{size}" fill="{color}"{weight}>{esc(t)}</text>'
        )

    def strike(self, x1, y1, x2, y2):
        self.el.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#C92A2A" stroke-width="3.5"/>'
        )

    def save(self, name: str):
        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
            f'viewBox="0 0 {self.w} {self.h}">' + "".join(self.el) + "</svg>"
        )
        (OUT / name).write_text(svg)
        print(f"wrote {name}")


# ── D-01 The two stores ───────────────────────────────────────────────────────
s = Svg(960, 420)
s.text(480, 34, "Two stores, two jobs", 20, "#1e1e1e", bold=True)
s.box(60, 130, 240, 160, "SQLite\nSystem of record", "store", sub="customers · products · policies")
s.box(660, 130, 240, 160, "Neo4j\nMemory", "store", sub="what the agent learned")
s.box(120, 320, 120, 40, "facts", "neutral")
s.box(680, 320, 70, 40, "convo", "short")
s.box(758, 320, 80, 40, "entities", "long")
s.box(846, 320, 70, 40, "traces", "reasoning")
s.box(360, 140, 240, 140, "SupportBot", "labs", sub="PydanticAI agent + tools")
s.arrow(300, 210, 360, 210, "SQL queries (tools)")
s.arrow(600, 210, 660, 210, "memory reads / writes")
s.text(180, 305, "what the agent ACTS ON", 12)
s.text(780, 305, "what the agent LEARNED", 12)
s.save("d01-two-stores.svg")

# ── D-02 Three memory types, one graph ────────────────────────────────────────
s = Svg(960, 420)
s.text(480, 34, "Three memory types, one knowledge graph", 20, "#1e1e1e", bold=True)
s.box(60, 90, 230, 110, "Short-term\nconversations & messages", "short")
s.box(60, 220, 230, 110, "Reasoning\ntraces, tool calls, outcomes", "reasoning")
s.box(60, 155, 230, 0, "", "short")  # spacer no-op
s.el.pop()
s.box(60, 155 - 0, 230, 0, "", "short")
s.el.pop()
s.box(360, 140, 220, 130, "Neo4j\none knowledge graph", "store")
s.box(670, 155, 230, 110, "Long-term\nentities · preferences · facts", "long")
s.arrow(290, 145, 360, 180)
s.arrow(290, 275, 360, 230)
s.arrow(670, 210, 580, 205)
s.text(480, 390, "every layer lives in the same graph — connections are the point", 14)
s.save("d02-three-memory-types.svg")

# ── D-03 The workshop arc ─────────────────────────────────────────────────────
s = Svg(960, 400)
s.text(480, 32, "The road: failure → memory layer → fix", 20, "#1e1e1e", bold=True)
steps = [
    ("1 · Stateless", "asks who you are\n— again", "neutral"),
    ("2 · Short-term", "survives restarts", "short"),
    ("3 · Long-term", "knows the customer", "long"),
    ("4 · Reasoning", "reuses past solutions", "reasoning"),
    ("5 · Distillation", "experience → skill", "labs"),
]
x = 30
for i, (title, sub, color) in enumerate(steps):
    s.box(x, 120, 160, 130, title, color, sub=sub)
    if i < 4:
        s.arrow(x + 160, 185, x + 190, 185)
    x += 190
s.text(480, 320, "Controlled retrieval probes: inspect exact facts and source IDs", 14)
s.save("d03-workshop-arc.svg")

# ── D-04 Environment map ──────────────────────────────────────────────────────
s = Svg(960, 420)
s.text(480, 34, "Where everything runs (and where credentials live)", 20, "#1e1e1e", bold=True)
s.box(60, 110, 300, 220, "GitHub Codespace\n(prebuilt)", "neutral")
s.text(210, 190, "FastAPI :8000  ·  Vite :5173\nuv env · scenarios · scripts", 13)
s.box(500, 80, 200, 90, "AuraDB\n(Neo4j)", "store", sub="your instance + key")
s.box(500, 190, 200, 80, "OpenAI", "neutral", sub="chat · embeddings · extraction")
s.box(500, 290, 200, 90, "NAMS\n(hosted memory)", "labs", sub="module 5 · nams_ key")
s.arrow(360, 150, 500, 125, "bolt")
s.arrow(360, 220, 500, 230, "API key")
s.arrow(360, 290, 500, 335, "REST")
s.text(210, 355, ".env or personal Codespaces secrets; never commit credentials", 12)
s.save("d04-environment-map.svg")

# ── D-05 Statelessness ────────────────────────────────────────────────────────
s = Svg(960, 380)
s.text(480, 34, "Module 1: no history between model calls", 20, "#1e1e1e", bold=True)
s.box(
    90,
    100,
    300,
    180,
    "Turn 1\n“Here is my email…”",
    "short",
    sub="self-contained account lookup",
)
s.box(
    570, 100, 300, 180, "Turn 2\n“What email did I give?”", "short", sub="agent asks: who are you?"
)
s.arrow(390, 190, 570, 190, "", red=True, dashed=True)
s.strike(440, 150, 520, 230)
s.text(480, 320, "No history is passed—even within one visible chat", 14)
s.save("d05-statelessness.svg")

# ── D-06 Message chains ───────────────────────────────────────────────────────
s = Svg(960, 380)
s.text(480, 34, "Short-term memory: the conversation persists", 20, "#1e1e1e", bold=True)
s.box(60, 150, 180, 90, "Conversation", "short", sub="session id")
s.box(320, 90, 170, 70, "Message 1\n(user)", "short")
s.box(320, 230, 170, 70, "Message 2\n(assistant)", "short")
s.box(560, 90, 170, 70, "Message 3\n(user)", "short")
s.box(560, 230, 170, 70, "Message 4\n(assistant)", "short")
s.arrow(240, 180, 320, 125, "HAS_MESSAGE")
s.arrow(490, 265, 560, 125, "NEXT")
s.arrow(645, 160, 645, 230, "NEXT")
s.arrow(405, 160, 405, 230, "NEXT")
s.text(480, 345, "NEXT = NEXT_MESSAGE; the same conversation survives restart", 14)
s.save("d06-message-chains.svg")

# ── D-07 Context assembly ─────────────────────────────────────────────────────
s = Svg(960, 380)
s.text(480, 34, "Per-turn context assembly: write before retrieval", 20, "#1e1e1e", bold=True)
for x, label, color in [
    (25, "customer\nmessage", "neutral"),
    (215, "store message\nadd_message", "short"),
    (405, "build_context\nexclude current ID", "short"),
    (595, "instructions\nbase + evidence", "store"),
    (785, "model call", "labs"),
]:
    s.box(x, 145, 150, 90, label, color)
for x in (175, 365, 555, 745):
    s.arrow(x, 190, x + 40, 190)
s.text(480, 320, "Recent prior messages + scoped semantic matches; then run and verify", 14)
s.save("d07-context-assembly.svg")

# ── D-08 Ontology-driven extraction ──────────────────────────────────────────
s = Svg(960, 420)
s.text(480, 34, "One document drives the prompt and the validation", 20, "#1e1e1e", bold=True)
s.box(50, 140, 200, 120, "acme_cloud.yaml", "neutral", sub="entity types · relations · aliases")
s.box(300, 60, 180, 80, "extraction\nprompt", "neutral")
s.box(300, 250, 180, 80, "relation\nvalidation", "neutral")
s.box(530, 140, 160, 90, "LLM\nextractor", "labs")
s.box(750, 60, 170, 70, "Customer\nMaya Chen", "long")
s.box(750, 160, 170, 70, "Product\nAcme Cloud…", "long")
s.arrow(250, 170, 300, 100, "rendered into")
s.arrow(250, 220, 300, 290, "validated against")
s.arrow(480, 100, 530, 160)
s.arrow(690, 150, 750, 95)
s.arrow(690, 185, 750, 195)
s.arrow(530, 230, 480, 290, "forbidden ↓ dropped", red=True, dashed=True)
s.save("d08-ontology-extraction.svg")

# ── D-10 The hybrid pipeline ──────────────────────────────────────────────────
s = Svg(960, 440)
s.text(480, 34, "LLM structure + source-marked SQL and public facts", 20, "#1e1e1e", bold=True)
s.box(40, 60, 220, 90, "LLM extractor", "labs", sub="structure")
s.box(40, 180, 220, 90, "SQLite", "store", sub="grounded facts")
s.box(40, 300, 220, 90, "Wikipedia", "neutral", sub="external knowledge")
s.box(560, 130, 340, 190, "Typed entity sources", "long")
s.text(730, 200, "types · relations (LLM)", 13, "#1e1e1e")
s.text(730, 232, "Customer: email · plan · date (SQLite)", 13, "#1971C2")
s.text(730, 264, "Organization: optional Wikimedia facts", 13, "#495057")
s.arrow(260, 105, 560, 160)
s.arrow(260, 225, 560, 225)
s.arrow(260, 345, 560, 290)
s.text(
    480,
    410,
    ("SQL grounding and optional Organization enrichment have separate source markers"),
    13,
)
s.save("d10-hybrid-pipeline.svg")

# ── D-11 Entity resolution ────────────────────────────────────────────────────
s = Svg(960, 380)
s.text(480, 34, "One real-world entity, many surface forms", 20, "#1e1e1e", bold=True)
s.box(60, 80, 220, 70, "“Acme Cloud”", "neutral", sub="message 3")
s.box(60, 220, 220, 70, "“AcmeCloud”", "neutral", sub="message 12")
s.box(390, 140, 180, 90, "entity\nresolution", "labs")
s.box(670, 130, 240, 110, "Organization\nAcme Cloud", "long", sub="aliases: AcmeCloud, Acme")
s.arrow(280, 115, 390, 165)
s.arrow(280, 255, 390, 205)
s.arrow(570, 185, 670, 185)
s.text(
    480, 320,
    "Illustrative resolution; inspect actual nodes and aliases. Duplicates remain possible.",
    14,
)
s.save("d11-entity-resolution.svg")

# ── D-13 Similar-task retrieval ───────────────────────────────────────────────
s = Svg(960, 400)
s.text(480, 34, "A familiar ticket recalls a recorded solution", 20, "#1e1e1e", bold=True)
s.box(50, 150, 210, 90, "new ticket\n“double-billed $129”", "neutral")
s.box(
    330,
    60,
    280,
    90,
    "Recorded success\n(conceptual example)",
    "reasoning",
    sub="task → steps → outcome: success",
)
s.box(
    330,
    250,
    280,
    90,
    "Fixed declined trace\n(ablation corpus)",
    "reasoning",
    sub="task → steps → outcome: rejected",
)
s.box(700, 150, 220, 90, "primed agent", "labs", sub="procedure from memory")
s.arrow(260, 175, 330, 105, "similar-task retrieval")
s.arrow(260, 215, 330, 295)
s.arrow(610, 195, 700, 195)
s.text(
    480, 375,
    "The ablation seeds one declined trace; separate SQL copies isolate both branches.",
    13,
)
s.save("d13-similar-task-retrieval.svg")

# ── D-15 Governance loop ──────────────────────────────────────────────────────
s = Svg(960, 400)
s.text(480, 34, "The governance loop", 20, "#1e1e1e", bold=True)
s.box(60, 150, 200, 90, "hosted memory changes\n(matched entity deleted)", "long")
s.box(
    380, 60, 220, 80, "inspect drift report\nSTALE if reported", "alert",
    sub="verify affected grounding",
)
s.box(380, 250, 220, 80, "re-distill\n(make nams-redistill)", "labs")
s.box(700, 150, 210, 90, "inspect updated skill\nre-run fresh agent", "reasoning")
s.arrow(260, 180, 380, 100)
s.arrow(490, 140, 490, 250)
s.arrow(600, 290, 700, 220)
s.text(480, 375, "Expected workflow; inspect actual reports. SQLite is not synchronized.", 13)
s.save("d15-governance-loop.svg")

# ── D-18 Bolt vs NAMS ─────────────────────────────────────────────────────────
s = Svg(960, 400)
s.text(480, 34, "Same memory model, two consumption models", 20, "#1e1e1e", bold=True)
s.box(60, 90, 380, 240, "Bolt — your database", "store")
s.text(250, 160, "your AuraDB · full Cypher access", 14, "#1e1e1e")
s.text(250, 195, "client-side extraction (your models)", 14, "#1e1e1e")
s.text(250, 240, "custom hydration / write paths", 14, "#1e1e1e")
s.text(250, 275, "full support apps: modules 1–5", 13, "#495057")
s.box(520, 90, 380, 240, "NAMS — hosted service", "labs")
s.text(710, 160, "separate seeded workspace", 14, "#1e1e1e")
s.text(710, 195, "REST generate → poll → publish", 14, "#1e1e1e")
s.text(710, 240, "download skill → fresh agent", 14, "#1e1e1e")
s.text(710, 275, "module 5 workflows (early access)", 13, "#495057")
s.save("d18-bolt-vs-nams.svg")

# Apply the reviewed native-deck design after the legacy/reference scenes.
if (OUT.parent / "visual-design.json").is_file():
    runpy.run_path(str(OUT / "generate_branded_diagrams.py"), run_name="__main__")
