#!/usr/bin/env python3
"""Replay a named workshop beat with explicit action scope and immutable output."""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
import shutil
import sqlite3
import sys
import tempfile
import time
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
SCENARIOS = ROOT / "scripts/scenarios"
TURN_PAUSE_S = 0.2


def save_replay(settings, report):
    folder = settings.data_dir / "replays"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{report['id']}.json"
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(report, indent=2, default=str))
    temporary.replace(path)


def measured_graph(turns):
    nodes = []
    edges = []
    for index, turn in enumerate(turns):
        node = f"turn-{index}"
        nodes.append(
            {
                "id": node,
                "labels": ["Message"],
                "properties": {
                    "content": turn["message"],
                    "reply": turn["result"]["reply"],
                    "source": "measured replay output",
                    "namespace": turn["namespace"],
                },
            }
        )
        for j, call in enumerate(turn["result"]["tool_calls"]):
            target = f"{node}-tool-{j}"
            nodes.append({"id": target, "labels": ["ToolCall"], "properties": call})
            edges.append(
                {
                    "id": target + "-edge",
                    "from": node,
                    "to": target,
                    "type": "EXECUTED",
                    "properties": {},
                }
            )
    return {"nodes": nodes, "relationships": edges, "truncated": False}


async def run_sessions(
    scenario,
    module,
    sessions,
    *,
    settings=None,
    namespace=None,
    output_settings=None,
    run_id=None,
    append=False,
    **options,
):
    from lib.settings import get_settings
    from lib.workshop import open_agent

    settings = settings or get_settings()
    run_id = run_id or uuid4().hex
    namespace = namespace or f"replay-{run_id}"
    local = settings.model_copy(update={"memory_namespace": namespace})
    report = {
        "id": run_id,
        "title": scenario["name"],
        "module": module,
        "namespace": namespace,
        "pid": os.getpid(),
        "append": append,
        "turns": [],
        "protocol": "Actual lesson agent; explicit per-turn action authorization.",
    }
    report["status"] = "starting"
    if append:
        path = (output_settings or settings).data_dir / "replays" / f"{run_id}.json"
        if path.exists():
            previous = json.loads(path.read_text())
            report["turns"] = previous.get("turns", [])
            report["process_ids"] = list(
                dict.fromkeys(previous.get("process_ids", [previous["pid"]]) + [report["pid"]])
            )
    report["graph"] = measured_graph(report["turns"])
    save_replay(output_settings or settings, report)
    print(f"Opening module {module} · process {os.getpid()} · namespace {namespace}", flush=True)
    started = time.monotonic()
    try:
        async with open_agent(module, local, **options) as chat:
            print(f"Ready in {time.monotonic() - started:.1f}s", flush=True)
            for session in sessions:
                for _index, entry in enumerate(session["messages"]):
                    turn = {"message": entry} if isinstance(entry, str) else entry
                    scope = {
                        k: session[k]
                        for k in ("account_email", "incident_id", "authorize_refund", "policy_plan")
                        if k in session
                    }
                    scope.update({k: v for k, v in turn.items() if k != "message"})
                    print(f"[{session['id']}] customer: {turn['message']}", flush=True)
                    result = await chat.chat(
                        turn["message"],
                        session_id=f"{scenario['name']}-{session['id']}",
                        request_id=uuid4().hex,
                        **scope,
                    )
                    report["turns"].append(
                        {"message": turn["message"], "namespace": namespace, "result": result}
                    )
                    print("SupportBot:", result["reply"], flush=True)
                    print(
                        "Tools:",
                        [
                            (
                                c["name"],
                                c["output"].get("status") if isinstance(c["output"], dict) else "",
                            )
                            for c in result["tool_calls"]
                        ],
                        flush=True,
                    )
                    print("Timing:", result["timing"], "Warnings:", result["warnings"], flush=True)
                    report["graph"] = measured_graph(report["turns"])
                    save_replay(output_settings or settings, report)
                    if result.get("status") == "failed":
                        raise RuntimeError(
                            "Agent execution failed; completed turns and receipt retained"
                        )
                    await asyncio.sleep(TURN_PAUSE_S)
        report["status"] = "completed"
        save_replay(output_settings or settings, report)
    except Exception as error:
        report.update(status="failed", error=type(error).__name__)
        save_replay(output_settings or settings, report)
        raise
    return report


async def run_ablation(scenario, module, settings, run_id):
    from importlib import import_module

    corpus_namespace = f"corpus-{run_id}"
    with tempfile.TemporaryDirectory(prefix="workshop-ablation-") as temp:
        root = Path(temp)
        base = root / "base.db"
        with sqlite3.connect(settings.db_path) as source, sqlite3.connect(base) as target:
            source.backup(target)
            from lib.db import ensure_case_schema

            target.row_factory = sqlite3.Row
            ensure_case_schema(target)
            target.execute(
                "DELETE FROM refunds WHERE incident_id IN (?,?)",
                ("dana-duplicate-storage", "ravi-spot-capacity"),
            )
        corpus_settings = settings.model_copy(update={"data_dir": root})
        shutil.copy2(base, root / "acme_cloud.db")
        corpus_id = await import_module(f"module_{module}.app.ablation").seed_corpus(
            corpus_settings, corpus_namespace
        )
        reports = []
        hashes = []
        for mode in (False, True):
            branch = "treatment" if mode else "control"
            directory = root / branch
            directory.mkdir()
            shutil.copy2(base, directory / "acme_cloud.db")
            hashes.append(hashlib.sha256((directory / "acme_cloud.db").read_bytes()).hexdigest())
            private = settings.model_copy(update={"data_dir": directory})
            report = await run_sessions(
                scenario,
                module,
                scenario["sessions"],
                settings=private,
                output_settings=settings,
                namespace=f"{branch}-{run_id}",
                run_id=f"{run_id}-{branch}",
                evaluation=True,
                reasoning_retrieval=mode,
                reasoning_namespace=corpus_namespace,
                record_reasoning=False,
            )
            reports.append(report)
        assert hashes[0] == hashes[1]
        comparison = {
            "id": run_id,
            "title": "Reasoning retrieval comparison",
            "module": module,
            "protocol": (
                "Identical private SQL copies; separate message namespaces; one "
                "fixed corpus; branch trace recording disabled."
            ),
            "corpus_namespace": corpus_namespace,
            "corpus_trace_id": corpus_id,
            "initial_sql_hashes": hashes,
            "branches": reports,
            "graph": measured_graph([t for r in reports for t in r["turns"]]),
        }
        save_replay(settings, comparison)
        print(
            (
                "Control/treatment input SQL hashes match. Branches could not "
                "write into the reasoning corpus."
            ),
            flush=True,
        )
        return comparison


async def main():
    from lib.settings import get_settings

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name")
    parser.add_argument("--module", type=int, choices=range(1, 6), required=True)
    parser.add_argument("--restart-beat", action="store_true")
    parser.add_argument("--ablation", action="store_true")
    parser.add_argument("--run-id")
    parser.add_argument("--phase", choices=["head", "tail"])
    args = parser.parse_args()
    settings = get_settings()
    run_id = args.run_id or uuid4().hex
    if args.name in ("s3-default", "s3-ontology"):
        from module_3.app.compare import run_extraction_snapshot

        variant = "default-poleo" if args.name == "s3-default" else "acme_cloud"
        print(
            f"Extracting fixed transcript with {variant}; no conversation or database mutation.",
            flush=True,
        )
        report = await run_extraction_snapshot(settings, variant)
        print(
            f"Snapshot {report['id']} · {report['seconds']}s · choose Saved replay in the UI",
            flush=True,
        )
        return
    if args.name == "s3-enrich":
        from module_3.app.enrichment import enrich_organization

        print(json.dumps(await enrich_organization(settings), indent=2))
        return
    aliases = {"s2-restart": "s2-return"}
    scenario = json.loads((SCENARIOS / f"{aliases.get(args.name, args.name)}.json").read_text())
    if args.ablation:
        if args.module not in (4, 5):
            parser.error("--ablation needs module 4 or 5")
        await run_ablation(scenario, args.module, settings, run_id)
        return
    if args.restart_beat and not args.phase:
        for phase in ("head", "tail"):
            child = await asyncio.create_subprocess_exec(
                sys.executable,
                str(Path(__file__).resolve()),
                args.name,
                "--module",
                str(args.module),
                "--run-id",
                run_id,
                "--phase",
                phase,
            )
            if await child.wait():
                raise SystemExit("Restart child failed; prior results remain saved")
        return
    sessions = scenario["sessions"]
    if args.phase:
        first, *rest = sessions
        sessions = (
            [{**first, "messages": first["messages"][:2]}]
            if args.phase == "head"
            else [{**first, "messages": first["messages"][2:]}, *rest]
        )
    await run_sessions(
        scenario,
        args.module,
        sessions,
        settings=settings,
        namespace=f"replay-{run_id}",
        run_id=run_id,
        append=args.phase == "tail",
    )


if __name__ == "__main__":
    asyncio.run(main())
