import csv

import pytest

from webscraper import store
from webscraper.cli import main


def test_add_target_then_list_targets_ac1(tmp_path, capsys):
    db = str(tmp_path / "test.db")

    exit_code = main(
        [
            "--db", db, "add-target",
            "--name", "Kulaklık X200",
            "--url", "http://example.test/product",
            "--name-selector", ".n",
            "--price-selector", ".p",
            "--currency", "TRY",
        ]
    )
    capsys.readouterr()
    exit_code_2 = main(["--db", db, "list-targets"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert exit_code_2 == 0
    assert "Kulaklık X200" in captured.out
    assert "http://example.test/product" in captured.out


def test_collect_command_prints_status_per_target_ac2(tmp_path, monkeypatch, capsys):
    db = str(tmp_path / "test.db")
    main(
        [
            "--db", db, "add-target",
            "--name", "T1", "--url", "http://example.test/p",
            "--name-selector", ".n", "--price-selector", ".p", "--currency", "TRY",
        ]
    )
    capsys.readouterr()

    monkeypatch.setattr(
        "webscraper.collect.fetch_html",
        lambda url, session=None: "<html><span class='n'>Ad</span><span class='p'>10 TL</span></html>",
    )

    exit_code = main(["--db", db, "collect"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "status=ok" in captured.out


def test_export_command_writes_csv_file_ac3(tmp_path, capsys):
    db = str(tmp_path / "test.db")
    main(
        [
            "--db", db, "add-target",
            "--name", "T1", "--url", "http://example.test/p",
            "--name-selector", ".n", "--price-selector", ".p", "--currency", "TRY",
        ]
    )
    capsys.readouterr()

    conn = store.connect(db)
    target_id = store.list_targets(conn)[0].id
    from datetime import datetime, timezone
    from decimal import Decimal

    from webscraper.models import PriceSnapshot

    store.save_snapshot(
        conn,
        PriceSnapshot(
            target_id=target_id,
            timestamp=datetime.now(timezone.utc),
            raw_price="10 TL",
            price=Decimal("10"),
            currency="TRY",
            in_stock=True,
        ),
    )
    out_path = tmp_path / "out.csv"

    exit_code = main(["--db", db, "export", "--format", "csv", "--output", str(out_path)])

    assert exit_code == 0
    with open(out_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    assert rows[0]["hedef_adi"] == "T1"


def test_schedule_command_builds_scheduler_with_requested_interval_ac4(tmp_path, monkeypatch):
    calls = {}

    class FakeScheduler:
        def start(self):
            calls["started"] = True

        def shutdown(self):
            calls["shutdown"] = True

    def fake_build_scheduler(job_func, interval_minutes, *, run_immediately=False, scheduler=None):
        calls["interval_minutes"] = interval_minutes
        calls["run_immediately"] = run_immediately
        return FakeScheduler()

    monkeypatch.setattr("webscraper.cli.build_scheduler", fake_build_scheduler)
    monkeypatch.setattr("webscraper.cli.time.sleep", lambda _seconds: (_ for _ in ()).throw(KeyboardInterrupt()))

    db = str(tmp_path / "test.db")
    exit_code = main(["--db", db, "schedule", "--interval-minutes", "15"])

    assert exit_code == 0
    assert calls["interval_minutes"] == 15
    assert calls["run_immediately"] is False
    assert calls["started"] is True
    assert calls["shutdown"] is True


def test_invalid_subcommand_exits_with_clear_error_not_traceback_ac5(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main(["not-a-real-command"])

    captured = capsys.readouterr()
    assert exc_info.value.code != 0
    assert "Traceback" not in captured.err
    assert "invalid choice" in captured.err
