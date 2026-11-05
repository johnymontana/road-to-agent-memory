from types import SimpleNamespace
from unittest.mock import AsyncMock

from neo4j_agent_memory.extraction import ExtractedEntity, ExtractionResult

from lib.settings import AppSettings
from module_3.lab.compare import run_extraction_snapshot


async def test_comparison_is_immutable_and_uses_one_fixed_transcript(tmp_path):
    extractor = SimpleNamespace(
        extract=AsyncMock(
            return_value=ExtractionResult(
                entities=[ExtractedEntity(name="Maya Chen", type="PERSON", subtype="CUSTOMER")]
            )
        )
    )
    settings = AppSettings(_env_file=None, data_dir=tmp_path)
    first = await run_extraction_snapshot(settings, "acme_cloud", extractor=extractor)
    again = await run_extraction_snapshot(settings, "acme_cloud", extractor=extractor)
    assert first["id"] != again["id"]
    assert first["transcript_sha256"] == again["transcript_sha256"]
    assert "Customer" in first["graph"]["nodes"][1]["labels"]
    assert (tmp_path / "replays" / f"{first['id']}.json").exists()


async def test_same_name_typed_mentions_do_not_reassign_relationships(tmp_path):
    from neo4j_agent_memory.extraction import ExtractedRelation

    settings = AppSettings(_env_file=None, data_dir=tmp_path)
    result = ExtractionResult(
        entities=[
            ExtractedEntity(id="customer", name="Maya Chen", type="PERSON", subtype="CUSTOMER"),
            ExtractedEntity(
                id="product", name="Acme Cloud Compute", type="OBJECT", subtype="PRODUCT"
            ),
            ExtractedEntity(
                id="organization", name="Acme Cloud Compute", type="ORGANIZATION", subtype="COMPANY"
            ),
        ],
        relations=[
            ExtractedRelation(
                source="Maya Chen",
                target="Acme Cloud Compute",
                source_id="customer",
                target_id="product",
                relation_type="USES",
            ),
            ExtractedRelation(
                source="Maya Chen", target="Acme Cloud Compute", relation_type="USES"
            ),
        ],
    )
    snapshot = await run_extraction_snapshot(
        settings, "acme_cloud", extractor=SimpleNamespace(extract=AsyncMock(return_value=result))
    )
    relations = [r for r in snapshot["graph"]["relationships"] if r["type"] == "USES"]
    assert len(relations) == 1 and relations[0]["to"] == "entity-1"
    assert len(snapshot["omitted_ambiguous_relations"]) == 1
