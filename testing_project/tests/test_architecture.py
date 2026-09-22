"""Architecture rules for dependencies between bounded-context apps."""

from __future__ import annotations

import ast
from importlib.util import resolve_name
from pathlib import Path

PROJECT_PACKAGE = "testing_project"
APPS_ROOT = Path(__file__).parents[1] / "src" / PROJECT_PACKAGE / "apps"
PUBLIC_SUFFIX = ("application", "contracts")


def _package_of(path: Path) -> str:
    relative = path.relative_to(APPS_ROOT).with_suffix("")
    parts = [PROJECT_PACKAGE, "apps", *relative.parts]
    parts.pop()
    return ".".join(parts)


def _imports(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    package = _package_of(path)
    imported: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            target = "." * node.level + (node.module or "")
            resolved = resolve_name(target, package) if node.level else target
            if not node.module or resolved == f"{PROJECT_PACKAGE}.apps":
                imported.extend(f"{resolved}.{alias.name}" for alias in node.names)
            else:
                imported.append(resolved)
    return imported


def test_apps_import_only_public_contracts() -> None:
    """One app may reach only another app's explicit application contract."""
    prefix = f"{PROJECT_PACKAGE}.apps."
    offenders: list[str] = []
    if not APPS_ROOT.exists():
        return
    for path in sorted(APPS_ROOT.rglob("*.py")):
        relative = path.relative_to(APPS_ROOT)
        owner = relative.parts[0]
        for imported in _imports(path):
            if not imported.startswith(prefix):
                continue
            parts = imported.removeprefix(prefix).split(".")
            target, *suffix = parts
            if target != owner and tuple(suffix) != PUBLIC_SUFFIX:
                offenders.append(f"{relative.as_posix()} imports {imported}")
    assert not offenders, "cross-app imports must target application.contracts:\n" + "\n".join(
        offenders
    )
