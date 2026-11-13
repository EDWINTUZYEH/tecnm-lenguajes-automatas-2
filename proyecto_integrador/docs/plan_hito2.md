# Plan del Hito 2 · Sesión 20 · Sentencias, ámbitos y diagnósticos

**Equipo:** Edwin, Blanca y Jimena
**Tag objetivo:** `v0.2-hito2`
**Estado:** ✅ completado (integrado en `main`; este documento queda como
mapa de trabajo y de explicación)

---

## 1. lo que se pide  (DoD oficial)

Según `docs/guia-proyecto.md` §4 y `PROYECTO.md` §4:

- [x] El parser acepta la gramática completa y rechaza lo inválido con `S01`.
- [x] Tabla de símbolos con ámbitos anidados y shadowing (la interna oculta
      a la externa mientras el bloque esté activo).
- [x] Errores `E01` (no declarada / sin valor), `E02` (redeclaración en el
      mismo ámbito) y `E04` (división entre cero constante). El formato y los
      códigos son los de `docs/gramatica.md` §6.
- [x] Se reportan **varios** errores en una pasada (recuperación, máx. 20).
- [x] `--run` ejecuta los programas (interpretar el AST está permitido en
      este hito).
- [x] `make test-hito2` en verde (14 pruebas: 9 válidos + 5 inválidos).
- [x] Tag `v0.2-hito2` y demo (3 minutos).

## 2. Punto de partida real (qué ya existe y se reutiliza)

- `lexer.[ch]` y `parser.[ch]` y `ast.[ch]`: completos (misma gramática del
  Hito 1). El parser ya cubre `if/else`, `while`, `print`, bloques y unaria.
- `diagnosticos.[ch]`: formato `archivo:línea:columna: error EXX: mensaje`,
  máximo 20 diagnósticos por pasada.
- `semantica.[ch]`: pila de ámbitos + shadowing + `E01` (no declarada /
  leída antes de asignar). Análisis conservador por ámbito (sin caminos).
- `compilador.c`: pipeline leer → lex → parse → `semantica` (solo si no hay
  errores de sintaxis). Los modos `--tac`, `--asm`, `--run` responden
  `aún no implementado`.
- `tests/propias/`: 13 casos del Hito 1. Los del Hito 2 empiezan en la
  numeración `14_*` (no se renumera nada anterior).

## 3. Orden de trabajo sugerido (un commit lógico por paso)

1. **E02** — redeclaración en el mismo ámbito: en `semantica.c`, al
   `declarar`, buscar el nombre en el ámbito más interno; si existe,
   reportar `E02`.
2. **E04** — división entre cero **constante**: al revisar `N_BIN` con
   `/`, si el divisor es constante 0 (número literal, `-n`, o binaria
   constante), reportar `E04`. Decidir dónde vive `evaluar_constante`
   (compartida con el Hito 3 en `ast.[ch]`).
3. **Lectura antes de asignar por caminos** — dejar de marcar
   `inicializada = 1` tras un `if` sin `else` o un `while` cuyo cuerpo
   asigna; solo marcarla si **todos** los caminos la asignan. Es la
   "decisión estática" que pide la especificación (aunque la rama no se
   ejecute, si no todos los caminos asignan → `E01`).
4. **Recuperación semántica**: el análisis ya continúa tras errores
   (hasta `MAX_ERRORES`); comprobar con un archivo con 2–3 errores
   mezclados (`S01` + `E01`) y añadirlo a `tests/propias/`.
5. **`--run` como intérprete del AST**: recorrer el AST en orden, con un
   entorno dinámico de ámbito (lista nombre→valor con pila de ámbitos).
   `print(e)` → `printf("%d\n", v)`. **No** genera código: es el plan
   permitido para este hito (en el Hito 4, `--run` usa el binario).
6. **Pruebas propias del Hito 2** (`tests/propias/14_*` en adelante):
   E02, E04 (`1 / 0`, `1 / (2 - 2)`), lectura antes de asignar por
   caminos, varios errores en una pasada, y `--run` de 2–3 programas.
7. **Cierre**: `make test-hito2` en verde → `README` (Estado + qué
   funciona) → `docs/avances.md` (Avance 2 con su commit) →
   `docs/entrega_hito2.md` (C-R-E-O) → tag `v0.2-hito2` → push.

## 4. Qué se toca y qué no

**Se toca:** `semantica.[ch]`, `compilador.c` (habilitar `--run`),
`ast.[ch]` o `evaluar_constante` si se comparte, `tests/propias/*`,
`docs/` (README, avances, `entrega_hito2.md`).

**No se toca:** `tests/` doradas (`validos/`, `invalidos/`, `hito1/`,
`tac/`, `run.py`), `docs/gramatica.md`, `docs/guia-proyecto.md`,
`Makefile` (ya trae `make test-hito2`).

## 5. Cómo se explica en la demo (mapa rápido)

- **Blanca**: `semantica.c` — ámbitos, shadowing, E01/E02/E04 y el
  formato de diagnóstico.
- **Edwin**: `parser.c` + recuperación + `--run` (intérprete del AST).
- **Jimena**: `tests/propias/` + demo + `docs/entrega_hito2.md`.
- Cualquier archivo: 30 segundos (qué hace / qué no hace). Si no se
  explica, esa parte no cuenta como entregada.

## 6. Riesgos y notas

- Las doradas mandan: `02_redeclaracion` → `2 E02`, `04_div_cero` →
  `1 E04`, `05_sintaxis` → `1 S01`, `01_no_declarada` y
  `03_asignacion_sin_declarar` → `1 E01`. `make test-hito2` debe dar
  **14/14** **sin modificar `tests/`**.
- El caso "leída antes de asignar" por caminos es el más fácil de pasar
  por alto: `int a; if (c) { a = 1; } print(a);` → `E01` aunque el bloque
  pueda ejecutarse (la spec exige que **todos** los caminos asignen).
- El `--run` de este hito es un intérprete; **no** es el backend del Hito 4.
