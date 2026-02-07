---
name: setup-ralph
description: >
  Set up the RALPH autonomous loop workflow in a repository. Use when the user asks to
  "set up ralph", "init ralph", "add the loop", "setup the build loop", "add PROMPT files",
  or wants to configure autonomous plan/build iteration for a project. Generates AGENTS.md,
  PROMPT_plan.md, PROMPT_build.md, and loop.sh — tailored to the detected project structure.
argument-hint: "[goal description]"
---

# RALPH Setup — Autonomous Plan/Build Loop

Generate the four workflow files for the Ralph Wiggum apporach to autonomous agents:

1. **AGENTS.md** — Operational notes for Claude (build commands, project layout, validation)
2. **PROMPT_plan.md** — Instructions for the planning phase
3. **PROMPT_build.md** — Instructions for the build phase
4. **loop.sh** — Shell script that drives plan/build iterations

## Step 1: Auto-Detect Project Structure

Analyse the repository to detect as much as possible. Check these files/patterns:

| Signal | Files to check |
|--------|---------------|
| Package manager | `uv.lock`, `poetry.lock`, `Pipfile.lock`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `Cargo.lock`, `go.sum` |
| Project config | `pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`, `Makefile` |
| Source layout | `src/`, `lib/`, `app/`, `cmd/`, `internal/` directories |
| Test layout | `tests/`, `test/`, `__tests__/`, `*_test.go` patterns |
| Specs/docs | `specs/`, `spec/`, `docs/`, `requirements/` directories |
| Entrypoint | `main.py`, `app.py`, `index.ts`, `main.go`, etc. |
| CI config | `.github/workflows/`, `.gitlab-ci.yml` |

Extract these values:
- **PACKAGE_MANAGER**: e.g. `uv`, `npm`, `poetry`, `cargo`
- **INSTALL_COMMAND**: e.g. `uv sync --all-extras`, `npm install`
- **SOURCE_DIR**: e.g. `src/my_package/`, `src/`, `lib/`
- **TESTS_DIR**: e.g. `tests/`, `test/`
- **SPECS_DIR**: e.g. `specs/` (may not exist)
- **TEST_COMMAND**: e.g. `uv run pytest`, `npm test`
- **TYPECHECK_COMMAND**: e.g. `uv run pyright`, `npx tsc --noEmit` (if configured)
- **LINT_COMMAND**: e.g. `uv run ruff check src tests`, `npm run lint`
- **LANGUAGE_VERSION**: e.g. `Python 3.12`, `Node 20`, `Go 1.22`
- **BUILD_BACKEND**: e.g. `hatchling`, `webpack`, `cargo`
- **PACKAGE_NAME**: the project/package name
- **PACKAGE_ROOT**: the import root, e.g. `src/my_package`
- **TEST_CONFIG_NOTES**: e.g. `testpaths = ["tests"], pythonpath = ["src"]`
- **DB_FIXTURE_HINT**: e.g. `Use DATABASE_URL=sqlite:///:memory: for test fixtures.` (if relevant)

## Step 2: Ask the User for Missing Information

Use AskUserQuestion for anything that cannot be reliably auto-detected. Typical questions:

1. **Run command** — How do you start the application? (e.g. `uv run uvicorn pkg.main:app`, `npm start`)
2. **Ultimate goal** — One-sentence description of what the project should become. This goes into PROMPT_plan.md. If `$ARGUMENTS` was provided, use that as the goal instead of asking.
3. **Specs directory** — If no `specs/` directory exists, ask whether to create one or skip spec-based workflows.
4. **Environment variables** — Any required env vars for running the app (e.g. `DATABASE_URL`).

Do NOT ask about things you successfully auto-detected. Only ask what's genuinely unclear.

## Step 3: Generate Files

### 3a. AGENTS.md

Write `AGENTS.md` in the repo root with this structure:

```markdown
## Build & Run

- Package manager: `{PACKAGE_MANAGER}`
- Install deps: `{INSTALL_COMMAND}`
- Run the app: `{RUN_COMMAND}`
- Source code: `{SOURCE_DIR}`
- Tests: `{TESTS_DIR}`
- Specs: `{SPECS_DIR}`

## Validation

Run these after implementing to get immediate feedback:

- Tests: `{TEST_COMMAND}`
- Typecheck: `{TYPECHECK_COMMAND}`
- Lint: `{LINT_COMMAND}`

## Operational Notes

- {LANGUAGE_VERSION}, {TYPECHECK_MODE}, {LINT_TOOL} already configured in `{CONFIG_FILE}`.
- Project uses `{BUILD_BACKEND}` build backend with `{LAYOUT_DESCRIPTION}`.
- Test config: {TEST_CONFIG_NOTES}.
- {DB_FIXTURE_HINT}

### Codebase Patterns

- Type annotations are mandatory ({TYPECHECK_MODE}).
- Follow existing {LINT_TOOL} rules — see `{CONFIG_FILE}` for enabled rule sets.
```

Omit sections that don't apply (e.g. skip Typecheck line if no type checker is configured, skip DB hint if no database). Keep it concise.

### 3b. PROMPT_plan.md

Write `PROMPT_plan.md` in the repo root:

```markdown
0a. Study `{SPECS_DIR}*` with up to 250 parallel Sonnet subagents to learn the application specifications.
0b. Study @IMPLEMENTATION_PLAN.md (if present) to understand the plan so far.
0c. Study `{SOURCE_DIR}*` with up to 250 parallel Sonnet subagents to understand shared utilities & components.
0d. For reference, the application source code is in `{SRC_WILDCARD}` and tests are in `{TESTS_WILDCARD}`.
0e. Before starting new work, check `git status` for uncommitted changes from a previous iteration. If any exist, review them and `git add -A && git commit` with a message describing those changes, then `git push`.
0f. Review project-level files (`README.md`, `{CONFIG_FILE}`) and plan updates needed so that a new developer can clone the repo, follow the README, and have the app running. Include documentation tasks in the plan.

1. Study @IMPLEMENTATION_PLAN.md (if present; it may be incorrect) and use up to 500 Sonnet subagents to study existing source code in `{SRC_WILDCARD}` and `{TESTS_WILDCARD}` and compare it against `{SPECS_DIR}*`. Use an Opus subagent to analyze findings, prioritize tasks, and create/update @IMPLEMENTATION_PLAN.md as a bullet point list sorted in priority of items yet to be implemented. Ultrathink. Consider searching for TODO, minimal implementations, placeholders, skipped/flaky tests, and inconsistent patterns. Study @IMPLEMENTATION_PLAN.md to determine starting point for research and keep it up to date with items considered complete/incomplete using subagents. For each task in the plan, derive required tests from the acceptance criteria in the relevant spec — what specific outcomes need verification. Tests verify WHAT works (behavior, edge cases), not HOW it's implemented. Include required tests as part of each task definition.

IMPORTANT: Plan only. Do NOT implement anything. Do NOT assume functionality is missing; confirm with code search first. Treat `{PACKAGE_ROOT}` as the project's package root.

CONVERGENCE: If IMPLEMENTATION_PLAN.md already exists and covers all specs, verify correctness but do NOT rewrite or restyle it. Only commit if you found a factual error (wrong status code, missing task, incorrect field name) or a missing task. Do NOT commit formatting-only, rewording-only, or restructuring changes — the plan does not need to be perfect prose, it needs to be correct and complete.

ULTIMATE GOAL: {ULTIMATE_GOAL}. Consider missing elements and plan accordingly. If an element is missing, search first to confirm it doesn't exist, then if needed author the specification at {SPECS_DIR}FILENAME.md. If you create a new element then document the plan to implement it in @IMPLEMENTATION_PLAN.md using a subagent.

COMMIT: When you have made changes to any files (IMPLEMENTATION_PLAN.md, specs, etc.), `git add -A` then `git commit` with a message describing the changes, then `git push`. If nothing changed, do not create an empty commit. If the only changes you would make are cosmetic (rewording, reformatting, reordering), discard them (`git checkout -- .`) and do not commit.
```

If there is no specs directory and the user chose not to create one, remove all references to specs from the prompt.

### 3c. PROMPT_build.md

Write `PROMPT_build.md` in the repo root:

```markdown
0a. Study `{SPECS_DIR}*` with up to 500 parallel Sonnet subagents to learn the application specifications.
0b. Study @IMPLEMENTATION_PLAN.md.
0c. For reference, the application source code is in `{SRC_WILDCARD}` and tests are in `{TESTS_WILDCARD}`.
0d. Before starting new work, check `git status` for uncommitted changes from a previous iteration. If any exist, run the tests for the affected code — if they pass, `git add -A && git commit` with a message describing those changes and `git push`. If they fail, fix them first.

1. Your task is to implement functionality per the specifications using parallel subagents. Follow @IMPLEMENTATION_PLAN.md and choose the most important item to address. Before making changes, search the codebase (don't assume not implemented) using Sonnet subagents. You may use up to 500 parallel Sonnet subagents for searches/reads and only 1 Sonnet subagent for build/tests. Use Opus subagents when complex reasoning is needed (debugging, architectural decisions).
2. After implementing functionality or resolving problems, run all required tests specified in the task definition. Tasks include required tests — implement tests as part of task scope. All required tests must exist and pass before the task is considered complete. If functionality is missing then it's your job to add it as per the application specifications. Ultrathink.
3. When you discover issues, immediately update @IMPLEMENTATION_PLAN.md with your findings using a subagent. When resolved, update and remove the item.
4. When the tests pass, update @IMPLEMENTATION_PLAN.md, then `git add -A` then `git commit` with a message describing the changes. After the commit, `git push`.

9999. Required tests derived from acceptance criteria must exist and pass before committing. Tests are part of implementation scope, not optional.
99999. Important: When authoring documentation, capture the why — tests and implementation importance.
999999. Important: Single sources of truth, no migrations/adapters. If tests unrelated to your work fail, resolve them as part of the increment.
9999999. As soon as there are no build or test errors create a git tag. If there are no git tags start at 0.0.0 and increment patch by 1 for example 0.0.1 if 0.0.0 does not exist.
99999999. You may add extra logging if required to debug issues.
999999999. Keep @IMPLEMENTATION_PLAN.md current with learnings using a subagent — future work depends on this to avoid duplicating efforts. Update especially after finishing your turn.
9999999999. When you learn something new about how to run the application, update @AGENTS.md using a subagent but keep it brief. For example if you run commands multiple times before learning the correct command then that file should be updated.
99999999999. For any bugs you notice, resolve them or document them in @IMPLEMENTATION_PLAN.md using a subagent even if it is unrelated to the current piece of work.
999999999999. Implement functionality completely. Placeholders and stubs waste efforts and time redoing the same work.
9999999999999. When @IMPLEMENTATION_PLAN.md becomes large periodically clean out the items that are completed from the file using a subagent.
99999999999999. If you find inconsistencies in the specs/* then use an Opus subagent with 'ultrathink' requested to update the specs.
999999999999999. IMPORTANT: Keep @AGENTS.md operational only — status updates and progress notes belong in `IMPLEMENTATION_PLAN.md`. A bloated AGENTS.md pollutes every future loop's context.
```

If there is no specs directory, remove spec references (lines 0a, the spec-related parts of step 1, and the final spec inconsistency rule).

### 3d. loop.sh

Copy the file from `<skill_path>/scripts/loop.sh` into the repo root. Make it executable with `chmod +x loop.sh`.

## Step 4: Add `logs/` to `.gitignore`

The loop script writes raw JSONL logs to a `logs/` directory. Ensure this directory is git-ignored:

1. Check if a `.gitignore` file exists in the repo root.
   - If it does, read it and check whether `logs/` (or `logs`) is already listed.
   - If it's already ignored, skip this step.
   - If not, append `logs/` to the existing `.gitignore`.
2. If no `.gitignore` exists, create one containing `logs/`.

## Step 5: Create specs/ directory (if agreed)

If the user agreed to create a specs directory, create `specs/` and add a placeholder `specs/README.md` with a one-liner explaining that spec files go here.

## Step 6: Summary

After generating all files, print a summary showing:
- Which files were created
- How to use the loop: `./loop.sh plan` for planning, `./loop.sh` for building
- Remind the user to create an `IMPLEMENTATION_PLAN.md` by running `./loop.sh plan`
- Note that `AGENTS.md` should be kept up to date as the project evolves
