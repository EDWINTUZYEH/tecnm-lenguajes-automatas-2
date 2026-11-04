# Proyecto Integrador · Lenguajito

Compilador para **Lenguajito**, el lenguaje del Proyecto Integrador de
*Lenguajes y Autómatas II (SCD-1016)*. Todo el proyecto vive en esta carpeta.

- Reglas y rúbrica: [`../PROYECTO.md`](../PROYECTO.md)
- Lenguaje, AST, diagnósticos y TAC: [`docs/gramatica.md`](docs/gramatica.md)
- Guía de trabajo: [`docs/guia-proyecto.md`](docs/guia-proyecto.md)
- Avances: [`docs/avances.md`](docs/avances.md)
- Pruebas: [`tests/`](tests/)

## Estado por hitos

| Hito | Tema | Estado |
| :--- | :--- | :--- |
| 1 | Léxico, sintaxis y AST de expresiones (`--tokens`, `--ast`, `--check`) | ✅ terminado |
| 2 | Sentencias, ámbitos y diagnósticos (`E01`, `E02`, `E04`) | ⏳ pendiente |
| 3 | TAC con plegado de constantes y código muerto | ⏳ pendiente |
| 4 | Backend x86-64, enlace y binario ELF | ⏳ pendiente |

> Esta tabla se actualiza en cada entrega. Ver `docs/entrega_hitoN.md`.

## Cómo se construye y se prueba

```bash
make            # construye ./lenguajito
make test       # ejecuta todas las pruebas del curso
make test-hito1 # solo las del Hito 1
./lenguajito programa.lj --tokens
./lenguajito programa.lj --ast
./lenguajito programa.lj --check
```

## Qué funciona hoy

- `--tokens`: imprime `LINEA:COLUMNA TIPO lexema`, un token por línea; el
  último token es `LINEA:COLUMNA EOF`. Los comentarios `//`, los espacios, los
  tabuladores y los saltos de línea se ignoran.
- `--ast`: imprime el árbol en el formato de la especificación (una sola
  línea). Cubre declaraciones, asignaciones, `if/else`, `while`, `print`,
  bloques y expresiones con la precedencia de la gramática.
- `--check`: por ahora valida **sintaxis**; reporta `S01` con
  `archivo:línea:columna: error S01: mensaje`, recupera y sigue analizando, y
  sale con código 1 si hay errores.

## Qué no funciona todavía

- `--check` no analiza semántica (variables no declaradas, ámbitos,
  redeclaración, división entre cero constante): llega en el Hito 2.
- `--tac`, `--asm` y `--run` responden `modo aún no implementado` (Hitos 3 y 4).

## Arquitectura

```text
src/
├── main.c          # interfaz de línea de comandos (proporcionada)
├── compilador.c    # orquesta las etapas según el modo
├── compilador.h
├── util.[ch]       # buffer dinámico y utilidades
├── diagnosticos.[ch] # registro de errores con formato e límite de 20
├── lexer.[ch]      # tokens con línea y columna
├── ast.[ch]        # nodos, liberación e impresión del AST
└── parser.[ch]     # descendente recursivo, recuperación con ';' y '}'
```

## Reparto de trabajo

| Integrante | Archivos / etapas | Commits |
| :--- | :--- | :--- |
| Edwin Armando Tuz Yeh | `util`, `diagnosticos`, `lexer`, `ast`, `parser`, `compilador` | Hito 1 |

## Bitácora de IA

Cada entrega incluye su bitácora C-R-E-O en `docs/entrega_hitoN.md`.
