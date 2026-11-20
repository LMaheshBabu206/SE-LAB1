"""Unit tests for expiry classification and alert generation."""
from datetime import date, timedelta

import pytest

from src.expiry_monitor import (
    Asset,
    ExpiryLevel,
    build_alert_message,
    classify_expiry,
    days_until,
    evaluate_asset,
)

TODAY = date(2026, 11, 20)


@pytest.mark.unit
def test_days_until_future_date():
    assert days_until(TODAY + timedelta(days=12), TODAY) == 12


@pytest.mark.unit
def test_days_until_expired_date_is_negative():
    assert days_until(TODAY - timedelta(days=2), TODAY) == -2


@pytest.mark.parametrize(
    "days, expected",
    [
        (-1, ExpiryLevel.EXPIRED),
        (0, ExpiryLevel.CRITICAL),
        (7, ExpiryLevel.CRITICAL),
        (8, ExpiryLevel.WARNING),
        (30, ExpiryLevel.WARNING),
        (31, ExpiryLevel.HEALTHY),
    ],
)
@pytest.mark.unit
def test_classify_expiry_boundaries(days, expected):
    assert classify_expiry(days) == expected


@pytest.mark.unit
def test_asset_normalizes_domain():
    asset = Asset(" Example.COM ", TODAY, TODAY)
    assert asset.domain == "example.com"


@pytest.mark.unit
def test_asset_rejects_invalid_domain():
    with pytest.raises(ValueError):
        Asset("not a domain", TODAY, TODAY)


@pytest.mark.unit
def test_evaluate_asset_flags_certificate_alert():
    asset = Asset(
        "example.com",
        TODAY + timedelta(days=90),
        TODAY + timedelta(days=5),
    )
    result = evaluate_asset(asset, TODAY)
    assert result["domain_status"] == "healthy"
    assert result["certificate_status"] == "critical"
    assert result["alert_required"] is True


@pytest.mark.unit
def test_healthy_asset_has_no_alert():
    asset = Asset(
        "example.com",
        TODAY + timedelta(days=90),
        TODAY + timedelta(days=60),
    )
    result = evaluate_asset(asset, TODAY)
    assert result["alert_required"] is False
    assert "no expiry alert" in build_alert_message(result)
