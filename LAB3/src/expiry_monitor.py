"""Core domain and TLS expiry calculations for Problem Statement #47."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timezone
from enum import Enum
from typing import Optional


class ExpiryLevel(str, Enum):
    """Alert urgency based on remaining days."""

    EXPIRED = "expired"
    CRITICAL = "critical"
    WARNING = "warning"
    HEALTHY = "healthy"


@dataclass(frozen=True)
class Asset:
    """A monitored domain and its TLS certificate expiry date."""

    domain: str
    domain_expiry: date
    certificate_expiry: date

    def __post_init__(self) -> None:
        normalized = self.domain.strip().lower()
        if not normalized or "." not in normalized or " " in normalized:
            raise ValueError("domain must be a valid hostname")
        object.__setattr__(self, "domain", normalized)


def days_until(expiry: date, today: Optional[date] = None) -> int:
    """Return calendar days from today to an expiry date (negative if expired)."""
    reference = today or datetime.now(timezone.utc).date()
    return (expiry - reference).days


def classify_expiry(days_remaining: int) -> ExpiryLevel:
    """Classify expiry: expired, <=7 critical, <=30 warning, otherwise healthy."""
    if days_remaining < 0:
        return ExpiryLevel.EXPIRED
    if days_remaining <= 7:
        return ExpiryLevel.CRITICAL
    if days_remaining <= 30:
        return ExpiryLevel.WARNING
    return ExpiryLevel.HEALTHY


def evaluate_asset(asset: Asset, today: Optional[date] = None) -> dict[str, object]:
    """Evaluate both domain and certificate expiry and return structured status."""
    domain_days = days_until(asset.domain_expiry, today)
    certificate_days = days_until(asset.certificate_expiry, today)
    domain_level = classify_expiry(domain_days)
    certificate_level = classify_expiry(certificate_days)
    return {
        "domain": asset.domain,
        "domain_days_remaining": domain_days,
        "domain_status": domain_level.value,
        "certificate_days_remaining": certificate_days,
        "certificate_status": certificate_level.value,
        "alert_required": domain_level != ExpiryLevel.HEALTHY
        or certificate_level != ExpiryLevel.HEALTHY,
    }


def build_alert_message(result: dict[str, object]) -> str:
    """Create a concise alert message from an evaluated asset."""
    if not result.get("alert_required"):
        return f"{result['domain']}: no expiry alert required."
    return (
        f"EXPIRY ALERT: {result['domain']} | "
        f"domain={result['domain_status']} ({result['domain_days_remaining']} days) | "
        f"TLS={result['certificate_status']} ({result['certificate_days_remaining']} days)"
    )
