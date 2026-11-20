"""Tests for the Lab 5-47 domain and certificate expiry monitor."""

from datetime import date, timedelta

import pytest

from domain_ssl_monitor import (
    MonitoredDomain,
    classify_expiry,
    days_remaining,
    evaluate_domain,
    write_alert_report,
)

TODAY = date(2026, 11, 20)


def test_domain_is_normalized():
    asset = MonitoredDomain(" Portal.Example.COM ", TODAY, TODAY)
    assert asset.domain == "portal.example.com"


def test_invalid_domain_is_rejected():
    with pytest.raises(ValueError):
        MonitoredDomain("not a domain", TODAY, TODAY)


@pytest.mark.parametrize(
    ("days_left", "expected"),
    [
        (-1, "expired"),
        (0, "critical"),
        (7, "critical"),
        (8, "warning"),
        (30, "warning"),
        (31, "healthy"),
    ],
)
def test_expiry_boundaries(days_left, expected):
    assert classify_expiry(days_left) == expected


def test_days_remaining_uses_injected_date():
    assert days_remaining(TODAY + timedelta(days=9), TODAY) == 9


def test_evaluate_domain_emits_only_expiring_assets():
    asset = MonitoredDomain(
        "portal.example.com",
        TODAY + timedelta(days=5),
        TODAY + timedelta(days=60),
    )
    alerts = evaluate_domain(asset, TODAY)
    assert len(alerts) == 1
    assert alerts[0]["asset_type"] == "domain"
    assert alerts[0]["status"] == "critical"


def test_expired_certificate_is_reported():
    asset = MonitoredDomain(
        "shop.example.org",
        TODAY + timedelta(days=90),
        TODAY - timedelta(days=2),
    )
    alerts = evaluate_domain(asset, TODAY)
    assert len(alerts) == 1
    assert alerts[0]["asset_type"] == "certificate"
    assert alerts[0]["status"] == "expired"


def test_healthy_domain_has_no_alerts():
    asset = MonitoredDomain(
        "status.example.net",
        TODAY + timedelta(days=90),
        TODAY + timedelta(days=90),
    )
    assert evaluate_domain(asset, TODAY) == []


def test_write_alert_report_creates_json_file(tmp_path, monkeypatch):
    import domain_ssl_monitor

    monkeypatch.setattr(domain_ssl_monitor.tempfile, "tempdir", str(tmp_path))
    asset = MonitoredDomain(
        "portal.example.com",
        TODAY + timedelta(days=3),
        TODAY + timedelta(days=50),
    )
    report_path = write_alert_report(evaluate_domain(asset, TODAY))
    assert report_path.exists()
    assert report_path.suffix == ".json"
    assert '"portal.example.com"' in report_path.read_text(encoding="utf-8")
