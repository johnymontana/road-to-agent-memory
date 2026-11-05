from types import SimpleNamespace
from unittest.mock import AsyncMock

from lib.settings import AppSettings
from module_3.lab.enrichment import enrich_organization


async def test_provider_failure_is_visible_cached_and_not_service_health(tmp_path):
    provider = SimpleNamespace(enrich=AsyncMock(side_effect=RuntimeError("403")))
    settings = AppSettings(_env_file=None, data_dir=tmp_path)
    first = await enrich_organization(settings, provider=provider)
    again = await enrich_organization(settings, provider=provider)
    assert first["status"] == "unavailable" and not first["cached"]
    assert again["cached"] and provider.enrich.await_count == 1
    assert "operational" not in str(first).lower()
    assert list((tmp_path / "replays").glob("*.json"))
