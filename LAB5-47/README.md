# Lab 5-47: Static Code Analysis – Domain & SSL Certificate Expiry Alert System

**Problem Statement #47 – Domain & SSL Certificate Expiry Alert System**

This project adapts the workflow demonstrated by the reference Lab 5 Parcel Tracker repository. The static-analysis practical is preserved, while the sample application is changed to domain registration and TLS certificate expiry monitoring.

## What the program does

The corrected program models a monitored domain with separate registration-expiry and TLS-certificate-expiry dates. It calculates days remaining, classifies each date as expired, critical, warning, or healthy, creates alert records for non-healthy assets, and writes a JSON report. A separate RDAP helper retrieves registration data over verified HTTPS with a request timeout. The offline demo does not call the RDAP service.

## Lab workflow

1. Run domain_ssl_monitor_before.py, the intentionally flawed baseline.
2. Run Pylint, Bandit and Flake8 against the baseline and save the *_before.txt reports.
3. Review issues.md and identify the findings.
4. Run domain_ssl_monitor.py, the corrected version.
5. Execute python -m pytest -v to check that the expected functionality remains.
6. Run the three static-analysis tools against the corrected version and save the *_after.txt reports.
7. Answer the reflection questions in reflection.md.

## Setup (Windows PowerShell)

    py -m venv .venv
    .venv\Scripts\Activate.ps1
    python -m pip install -r requirements.txt

## Run

    python domain_ssl_monitor_before.py
    python domain_ssl_monitor.py
    python -m pytest -v

See commands.txt for the complete before/after scan commands.

## Security note

domain_ssl_monitor_before.py intentionally contains insecure patterns for the static-analysis exercise. It is for analysis only. Do not use its unsafe RDAP request, temporary-file creation, or weak alert-ID generation in a real system. Use domain_ssl_monitor.py for the corrected implementation.

## Reports

Run the commands on your own machine to generate actual tool reports. The reports folder contains instructions only until those scans are executed; no scan results are fabricated.
