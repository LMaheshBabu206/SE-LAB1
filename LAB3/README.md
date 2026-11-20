# LAB 3 – Git Workflow, Testing and Code Quality

**Problem Statement #47 – Domain & SSL Certificate Expiry Alert System**

This folder contains a small Python expiry-monitoring module, unit and integration-style tests, pytest configuration, and the Git/tooling commands used in the practical.

## Setup (Windows PowerShell)

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run quality checks

```powershell
pytest tests/ --cov=src --cov-report=html
pylint src/
black src/ tests/ --check
bandit -r src/
```

## Local validation reported

- Pytest: 14 passed.
- Pylint: 10.00/10.
- Bandit: no issues identified.
- Black: formatting was applied after the initial check flagged three files; rerun `black src/ tests/ --check` to confirm the final state.

The repository does not contain the user's local terminal screenshots. Add those separately if the instructor requires practical evidence.
