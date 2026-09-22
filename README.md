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
* Resolución correcta de dependencias y comandos CLI (ej: `agnara --version`, `agnara --help`).
* Funcionalidad interactiva y fail-safe de `project create`.
* Ejecución de simulacros seguros con `--dry-run`, determinismo de salida programática (`--json`), garantizando inmutabilidad.
* Comportamiento determinista: rechazo de nombres inválidos y validación explícita del flag `--overwrite`.
* Estructuración real de aplicaciones (scaffolding) vía comandos `app create` y sus atajos de perfiles (`app-api`, `app-mcp`, `app-agent`, `app-worker`).
* Conformidad con la arquitectura `modular-hexagonal` generada: `domain`, `application`, `adapters` (inbound/outbound), asertando exposiciones y archivos generados (`http.py`, `mcp.py`, `a2a.py`, `tasks.py`, `events.py`).
* Consistencia del manifiesto `agnara.toml`, validando la declaración, arquitectura y *exposures* de las apps.

## 🚫 Qué NO Valida
* No compila dependencias de ramas Git.
* No utiliza instalaciones _editable_.
* No altera el comportamiento de `site-packages`.
* No inventa el contrato de layout ni parchea el código.

---

## 🏗️ Arquitectura de la Validación
La estructura sigue rigurosamente el estándar del ecosistema A8. El test suite orquesta llamadas `subprocess` bajo directorios temporales contra el CLI empaquetado:
- `tests/test_cli.py`: Verifica aserciones deterministas de la arquitectura.
- `examples/smoke_example.py`: Prueba de humo de ejecución standalone end-to-end.
- Pipeline `validate.yml` orquestando Quality Gates obligatorios.

## 🚀 Quick Start
Para reproducir la validación localmente:

```bash
# 1. Utiliza Python 3.14 o superior
py -3.14 -m venv .venv
source .venv/bin/activate  # En Windows: .\.venv\Scripts\activate

# 2. Instala dependencias y empaquetado del validador
pip install .[dev]

# 3. Ejecuta validaciones y Quality Gates
python -m pip check
ruff format --check .
ruff check .
pytest -v
python examples/smoke_example.py
```

## 🔒 Quality Gates
El repositorio superó exitosamente el control de calidad local y la integración continua:
* **Lint y Formato:** `ruff format`, `ruff check` (completamente verde).
* **Tests:** `10` escenarios superados bajo `pytest`.
* **Smoke Test:** Ejecución end-to-end validada con éxito.
* **Empaquetado:** Validación clean install de wheel vía `python -m build`.

## 📌 Findings Reales
- **Agnara CLI Architecture:** El layout generado separa `domain`, `application` y `adapters` con jerarquías limpias de `inbound` y `outbound`.
- **Profiles / Exposures:** Los perfiles se acoplan exactamente a los *exposures* correctos y estos son registrados fielmente en el `agnara.toml`.
- **Fail-safe mechanism / Overwrite:** La prevención de sobrescritura de proyectos y el flag explícito `--overwrite` responden fielmente bajo entornos idénticos.

## ⚠️ Limitaciones Reales
- **Sintaxis Exclusiva 3.14:** El CLI requiere rigurosamente un intérprete de Python 3.14 o superior debido a convenciones internas de sintaxis y dependencias declaradas en PyPI. 

---

**Status:** Historical / Frozen / Complete