"""Explicit settings for the testing_project project.

Deliberately plain: a frozen value type constructed by ``bootstrap`` rather
than a module that reads the environment when imported. Where configuration
comes from is a decision this project has not made yet, and a generator should
not make it silently. Add a loader here when you choose one, and keep secrets
out of the manifest and out of version control.
"""

from __future__ import annotations

from dataclasses import dataclass

__all__ = ["Settings"]


@dataclass(frozen=True, slots=True)
class Settings:
    """Values the composition needs to build the application."""

    name: str = "testing_project"
    debug: bool = False
