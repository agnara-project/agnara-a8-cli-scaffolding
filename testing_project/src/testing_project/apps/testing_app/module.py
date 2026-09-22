"""Wire the testing_app app into a project composition.

This is the only module that knows about both the application and its
adapters. Keep it small: it registers, it does not implement.

Call it from the project composition root::

    from testing_project.apps.testing_app import module as testing_app_module

    testing_app_module.register(app, dependencies)
"""

from __future__ import annotations

from agnara import Agnara, App
from agnara.core.di import DIRegistry, provider

from .adapters.outbound.memory import InMemoryRecordRepository
from .application.capabilities import get_record, list_records
from .application.ports import RecordRepository
from .domain.models import Record
from .domain.value_objects import Reference

__all__ = ["testing_app", "provide_records", "register"]


@provider()
def provide_records() -> RecordRepository:
    """Build this app's record repository.

    Replace the in-memory adapter with the real one here. Nothing in the
    application layer changes when you do.
    """
    return InMemoryRecordRepository([Record(Reference("example-1"), "first example record")])


#: This bounded context, and the capabilities it owns. Declared at import
#: time, so importing this module is enough to inspect or test the app on its
#: own -- no project required. The name becomes the capability namespace, so
#: these are ``testing_app.get_record`` and ``testing_app.list_records`` whichever project
#: mounts them.
testing_app = App(
    "testing_app",
    description="The testing_app bounded context.",
    module="testing_project.apps.testing_app",
)

testing_app.capability(
    description="Read one testing_app record.",
    idempotent=True,
)(get_record)
testing_app.capability(
    description="List every testing_app record.",
    idempotent=True,
)(list_records)


def register(app: Agnara, dependencies: DIRegistry) -> None:
    """Bind this app's providers and mount it on a composition.

    Registration closes when the project calls ``compile()``, so this must run
    at import time of the composition root, not later.
    """
    dependencies.bind(RecordRepository, provide_records)
    app.include(testing_app)
