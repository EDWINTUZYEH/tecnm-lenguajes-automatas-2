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
| 1 | Léxico, sintaxis y AST (`--tokens`, `--ast`, `--check`) | ✅ terminado |
| 2 | Sentencias, ámbitos y diagnósticos (`E01`, `E02`, `E04`) | ✅ terminado |
| 3 | TAC con plegado de constantes y código muerto | ✅ terminado |
| 4 | Backend x86-64, enlace y binario ELF | ⏳ pendiente |

> Esta tabla se actualiza en cada entrega. Ver `docs/entrega_hitoN.md`.

## Cómo se construye y se prueba

```bash
make             # construye ./lenguajito
make test        # ejecuta todas las pruebas del curso
make test-hito1 # solo las del Hito 1
make test-hito2 # solo las del Hito 2
make test-hito3 # solo las del Hito 3
make test-propias # pruebas propias del equipo (tests/propias/)
./lenguajito programa.lj --tokens
./lenguajito programa.lj --ast
./lenguajito programa.lj --check
./lenguajito programa.lj --tac
./lenguajito programa.lj --run
```

## Qué funciona hoy

- `--tokens`: imprime `LINEA:COLUMNA TIPO lexema`, un token por línea; el
  último token es `LINEA:COLUMNA EOF`. Los comentarios `//`, los espacios, los
  tabuladores y los saltos de línea se ignoran.
- `--ast`: imprime el árbol en el formato de la especificación (una sola
  línea). Cubre declaraciones, asignaciones, `if/else`, `while`, `print`,
  bloques y expresiones con la precedencia de la gramática.
- `--check`: análisis léxico, sintáctico y semántico completo:
  - ámbitos anidados por bloque y shadowing;
  - `E01` variable no declarada / leída antes de asignar valor;
  - `E02` redeclaración en el mismo ámbito;
  - `E04` división entre cero constante (incluye expresiones como `1 - 1`);
  - `S01` de sintaxis con recuperación: se reportan varios errores por pasada
    (máximo 20) y el compilador sale con código 1.
- `--run`: ejecuta el programa. En este hito interpreta el AST (permitido por
  la guía); en el Hito 4 pasará a ejecutar el binario generado.
- `--tac`: genera código de tres direcciones optimizado:
  - temporales únicos `_t0`, `_t1`, ... sin reutilizar;
  - `ifFalso`, `goto`, etiquetas `L1`, `L2`, ..., `print`;
  - plegado de constantes (no queda ninguna operación entre constantes);
  - propagación de constantes a nivel TAC y eliminación de código muerto:
    no quedan temporales asignados que nadie lea.

## Qué no funciona todavía

- `--asm` responde `modo aún no implementado` (Hito 4).
- `--run` todavía no usa el binario ELF (llega en el Hito 4).
- Los literales mayores que `INT_MAX` se truncan con `strtol`.

## Arquitectura

```text
src/
├── main.c          # interfaz de línea de comandos (proporcionada)
├── compilador.c    # orquesta las etapas según el modo
├── compilador.h
├── util.[ch]       # buffer dinámico y utilidades
├── diagnosticos.[ch] # registro de errores con formato y límite de 20
├── lexer.[ch]      # tokens con línea y columna
├── ast.[ch]        # nodos, liberación, impresión y plegado de constantes
├── parser.[ch]     # descendente recursivo, recuperación con ';' y '}'
├── semantica.[ch]  # tabla de símbolos con ámbitos y diagnósticos
├── interprete.[ch] # ejecución del AST para --run (Hito 2)
└── tac.[ch]        # TAC: generación, propagación/plegado y código muerto
```

## Reparto de trabajo

| Integrante | Archivos / etapas | Commits |
| :--- | :--- | :--- |
| Edwin Armando Tuz Yeh | `util`, `diagnosticos`, `lexer`, `ast`, `parser`, `compilador` | Hito 1 |
| Edwin Armando Tuz Yeh | `semantica`, `interprete`, pruebas propias | Hito 2 |
| Edwin Armando Tuz Yeh | `tac`, plegado de constantes, código muerto | Hito 3 |

## Bitácora de IA

Cada entrega incluye su bitácora C-R-E-O en `docs/entrega_hitoN.md`.
