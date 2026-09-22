"""Errors of the testing_app domain.

Domain errors are protocol-neutral. An adapter decides what an HTTP status or
an MCP error looks like; the domain only says what went wrong.
"""

from __future__ import annotations

from .value_objects import Reference

__all__ = ["TestingAppError", "RecordNotFound"]


class TestingAppError(Exception):
    """Base class for every error this app raises.

    One base lets a caller distinguish this app's failures from anything else
    without catching bare ``Exception``.
    """


class RecordNotFound(TestingAppError):
    """No record exists for the requested reference."""

    def __init__(self, reference: Reference) -> None:
        super().__init__(f"no record for {reference.value!r}")
        self.reference = reference
