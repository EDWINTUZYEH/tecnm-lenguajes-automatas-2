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
- Plan del Hito 2 (mapa de trabajo y de explicación): [`docs/plan_hito2.md`](docs/plan_hito2.md)
- Diseño del Hito 2 (cómo se implementó): [`docs/diseno_hito2.md`](docs/diseno_hito2.md)
- Entrega del Hito 2: [`docs/entrega_hito2.md`](docs/entrega_hito2.md)
- Pruebas: [`tests/`](tests/)

## Estado por hitos

| Hito | Tema | Estado |
| :--- | :--- | :--- |
| 1 | Léxico, sintaxis y AST (`--tokens`, `--ast`, `--check`) | ✅ terminado (tag `v0.1-hito1`) |
| 2 | Sentencias, ámbitos y diagnósticos completos (`E02`, `E04`, `--run`) | ✅ terminado (tag `v0.2-hito2`) |
| 3 | TAC con plegado de constantes y código muerto | ⏳ pendiente (sesión 30) |
| 4 | Backend x86-64, enlace y binario ELF | ⏳ pendiente (sesión 40) |

> Esta tabla se actualiza en cada entrega. Ver `docs/entrega_hitoN.md`.

## Cómo se construye y se prueba

```bash
make             # construye ./lenguajito
make test-hito1  # pruebas del Hito 1 → 4/4
make test-hito2  # pruebas del Hito 2 → 14/14
make test-propias  # pruebas propias del equipo → 21/21
./lenguajito programa.lj --tokens
./lenguajito programa.lj --ast
./lenguajito programa.lj --check
./lenguajito programa.lj --run
```

> `make test` (toda la suite) da **18/20**: solo fallan las pruebas doradas de
> los Hitos 3 y 4 (`--tac` y `--asm`), que todavía no están implementados. La
> evidencia de los Hitos 1 y 2 es `make test-hito1`, `make test-hito2` y
> `make test-propias`.

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
- `--run`: ejecuta los programas válidos interpretando el AST (el plan
  permitido para el Hito 2). `print(e)` escribe un valor por línea. Una
  división entre cero en tiempo de ejecución termina con código 1.
- Códigos de salida del compilador: `0` sin errores, `1` errores de
  compilación o de ejecución, `2` uso incorrecto de la línea de comandos.
- `make test-hito1` → `4/4`, `make test-hito2` → `14/14`,
  `make test-propias` → `21/21`.

## Qué no funciona todavía

- `--tac` (Hito 3): responde `modo --tac aún no implementado`.
- `--asm` (Hito 4): responde `modo --asm aún no implementado`.
- En el Hito 4, `--run` pasará a ejecutar el binario generado en lugar del
  intérprete del AST.
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
├── ast.[ch]          # nodos, liberación, impresión y evaluación constante
├── parser.[ch]       # descendente recursivo, recuperación con ';' y '}'
├── semantica.[ch]    # ámbitos, shadowing, E01/E02/E04 y caminos
└── interprete.[ch]   # ejecución directa del AST para --run (Hito 2)
```

## Reparto de trabajo

| Integrante | Archivos / etapas | Entrega |
| :--- | :--- | :--- |
| Edwin | `util`, `lexer`, `parser`, `ast`, `compilador` (léxico, sintaxis, AST, CLI, `--run`) | Hitos 1 y 2 |
| Blanca | `diagnosticos`, `semantica` (ámbitos, shadowing, E01/E02/E04, caminos) | Hitos 1 y 2 |
| Jimena | `tests/propias/`, `revisar.py`, documentación y demo | Hitos 1 y 2 |

## Bitácora de IA

Cada entrega incluye su bitácora C-R-E-O en `docs/entrega_hitoN.md`
([`docs/entrega_hito1.md`](docs/entrega_hito1.md) y
[`docs/entrega_hito2.md`](docs/entrega_hito2.md)).
