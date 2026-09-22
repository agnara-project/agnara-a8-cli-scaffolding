"""Entities of the testing_app domain.

Pure business concepts. No framework import, no transport type, no storage
concern: this module should still make sense if every adapter were replaced.
"""

from __future__ import annotations

from dataclasses import dataclass

from .value_objects import Reference

__all__ = ["Record"]


@dataclass(frozen=True, slots=True)
class Record:
    """One thing this app is responsible for.

    Rename it to whatever your domain calls its central concept, and give it
    the invariants that concept actually has.
    """

    reference: Reference
    label: str
