"""Public application contracts offered by the testing_app app.

Another app may import types and protocols from this module. Everything else
inside this app remains an implementation detail. A contract describes data
or behaviour; it never imports an adapter and never calls a capability
directly, because an internal call must not bypass runtime policy.
"""

from __future__ import annotations

from typing import TypedDict

__all__ = ["RecordView"]


class RecordView(TypedDict):
    """The stable record shape this app offers to other application code."""

    reference: str
    label: str
