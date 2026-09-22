# Protocolo para Agentes (A8 Agents Guidelines)

Cualquier sistema autónomo o agente de código operando en este repositorio debe acatar estrictamente las siguientes directivas:

1. **Inmutabilidad de Dependencias:** NO actualizar bajo ningún motivo la versión de `agnara` o `agnara-cli` configurada en `pyproject.toml`. El objetivo central es validar `0.1.0a8`.
2. **Respeto a la Evidencia Real:** NO alterar expectativas de los tests (asserts) meramente para "hacerlos pasar" encubriendo una falla. Si A8 presenta un comportamiento distinto, documenta el hallazgo, corrige el test *para coincidir con la salida real* del framework y resáltalo.
3. **Black-box Testing:** NO simular comandos ni mockear (mock) I/O del CLI. Usa `subprocess` contra el binario `agnara`.
4. **No Inventar Estructuras:** NO asumir la forma del layout modular. Si `agnara` genera carpetas `adapters/` en lugar de `infrastructure/`, asertar contra `adapters/`. Observa antes de validar.
5. **Quality Gates Mandatory:** NO finalizar ni declarar completitud sin ejecutar *y obtener luz verde* en la totalidad de los quality gates: `ruff format`, `ruff check`, `pytest`, `smoke test` y `build` + clean install.
