"""Integration-style tests of asset evaluation and alert output."""
from datetime import date, timedelta

import pytest

from src.expiry_monitor import Asset, build_alert_message, evaluate_asset


@pytest.mark.integration
def test_expiry_workflow_generates_domain_and_tls_alerts():
    today = date(2026, 11, 20)
    asset = Asset(
        "portal.example.org",
        today + timedelta(days=4),
        today - timedelta(days=1),
    )
    result = evaluate_asset(asset, today)
    message = build_alert_message(result)
    assert result["alert_required"] is True
    assert "domain=critical" in message
    assert "TLS=expired" in message


@pytest.mark.integration
def test_workflow_preserves_domain_identity():
    today = date(2026, 11, 20)
    asset = Asset(
        "STATUS.Example.org",
        today + timedelta(days=100),
        today + timedelta(days=100),
    )
    result = evaluate_asset(asset, today)
    assert result["domain"] == "status.example.org"
    assert result["alert_required"] is False
