"""Capabilities of the testing_app app.

A capability is the unit of behaviour. It is declared once, here, and exposed
over any transport by an adapter — never the other way round. These functions
know nothing about HTTP, MCP or any protocol, and that is the point.

A parameter annotated with a registered dependency type is supplied by the
runtime, not by the caller: ``records`` never appears in a capability's input
schema and a caller cannot pass one.
"""

from __future__ import annotations

from ..domain.errors import RecordNotFound
from ..domain.value_objects import Reference
from .contracts import RecordView
from .ports import RecordRepository

__all__ = ["get_record", "list_records"]


def get_record(reference: str, records: RecordRepository) -> RecordView:
    """Read one record by its reference."""
    identifier = Reference(reference)
    found = records.get(identifier)
    if found is None:
        raise RecordNotFound(identifier)
    return {"reference": found.reference.value, "label": found.label}


def list_records(records: RecordRepository) -> list[RecordView]:
    """List every record this app holds."""
    return [
        {"reference": record.reference.value, "label": record.label} for record in records.all()
    ]
