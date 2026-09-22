# Agnara CLI 0.1.0a8 Validation

Este proyecto es un entorno de validación exclusivo para `agnara-cli==0.1.0a8`, diseñado para probar la experiencia de un desarrollador al iniciar un nuevo proyecto ("commerce") con diseño hexagonal-modular y los módulos "users", "catalog" y "payments".

## ⚠️ Estado de la Validación: BLOQUEADO

La validación del CLI en la versión `0.1.0a8` ha revelado problemas críticos que impiden la ejecución de cualquier comando. No fue posible validar el comportamiento del layout, `--dry-run`, salida `--json` ni instrucciones de bootstrap, ya que la herramienta falla inmediatamente al ser importada.

Siguiendo la directiva de no modificar el framework y no ocultar comportamientos distintos, los problemas han sido aislados y documentados.

---

## Release validation

### Entorno y Versión
- **Versión a validar:** `agnara-cli==0.1.0a8` (instalado desde PyPI)
- **Versión de Python utilizada:** `3.13.14`
- **Paquetes principales instalados:**
  - `agnara==0.1.0a8`
  - `agnara-cli==0.1.0a8`

### Comandos de Instalación Reproducibles

Durante la instalación se detectó que el paquete declara requerir `Python >= 3.14`. Para poder instalarlo, fue necesario usar el flag `--ignore-requires-python`:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install agnara-cli==0.1.0a8 --ignore-requires-python pytest
```

### Hallazgos y Limitaciones (Gaps)

**1. Metadatos de PyPI Incorrectos (`Requires-Python >=3.14`)**
El paquete `agnara-cli==0.1.0a8` no puede ser instalado normalmente con versiones estables de Python debido a su restricción de versión en los metadatos.

**2. CLI Inutilizable por `SyntaxError` (Sintaxis antigua de Python)**
Al intentar ejecutar `agnara` en la terminal (ej: `agnara --help` o `agnara project create`), el framework lanza un error de sintaxis nativo que bloquea toda la ejecución. El error se origina en el archivo `agnara/capability/registry.py` por usar una sintaxis de captura de excepciones incompatible con Python 3 (`except E, V:`).

**Traza del error:**
```text
  File "...\.venv\Lib\site-packages\agnara\capability\registry.py", line 77
    except KeyError, DefinitionError:
           ^^^^^^^^^^^^^^^^^^^^^^^^^
SyntaxError: multiple exception types must be parenthesized
```

**Impacto:** Es **imposible** validar los comandos `project create`, `app create`, o las salidas en formato JSON y dry-run.

---

## Ejemplo Ejecutable (MRE)

Se ha creado un Caso Mínimo Reproducible (MRE) en `mre.py` que aisla e ilustra el problema de importación sin dependencias complejas. 

Para ejecutarlo:
```bash
python mre.py
```

## Pruebas (Test Suite)

Se implementó el suite de validación `test_cli.py` con las aserciones preparadas para el comportamiento esperado del CLI (`dry-run` sin modificar el sistema de archivos, salida `json` parseable, y creación de arquitectura hexagonal). 

Al ejecutar las pruebas con `pytest test_cli.py -v`, estas fallan (y una es omitida) correctamente, reflejando que el CLI actual es incapaz de completar las operaciones requeridas.

## Integración Continua (CI)
Se configuró un flujo de GitHub Actions en `.github/workflows/validate.yml` que instala el CLI, ejecuta el MRE y el suite de pruebas, documentando el estado actual de la versión `0.1.0a8`.