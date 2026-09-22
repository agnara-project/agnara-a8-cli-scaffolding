"""The testing_app app: one bounded context of the testing_project project.

Layers, and the direction they depend in:

    adapters/inbound  -> application -> domain
    adapters/outbound -> application (implements its ports)

Nothing here imports a transport package. ``module.register`` is the only
place that wires this app into a project composition.
"""

__all__: list[str] = []
