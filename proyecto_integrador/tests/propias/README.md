# Pruebas propias · Hito 1

Programas de prueba del equipo para el **Hito 1** (léxico, sintaxis, AST y
semántica básica `E01`). No tocan las pruebas doradas de `../validos/`,
`../invalidos/`, `../hito1/` ni `../tac/`.

Se ejecutan con:

```bash
cd proyecto_integrador
make
make test-propias     # python3 tests/propias/revisar.py
```

Convención (ver `revisar.py` para el detalle): junto a cada `caso.lj` puede
haber un `caso.tokens` (salida exacta de `--tokens`), un `caso.ast` (salida
exacta de `--ast`) o un `caso.err` (una línea `LINEA CODIGO` por diagnóstico
esperado en `--check`, que debe salir con código 1). Si no hay `.err`,
`--check` debe salir con 0.

| Caso | Qué cubre |
| :--- | :--- |
| `01_comentarios` | `--tokens`: comentarios `//`, columnas y línea `EOF` final |
| `02_precedencia` | `--ast`: precedencia `* /` sobre `+ -` y asociatividad izquierda |
| `03_comparaciones` | `--ast`: comparaciones dentro de una declaración |
| `04_unario_parentesis` | `--ast`: menos unario, más unario y paréntesis anidados |
| `05_si_si_no` | `--ast`: `if/else` con bloques y formato `(si ...)` |
| `06_mientras` | `--ast`: `while` con bloque y asignación dentro |
| `07_e01_no_declarada` | `--check`: E01 al leer una variable no declarada |
| `08_asignacion_sin_declarar` | `--check`: E01 al asignar a una variable no declarada |
| `09_leida_antes_asignar` | `--check`: E01 al leer una variable declarada sin valor |
| `10_sombra_ok` | `--check`: shadowing en bloque anidado, sin errores |
| `11_ambito_bloque` | `--check`: las variables de un bloque mueren al cerrarlo |
| `12_multiples_errores` | `--check`: varios diagnósticos `E01` en una sola pasada |
| `13_caracter_invalido` | `--check`: error léxico `S01` por carácter inválido |
