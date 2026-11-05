"""Cold Vite/NVL transport and participant controls, with explicit HTTP fixtures."""

import json
import os
import subprocess
import time
import urllib.request
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

pytestmark = pytest.mark.skipif(os.environ.get("RUN_UI") != "1", reason="RUN_UI=1 browser check")
ROOT = Path(__file__).resolve().parents[1]


def test_cold_workers_startup_sessions_and_retained_trace(tmp_path):
    with (tmp_path / "vite.log").open("w") as log:
        server = subprocess.Popen(
            [
                "npm",
                "--prefix",
                "web",
                "run",
                "dev",
                "--",
                "--port",
                "5183",
                "--strictPort",
                "--force",
            ],
            cwd=ROOT,
            stdout=log,
            stderr=log,
        )
        try:
            for _ in range(100):
                try:
                    urllib.request.urlopen("http://localhost:5183", timeout=1)
                    break
                except OSError:
                    time.sleep(0.1)
            with sync_playwright() as pw:
                browser = pw.chromium.launch()
                workers = []
                cdp = browser.new_browser_cdp_session()
                cdp.on(
                    "Target.targetCreated",
                    lambda event: (
                        workers.append(event["targetInfo"]["url"])
                        if event["targetInfo"]["type"] == "shared_worker"
                        else None
                    ),
                )
                cdp.send("Target.setDiscoverTargets", {"discover": True})
                page = browser.new_page(viewport={"width": 1600, "height": 1000})
                page.add_init_script("""
                    window.drawnGraphLabels=[];
                    const originalFillText=CanvasRenderingContext2D.prototype.fillText;
                    CanvasRenderingContext2D.prototype.fillText=function(text,...rest){
                      if(String(text).includes('Fixture') &&
                         this.canvas.width>0 && this.canvas.height>0)
                        window.drawnGraphLabels.push(String(text));
                      return originalFillText.call(this,text,...rest);
                    };
                """)
                errors = []
                counts = {"health": 0, "chat": 0, "eval": 0}
                requests = []
                fixture_module = 2
                page.on(
                    "pageerror",
                    lambda error: (
                        errors.append(str(error)),
                        print("BROWSER ERROR:", error, flush=True),
                    ),
                )
                page.on(
                    "console",
                    lambda message: (
                        print("CONSOLE:", message.text, flush=True)
                        if message.type == "error"
                        else None
                    ),
                )
                page.on(
                    "response",
                    lambda response: (
                        workers.append((response.url, response.status))
                        if ".worker" in response.url
                        else None
                    ),
                )
                graph = {
                    "nodes": [
                        {
                            "id": str(i),
                            "labels": ["Message"],
                            "properties": {"content": f"Fixture node {i}"},
                        }
                        for i in range(3)
                    ],
                    "relationships": [
                        {"id": f"e{i}", "from": str(i), "to": str(i + 1), "type": "NEXT"}
                        for i in range(2)
                    ],
                }

                def api(route):
                    path = route.request.url.split("/api/")[1]
                    data = {}
                    status = 200
                    if path == "health":
                        counts["health"] += 1
                        if counts["health"] == 1:
                            status = 503
                        data = {"module": fixture_module, "memory_layers": ["short_term"]}
                    elif path == "graph/nams":
                        data = {"nodes": [], "relationships": [], "unavailable": True}
                    elif path.startswith("graph"):
                        data = graph
                    elif path == "accounts":
                        data = [{"email": "maya@example.test", "name": "Maya"}]
                    elif path == "cases":
                        data = [
                            {
                                "id": "case-1",
                                "email": "maya@example.test",
                                "customer": "Maya",
                                "plan": "Pro",
                                "amount": 49,
                                "description": "Duplicate charge",
                            }
                        ]
                    elif path == "replays":
                        data = {
                            "runs": [
                                {
                                    "id": "cli",
                                    "title": "Fixture replay",
                                    "module": 2,
                                    "session_ids": ["m2-cli"],
                                }
                            ]
                        }
                    elif path.startswith("replays/"):
                        data = {
                            "id": "cli",
                            "title": "Fixture replay",
                            "graph": graph,
                            "protocol": "Saved measured fixture",
                            "turns": [
                                {
                                    "message": "Which phrase did I give you?",
                                    "result": {
                                        "request_id": "cli-op",
                                        "reply": "Violet comet.",
                                        "context": {"evidence": [{"source_id": "cli-message-17"}]},
                                    },
                                }
                            ],
                        }
                    elif path == "chat":
                        counts["chat"] += 1
                        body = route.request.post_data_json
                        requests.append(body)
                        data = {
                            "reply": "**Pro** account",
                            "session_id": body["session_id"],
                            "request_id": body["request_id"],
                            "tool_calls": [
                                {
                                    "name": "lookup_account",
                                    "input": {},
                                    "output": {"plan": "Pro"},
                                    "sql": "SELECT plan FROM customers",
                                    "duration_ms": 1,
                                }
                            ]
                            if counts["chat"] == 1
                            else [],
                            "context": {"evidence": []},
                            "warnings": [],
                            "execution_status": "succeeded",
                            "business_status": "no_action",
                            "timing": {},
                        }
                    elif path.startswith("eval"):
                        if route.request.method == "POST":
                            counts["eval"] += 1
                        data = {"runs": [], "status": "running", "questions": []}
                    route.fulfill(
                        status=status, content_type="application/json", body=json.dumps(data)
                    )

                page.route("**/api/**", api)
                page.goto("http://localhost:5183")
                page.get_by_role("button", name="New conversation").wait_for(state="visible")
                page.wait_for_function("!document.querySelector('.starting-banner')")
                assert counts["health"] >= 2
                page.get_by_label("Graph view").select_option("replay:cli")
                page.wait_for_function(
                    "document.querySelector('.graph-"
                    "notice')?.textContent.includes('saved projection')"
                )
                assert page.get_by_label("Memory layer").is_disabled()
                evidence_panel = page.locator(".trace-panel")
                evidence_panel.get_by_text("Retrieved evidence and memory writes").click()
                assert "cli-message-17" in page.locator(".trace-panel").inner_text()
                page.get_by_label("Graph view").select_option("session:m2-cli")
                assert not page.get_by_label("Memory layer").is_disabled()
                page.wait_for_function(
                    "document.querySelector('.graph-notice')?.textContent.includes('m2-cli')"
                )
                evidence_panel.get_by_text("Execution evidence · browser conversation").wait_for()
                assert "cli-message-17" not in page.locator(".trace-panel").inner_text()
                page.locator(".graph-accessible-list summary").click()
                page.get_by_role("button", name="Fixture node 1", exact=True).focus()
                page.keyboard.press("Enter")
                assert page.locator(".details-drawer").inner_text().find("Fixture node 1") >= 0
                page.get_by_role("button", name="Outgoing · NEXT · Fixture node 2").click()
                assert page.locator(".details-header strong").inner_text() == "Fixture node 2"
                page.get_by_role("button", name="Incoming · NEXT · Fixture node 1").click()
                assert page.locator(".details-header strong").inner_text() == "Fixture node 1"
                page.get_by_role("button", name="Close node details").click()
                page.get_by_label("Billing case", exact=True).select_option("case-1")
                page.get_by_label("Authorize selected refund for this message").check()
                textbox = page.get_by_role("textbox")
                for text in ("Look up my account", "Thank you"):
                    textbox.fill(text)
                    page.get_by_role("button", name="Send", exact=True).click()
                    page.wait_for_function("!document.querySelector('#chat-message').disabled")
                assert [r["authorize_refund"] for r in requests] == [True, False]
                assert requests[0]["account_email"] == "maya@example.test"
                assert not page.get_by_label(
                    "Authorize selected refund for this message"
                ).is_checked()
                assert page.locator(".chat-panel strong").first.inner_text() == "Pro"
                assert page.locator(".trace-details").count() == 2
                page.locator(".trace-details").first.locator("summary").first.click()
                assert "lookup_account" in page.locator(".trace-panel").inner_text()
                page.reload()
                page.wait_for_function("!document.querySelector('.starting-banner')")
                assert "Pro account" in page.locator(".chat-panel").inner_text()
                previous = page.get_by_label("Resume conversation").input_value()
                page.get_by_role("button", name="New conversation").click()
                assert page.locator(".chat-empty").is_visible()
                page.get_by_label("Resume conversation").select_option(previous)
                assert "Pro account" in page.locator(".chat-panel").inner_text()
                page.get_by_role("button", name="Evaluation lab").click()
                assert counts["eval"] == 0
                page.get_by_role("button", name="Start new isolated evaluation").click()
                page.wait_for_timeout(100)
                assert counts["eval"] == 1
                page.get_by_role("button", name="Close evaluation").click()
                page.get_by_role("button", name="Evaluation lab").click()
                page.wait_for_timeout(100)
                assert counts["eval"] == 1
                page.get_by_role("button", name="Close evaluation").click()
                page.set_viewport_size({"width": 390, "height": 844})
                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
                page.wait_for_timeout(1500)
                assert page.evaluate("window.drawnGraphLabels.length > 0"), (
                    "NVL node captions were not drawn"
                )
                fixture_module = 5
                page.reload()
                page.get_by_label("Graph view").select_option("replay:cli")
                page.get_by_role("checkbox", name="NAMS").check()
                page.get_by_text("NAMS workspace unavailable", exact=False).wait_for()
                graph_view = page.get_by_label("Graph view")
                assert graph_view.is_disabled()
                assert page.locator(".graph-notice").count() == 0
                page.get_by_role("checkbox", name="NAMS").uncheck()
                evidence_panel.get_by_text("Fixture replay", exact=True).wait_for()
                fixture_module = 1
                page.reload()
                graph_view.locator("option[value='replay:cli']").wait_for(state="attached")
                assert graph_view.locator("option[value^='session:']").count() == 0
                assert workers, "No NVL worker request was exercised"
                for worker in workers:
                    if isinstance(worker, tuple):
                        assert worker[1] == 200, worker
                    else:
                        assert urllib.request.urlopen(worker, timeout=10).status == 200
                assert not errors, errors
                browser.close()
        finally:
            server.terminate()
            server.wait(timeout=10)
