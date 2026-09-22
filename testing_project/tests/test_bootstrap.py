"""The composition root builds an application that Agnara can read.

This is the check that the project is wired correctly. It fails if the
composition stops importing, if the application loses its name, or if the
registry cannot be compiled and frozen for startup.
"""

from __future__ import annotations

from agnara import Agnara

from testing_project.bootstrap import app, dependencies


def test_the_composition_builds_an_application() -> None:
    assert isinstance(app, Agnara)
    assert app.name == "testing_project"


def test_the_dependency_registry_exists_for_capabilities_to_use() -> None:
    assert dependencies is not None


def test_the_registry_can_be_compiled_and_frozen() -> None:
    """Registration closes at startup; a capability added later is a defect."""
    compiled = app.compile()

    assert compiled is not None
    assert app.is_compiled
