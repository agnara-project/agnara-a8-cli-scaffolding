# Agnara 0.1.0a8 CLI & Scaffolding Validation

**Ecosystem Role:** CLI & Scaffolding Validation  
**Target:** `agnara==0.1.0a8`  
**CLI:** `agnara-cli==0.1.0a8`  
**Python:** `>=3.14`  

Este repositorio actúa de forma exclusiva como consumidor externo y validador de los binarios distribuidos en PyPI para el framework Agnara 0.1.0a8. Demuestra la experiencia real de un desarrollador al inicializar y estructurar proyectos mediante la herramienta `agnara`.

---

## 🎯 Qué Valida
El validador consume el paquete oficial de PyPI y comprueba:
* Instalación en un entorno limpio (`Python 3.14.x`).
* Resolución correcta de dependencias y CLI commands (ej: `agnara --version`, `agnara --help`).
* Funcionalidad interactiva y fail-safe de `project create`.
* Ejecución de simulacros seguros con `--dry-run` y salidas programáticas (`--json`).
* Comportamiento determinista: rechazo de nombres inválidos y conflictos con archivos existentes.
* Estructuración real de aplicaciones (scaffolding) vía comandos `app create` y sus atajos (`app-api`, `app-mcp`, `app-agent`, `app-worker`).
* Conformidad con la arquitectura `modular-hexagonal` generada: `domain`, `application`, `adapters` (inbound/outbound).

## 🚫 Qué NO Valida
* No compila dependencias de ramas Git.
* No utiliza instalaciones _editable_.
* No altera el comportamiento de `site-packages`.
* No comprueba las versiones obsoletas o sintaxis antiguas que no correspondan con el target (Python 3.14+).

---

## 🏗️ Arquitectura de la Validación
La estructura sigue rigurosamente el estándar del ecosistema A8. El test suite fue diseñado aislando comandos `subprocess` bajo directorios temporales, y consumiendo los binarios ubicados en el `PATH` para evitar mutar el _FS_ y afirmar el comportamiento real:
- `tests/test_cli.py`: Verifica aserciones deterministas de la arquitectura.
- `examples/smoke_example.py`: Prueba de humo de ejecución standalone.
- Pipeline `validate.yml` con Quality Gates.

## 🚀 Quick Start
Para reproducir la validación localmente:

```bash
# 1. Utiliza Python 3.14 o superior
py -3.14 -m venv .venv
source .venv/bin/activate  # En Windows: .\.venv\Scripts\activate

# 2. Instala dependencias y empaquetado del validador
pip install .[dev]

# 3. Ejecuta validaciones y Quality Gates
ruff check .
pytest -v
python examples/smoke_example.py
```

## 🔒 Quality Gates
El repositorio superó exitosamente el control de calidad local y la integración continua:
* **Lint y Formato:** `ruff format`, `ruff check`
* **Tests:** 9 escenarios superados bajo `pytest`.
* **Empaquetado:** Validación clean install de wheel vía `python -m build`.

## 📌 Findings Reales
- **Agnara CLI Architecture:** El layout generado separa correctamente `domain`, `application` y `adapters` con jerarquías limpias de `inbound` y `outbound`, alineándose al patrón modular-hexagonal prometido.
- **Fail-safe mechanism:** La prevención de sobrescritura de proyectos existentes es robusta y retorna advertencias limpias.

## ⚠️ Limitaciones Reales
- **Sintaxis de Python:** `agnara-cli==0.1.0a8` requiere estrictamente **Python 3.14 o superior** como se estipula en sus metadatos de PyPI. Las instalaciones en versiones previas (como 3.13) arrojan fallos nativos de `SyntaxError` (ej: `except KeyError, DefinitionError:`), debido a que esa notación es dependiente de las características del runtime actual.

---

**Status:** Historical / Frozen / Complete