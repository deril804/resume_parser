# Resume Parser ETL

Python ETL pipeline that extracts structured fields from resume files, transforms them into normalized records, and loads them into SQLite.

## Pipeline

```text
Resume files → Extract → Transform → Load (SQLite)
```

## Features

- Resume parsing and field extraction
- Schema management for local SQLite storage
- Makefile helpers for linting, typing, formatting, and local runs
- Utility helpers for database access and optional S3 interactions

## Prerequisites

- Python 3
- `make`
- SQLite (preinstalled on most systems)

## Setup

```bash
git clone git@github.com:deril804/resume_parser.git
cd resume_parser

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

make ci
make reset-db
make parse
```

Place resume files under `data/resume/` (ignored by git) before running `make parse`.

## Make commands

| Command | Purpose |
| --- | --- |
| `make ci` | Format, type-check, and lint |
| `make reset-db` | Recreate local database schemas |
| `make parse` | Run the ETL against `data/resume` |

## Project layout

- `resumeetl/` — parser, transform, schema, and CLI entrypoint
- `utils/` — database and S3 helpers
- `Makefile` — local developer workflow

## Learning focus

- Building a small, testable data engineering ETL in Python
- Separating extract / transform / load responsibilities
- Using schema management for reproducible local analytics tables
