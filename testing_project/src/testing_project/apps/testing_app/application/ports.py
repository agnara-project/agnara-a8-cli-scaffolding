"""What the testing_app application needs from the outside world.

A port is a protocol the application depends on and an adapter implements.
Declaring it here, rather than importing a repository directly, is what keeps
the direction of the dependency pointing inward: storage can be replaced
without the application knowing.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from ..domain.models import Record
from ..domain.value_objects import Reference

__all__ = ["RecordRepository"]


@runtime_checkable
class RecordRepository(Protocol):
    """Read access to this app's records."""

    def get(self, reference: Reference) -> Record | None:
        """Return the record with this reference, or ``None``."""
        ...

    def all(self) -> tuple[Record, ...]:
        """Return every record, in a stable order."""
        ...
