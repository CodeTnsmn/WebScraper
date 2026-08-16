from decimal import Decimal
from unittest.mock import Mock

from webscraper import store
from webscraper.collect import collect_all, collect_target
from webscraper.models import Target


def _target(id_, url="http://example.test/product"):
    return Target(
        id=id_,
        name=f"Target {id_}",
        url=url,
        name_selector=".product-title",
        price_selector=".product-price",
        default_currency="TRY",
    )


def _ok_session(html):
    session = Mock()
    session.get.return_value = Mock(status_code=200, text=html)
    return session


GOOD_HTML = (
    "<html><body><h1 class='product-title'>Ürün</h1>"
    "<span class='product-price'>100 TL</span></body></html>"
)


def test_collect_target_saves_snapshot_on_success_ac2():
    conn = store.connect(":memory:")
    target_id = store.add_target(conn, _target(None))
    target = _target(target_id)

    result = collect_target(conn, target, session=_ok_session(GOOD_HTML))

    assert result.status == "ok"
    history = store.get_history(conn, target_id)
    assert len(history) == 1
    assert history[0].raw_price == "100 TL"
    assert history[0].price == Decimal("100")


def test_collect_target_no_snapshot_on_parse_failure_ac3():
    conn = store.connect(":memory:")
    target_id = store.add_target(conn, _target(None))
    target = _target(target_id)
    session = _ok_session("<html><body>no product here</body></html>")

    result = collect_target(conn, target, session=session)

    assert result.status == "failed"
    assert store.get_history(conn, target_id) == []


def test_collect_target_no_snapshot_on_clean_failure_ac6():
    conn = store.connect(":memory:")
    target_id = store.add_target(conn, _target(None))
    target = _target(target_id)
    html = (
        "<html><body><h1 class='product-title'>Ürün</h1>"
        "<span class='product-price'>Fiyat için tıklayın</span></body></html>"
    )

    result = collect_target(conn, target, session=_ok_session(html))

    assert result.status == "failed"
    assert store.get_history(conn, target_id) == []


def test_collect_all_continues_after_one_target_fails_ac3(monkeypatch):
    conn = store.connect(":memory:")
    ok_id = store.add_target(conn, _target(None, url="http://example.test/ok"))
    bad_id = store.add_target(conn, _target(None, url="http://example.test/bad"))
    targets = [_target(bad_id, url="http://example.test/bad"), _target(ok_id, url="http://example.test/ok")]

    session = Mock()

    def fake_get(url, headers, timeout):
        if url.endswith("/bad"):
            return Mock(status_code=200, text="<html><body>nothing</body></html>")
        return Mock(status_code=200, text=GOOD_HTML)

    session.get.side_effect = fake_get
    sleep_calls = []

    results = collect_all(conn, targets, session=session, sleep_fn=sleep_calls.append)

    assert [r.status for r in results] == ["failed", "ok"]
    assert store.get_history(conn, ok_id) != []
    assert store.get_history(conn, bad_id) == []
    assert sleep_calls == [2.0]
