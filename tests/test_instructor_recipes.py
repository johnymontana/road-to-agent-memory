from lib.settings import AppSettings
from scripts import instructor, seed_sqlite


async def test_plan_recipe_runs_real_hydrator_before_after_and_restore(
    tmp_path, monkeypatch, capsys
):
    from lib import settings

    monkeypatch.setattr(seed_sqlite, "DB_PATH", tmp_path / "acme_cloud.db")
    seed_sqlite.main()
    monkeypatch.setattr(
        settings, "get_settings", lambda: AppSettings(_env_file=None, data_dir=tmp_path)
    )
    before = seed_sqlite.DB_PATH.read_bytes()
    await instructor.plan_demo()
    output = capsys.readouterr().out
    assert output.count("Local hydrated entity: local-maya Pro") == 2
    assert "Local hydrated entity: local-maya Enterprise" in output
    assert seed_sqlite.DB_PATH.read_bytes() == before


def test_explicit_validator_drop_and_raise(capsys):
    instructor.strict_demo()
    assert "raises ValueError" in capsys.readouterr().out
