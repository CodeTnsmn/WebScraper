import argparse
import sys
import time

from webscraper import config, export, store
from webscraper.collect import collect_all
from webscraper.models import Target
from webscraper.schedule import build_scheduler


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="webscraper")
    parser.add_argument("--db", default=config.DEFAULT_DB_PATH, help="SQLite veritabanı dosyası")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_target = subparsers.add_parser("add-target", help="Yeni takip hedefi ekle")
    add_target.add_argument("--name", required=True)
    add_target.add_argument("--url", required=True)
    add_target.add_argument("--name-selector", required=True)
    add_target.add_argument("--price-selector", required=True)
    add_target.add_argument("--currency", required=True)
    add_target.add_argument("--stock-selector")
    add_target.add_argument("--stock-in-stock-text")

    subparsers.add_parser("list-targets", help="Tanımlı hedefleri listele")

    subparsers.add_parser("collect", help="Tüm hedefler için bir toplama turu çalıştır")

    export_parser = subparsers.add_parser("export", help="Fiyat geçmişini dışa aktar")
    export_parser.add_argument("--format", choices=["csv", "excel"], required=True)
    export_parser.add_argument("--output", required=True)
    export_parser.add_argument("--target-id", type=int, default=None)

    schedule_parser = subparsers.add_parser("schedule", help="Zamanlanmış toplama başlat")
    schedule_parser.add_argument("--interval-minutes", type=int, required=True)
    schedule_parser.add_argument("--run-immediately", action="store_true")

    return parser


def _cmd_add_target(args) -> int:
    conn = store.connect(args.db)
    target_id = store.add_target(
        conn,
        Target(
            name=args.name,
            url=args.url,
            name_selector=args.name_selector,
            price_selector=args.price_selector,
            default_currency=args.currency,
            stock_selector=args.stock_selector,
            stock_in_stock_text=args.stock_in_stock_text,
        ),
    )
    print(f"Hedef eklendi: id={target_id} name={args.name!r}")
    return 0


def _cmd_list_targets(args) -> int:
    conn = store.connect(args.db)
    targets = store.list_targets(conn)
    if not targets:
        print("Tanımlı hedef yok.")
        return 0
    for target in targets:
        print(f"{target.id}\t{target.name}\t{target.url}\t{target.default_currency}")
    return 0


def _cmd_collect(args) -> int:
    conn = store.connect(args.db)
    targets = store.list_targets(conn)
    results = collect_all(conn, targets)
    for result in results:
        print(f"target={result.target_id}\tstatus={result.status}\terror={result.error or '-'}")
    return 0


def _cmd_export(args) -> int:
    conn = store.connect(args.db)
    if args.format == "csv":
        export.export_csv(conn, args.output, target_id=args.target_id)
    else:
        export.export_excel(conn, args.output, target_id=args.target_id)
    print(f"Dışa aktarıldı: {args.output}")
    return 0


def _cmd_schedule(args) -> int:
    conn = store.connect(args.db)

    def job() -> None:
        collect_all(conn, store.list_targets(conn))

    sched = build_scheduler(job, args.interval_minutes, run_immediately=args.run_immediately)
    return _run_scheduler_until_interrupted(sched, args.interval_minutes)


def _run_scheduler_until_interrupted(sched, interval_minutes: int) -> int:
    sched.start()
    print(f"Zamanlayıcı başladı: her {interval_minutes} dakikada bir. Durdurmak için Ctrl+C.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        sched.shutdown()
        print("Zamanlayıcı durduruldu.")
    return 0


_HANDLERS = {
    "add-target": _cmd_add_target,
    "list-targets": _cmd_list_targets,
    "collect": _cmd_collect,
    "export": _cmd_export,
    "schedule": _cmd_schedule,
}


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    return _HANDLERS[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
