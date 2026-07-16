---
schema_version: 1
id: python
display_name: Python
priority: 75
kind: normal
aliases: [py]

signatures:
  any:
    - pyproject.toml
    - requirements.txt
    - setup.py
    - setup.cfg
    - Pipfile
    - environment.yml

exclusions:
  any: []

refinements: []

workspace_files:
  - pyproject.toml

priority_files:
  - pyproject.toml
  - requirements.txt
  - README.md

entry_point_patterns:
  - '__name__ == "__main__"'
  - 'app = Flask'
  - 'app = FastAPI'
  - 'def main'

external_reference_mechanisms:
  - editable installs
  - local path dependencies

generated_paths:
  - "*.egg-info/"
  - build/
  - dist/

large_structured_files:
  - "*.ipynb"

binary_asset_types:
  - "*.pt"
  - "*.pth"
  - "*.onnx"
  - "*.npy"

default_ignore_paths:
  - __pycache__/
  - .venv/
  - venv/
  - "*.egg-info/"

known_blind_spots:
  - runtime plugin discovery
  - notebook execution state

optional_output_sections:
  - Python Package Layout
  - Notebook Workflows
---

Copyright (C) 2026 ZionXiaoxiSuOGLocGo
SPDX-License-Identifier: GPL-3.0-or-later

# Python Project Analysis Rules

## Signature Detection
- `pyproject.toml` or `requirements.txt` or `setup.py` or `setup.cfg` or `Pipfile` or `environment.yml`

## Scan Steps

### 1. Read Dependency Manifest
Check in order of preference:
1. `pyproject.toml` ->Modern Python project (Poetry, PDM, uv, setuptools)
2. `requirements.txt` ->pip-based
3. `setup.py` / `setup.cfg` ->Legacy setuptools
4. `Pipfile` ->Pipenv
5. `environment.yml` ->Conda

Extract key frameworks:
- `django` ->Django web framework
- `flask`, `fastapi`, `starlette` ->Web API
- `sqlalchemy`, `tortoise-orm` ->ORM
- `pydantic` ->Data validation
- `celery` ->Task queue
- `pytest` ->Testing
- `click`, `typer` ->CLI tool
- `numpy`, `pandas`, `scipy` ->Data science
- `torch`, `tensorflow` ->ML/AI
- `pygame` ->Game
- `pillow`, `opencv-python` ->Image processing
- `discord.py`, `hikari` ->Discord bot

### 2. Map Directory Structure
| Directory | Common Role |
|---|---|
| `src/` or the project-named dir | Main package source |
| `tests/` or `test/` | Test suite |
| `migrations/` | Django/Alembic DB migrations |
| `templates/` | Web templates (Jinja2 / Django) |
| `static/` | Static files |
| `scripts/` | Utility/management scripts |
| `config/` | Configuration files |
| `notebooks/` | Jupyter notebooks |
| `data/` | Data files |

### 3. Find Entry Points
```bash
grep "if __name__ == .__main__." in src/ or *.py
```
Framework-specific:
- Django: `manage.py`, check `settings.py` for main app config
- Flask/FastAPI: look for `app = Flask(` or `app = FastAPI(`
- CLI: look for `@click.command()` or `@app.command()` or `argparse`

### 4. Check Python Version
```bash
read pyproject.toml (check "requires-python")
read .python-version (if exists)
```

### 5. Build & Run Commands
Extract from project configuration:
- **Install deps**: `pip install -r requirements.txt` or `poetry install` or `pipenv install`
- **Run**: `python main.py` or `uvicorn app:app` (FastAPI) or `python manage.py runserver` (Django)
- **Test**: `pytest` or `python -m pytest` or `python manage.py test` (Django)
- **Lint**: `ruff`, `flake8`, `mypy`
- **Format**: `black`, `isort`

### 6. Config Files
- `.env.example` / `.env.sample` / `.env.template` ->Environment variable names (never read real `.env`)
- `Dockerfile` ->Container deployment
- `docker-compose.yml` ->Multi-service
- `Makefile` or `Taskfile` ->Build/dev commands
- `.github/workflows/` ->CI/CD
