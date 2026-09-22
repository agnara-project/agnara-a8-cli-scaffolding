"""An in-memory implementation of the testing_app record port.

Enough to run and to test against. Replace it with the real storage adapter —
a database, an HTTP client, a queue — and the application layer does not
change, because it depends on the port rather than on this class.
"""

from __future__ import annotations

from collections.abc import Iterable

from ...domain.models import Record
from ...domain.value_objects import Reference

__all__ = ["InMemoryRecordRepository"]


class InMemoryRecordRepository:
    """Holds records in a dictionary keyed by reference."""

    __slots__ = ("_records",)

    def __init__(self, records: Iterable[Record] = ()) -> None:
        self._records: dict[Reference, Record] = {record.reference: record for record in records}

    def get(self, reference: Reference) -> Record | None:
        """Return the record with this reference, or ``None``."""
        return self._records.get(reference)

    def all(self) -> tuple[Record, ...]:
        """Return every record, in insertion order."""
        return tuple(self._records.values())
