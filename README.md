# claude-code-stuff

A personal collection of Claude Code artifacts — custom skills, plugins, and configuration references.

## Skills

### `/python-bootstrap`
Scaffolds a new Python project with a production-ready toolchain: uv, ruff, pyright (strict), pytest, pre-commit hooks, and GitHub Actions CI.

### `/setup-ralph`
Sets up an autonomous plan/build loop (RALPH) in a repository. Generates `AGENTS.md`, `PROMPT_plan.md`, `PROMPT_build.md`, and `loop.sh` tailored to the detected project structure.

## Claude Code Configuration

Claude Code settings live in JSON files at two levels:

| Scope | File | Purpose |
|-------|------|---------|
| **User** | `~/.claude/settings.json` | Global defaults — applies to all projects |
| **Project** | `.claude/settings.json` | Per-repo settings — committed and shared with the team |
| **Project (local)** | `.claude/settings.local.json` | Per-repo overrides — gitignored, personal preferences |

Settings are merged with project taking precedence over user.

Key things you can configure:
- **Allowed/denied tools** — control which tools Claude can use without prompting (e.g. `Bash(git *)`, `Read`, `Edit`)
- **MCP servers** — add custom tool servers for additional capabilities
- **Custom slash commands** — project-specific skills via `.claude/commands/` directory
- **Environment variables** — set `CLAUDE_CODE_*` vars to control behaviour

### CLAUDE.md

`CLAUDE.md` is a special file Claude reads automatically for project context. Place it in the repo root for project-wide instructions or in subdirectories for scoped context. Use it for:
- Build/test/lint commands
- Code style preferences and conventions
- Architecture notes and project-specific guidance

## Useful Links

- [Claude Code Documentation](https://code.claude.com/docs/en/overview)
- [Claude Code Extensibility Guide](https://happysathya.github.io/claude-code-extensibility-guide.html)
