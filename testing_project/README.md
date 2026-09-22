# testing_project

An Agnara project.

## Layout

```text
testing_project/
├── agnara.toml          # what this project contains
├── pyproject.toml
├── src/testing_project/
│   ├── bootstrap.py     # the composition root: `app` lives here
│   ├── settings.py
│   └── apps/            # one directory per bounded context
└── tests/
```

## Install

```bash
uv sync
```

## Inspect

The composition root exposes `app`, which every Agnara tool reads:

```bash
agnara apps
agnara inspect testing_project.bootstrap:app --path src
agnara graph testing_project.bootstrap:app --path src
agnara context testing_project.bootstrap:app --path src
```

Seeing a capability is not permission to invoke it. Inspection applies the
same visibility rules a transport does; use `--visibility agent` to read the
project as a caller would.

## Test

```bash
uv run pytest
```

## Next

Add a bounded context:

```bash
agnara app create billing
```

Capabilities are declared once and exposed over any transport. Nothing in
`src/testing_project` should import a protocol package.
