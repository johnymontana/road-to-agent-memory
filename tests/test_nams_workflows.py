"""Module 5's hosted request choreography against the published NAMS contract.

Mocks follow https://memory.neo4jlabs.com/openapi.json and responses observed live
(run statuses, the zipped skill package, drift reports). They check our requests,
not the hosted service itself; `make nams-*` against a real workspace does that.
"""

import io
import json
import zipfile
from types import SimpleNamespace

import httpx
import pytest

from module_5.workflows import distill, drift, nams, seed


def connect(monkeypatch, handler, tmp_path):
    from lib import settings

    monkeypatch.setattr(
        settings,
        "get_settings",
        lambda: SimpleNamespace(
            nams_base_url="https://nams.test", nams_api_key="test-nams-key", data_dir=tmp_path
        ),
    )
    real_client = httpx.AsyncClient
    monkeypatch.setattr(
        httpx,
        "AsyncClient",
        lambda **kw: real_client(**kw, transport=httpx.MockTransport(handler)),
    )


def body(request):
    return json.loads(request.content) if request.content else None


async def test_seed_writes_completed_traces_and_records_the_conversation(monkeypatch, tmp_path):
    requests = []

    def handle(request):
        path = request.url.path
        requests.append((path, body(request)))
        if path == "/v1/entities":
            return httpx.Response(201, json={"id": f"entity-{len(requests)}"})
        if path == "/v1/conversations":
            return httpx.Response(201, json={"id": "conv-1"})
        if path.endswith("/messages/bulk"):
            return httpx.Response(201, json={"messages": [{"id": "msg-1"}]})
        return httpx.Response(201, json={"id": f"node-{len(requests)}"})

    connect(monkeypatch, handle, tmp_path)
    await seed.main()
    paths = [path for path, _ in requests]
    assert paths[:6] == ["/v1/entities"] * 4 + [
        "/v1/conversations",
        "/v1/conversations/conv-1/messages/bulk",
    ]
    traces = [b for p, b in requests if p == "/v1/reasoning/traces"]
    assert traces[0]["triggeredByMessageId"] == "msg-1"
    tool_call = next(b for p, b in requests if p == "/v1/reasoning/tool-calls")
    assert json.loads(tool_call["input"])["customer_email"] == "maya.chen@northwind.example"
    assert isinstance(tool_call["output"], str)  # NAMS wants JSON-encoded strings.
    completions = [b for p, b in requests if p.endswith("/complete")]
    assert len(completions) == len(seed.TRACES) and all(c["success"] for c in completions)
    state = json.loads(nams.seed_state_path(SimpleNamespace(data_dir=tmp_path)).read_text())
    assert state["conversationId"] == "conv-1"


async def test_seed_stops_on_the_first_failed_write(monkeypatch, tmp_path):
    def handle(request):
        if request.url.path.endswith("/tool-calls"):
            return httpx.Response(500, json={"error": "Cannot write tool call"})
        if request.url.path.endswith("/messages/bulk"):
            return httpx.Response(201, json={"messages": [{"id": "msg-1"}]})
        return httpx.Response(201, json={"id": "node"})

    connect(monkeypatch, handle, tmp_path)
    with pytest.raises(httpx.HTTPStatusError):
        await seed.main()
    assert not nams.seed_state_path(SimpleNamespace(data_dir=tmp_path)).exists()


def skill_zip(text):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("acme-refund-procedure/SKILL.md", text)
        archive.writestr("acme-refund-procedure/provenance.json", '{"claims": [], "steps": []}')
        archive.writestr("acme-refund-procedure/references/procedures.md", "steps")
        archive.writestr("acme-refund-procedure/../escape.md", "outside")
    return buffer.getvalue()


async def test_distill_scopes_to_the_seed_versions_the_skill_and_unpacks(
    monkeypatch, tmp_path, capsys
):
    calls = []

    def handle(request):
        path = request.url.path
        calls.append((request.method, path, body(request)))
        if path == "/v1/skills":
            skills = [
                {"id": "draft", "name": "acme-refund-procedure", "status": "draft"},
                {"id": "skill-1", "name": "acme-refund-procedure", "status": "published"},
            ]
            return httpx.Response(200, json={"skills": skills})
        if path == "/v1/skills/generate":
            return httpx.Response(202, json={"runId": "run-1", "status": "queued"})
        if path == "/v1/skills/runs/run-1":
            run = {"id": "run-1", "status": "succeeded", "skillId": "skill-1", "error": ""}
            run.update(skillVersionId="sv-2", groundingScore=1, coverageScore=0.9, failCode="")
            return httpx.Response(200, json=run)
        if path.endswith("/review"):
            return httpx.Response(200, json={"reviewStatus": "approved"})
        if path.endswith("/publish"):
            return httpx.Response(200, json={"status": "published"})
        if path.endswith("/download"):
            return httpx.Response(200, content=skill_zip("# Updated refund procedure"))
        raise AssertionError(path)

    connect(monkeypatch, handle, tmp_path)
    nams.write_json(
        nams.seed_state_path(SimpleNamespace(data_dir=tmp_path)), {"conversationId": "c1"}
    )
    out = tmp_path / "distilled"
    monkeypatch.setattr(distill, "OUT_DIR", out)
    monkeypatch.setattr(distill, "POLL_S", 0)
    out.mkdir()
    (out / "SKILL.md").write_text("# Old procedure")
    (out / "skill.json").write_text('{"skillId": "skill-1"}')

    await distill.main(redistill=True)

    generate = next(b for m, p, b in calls if p == "/v1/skills/generate")
    assert generate == {
        "nameHint": "acme-refund-procedure",
        "scope": {"type": "conversations", "conversationIds": ["c1"]},
        "skillId": "skill-1",  # The published skill, not the stray draft.
    }
    review = next(b for m, p, b in calls if p.endswith("/review"))
    assert review["decision"] == "approve"
    assert [p for m, p, b in calls][-3:] == [
        "/v1/skills/skill-1/review",
        "/v1/skills/skill-1/publish",
        "/v1/skills/skill-1/download",
    ]
    assert (out / "SKILL.md").read_text() == "# Updated refund procedure"
    assert (out / "references" / "procedures.md").exists()
    assert not (tmp_path / "escape.md").exists()
    assert json.loads((out / "skill.json").read_text())["versionId"] == "sv-2"
    assert "-# Old procedure" in capsys.readouterr().out


async def test_failed_distillation_does_not_publish(monkeypatch, tmp_path):
    calls = []

    def handle(request):
        calls.append(request.url.path)
        if request.url.path == "/v1/skills":
            return httpx.Response(200, json={"skills": []})
        if request.url.path.endswith("/generate"):
            return httpx.Response(202, json={"runId": "run-1", "status": "queued"})
        return httpx.Response(200, json={"id": "run-1", "status": "failed", "error": "no traces"})

    connect(monkeypatch, handle, tmp_path)
    monkeypatch.setattr(distill, "OUT_DIR", tmp_path / "distilled")
    monkeypatch.setattr(distill, "POLL_S", 0)
    with pytest.raises(SystemExit):
        await distill.main(redistill=False)
    assert not any("publish" in path for path in calls)


async def test_drift_deletes_the_policy_grounding_and_reports_stale_claims(
    monkeypatch, tmp_path, capsys
):
    calls = []
    entities = {
        "maya": {"id": "maya", "name": "Maya Chen", "type": "Person"},
        "policy": {"id": "policy", "name": "refund policy", "type": "Concept"},
    }

    def handle(request):
        path = request.url.path
        calls.append((request.method, path))
        if request.method == "GET" and path.startswith("/v1/entities/"):
            entity = entities.get(path.rsplit("/", 1)[1])
            return httpx.Response(200 if entity else 404, json=entity or {"error": "not found"})
        if request.method == "DELETE":
            return httpx.Response(200, json={"status": "deleted"})
        report = {
            "status": "drifted",
            "totalClaims": 1,
            "totalSteps": 1,
            "staleClaims": [{"claimId": "c-1", "missingSources": ["policy"]}],
            "staleSteps": [{"stepId": "step-1", "missingSources": ["policy"]}],
        }
        return httpx.Response(200, json=report)

    skill_dir = tmp_path / "distilled"
    monkeypatch.setattr(drift, "SKILL_DIR", skill_dir)
    nams.write_json(skill_dir / "skill.json", {"skillId": "skill-1"})
    nams.write_json(
        skill_dir / "provenance.json",
        {
            "claims": [
                {
                    "claimId": "c-1",
                    "text": "Pro refunds need no approval",
                    "groundedIn": ["policy", "maya"],
                }
            ],
            "steps": [
                {
                    "id": "step-1",
                    "name": "Check the refund policy",
                    "groundedIn": ["policy", "step-node"],
                }
            ],
        },
    )
    connect(monkeypatch, handle, tmp_path)
    await drift.main()
    # Only the policy entity is deleted, even though the customer also grounds a claim.
    assert [c for c in calls if c[0] == "DELETE"] == [("DELETE", "/v1/entities/policy")]
    out = capsys.readouterr().out
    assert "status: drifted" in out
    assert "Pro refunds need no approval" in out and "Check the refund policy" in out


def test_nams_check_reports_disabled_skills_without_claiming_lifecycle_success(monkeypatch, capsys):
    from lib import settings
    from module_5.workflows import check

    monkeypatch.setattr(
        settings,
        "get_settings",
        lambda: SimpleNamespace(nams_api_key="test-key", nams_base_url="https://nams.test"),
    )
    real_client = httpx.Client

    def handle(request):
        assert request.headers["Authorization"] == "Bearer test-key"
        return httpx.Response(200 if request.url.path == "/v1/conversations" else 404, json={})

    monkeypatch.setattr(
        httpx, "Client", lambda **kw: real_client(**kw, transport=httpx.MockTransport(handle))
    )
    assert check.main() == 0
    assert "may be disabled" in capsys.readouterr().out


async def test_nams_graph_reads_object_rows_and_hides_large_documents(monkeypatch):
    from lib import graph

    row = {
        "nodes": [
            {"id": "s", "labels": ["Skill"], "properties": {"name": "refund"}},
            {"id": "v", "labels": ["SkillVersion"], "properties": {"skillMd": "# big", "id": "v1"}},
        ],
        "relationships": [
            {"id": "r", "from": "s", "to": "v", "type": "HAS_VERSION"},
            {"id": "x", "from": "v", "to": "hidden", "type": "GROUNDED_IN"},
        ],
        "truncated": False,
    }
    real_client = httpx.AsyncClient

    def handle(request):
        assert request.url.path == "/v1/query"
        return httpx.Response(200, json={"columns": list(row), "rows": [row]})

    monkeypatch.setattr(
        httpx, "AsyncClient", lambda **kw: real_client(**kw, transport=httpx.MockTransport(handle))
    )
    settings = SimpleNamespace(nams_api_key="k", nams_base_url="https://nams.test")
    result = await graph.nams_graph(settings)
    assert [n["id"] for n in result["nodes"]] == ["s", "v"]
    assert "skillMd" not in result["nodes"][1]["properties"]
    assert [r["id"] for r in result["relationships"]] == ["r"]
