"""The testing_app capabilities work against the port, not against storage.

These tests construct the adapter directly and call the capabilities as
functions. No application, no transport and no dependency injection is needed
to prove the behaviour, which is what the layering buys.
"""

from __future__ import annotations

import pytest

from ..adapters.outbound.memory import InMemoryRecordRepository
from ..application.capabilities import get_record, list_records
from ..domain.errors import RecordNotFound
from ..domain.models import Record
from ..domain.value_objects import Reference


def repository() -> InMemoryRecordRepository:
    return InMemoryRecordRepository(
        [
            Record(Reference("r-1"), "first"),
            Record(Reference("r-2"), "second"),
        ]
    )


def test_get_record_returns_the_stored_record() -> None:
    assert get_record("r-1", repository()) == {"reference": "r-1", "label": "first"}


def test_get_record_rejects_an_unknown_reference() -> None:
    with pytest.raises(RecordNotFound):
        get_record("missing", repository())


def test_list_records_returns_every_record_in_order() -> None:
    assert [record["reference"] for record in list_records(repository())] == ["r-1", "r-2"]


def test_a_reference_may_not_be_empty() -> None:
    """The value object holds the invariant, so no caller has to remember it."""
    with pytest.raises(ValueError, match="must not be empty"):
        Reference("   ")


def test_an_empty_repository_lists_nothing() -> None:
    assert list_records(InMemoryRecordRepository()) == []
