# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## IMPORTANT: Keep Docs In Sync

**Every change to this repository MUST include corresponding updates to both `CLAUDE.md` and `README.md`.** No PR or commit is complete without this. Adding a skill, renaming a script, changing behaviour — update both files as part of the same change.

## What This Repo Is

A personal collection of Claude Code custom skills and configuration references. There is no build system, test suite, or application code — only skill definitions and their supporting scripts.

## Repository Structure

```
skills/
  <skill-name>/
    SKILL.md          # Skill metadata (name, description, triggers) + full instructions
    scripts/          # Supporting scripts referenced by the skill
```

Each skill is a self-contained directory under `skills/`. The `SKILL.md` frontmatter (`name`, `description`) defines how Claude Code discovers and triggers the skill. The body contains step-by-step instructions Claude follows when the skill is invoked.

## Current Skills

- **python-bootstrap** (`/python-bootstrap`) — Scaffolds a Python project with uv, ruff, pyright (strict), pytest, pre-commit, and GitHub Actions CI. Runs `scripts/bootstrap.py` which generates all config and verifies tooling passes.
- **setup-ralph** (`/setup-ralph`) — Sets up an autonomous plan/build loop (RALPH) in a target repo. Auto-detects project structure, generates `AGENTS.md`, `PROMPT_plan.md`, `PROMPT_build.md`, `loop.sh`, and Docker files (`docker/Dockerfile`, `docker/entrypoint.sh`, `docker/loop.sh`, `.dockerignore`). The loop runs exclusively in Docker for isolation — `loop.sh` builds the image and runs the container, while `docker/loop.sh` orchestrates Claude invocations inside it with stale-detection and cost tracking.

## Adding a New Skill

1. Create `skills/<skill-name>/SKILL.md` with YAML frontmatter (`name`, `description`, optionally `argument-hint`)
2. Put any supporting scripts in `skills/<skill-name>/scripts/`
3. The skill description in frontmatter controls when Claude Code offers to invoke it — write it to match natural user triggers
