# Proyecto Integrador · Lenguajito

Empieza por la **[guía del proyecto](docs/guia-proyecto.md)**: explica cómo se
trabaja, qué se entrega en cada hito y cómo se evalúa.

Compilador para **Lenguajito**, el lenguaje del Proyecto Integrador de
*Lenguajes y Autómatas II (SCD-1016)*. Todo el proyecto vive en esta carpeta.

**Equipo:** Edwin, Blanca y Jimena

- Reglas y rúbrica: [`../PROYECTO.md`](../PROYECTO.md)
- Lenguaje, AST, diagnósticos y TAC: [`docs/gramatica.md`](docs/gramatica.md)
- Guía de trabajo: [`docs/guia-proyecto.md`](docs/guia-proyecto.md)
- Avances: [`docs/avances.md`](docs/avances.md)
- Plan del Hito 2 (mapa de trabajo y de explicación): [`docs/plan-hito2.md`](docs/plan-hito2.md)
- Pruebas: [`tests/`](tests/)

## Estado por hitos

| Hito | Tema | Estado |
| :--- | :--- | :--- |
| 1 | Léxico, sintaxis y AST (`--tokens`, `--ast`, `--check`) | ✅ terminado (tag `v0.1-hito1`) |
| 2 | Sentencias, ámbitos y diagnósticos completos (`E02`, `E04`, `--run`) | ⏳ pendiente (sesión 20) |
| 3 | TAC con plegado de constantes y código muerto | ⏳ pendiente (sesión 30) |
| 4 | Backend x86-64, enlace y binario ELF | ⏳ pendiente (sesión 40) |

> Esta tabla se actualiza en cada entrega. Ver `docs/entrega_hitoN.md`.

## Cómo se construye y se prueba

```bash
make             # construye ./lenguajito
make test-hito1  # pruebas del Hito 1 → 4/4
python3 tests/propias/revisar.py  # pruebas propias del equipo → 13/13
./lenguajito programa.lj --tokens
./lenguajito programa.lj --ast
./lenguajito programa.lj --check
```

> `make test` (toda la suite) **todavía no está en verde**: incluye las
> pruebas doradas de los Hitos 2, 3 y 4, que se entregan en las sesiones
> siguientes. La evidencia del Hito 1 es `make test-hito1`.

## Qué funciona hoy

- `--tokens`: imprime `LINEA:COLUMNA TIPO lexema`, un token por línea; el
  último token es `LINEA:COLUMNA EOF`. Los comentarios `//`, los espacios,
  los tabuladores y los saltos de línea se ignoran (los archivos CRLF
  funcionan igual).
- `--ast`: imprime el árbol en una sola línea con el formato de la
  especificación (sección 4 de `docs/gramatica.md`). Cubre declaraciones,
  asignaciones, `if/else`, `while`, `print`, bloques y expresiones con la
  precedencia de la gramática (asociatividad izquierda).
- `--check`: análisis léxico, sintáctico y semántico básico:
  - `S01` de sintaxis y de carácter inválido; el parser recupera en `;` y
    `}` y reporta varios errores por pasada (máximo 20);
  - `E01` **variable no declarada** (lectura o asignación) y
    **leída antes de asignar valor**, con ámbitos anidados por bloque y
    shadowing (el ámbito interno oculta al externo mientras el bloque
    esté activo; al cerrarlo, sus variables dejan de existir);
  - el análisis es conservador por ámbito: no distingue caminos de
    `if`/`while` (se afina en el Hito 2);
  - los diagnósticos usan el formato `archivo:línea:columna: error EXX:
    mensaje` y el compilador sale con código 1 si hay errores.
- Códigos de salida del compilador: `0` sin errores, `1` errores de
  compilación, `2` uso incorrecto de la línea de comandos.
- `make test-hito1` → `4/4 pruebas superadas`;
  `python3 tests/propias/revisar.py` → `13/13 pruebas superadas`.

## Qué no funciona todavía

- `E02` (redeclaración en el mismo ámbito) y `E04` (división entre cero
  constante): llegan en el **Hito 2**, junto con el análisis semántico
  completo y `--run`.
- Lectura antes de asignar por caminos (`if`/`while`): hoy el análisis es
  conservador; el diagnóstico exacto en todos los caminos es del Hito 2.
- `--tac`, `--asm` y `--run` responden `modo ... aún no implementado`
  (Hitos 3 y 4).
- Los literales enteros mayores que `INT_MAX` se truncan con `strtol`
  (el lenguaje base no exige otro comportamiento).

## Arquitectura

```text
src/
├── main.c            # interfaz de línea de comandos (proporcionada)
├── compilador.c      # orquesta las etapas según el modo
├── compilador.h
├── util.[ch]         # buffer dinámico y utilidades
├── diagnosticos.[ch] # registro de errores con formato y límite de 20
├── lexer.[ch]        # tokens con línea y columna
├── ast.[ch]          # nodos, liberación e impresión del AST
├── parser.[ch]       # descendente recursivo, recuperación con ';' y '}'
└── semantica.[ch]    # ámbitos por bloque, shadowing y E01 (variable no declarada)
```

## Reparto de trabajo

| Integrante | Archivos / etapas | Entrega |
| :--- | :--- | :--- |
| Edwin | `util`, `lexer`, `parser`, `ast`, `compilador` (léxico, sintaxis, AST, CLI) | Hito 1 (tag `v0.1-hito1`) |
| Blanca | `diagnosticos`, `semantica` (ámbito y E01), `tests/propias/` | Hito 1 (tag `v0.1-hito1`) |
| Jimena | Documentación del entregable (`README`, `docs/avances.md`, `docs/entrega_hito1.md`) y preparación de la demo | Hito 1 (tag `v0.1-hito1`) |

## Bitácora de IA

Cada entrega incluye su bitácora C-R-E-O en `docs/entrega_hitoN.md`
([`docs/entrega_hito1.md`](docs/entrega_hito1.md) para el Hito 1).
