"""Value objects of the testing_app domain.

A value object has no identity of its own: two with the same contents are the
same value. Frozen, so one cannot be changed after it has been validated.
"""

from __future__ import annotations

from dataclasses import dataclass

__all__ = ["Reference"]


@dataclass(frozen=True, slots=True)
class Reference:
    """A stable identifier for one record in this app.

    Replace this with the identifier your domain actually has. Keeping it a
    value object rather than a bare ``str`` is what lets the type system say
    which strings are references and which are not.
    """

    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("a reference must not be empty")
