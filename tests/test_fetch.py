from unittest.mock import Mock

import pytest
import requests

from webscraper.exceptions import FetchError
from webscraper.fetch import fetch_html


def test_fetch_html_returns_body_on_200():
    session = Mock()
    session.get.return_value = Mock(status_code=200, text="<html>ok</html>")

    result = fetch_html("http://example.test/product", session=session)

    assert result == "<html>ok</html>"
    session.get.assert_called_once()


def test_fetch_html_non_200_raises_fetch_error_without_retry_ac5():
    session = Mock()
    session.get.return_value = Mock(status_code=404, text="not found")

    with pytest.raises(FetchError, match="404"):
        fetch_html("http://example.test/missing", session=session)

    assert session.get.call_count == 1


def test_fetch_html_retries_on_connection_error_then_succeeds_ac4(monkeypatch):
    monkeypatch.setattr("webscraper.fetch.time.sleep", lambda _seconds: None)
    session = Mock()
    session.get.side_effect = [
        requests.ConnectionError("boom"),
        requests.ConnectionError("boom"),
        Mock(status_code=200, text="<html>ok</html>"),
    ]

    result = fetch_html("http://example.test/product", session=session)

    assert result == "<html>ok</html>"
    assert session.get.call_count == 3


def test_fetch_html_all_retries_fail_raises_fetch_error_ac4(monkeypatch):
    monkeypatch.setattr("webscraper.fetch.time.sleep", lambda _seconds: None)
    session = Mock()
    session.get.side_effect = requests.ConnectionError("boom")

    with pytest.raises(FetchError):
        fetch_html("http://example.test/product", session=session)

    assert session.get.call_count == 3
