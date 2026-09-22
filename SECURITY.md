# Security Policy

## Alcance del Proyecto
Este es un proyecto validador. Las políticas de seguridad se centran en el aislamiento de las pruebas:
- **Ausencia de secretos:** El código no maneja, requiere ni produce secretos o credenciales.
- **Aislamiento de I/O:** El CLI se ejecuta de forma exclusiva en directorios temporales (`tempfile.TemporaryDirectory`).
- **No se modifica `site-packages`:** Todas las operaciones ocurren en aislamiento, sin parchear ni interceptar dependencias nativas instaladas en el sistema o en el entorno activo.
- **Fuentes oficiales:** No se prueban artefactos no oficiales (forks, ramas `main`, etc). Los findings deben reproducirse contra las versiones publicadas en PyPI A8 (`agnara==0.1.0a8`).

## Reporte de vulnerabilidades
Si detectas un comportamiento malicioso originado por la ejecución del CLI, debes reportarlo al repositorio principal del framework `agnara-project`. Este repositorio validador sólo orquesta pruebas inofensivas.
