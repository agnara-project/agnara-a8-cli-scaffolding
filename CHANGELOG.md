# Changelog

All notable changes to this validation project will be documented in this file.

## [0.1.0] - 2026-09-21

### Added
- Validación histórica para `agnara-cli==0.1.0a8`.
- Casos de prueba exhaustivos para scaffolding (`project create`, `app create`).
- Verificación estructural de arquitectura modular-hexagonal (`domain/`, `application/`, `adapters/`).
- Validaciones para atajos de perfiles (`app-api`, `app-mcp`, `app-agent`, `app-worker`).
- Pruebas estrictas de comportamiento inmutable en `--dry-run` y salidas JSON deterministas.
- Controles de overwrite y fail-safe de colisión de archivos.
- `smoke_example.py` orquestando ciclo de vida end-to-end de un proyecto efímero.
