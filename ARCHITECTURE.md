# Architecture

Este repositorio funciona exclusivamente como un entorno validador de los binarios distribuidos. No contiene código fuente del framework ni modifica su comportamiento interno.

## Flujo de Validación

El modelo de ejecución obedece a la siguiente cadena:

```text
PyPI
  ↓
agnara-cli==0.1.0a8
  ↓
agnara executable
  ↓
project/app scaffolding
  ↓
temporary validation workspace
```

Las pruebas de integración y los ejemplos (`tests/test_cli.py`, `examples/smoke_example.py`) orquestan llamadas puras mediante `subprocess` al ejecutable `agnara` proveído en el entorno virtual activo. Todas las pruebas que involucran creación de proyectos interactúan contra un sistema de archivos temporal, de manera que:
1. No se corrompe el repositorio.
2. El proyecto no modifica Agnara ni replica su CLI.
3. El estado observado es 100% idéntico a la experiencia final de usuario (black-box testing).
