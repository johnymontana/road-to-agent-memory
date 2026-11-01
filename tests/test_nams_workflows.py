"""Verify module 5's hosted request choreography without claiming live NAMS parity."""

import json
from types import SimpleNamespace

import httpx
import pytest

from module_5.workflows import distill, drift, seed


def connect(monkeypatch, workflow, handler):
    from lib import settings

    monkeypatch.setattr(
        settings,
        "get_settings",
        lambda: SimpleNamespace(
            nams_base_url="https://nams.test",
            nams_api_key="test-nams-key",
        ),
    )
    real_client = httpx.AsyncClient
    monkeypatch.setattr(
        httpx,
        "AsyncClient",
        lambda **kw: real_client(
            **kw,
            transport=httpx.MockTransport(handler),
        ),
    )


async def test_seed_creates_history_in_dependency_order_and_checks_tool_errors(monkeypatch):
    requests = []

    def handle(request):
        requests.append((request.url.path, json.loads(request.content)))
        path = request.url.path
        if path == "/v1/entities":
            return httpx.Response(200, json={"id": f"entity-{len(requests)}"})
        if path.endswith("/tool-calls"):
            return httpx.Response(500, json={"error": "Cannot write tool call"})
        return httpx.Response(200, json={"id": f"node-{len(requests)}"})

    connect(monkeypatch, seed, handle)
    with pytest.raises(httpx.HTTPStatusError):
        await seed.main()
    paths = [path for path, _ in requests]
    assert paths[:4] == ["/v1/entities"] * 4
    assert paths[4:6] == ["/v1/conversations", "/v1/conversations/node-5/messages/bulk"]
    assert paths[6:] == ["/v1/reasoning/traces", "/v1/reasoning/steps", "/v1/reasoning/tool-calls"]
    payload = requests[-1][1]
    assert json.loads(payload["input"])["customer_email"] == "maya.chen@northwind.example"
    assert isinstance(payload["output"], str)


async def test_distill_handles_review_gate_downloads_and_diffs(monkeypatch, tmp_path, capsys):
    calls = []
    publishes = 0

    def handle(request):
        nonlocal publishes
        path = request.url.path
        calls.append((request.method, path))
        if path == "/v1/skills/generate":
            return httpx.Response(200, json={"runId": "run-1"})
        if path == "/v1/skills/runs/run-1":
            return httpx.Response(200, json={"status": "completed", "skillId": "skill-1"})
        if path.endswith("/publish"):
            publishes += 1
            return httpx.Response(409 if publishes == 1 else 200, json={})
        if path.endswith("/review"):
            assert json.loads(request.content) == {"action": "approve"}
            return httpx.Response(200, json={})
        if path.endswith("/download"):
            return httpx.Response(200, text="# Updated refund procedure")
        raise AssertionError(path)

    connect(monkeypatch, distill, handle)
    monkeypatch.setattr(distill, "OUT_DIR", tmp_path)
    monkeypatch.setattr(distill, "POLL_S", 0)
    (tmp_path / "SKILL.md").write_text("# Old procedure")
    await distill.main(redistill=True)
    assert (tmp_path / "SKILL.md").read_text() == "# Updated refund procedure"
    assert calls[-4:] == [
        ("POST", "/v1/skills/skill-1/publish"),
        ("POST", "/v1/skills/skill-1/review"),
        ("POST", "/v1/skills/skill-1/publish"),
        ("GET", "/v1/skills/skill-1/download"),
    ]
    assert "-# Old procedure" in capsys.readouterr().out


async def test_failed_distillation_poll_does_not_publish(monkeypatch, tmp_path):
    calls = []

    def handle(request):
        calls.append(request.url.path)
        if request.url.path.endswith("/generate"):
            return httpx.Response(200, json={"id": "run-1"})
        return httpx.Response(503, json={"error": "Unavailable"})

    connect(monkeypatch, distill, handle)
    monkeypatch.setattr(distill, "OUT_DIR", tmp_path)
    monkeypatch.setattr(distill, "POLL_S", 0)
    with pytest.raises(httpx.HTTPStatusError):
        await distill.main(redistill=False)
    assert not (tmp_path / "SKILL.md").exists()
    assert not any("publish" in path for path in calls)


async def test_drift_deletes_selected_entity_then_reads_reports(monkeypatch, capsys):
    calls = []

    def handle(request):
        path = request.url.path
        calls.append((request.method, path))
        if path.endswith("/entities/search"):
            return httpx.Response(200, json={"entities": [{"id": "policy", "name": "Pro"}]})
        if request.method == "DELETE":
            return httpx.Response(204)
        if path == "/v1/skills":
            return httpx.Response(200, json={"skills": [{"id": "skill", "name": "refund"}]})
        return httpx.Response(200, json={"flagged_claims": ["Missing policy evidence"]})

    connect(monkeypatch, drift, handle)
    await drift.main()
    assert calls == [
        ("POST", "/v1/entities/search"),
        ("DELETE", "/v1/entities/policy"),
        ("GET", "/v1/skills"),
        ("GET", "/v1/skills/skill/drift"),
    ]
    assert "1 claim(s) lost grounding" in capsys.readouterr().out


def test_nams_check_reports_disabled_skills_without_claiming_lifecycle_success(monkeypatch, capsys):
    from lib import settings
    from module_5.workflows import check

    monkeypatch.setattr(
        settings,
        "get_settings",
        lambda: SimpleNamespace(
            nams_api_key="test-key",
            nams_base_url="https://nams.test",
        ),
    )
    real_client = httpx.Client

    def handle(request):
        assert request.headers["Authorization"] == "Bearer test-key"
        return httpx.Response(200 if request.url.path == "/v1/conversations" else 404, json={})

    monkeypatch.setattr(
        httpx,
        "Client",
        lambda **kw: real_client(
            **kw,
            transport=httpx.MockTransport(handle),
        ),
    )
    assert check.main() == 0
    assert "may be disabled" in capsys.readouterr().out
