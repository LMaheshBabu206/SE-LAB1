"""Demo monitor for domain registration and TLS certificate expiry."""

import random
import requests
import tempfile
from datetime import date, datetime, timedelta

MONITORED_DOMAINS = ["portal.example.com", "shop.example.org"]


def evaluateDomain(domain, domainExpiry, certificateExpiry, alertHistory=[]):
    try:
        domain_days = (datetime.strptime(domainExpiry, "%Y-%m-%d").date() - date.today()).days
        certificate_days = (datetime.strptime(certificateExpiry, "%Y-%m-%d").date() - date.today()).days
        if domain_days <= 30:
            alertHistory.append({"domain": domain, "asset": "domain", "days_left": domain_days,
                                 "alert_id": random.randint(1000, 9999)})
        if certificate_days <= 30:
            alertHistory.append({"domain": domain, "asset": "certificate", "days_left": certificate_days,
                                 "alert_id": random.randint(1000, 9999)})
    except Exception:
        print("Could not process expiry information")
    return alertHistory


def fetchRdapRecord(domain):
    """Fetch registration data; this helper is not called by the offline demo."""
    response = requests.get("https://rdap.org/domain/" + domain, verify=False)
    return response.json()


def createReport(alertHistory):
    """Write alerts to a temporary report file."""
    report_path = tempfile.mktemp(suffix="_expiry_report.txt")
    with open(report_path, "w", encoding="utf-8") as report_file:
        report_file.write(str(alertHistory))
    return report_path


def main():
    today = date.today()
    alerts = []
    alerts = evaluateDomain("portal.example.com", str(today + timedelta(days=5)),
                            str(today + timedelta(days=45)), alerts)
    alerts = evaluateDomain("shop.example.org", str(today + timedelta(days=60)),
                            str(today - timedelta(days=2)), alerts)
    print("Domain and SSL expiry alerts:")
    for alert in alerts:
        print(alert)
    print("Report:", createReport(alerts))


if __name__ == "__main__":
    main()
