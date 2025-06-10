# OULAD-CASE

![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https://raw.githubusercontent.com/Mandroide/cms-otek-backend/refs/heads/main/pyproject.toml)

This is an implementation of EDA and ETL for [OULAD Dataset](https://analyse.kmi.open.ac.uk/#open-dataset).

The environment variables must be modified before running the app

Basic Structure of the project
```
oulad-case/                   # ── repo root ─────────────────────────────
├── pyproject.toml               # Poetry config (deps, tooling, packaging)
├── README.md                    # What / why / quick-start
├── .gitignore
├── .pre-commit-config.yaml      # Black, Ruff, Mypy, Detect-Secrets, Pytest
├── .env.example                 # Template for runtime variables (e.g. DB_URL)
├── Makefile                     # Handy one-liners (lint, test, run)
│
├── data/                        # ── datasets ------------------------------
│   ├── raw/                     # original OULAD CSVs
│   └── processed/               # cleaned / parquet / feature files
│
├── notebooks/                   # EDA notebooks only (no business logic)
│   └── 00_eda_overview.ipynb
│
├── src/oulad_etl/               # ── importable Python package ------------
│   ├── __init__.py
│   ├── settings.py              # pydantic-based config (env driven)
│   │
│   ├── etl/                     # ETL pipeline modules
│   │   ├── extract.py
│   │   ├── transform.py
│   │   └── load.py              # (to file, to S3, to DB—your choice)
│   │
│   └── eda/                     # helper functions (profiling, plots)
│       └── summary.py
│
├── tests/                       # pytest suite
│   ├── conftest.py
│   └── unit/
│
└── .github/                     # ── CI/CD --------------------------------
    └── workflows/
        └── ci.yml               # lint → type-check → test → coverage
```
## Quick start

### Boostrap the app
```bash
git clone <repo-url>
cd oulad-case
poetry install
cp .env.example .env
pre-commit install
poetry run jupyter lab
```


## References

