"""Domain registration and TLS certificate expiry monitoring utilities."""

from __future__ import annotations

import json
import re
import secrets
import tempfile
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote

import requests

DOMAIN_PATTERN = re.compile(
    r"^(?=.{1,253}$)"
    r"(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+"
    r"[a-zA-Z]{2,63}$"
)
WARNING_DAYS = 30
CRITICAL_DAYS = 7


@dataclass(frozen=True)
class MonitoredDomain:
    """A domain together with its registration and TLS expiry dates."""

    domain: str
    domain_expiry: date
    certificate_expiry: date

    def __post_init__(self) -> None:
        normalized_domain = self.domain.strip().lower()
        if not DOMAIN_PATTERN.fullmatch(normalized_domain):
            raise ValueError("domain must be a valid fully qualified hostname")
        object.__setattr__(self, "domain", normalized_domain)


def days_remaining(expiry_date: date, today: date | None = None) -> int:
    """Return the number of calendar days until an expiry date."""
    reference_date = today or datetime.now(timezone.utc).date()
    return (expiry_date - reference_date).days


def classify_expiry(days_left: int) -> str:
    """Classify an expiry as expired, critical, warning, or healthy."""
    if days_left < 0:
        return "expired"
    if days_left <= CRITICAL_DAYS:
        return "critical"
    if days_left <= WARNING_DAYS:
        return "warning"
    return "healthy"


def evaluate_domain(
    monitored_domain: MonitoredDomain, today: date | None = None
) -> list[dict[str, Any]]:
    """Create separate alerts for domain and certificate dates at risk."""
    expiry_dates = {
        "domain": monitored_domain.domain_expiry,
        "certificate": monitored_domain.certificate_expiry,
    }
    alerts: list[dict[str, Any]] = []

    for asset_type, expiry_date in expiry_dates.items():
        remaining_days = days_remaining(expiry_date, today)
        status = classify_expiry(remaining_days)
        if status != "healthy":
            alerts.append(
                {
                    "alert_id": secrets.token_hex(4),
                    "domain": monitored_domain.domain,
                    "asset_type": asset_type,
                    "days_remaining": remaining_days,
                    "status": status,
                }
            )
    return alerts


def fetch_rdap_record(domain: str, timeout: float = 10.0) -> dict[str, Any]:
    """Fetch an RDAP record over verified HTTPS with a timeout."""
    normalized_domain = domain.strip().lower()
    if not DOMAIN_PATTERN.fullmatch(normalized_domain):
        raise ValueError("domain must be a valid fully qualified hostname")
    endpoint = f"https://rdap.org/domain/{quote(normalized_domain, safe='')}"
    response = requests.get(endpoint, timeout=timeout)
    response.raise_for_status()
    return response.json()


def write_alert_report(alerts: list[dict[str, Any]]) -> Path:
    """Write alerts to a securely created temporary JSON report."""
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", suffix="_expiry_report.json", delete=False
    ) as report_file:
        json.dump(alerts, report_file, indent=2)
        return Path(report_file.name)


def demo_assets(today: date | None = None) -> list[MonitoredDomain]:
    """Return sample assets relative to the supplied or current date."""
    reference_date = today or datetime.now(timezone.utc).date()
    return [
        MonitoredDomain(
            "portal.example.com",
            reference_date + timedelta(days=5),
            reference_date + timedelta(days=45),
        ),
        MonitoredDomain(
            "shop.example.org",
            reference_date + timedelta(days=60),
            reference_date - timedelta(days=2),
        ),
        MonitoredDomain(
            "status.example.net",
            reference_date + timedelta(days=120),
            reference_date + timedelta(days=90),
        ),
    ]


def main() -> None:
    """Run the offline domain and TLS expiry demonstration."""
    today = datetime.now(timezone.utc).date()
    alerts: list[dict[str, Any]] = []
    for monitored_domain in demo_assets(today):
        alerts.extend(evaluate_domain(monitored_domain, today))

    print("Domain and SSL certificate expiry alerts:")
    if not alerts:
        print("No expiry alerts.")
    for alert in alerts:
        print(
            f"{alert['domain']} | {alert['asset_type']} | "
            f"{alert['status']} | {alert['days_remaining']} days | "
            f"ID {alert['alert_id']}"
        )
    report_path = write_alert_report(alerts)
    print(f"JSON report written to: {report_path}")


if __name__ == "__main__":
    main()
