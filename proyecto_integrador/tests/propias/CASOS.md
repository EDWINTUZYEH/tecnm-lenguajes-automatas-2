# Casos de prueba propios · Hitos 1 y 2

Programas de prueba del equipo para los **Hitos 1 y 2** (léxico, sintaxis,
AST, semántica completa y `--run`). No tocan las pruebas doradas de
`../validos/`, `../invalidos/`, `../hito1/` ni `../tac/`.

Se ejecutan con (desde `proyecto_integrador/`):

```bash
make
make test-propias
```

Convención (ver `revisar.py` para el detalle): junto a cada `caso.lj` puede
haber un `caso.tokens` (salida exacta de `--tokens`), un `caso.ast` (salida
exacta de `--ast`), un `caso.out` (salida exacta de `--run`), un `caso.err`
(una línea `LINEA CODIGO` por diagnóstico esperado en `--check`, que debe
salir con código 1) o un `caso.diag` (lista exacta y ordenada de todos los
diagnósticos de una pasada). Si no hay `.err` ni `.diag`, `--check` debe
salir con 0.

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
| `14_caminos_if` | `--run`: `if/else` y `if` anidados inicializan en todos los caminos |
| `15_ambito_while` | `--run`: ámbito nuevo en cada vuelta del `while` |
| `16_sombra_init` | `--run`: el inicializador de la variable interna ve la externa |
| `17_ambito_anidado` | `--run`: shadowing en tres niveles de bloques |
| `18_e01_if_sin_else` | `--check`: E01 porque un `if` sin `else` no inicializa |
| `19_e01_while` | `--check`: E01 porque el cuerpo del `while` puede no ejecutarse |
| `20_multiples_errores` | `--check`: `E01`, `E01` y `E04` en una sola pasada |
| `21_sintaxis_multiples` | `--check`: recuperación sintáctica con dos `S01` |
