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
    assert paths[:7] == ["/v1/entities"] * 5 + [
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
    scoped = [b["userId"] for p, b in requests if p in ("/v1/entities", "/v1/conversations")]
    assert all(user_id == state["userId"] for user_id in scoped)
    policy_id = state["policyEntityId"]
    assert policy_id == "entity-5"
    assert all(policy_id in c["relatedEntityIds"] for c in completions)
    assert all(
        b["touchedEntityIds"] == [policy_id]
        for p, b in requests
        if p.endswith("/tool-calls") and b["toolName"] == "fetch_policy"
    )


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
        archive.writestr(
            "acme-refund-procedure/provenance.json",
            '{"distillationRun": "run-1", "claims": [], "steps": []}',
        )
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
            assert request.url.params["version"] == "sv-2"
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
    (out / "references").mkdir()
    (out / "references" / "obsolete.md").write_text("Previous version only")

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
    assert not (out / "references" / "obsolete.md").exists()
    assert not (tmp_path / "escape.md").exists()
    receipt = json.loads((out / "skill.json").read_text())
    assert receipt["versionId"] == "sv-2" and receipt["conversationId"] == "c1"
    assert "-# Old procedure" in capsys.readouterr().out


@pytest.mark.parametrize("defect", ["skill", "provenance", "wrong_run", "malformed_step"])
def test_invalid_download_keeps_the_previous_package(tmp_path, defect):
    out = tmp_path / "distilled"
    old_receipt = {"runId": "run-1", "versionId": "v1"}
    distill.install_package(skill_zip("Old procedure"), out, old_receipt)
    provenance = {
        "distillationRun": "other-run" if defect == "wrong_run" else "run-2",
        "claims": [],
        "steps": [{}] if defect == "malformed_step" else [],
    }
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        if defect != "skill":
            archive.writestr("skill/SKILL.md", "New procedure")
        if defect != "provenance":
            archive.writestr("skill/provenance.json", json.dumps(provenance))
    with pytest.raises((ValueError, FileNotFoundError)):
        distill.install_package(buffer.getvalue(), out, {"runId": "run-2", "versionId": "v2"})
    assert (out / "SKILL.md").read_text() == "Old procedure"
    assert nams.read_json(out / "skill.json") == old_receipt
    assert nams.read_json(out / "provenance.json")["distillationRun"] == "run-1"


@pytest.mark.parametrize(
    "receipt", [{}, {"skillId": "skill-1"}, {"skillId": "skill-1", "versionId": "v1"}]
)
def test_policy_change_uses_the_exact_downloaded_version(monkeypatch, tmp_path, capsys, receipt):
    from scripts.change_policy import report_drift

    monkeypatch.setattr(nams, "SKILL_DIR", tmp_path)
    if receipt:
        nams.write_json(tmp_path / "skill.json", receipt)
    versions = []

    def read_version(url, *, params, **kwargs):
        versions.append(params["version"])
        assert url == "https://nams.test/v1/skills/skill-1/drift"
        return httpx.Response(200, json={"status": "drifted"}, request=httpx.Request("GET", url))

    monkeypatch.setattr(httpx, "get", read_version)
    report_drift(SimpleNamespace(nams_api_key="test", nams_base_url="https://nams.test"))
    output = capsys.readouterr().out
    if "versionId" in receipt:
        assert versions == ["v1"] and "v1: drifted" in output
    else:
        assert versions == [] and "Hosted drift status unavailable" in output


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
    nams.write_json(tmp_path / "nams-workspace.json", {"conversationId": "c1"})
    with pytest.raises(SystemExit):
        await distill.main(redistill=False)
    assert "/v1/skills/generate" in calls
    assert not any("publish" in path for path in calls)


async def test_distill_requires_seed_and_never_uses_workspace_scope(monkeypatch, tmp_path):
    def unexpected(request):
        pytest.fail(f"Unexpected NAMS request: {request.url.path}")

    connect(monkeypatch, unexpected, tmp_path)
    with pytest.raises(SystemExit, match="make nams-seed"):
        await distill.main(redistill=False)


def drift_receipts(monkeypatch, tmp_path):
    skill_dir = tmp_path / "distilled"
    monkeypatch.setattr(drift, "SKILL_DIR", skill_dir)
    nams.write_json(
        tmp_path / "nams-workspace.json",
        {"conversationId": "c1", "userId": "seed-user", "policyEntityId": "policy"},
    )
    nams.write_json(
        skill_dir / "skill.json",
        {"skillId": "skill-1", "versionId": "v1", "conversationId": "c1", "runId": "r1"},
    )
    nams.write_json(
        skill_dir / "provenance.json",
        {
            "distillationRun": "r1",
            "claims": [
                {
                    "claimId": "c-1",
                    "text": "Pro refunds need no approval",
                    "groundedIn": ["extracted", "maya", "other-user-policy"],
                }
            ],
            "steps": [
                {
                    "id": "step-1",
                    "name": "Check the refund policy",
                    "groundedIn": ["extracted", "step-node"],
                }
            ],
        },
    )
    return skill_dir


async def test_drift_deletes_the_policy_grounding_and_reports_stale_claims(
    monkeypatch, tmp_path, capsys
):
    calls = []
    entities = {
        "maya": {"id": "maya", "name": "Maya Chen", "type": "Person", "userId": "seed-user"},
        "policy": {
            "id": "policy",
            "name": seed.POLICY_NAME,
            "type": "custom",
            "userId": "seed-user",
        },
    }
    entities["extracted"] = {**entities["policy"], "id": "extracted", "type": "Concept"}
    entities["other"] = {**entities["policy"], "id": "other-user-policy", "userId": "another"}

    def handle(request):
        path = request.url.path
        calls.append((request.method, path))
        if path == "/v1/skills/skill-1":
            return httpx.Response(200, json={"skill": {"publishedVersionId": "v1"}})
        if path == "/v1/conversations/c1":
            return httpx.Response(200, json={"userId": "seed-user"})
        if path == "/v1/entities":
            assert request.url.params["userId"] == "seed-user"
            return httpx.Response(200, json={"entities": list(entities.values())})
        if request.method == "DELETE":
            return httpx.Response(200, json={"status": "deleted"})
        assert request.url.params["version"] == "v1"
        report = {
            "status": "drifted",
            "totalClaims": 1,
            "totalSteps": 1,
            "staleClaims": [{"claimId": "c-1", "missingSources": ["extracted"]}],
            "staleSteps": [{"stepId": "step-1", "missingSources": ["extracted"]}],
        }
        return httpx.Response(200, json=report)

    drift_receipts(monkeypatch, tmp_path)
    connect(monkeypatch, handle, tmp_path)
    await drift.main()
    assert [c for c in calls if c[0] == "DELETE"] == [("DELETE", "/v1/entities/extracted")]
    out = capsys.readouterr().out
    assert "status: drifted" in out
    assert "Pro refunds need no approval" in out and "Check the refund policy" in out


@pytest.mark.parametrize(
    "mismatch", ["legacy", "conversation", "run", "uncited", "version", "owner", "foreign-policy"]
)
async def test_drift_refuses_to_delete_unverified_evidence(monkeypatch, tmp_path, mismatch):
    skill_dir = drift_receipts(monkeypatch, tmp_path)
    seed_path = tmp_path / "nams-workspace.json"
    state = nams.read_json(seed_path)
    if mismatch == "legacy":
        del state["userId"]
    if mismatch == "conversation":
        state["conversationId"] = "different-conversation"
    if mismatch == "run":
        receipt = nams.read_json(skill_dir / "skill.json")
        nams.write_json(skill_dir / "skill.json", {**receipt, "runId": "old-run"})
    nams.write_json(seed_path, state)

    def handle(request):
        assert request.method == "GET"
        if request.url.path == "/v1/skills/skill-1":
            version = "new-v2" if mismatch == "version" else "v1"
            return httpx.Response(200, json={"skill": {"publishedVersionId": version}})
        if request.url.path == "/v1/conversations/c1":
            return httpx.Response(
                200, json={"userId": "other" if mismatch == "owner" else "seed-user"}
            )
        assert request.url.path == "/v1/entities" and mismatch in ("uncited", "foreign-policy")
        owner = "other" if mismatch == "foreign-policy" else "seed-user"
        entities = [{"id": "policy", "name": seed.POLICY_NAME, "userId": owner}]
        return httpx.Response(200, json={"entities": entities})

    connect(monkeypatch, handle, tmp_path)
    with pytest.raises(SystemExit):
        await drift.main()


@pytest.mark.parametrize("failure", ["disabled", "missing", "network", "capability-timeout"])
def test_nams_check_stops_hosted_route_and_prints_fallback(monkeypatch, capsys, failure):
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
        if failure == "network":
            raise httpx.ConnectError("offline", request=request)
        if request.url.path == "/v1/conversations":
            return httpx.Response(200, json={})
        if failure == "capability-timeout":
            raise httpx.ReadTimeout("timeout", request=request)
        return httpx.Response(404 if failure == "missing" else 200, json={"distillation": False})

    monkeypatch.setattr(
        httpx, "Client", lambda **kw: real_client(**kw, transport=httpx.MockTransport(handle))
    )
    assert check.main() == 1
    assert "make s5-fresh-agent WITH_SKILL=fallback" in capsys.readouterr().out


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


async def test_seed_explains_an_ontology_rejection(monkeypatch, tmp_path):
    """A workspace whose active ontology requires extra properties rejects the plain seed."""
    paths = []

    def handle(request):
        paths.append(request.url.path)
        assert request.url.path == "/v1/entities"
        rejection = {
            "active_ontology": {"id": "ont_7433bcbb406b", "revision": 1},
            "error": "schema_violation",
            "message": 'Type "person" is missing required properties: customer_id',
            "missing_properties": ["customer_id"],
        }
        return httpx.Response(422, json=rejection)

    connect(monkeypatch, handle, tmp_path)
    with pytest.raises(SystemExit) as stop:
        await seed.main()
    message = str(stop.value)
    assert "Maya Chen" in message and "ont_7433bcbb406b" in message
    assert "make nams-check" in message and "WITH_SKILL=fallback" in message
    assert paths == ["/v1/entities"]
    assert not nams.seed_state_path(SimpleNamespace(data_dir=tmp_path)).exists()


RIDGELINE = {
    "ontology": {
        "domain": {"name": "ridgeline-hardware-context"},
        "entity_types": [
            {
                "label": "person",
                "properties": [{"name": "customer_id", "required": True}, {"name": "email"}],
            },
            {"label": "project", "properties": [{"name": "status", "required": True}]},
        ],
    },
    "version": {"ontology_id": "ont_7433bcbb406b", "validation_mode": "review"},
}
AGENT_MEMORY = {
    "ontology": {
        "domain": {"name": "agent-memory"},
        "entity_types": [{"label": "person", "properties": [{"name": "email"}]}],
    },
    "version": {"validation_mode": "review"},
}


@pytest.mark.parametrize(
    "workspace", ["default", "compatible", "conflict", "strict-undeclared", "foreign-package"]
)
def test_nams_check_reads_ontology_and_package(monkeypatch, tmp_path, capsys, workspace):
    from lib import settings
    from module_5.workflows import check

    monkeypatch.setattr(
        settings,
        "get_settings",
        lambda: SimpleNamespace(nams_api_key="test-key", nams_base_url="https://nams.test"),
    )
    monkeypatch.setattr(check, "SKILL_DIR", tmp_path)
    if workspace == "foreign-package":
        nams.write_json(tmp_path / "skill.json", {"skillId": "sk-other", "versionId": "sv-9"})
    real_client = httpx.Client

    def handle(request):
        path = request.url.path
        if path == "/v1/conversations":
            return httpx.Response(200, json={"conversations": []})
        if path == "/v1/skills/capabilities":
            gates = {"distillation": True, "groundingThreshold": 0.9, "coverageThreshold": 0.6}
            return httpx.Response(200, json=gates)
        if path == "/v1/ontologies/active":
            if workspace == "default":
                return httpx.Response(404, json={"error": "no active ontology"})
            if workspace == "conflict":
                return httpx.Response(200, json=RIDGELINE)
            if workspace == "strict-undeclared":
                strict = {**AGENT_MEMORY, "version": {"validation_mode": "strict"}}
                return httpx.Response(200, json=strict)
            return httpx.Response(200, json=AGENT_MEMORY)
        if path == "/v1/skills":
            skills = [{"id": "sk-1", "name": "acme-refund-procedure", "status": "published"}]
            return httpx.Response(200, json={"skills": skills if workspace != "default" else []})
        if path == "/v1/skills/sk-other":
            return httpx.Response(404, json={"error": "skill not found"})
        raise AssertionError(path)

    monkeypatch.setattr(
        httpx, "Client", lambda **kw: real_client(**kw, transport=httpx.MockTransport(handle))
    )
    code = check.main()
    out = capsys.readouterr().out
    if workspace in ("conflict", "strict-undeclared"):
        assert code == 1
        assert "would reject make nams-seed" in out
        assert "WITH_SKILL=fallback" in out
        if workspace == "conflict":
            assert "person requires customer_id" in out and "project" not in out
        else:
            assert "organization is not declared" in out
        return
    assert code == 0, out
    assert "distillation enabled" in out
    if workspace == "default":
        assert "Default ontology" in out and "No acme-refund-procedure skill" in out
    else:
        assert "agent-memory" in out and "accepts the seed" in out
        assert "acme-refund-procedure: published" in out
    if workspace == "foreign-package":
        assert "not in this workspace" in out and "HTTP 404" in out
    else:
        assert "not in this workspace" not in out
