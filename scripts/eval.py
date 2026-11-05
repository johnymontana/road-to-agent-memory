#!/usr/bin/env python3
"""Controlled retrieval probes: isolated SQL and namespaced memory, no action tools."""

from __future__ import annotations

import argparse
import asyncio
import json
import sqlite3
import sys
import tempfile
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def grade_answer(question, answer):
    checks = []
    try:
        value = json.loads(
            answer.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        )
        if not isinstance(value, dict):
            raise ValueError("object required")
    except (ValueError, TypeError):
        return {"answered": False, "checks": ["valid JSON object: failed"], "sources": []}
    for key, expected in question["expected"].items():
        matches = (
            isinstance(value.get(key), str)
            and value[key].strip().casefold() == str(expected).strip().casefold()
        )
        checks.append((key, matches))
    sources = value.get("source_ids", [])
    if not isinstance(sources, list):
        sources = []
    valid_sources = [s for s in sources if s in question["source_ids"]]
    checks.append(("verified source ID", bool(valid_sources)))
    return {
        "answered": all(passed for _, passed in checks),
        "checks": [f"{name}: {'pass' if passed else 'fail'}" for name, passed in checks],
        "sources": valid_sources,
    }


def save_report(path, report):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(report, indent=2, default=str))
    temporary.replace(path)


async def seed_fixture(chat, namespace, name, email, phrase, date, quote, reference):
    from neo4j_agent_memory.schema.models import EntityRef, TraceOutcome

    ids = {"message": [], "entity": [], "trace": []}
    if chat.memory is None:
        return ids
    session = f"{namespace}:history"
    await chat.memory.short_term.create_conversation(session)
    mentions = []
    if chat.module >= 3:
        entity, _ = await chat.memory.long_term.add_entity(
            name,
            "PERSON",
            subtype="CUSTOMER",
            description=f"Customer {name}; email {email}; signup_date {date}. Source: isolated SQLite fixture.",
            attributes={"email": email, "signup_date": date, "hydrated_from": "sqlite:customers"},
            resolve=False,
            deduplicate=False,
            enrich=False,
        )
        mentions = [EntityRef(id=str(entity.id))]
        ids["entity"] = [str(entity.id)]
    message = await chat.memory.short_term.add_message(
        session,
        "user",
        f"I am {name}; my email is {email}. My verification phrase is {phrase}.",
        extraction_mode="explicit",
        explicit_mentions=mentions,
        extract_entities=False,
    )
    ids["message"] = [str(message.id)]
    if chat.module >= 3:
        # Hydrate only the unique fixture Customer, never a participant's profile.
        from importlib import import_module

        hydration = import_module(f"module_{chat.module}.app.hydrate")
        await hydration.hydrate_session_entities(
            chat.memory,
            session,
            chat.settings.db_path,
            message_id=message.id,
            writer=chat.writer,
        )
    if chat.module >= 4:
        trace = await chat.memory.reasoning.start_trace(
            f"{namespace}:fixed-corpus", f"Recorded approval decision {reference}"
        )
        await chat.memory.reasoning.add_step(
            trace.id, action="refund_policy_guard", observation=quote, generate_embedding=False
        )
        await chat.memory.reasoning.complete_trace(
            trace.id,
            outcome=TraceOutcome(
                success=False,
                summary=json.dumps(
                    {
                        "reply": quote,
                        "business_status": "rejected_over_limit",
                        "execution_status": "succeeded",
                    }
                ),
                error_kind="policy_declined",
            ),
        )
        ids["trace"] = [str(trace.id)]
    return ids


async def run_eval(chat, questions=None, *, on_result=None):
    """Run already-prepared probes; every question retains success/error independently."""
    if questions is None:
        raise ValueError("Use run_isolated_eval to create controlled fixtures first")
    results = []
    for question in questions:
        try:
            result = await chat.chat(
                question["question"], session_id=question["session"], request_id=uuid4().hex
            )
            grade = grade_answer(question, result["reply"])
            item = {
                k: v for k, v in question.items() if k not in ("expected", "source_ids", "session")
            }
            item.update(
                grade,
                answer=result["reply"],
                warnings=result.get("warnings", []),
                timing=result.get("timing", {}),
            )
            if result.get("status") == "failed":
                item["error"] = "Agent execution failed; see operation receipt"
        except Exception as error:
            item = {
                "id": question["id"],
                "question": question["question"],
                "answered": False,
                "error": type(error).__name__,
                "checks": ["request failed"],
                "sources": [],
            }
        results.append(item)
        if on_result:
            on_result(results)
    return {"questions": results}


async def run_isolated_eval(module, settings, *, run_id=None, output_path=None):
    from lib.workshop import open_agent

    run_id = run_id or uuid4().hex
    namespace = f"eval-{run_id}"
    output_path = output_path or settings.data_dir / "evaluations" / f"{run_id}.json"
    report = {
        "id": run_id,
        "module": module,
        "status": "running",
        "questions": [],
        "protocol": "Controlled seeded retrieval; no business tools; extraction verified separately.",
        "namespace": namespace,
    }
    save_report(output_path, report)
    try:
        with tempfile.TemporaryDirectory(prefix="workshop-eval-") as temp:
            folder = Path(temp)
            with (
                sqlite3.connect(settings.db_path) as source,
                sqlite3.connect(folder / "acme_cloud.db") as target,
            ):
                source.backup(target)
            name = f"Maya Eval{run_id[:10]}"
            email = f"maya.{run_id[:10]}@workshop.example"
            phrase = f"compass-{run_id[10:20]}"
            quote = f"Policy decision {run_id[20:30]}: $400 exceeds Pro $250; approval required."
            date = "2025-03-14"
            reference = run_id[20:30]
            with sqlite3.connect(folder / "acme_cloud.db") as db:
                db.execute(
                    "UPDATE customers SET name=?,email=? WHERE email='maya.chen@northwind.example'",
                    (name, email),
                )
            isolated = settings.model_copy(
                update={"data_dir": folder, "memory_namespace": namespace}
            )
            options = {"business_tools": False, "evaluation": True}
            if module >= 4:
                options.update(record_reasoning=False, reasoning_namespace=namespace)
            async with open_agent(module, isolated, **options) as chat:
                ids = await seed_fixture(
                    chat, namespace, name, email, phrase, date, quote, reference
                )

                def probe(identifier, text, fields, expected, sources, first, session):
                    return {
                        "id": identifier,
                        "question": text
                        + " Return ONLY JSON with fields "
                        + ", ".join(fields)
                        + ", source_ids (array of evidence IDs); use null for unknown fields.",
                        "expected": expected,
                        "source_ids": sources,
                        "expected_from_module": first,
                        "session": f"{namespace}:{session}",
                    }

                questions = [
                    probe(
                        "q1",
                        f"What name and email did the customer {name} provide?",
                        ["name", "email"],
                        {"name": name, "email": email},
                        ids["message"] + ids["entity"],
                        2,
                        "identity",
                    ),
                    probe(
                        "q2",
                        "What is my exact verification phrase from this conversation?",
                        ["verification_phrase"],
                        {"verification_phrase": phrase},
                        ids["message"],
                        2,
                        "history",
                    ),
                    probe(
                        "q3",
                        f"What is the grounded signup date for {name}?",
                        ["signup_date"],
                        {"signup_date": date},
                        ids["entity"],
                        3,
                        "account",
                    ),
                    probe(
                        "q4",
                        f"Recall the recorded approval decision {reference}. What is the exact refusal quote?",
                        ["refusal_quote"],
                        {"refusal_quote": quote},
                        ids["trace"],
                        4,
                        "procedure",
                    ),
                ]

                def progress(results):
                    report["questions"] = results.copy()
                    save_report(output_path, report)

                outcome = await run_eval(chat, questions, on_result=progress)
                report.update(
                    outcome,
                    status="completed_with_errors"
                    if any(q.get("error") for q in outcome["questions"])
                    else "completed",
                )
    except asyncio.CancelledError:
        report.update(
            status="interrupted", error="Server stopped; completed questions were retained"
        )
    except Exception as error:
        report.update(status="failed", error=type(error).__name__)
    save_report(output_path, report)
    return report


async def main():
    from lib.settings import get_settings

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--module", type=int, choices=range(1, 6), default=1)
    args = parser.parse_args()
    report = await run_isolated_eval(args.module, get_settings())
    print(f"Controlled retrieval scorecard — module {args.module} ({report['id']})")
    print(
        "SQL copy + unique memory fixtures; business tools disabled; not an end-to-end quality grade."
    )
    for q in report["questions"]:
        print(
            f"{'PASS' if q['answered'] else 'ERROR' if q.get('error') else 'UNKNOWN'} {q['id']}: {q['checks']} sources={q['sources']}"
        )
    print(f"{sum(q['answered'] for q in report['questions'])}/4 checks · {report['status']}")
    if report["status"] in ("failed", "completed_with_errors"):
        raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(main())
