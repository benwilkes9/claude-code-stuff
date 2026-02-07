---
name: python-bootstrap
description: >
  Bootstrap a new Python project with a production-ready toolchain. Use when the user asks to
  create, initialise, scaffold, or set up a new Python project or repository. Triggers include
  phrases like "new Python project", "init a Python repo", "scaffold a Python app", "set up a
  Python package", or "bootstrap Python". The skill creates a fully configured project using uv
  (package management), ruff (linting/formatting), pyright in strict mode (type checking), pytest
  (testing), pre-commit hooks, and GitHub Actions CI — all following PEP 8 conventions with
  mandatory static type annotations.
---

# Python Project Bootstrap

Scaffold a new Python project with an opinionated, production-ready toolchain.

## Toolchain

| Tool | Purpose | Config |
|------|---------|--------|
| **uv** | Package management, venv, dependency resolution | `pyproject.toml` |
| **ruff** | Linting (PEP 8, isort, bugbear, etc.) + formatting | `pyproject.toml [tool.ruff]` |
| **pyright** | Static type checking in **strict** mode | `pyproject.toml [tool.pyright]` |
| **pytest** | Testing | `pyproject.toml [tool.pytest]` |
| **pre-commit** | Git hooks (ruff + pyright) | `.pre-commit-config.yaml` |
| **GitHub Actions** | CI (lint, format, type check, test) | `.github/workflows/ci.yml` |

## Usage

Run the bootstrap script. It accepts a project name and optional flags:

```bash
python <skill_path>/scripts/bootstrap.py <project-name> \
  --python 3.12 \
  --description "Short project description" \
  --dir /optional/parent/directory
```

The script:
1. Creates the project directory with src layout (`src/<package_name>/`)
2. Generates `pyproject.toml` with all tool configuration
3. Creates test scaffolding, `.gitignore`, `README.md`, pre-commit config, and CI workflow
4. Runs `uv venv` and `uv sync --all-extras` to install dependencies
5. Verifies all checks pass (ruff lint, ruff format, pyright, pytest)

## Coding Standards

All code in projects created by this skill must follow:

- **PEP 8** — enforced by ruff (E, W, F, I, N, UP, B, SIM, TCH, RUF rule sets)
- **Static type annotations** on all functions, parameters, and return types — enforced by pyright in strict mode
- **`py.typed` marker** included for PEP 561 compliance

## Defaults

- Python version: **3.12** (override with `--python`)
- Line length: **88** (ruff/black standard)
- Layout: **src layout** (`src/<package_name>/`)

## After Bootstrap

Remind the user to:
1. `cd <project-name>`
2. `git init && uv run pre-commit install`
3. Start coding in `src/<package_name>/`
