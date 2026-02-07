#!/usr/bin/env python3
"""Bootstrap a new Python project with uv, ruff, pyright, pytest, pre-commit, and GitHub Actions CI."""

import argparse
import os
import subprocess
import sys
import textwrap
from pathlib import Path


def create_file(path: Path, content: str) -> None:
    """Write content to a file, creating parent directories as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip())
    print(f"  ✅ Created {path}")


def run(cmd: list[str], cwd: Path) -> None:
    """Run a shell command in the given directory."""
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ❌ Command failed: {' '.join(cmd)}")
        print(result.stderr)
        sys.exit(1)


def bootstrap(project_dir: Path, project_name: str, python_version: str, description: str) -> None:
    """Scaffold the full project structure."""
    # Derive the package name (PEP 8: lowercase, underscores)
    package_name = project_name.replace("-", "_").lower()

    print(f"\n🚀 Bootstrapping project: {project_name}")
    print(f"   Directory: {project_dir}")
    print(f"   Package:   {package_name}")
    print(f"   Python:    {python_version}\n")

    project_dir.mkdir(parents=True, exist_ok=True)

    # --- pyproject.toml ---
    create_file(
        project_dir / "pyproject.toml",
        f"""\
        [project]
        name = "{project_name}"
        version = "0.1.0"
        description = "{description}"
        readme = "README.md"
        requires-python = ">={python_version}"
        dependencies = []

        [project.optional-dependencies]
        dev = [
            "pytest>=8.0",
            "ruff>=0.8",
            "pyright>=1.1",
            "pre-commit>=4.0",
        ]

        [build-system]
        requires = ["hatchling"]
        build-backend = "hatchling.build"

        [tool.hatch.build.targets.wheel]
        packages = ["src/{package_name}"]

        [tool.ruff]
        target-version = "py{python_version.replace('.', '')}"
        src = ["src", "tests"]
        line-length = 88

        [tool.ruff.lint]
        select = [
            "E",    # pycodestyle errors
            "W",    # pycodestyle warnings
            "F",    # pyflakes
            "I",    # isort
            "N",    # pep8-naming
            "UP",   # pyupgrade
            "B",    # flake8-bugbear
            "SIM",  # flake8-simplify
            "TCH",  # flake8-type-checking
            "RUF",  # ruff-specific rules
        ]

        [tool.ruff.lint.isort]
        known-first-party = ["{package_name}"]

        [tool.pyright]
        pythonVersion = "{python_version}"
        typeCheckingMode = "strict"
        include = ["src", "tests"]
        venvPath = "."
        venv = ".venv"

        [tool.pytest.ini_options]
        testpaths = ["tests"]
        pythonpath = ["src"]
        """,
    )

    # --- src layout ---
    create_file(
        project_dir / "src" / package_name / "__init__.py",
        f'''\
        """{project_name}: {description}."""
        ''',
    )

    create_file(
        project_dir / "src" / package_name / "py.typed",
        "",
    )

    # --- tests ---
    create_file(
        project_dir / "tests" / "__init__.py",
        "",
    )

    create_file(
        project_dir / "tests" / f"test_{package_name}.py",
        f"""\
        \"\"\"Tests for {package_name}.\"\"\"

        from {package_name} import __doc__


        def test_package_has_docstring() -> None:
            \"\"\"Verify package is importable and has a docstring.\"\"\"
            assert __doc__ is not None
        """,
    )

    # --- pre-commit config ---
    create_file(
        project_dir / ".pre-commit-config.yaml",
        f"""\
        repos:
          - repo: https://github.com/astral-sh/ruff-pre-commit
            rev: v0.8.6
            hooks:
              - id: ruff
                args: [--fix]
              - id: ruff-format

          - repo: local
            hooks:
              - id: pyright
                name: pyright
                entry: uv run pyright
                language: system
                types: [python]
                pass_filenames: false
        """,
    )

    # --- GitHub Actions CI ---
    create_file(
        project_dir / ".github" / "workflows" / "ci.yml",
        f"""\
        name: CI

        on:
          push:
            branches: [main]
          pull_request:
            branches: [main]

        jobs:
          check:
            runs-on: ubuntu-latest
            steps:
              - uses: actions/checkout@v4

              - name: Install uv
                uses: astral-sh/setup-uv@v4

              - name: Set up Python
                run: uv python install {python_version}

              - name: Install dependencies
                run: uv sync --all-extras

              - name: Lint (ruff)
                run: uv run ruff check src tests

              - name: Format check (ruff)
                run: uv run ruff format --check src tests

              - name: Type check (pyright)
                run: uv run pyright

              - name: Test (pytest)
                run: uv run pytest
        """,
    )

    # --- .gitignore ---
    create_file(
        project_dir / ".gitignore",
        """\
        __pycache__/
        *.py[cod]
        *$py.class
        *.egg-info/
        dist/
        build/
        .venv/
        .mypy_cache/
        .pyright/
        .ruff_cache/
        .pytest_cache/
        .coverage
        htmlcov/
        """,
    )

    # --- README ---
    create_file(
        project_dir / "README.md",
        f"""\
        # {project_name}

        {description}

        ## Development

        ```bash
        # Install dependencies
        uv sync --all-extras

        # Run tests
        uv run pytest

        # Lint and format
        uv run ruff check src tests
        uv run ruff format src tests

        # Type check
        uv run pyright

        # Install pre-commit hooks
        uv run pre-commit install
        ```
        """,
    )

    # --- uv init and install ---
    print("\n📦 Initialising uv environment...")
    run(["uv", "venv", "--python", python_version], cwd=project_dir)
    print("  ✅ Created .venv")

    run(["uv", "sync", "--all-extras"], cwd=project_dir)
    print("  ✅ Installed dependencies")

    # --- Verify tooling ---
    print("\n🔍 Running checks...")
    run(["uv", "run", "ruff", "check", "src", "tests"], cwd=project_dir)
    print("  ✅ ruff lint passed")

    run(["uv", "run", "ruff", "format", "--check", "src", "tests"], cwd=project_dir)
    print("  ✅ ruff format passed")

    run(["uv", "run", "pyright"], cwd=project_dir)
    print("  ✅ pyright passed")

    run(["uv", "run", "pytest"], cwd=project_dir)
    print("  ✅ pytest passed")

    print(f"\n🎉 Project '{project_name}' is ready!")
    print(f"   cd {project_dir}")
    print("   git init && uv run pre-commit install\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bootstrap a new Python project")
    parser.add_argument("project_name", help="Name of the project (e.g. my-cool-project)")
    parser.add_argument("--dir", default=None, help="Parent directory (default: current dir)")
    parser.add_argument("--python", default="3.12", help="Python version (default: 3.12)")
    parser.add_argument("--description", default="", help="Short project description")
    args = parser.parse_args()

    target_dir = Path(args.dir) / args.project_name if args.dir else Path(args.project_name)
    bootstrap(target_dir.resolve(), args.project_name, args.python, args.description)
