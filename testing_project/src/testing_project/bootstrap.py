"""Compose the testing_project application.

This module is the composition root: it builds the application and the
dependency registry, and nothing else imports a transport. An adapter — HTTP,
MCP, or another — is wired where the process starts, so the same capabilities
stay reachable from every one of them.

``app`` is the attribute Agnara tooling reads::

    agnara inspect testing_project.bootstrap:app --path src
    agnara graph testing_project.bootstrap:app --path src

Add capabilities with ``agnara app create``, or declare one here with
``@app.capability`` while the project is small.
"""

from __future__ import annotations

from agnara import Agnara
from agnara.core.di import DIRegistry

from testing_project.settings import Settings

__all__ = ["app", "dependencies", "settings"]

settings = Settings()

#: The application. Its name becomes the namespace of every capability
#: declared on it, so a capability here is ``testing_project.<name>``.
app = Agnara(settings.name)

#: Providers the capabilities in this project depend on. Register them here so
#: one composition owns the graph, and pass it to the tooling with
#: ``--dependencies dependencies``.
dependencies = DIRegistry()
