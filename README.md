# Software Engineering Lab Portfolio

**Problem Statement #47 – Domain & SSL Certificate Expiry Alert System**

This repository contains the deliverables for Software Engineering Labs 1–3. All three labs use the same problem statement and are organized separately for easy review.

## Repository structure

- [LAB1/](LAB1/) – Requirements engineering: requirements and actors, UML use-case diagram, and use-case flow.
- [LAB2/](LAB2/) – Agile planning with Jira: epics, user stories, story points, backlog import CSV, sprint/burndown artefacts, and reflection.
- [LAB3/](LAB3/) – Git workflow and software quality: Python source, unit/integration tests, pytest configuration, and commands for coverage, linting, formatting, and security scanning.

## Lab 3 test commands

Run from the LAB3 folder:

```bash
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
pytest tests/ --cov=src --cov-report=html
pylint src/
black src/ tests/ --check
bandit -r src/
```

## Notes

- Lab 2's burndown graphic is an illustrative planning artefact, not a screenshot from a live Jira workspace. Capture actual Jira screenshots separately if required by the instructor.
- Lab 3 local execution reported 14 tests passed, Pylint 10.00/10, and no Bandit issues. Black formatting should be verified locally with `black src/ tests/ --check`.
- Generated caches, virtual environments, and local machine-specific files are excluded.
