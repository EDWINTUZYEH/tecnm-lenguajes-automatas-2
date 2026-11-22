# Proyecto Integrador · Lenguajito

Empieza por la **[guía del proyecto](docs/guia-proyecto.md)**: explica cómo se
trabaja, qué se entrega en cada hito y cómo se evalúa.

Compilador para **Lenguajito**, el lenguaje del Proyecto Integrador de
*Lenguajes y Autómatas II (SCD-1016)*. Todo el proyecto vive en esta carpeta.

**Equipo:** Edwin, Blanca y Jimena

- Reglas y rúbrica: [`../PROYECTO.md`](../PROYECTO.md)
- Índice de documentación: [`docs/README.md`](docs/README.md)
- Lenguaje, AST, diagnósticos y TAC: [`docs/gramatica.md`](docs/gramatica.md)
- Guía de trabajo: [`docs/guia-proyecto.md`](docs/guia-proyecto.md)
- Avances: [`docs/avances.md`](docs/avances.md)
- Entrega del Hito 1: [`docs/entrega_hito1.md`](docs/entrega_hito1.md)
- Plan del Hito 2 (mapa de trabajo y de explicación): [`docs/plan_hito2.md`](docs/plan_hito2.md)
- Diseño del Hito 2 (cómo se implementó): [`docs/diseno_hito2.md`](docs/diseno_hito2.md)
- Entrega del Hito 2: [`docs/entrega_hito2.md`](docs/entrega_hito2.md)
- Diseño del Hito 3 (TAC y optimización): [`docs/diseno_hito3.md`](docs/diseno_hito3.md)
- Entrega del Hito 3: [`docs/entrega_hito3.md`](docs/entrega_hito3.md)
- Diseño del Hito 4 (backend x86-64): [`docs/diseno_hito4.md`](docs/diseno_hito4.md)
- Entrega del Hito 4: [`docs/entrega_hito4.md`](docs/entrega_hito4.md)
- Pruebas: [`tests/`](tests/)

## Estado por hitos

| Hito | Tema | Estado |
| :--- | :--- | :--- |
| 1 | Léxico, sintaxis y AST (`--tokens`, `--ast`, `--check`) |  terminado (tag `v0.1-hito1`) |
| 2 | Sentencias, ámbitos y diagnósticos completos (`E02`, `E04`, `--run`) |  terminado (tag `v0.2-hito2`) |
| 3 | TAC con plegado de constantes y código muerto | terminado (tag `v0.3-hito3`) |
| 4 | Backend x86-64, enlace y binario ELF |  terminado (tag `v1.0-hito4`) |

> Esta tabla se actualiza en cada entrega. Ver `docs/entrega_hitoN.md`.

## Cómo se construye y se prueba

```bash
make             # construye ./lenguajito
make test        # toda la suite → 20/20
make test-hito1  # pruebas del Hito 1 → 4/4
make test-hito2  # pruebas del Hito 2 → 14/14
make test-hito3  # pruebas del Hito 3 → 15/15
make test-hito4  # pruebas del Hito 4 → 16/16
make test-propias  # pruebas propias del equipo → 23/23
./lenguajito programa.lj --tokens
./lenguajito programa.lj --ast
./lenguajito programa.lj --check
./lenguajito programa.lj --tac
./lenguajito programa.lj --asm
./lenguajito programa.lj --run
```

> La suite completa (`make test`) incluye los 4 hitos y da **20/20**.

## Qué funciona hoy

- `--tokens`: imprime `LINEA:COLUMNA TIPO lexema`, un token por línea; el
  último token es `LINEA:COLUMNA EOF`. Los comentarios `//`, los espacios,
  los tabuladores y los saltos de línea se ignoran (los archivos CRLF
  funcionan igual).
- `--ast`: imprime el árbol en una sola línea con el formato de la
  especificación (sección 4 de `docs/gramatica.md`). Cubre declaraciones,
  asignaciones, `if/else`, `while`, `print`, bloques y expresiones con la
  precedencia de la gramática (asociatividad izquierda).
- `--check`: análisis léxico, sintáctico y semántico completo:
  - `S01` de sintaxis y de carácter inválido; el parser recupera en `;` y
    `}` y reporta varios errores por pasada (máximo 20);
  - `E01` para variable no declarada y para lectura antes de asignar valor;
  - `E02` para redeclaración de un nombre en el mismo ámbito;
  - `E04` para división entre cero con divisor constante (`1 / 0`,
    `10 / (2 - 2)`, etc.);
  - ámbitos anidados por bloque y shadowing (el ámbito interno oculta al
    externo mientras el bloque esté activo; al cerrarlo, sus variables dejan
    de existir);
  - **inicialización por caminos**: una variable cuenta como inicializada
    solo si todas las rutas que llegan a su lectura le asignaron valor. Un
    `if` sin `else` o el cuerpo de un `while` no la inicializan; un `if/else`
    que asigna en ambas ramas sí;
  - los diagnósticos usan el formato `archivo:línea:columna: error EXX:
    mensaje` y el compilador sale con código 1 si hay errores.
- `--tac`: genera código de tres direcciones optimizado (sección 8 de
  `docs/gramatica.md`): expresiones, asignaciones, `if/else`, `while`,
  `print` y bloques. Temporales `_t0`, `_t1`, ... únicos y etiquetas `L1`,
  `L2`, ... Plegado y propagación de constantes y eliminación de temporales
  sin usos.
- `--asm`: genera ensamblador **x86-64 AT&T** con `.text`, `.globl main`,
  prólogo, cuerpo y epílogo. `print` usa `printf("%d\n", ...)`. El binario
  generado es un ELF de 64 bits para Linux.
- `--run`: escribe el ensamblador, lo ensambla con `as --64`, lo enlaza con
  `gcc` y ejecuta el binario generado, reenviando su salida y su código de
  salida. `print(e)` escribe un valor por línea.
- Códigos de salida del compilador: `0` sin errores, `1` errores de
  compilación o de ejecución, `2` uso incorrecto de la línea de comandos.
- `make test` → `20/20`; `make test-hito1` → `4/4`, `make test-hito2` →
  `14/14`, `make test-hito3` → `15/15`, `make test-hito4` → `16/16`,
  `make test-propias` → `23/23`.

## Límites conocidos

- El binario es para Linux x86-64; no se genera para otras plataformas.
- La división entre cero en tiempo de ejecución no se detecta al compilar
  salvo el caso constante `E04`.
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
├── ast.[ch]          # nodos, liberación, impresión, constantes y plegado
├── parser.[ch]       # descendente recursivo, recuperación con ';' y '}'
├── semantica.[ch]    # ámbitos, shadowing, E01/E02/E04 y caminos
├── tac.[ch]          # generación de TAC y optimizaciones
└── codegen.[ch]      # ensamblador x86-64 AT&T para --asm y --run
```

## Reparto de trabajo

| Integrante | Archivos / etapas | Entrega |
| :--- | :--- | :--- |
| Edwin | `util`, `lexer`, `parser`, `ast`, `tac`, `codegen`, `compilador` (léxico, sintaxis, AST, TAC, backend, CLI, `--run`) | Hitos 1 a 4 |
| Blanca | `diagnosticos`, `semantica` (ámbitos, shadowing, E01/E02/E04, caminos), revisión de optimizaciones y ABI | Hitos 1 a 4 |
| Jimena | `tests/propias/`, `revisar.py`, documentación y demo | Hitos 1 a 4 |

## Bitácora de IA

Cada entrega incluye su bitácora C-R-E-O en `docs/entrega_hitoN.md`
([`docs/entrega_hito1.md`](docs/entrega_hito1.md),
[`docs/entrega_hito2.md`](docs/entrega_hito2.md),
[`docs/entrega_hito3.md`](docs/entrega_hito3.md) y
[`docs/entrega_hito4.md`](docs/entrega_hito4.md)).
