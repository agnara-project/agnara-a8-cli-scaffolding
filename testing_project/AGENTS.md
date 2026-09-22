# AGENTS.md — testing_project

Instructions for coding agents working in this project.

## Model

This is an Agnara project. A **capability** is the unit of behaviour: it is
declared once, in Python, and exposed over any transport. HTTP, MCP and other
protocols are adapters, never the source of truth.

An **app** under `src/testing_project/apps/` is a bounded context. It owns its
capabilities and is understandable on its own.

## Rules

- Do not import a transport package (`agnara_http`, `agnara_mcp`, or any web
  framework) from domain or application code. Adapters are wired where the
  process starts.
- `src/testing_project/bootstrap.py` is the composition root. Keep `app` there.
- Registration closes at startup. Declare capabilities at import time; do not
  add them after `compile()`.
- `agnara.toml` records what this project contains. Change it with
  `agnara app create` rather than by hand where a command exists.
- Never put secrets in `agnara.toml` or in `settings.py`.

## Commands

```bash
uv run pytest
uv run ruff check .
agnara apps
agnara inspect testing_project.bootstrap:app --path src
```

## Before finishing

Run the tests and the linter. Do not mark work complete without them passing.
