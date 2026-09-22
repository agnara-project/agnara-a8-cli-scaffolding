# Contributing

## Estado del Repositorio
Este repositorio quedará **congelado** después de cerrar la validación actual para la versión `0.1.0a8`. 
Por diseño, **no debe migrarse** a versiones posteriores de Agnara. Su propósito es actuar como registro inmutable e histórico (snapshot) de la usabilidad y calidad estructural producida por esta versión exacta del CLI.

## Restricciones
- No se aceptan Pull Requests que añadan nuevas features propias al CLI o al Framework.
- No se aceptan actualizaciones de versión de `agnara` o `agnara-cli`.
- Cualquier modificación a los tests debe preservar la filosofía "black-box" y limitarse estrictamente a evidenciar y documentar comportamientos existentes de `0.1.0a8` en `Python 3.14.x`.
