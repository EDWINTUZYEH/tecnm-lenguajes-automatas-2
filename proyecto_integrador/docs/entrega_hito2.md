# Entrega · Hito 2

**Equipo:** Edwin, Blanca y Jimena
**Repositorio:** https://github.com/EDWINTUZYEH/tecnm-lenguajes-automatas-2
**Tag:** `v0.2-hito2`
**Fecha:** 2026-11-13

---

## 1. Qué funciona

```bash
cd proyecto_integrador
make

make test-hito1     # Hito 1: 4/4 pruebas superadas
make test-hito2     # Hito 2: 14/14 pruebas superadas
make test-propias   # Pruebas propias: 21/21 superadas

./lenguajito tests/validos/08_anidado.lj --run
# 1 2 4 3 6 9 (un valor por línea)

./lenguajito tests/invalidos/02_redeclaracion.lj --check
# tests/invalidos/02_redeclaracion.lj:2:5: error E02: redeclaración de 'x' en el mismo ámbito
```

- Parser completo: declaraciones, asignaciones, `if/else`, `while`, `print` y
  bloques anidados.
- Tabla de símbolos con ámbitos anidados y shadowing; la redeclaración en el
  mismo ámbito se reporta como `E02`.
- `E01` para variable no declarada y para lectura antes de asignar valor.
- **Inicialización por caminos:** una variable solo cuenta como inicializada si
  todas las rutas que llegan a su lectura le asignaron valor. Por ejemplo,
  `int a; if (c) { a = 1; } print(a);` y `int a; while (c) { a = 1; }
  print(a);` producen `E01`; un `if/else` que asigna en ambas ramas no.
- `E04` para división entre cero constante, incluida una expresión constante
  como `k / (1 - 1)`.
- Se reportan varios errores en una pasada (máximo 20) y el proceso sale con
  código 1.
- `--run` ejecuta los 9 programas válidos interpretando el AST (la forma
  permitida para este hito) y compara su salida con los `.out`. Una división
  entre cero en tiempo de ejecución termina con código 1 sin abortar.
- `make test` da **18/20**: solo fallan las pruebas doradas de los Hitos 3 y 4
  (`--tac` y `--asm`), todavía pendientes.

## 2. Fuera del alcance del Hito 2

- `--tac` y `--asm` corresponden a los Hitos 3 y 4 y responden
  `modo ... aún no implementado`.
- En el Hito 4, `--run` pasará a ejecutar el binario generado en lugar del
  intérprete del AST.
- La división entre cero en tiempo de ejecución (divisor no constante) no se
  exige en el contrato; el intérprete la detecta y sale con código 1.

## 3. Pruebas

`make test-hito2`:

```text
Hito 2: 14/14 pruebas superadas
```

`make test-propias`:

```text
Pruebas propias: 21/21 superadas
```

El Hito 2 agrega 8 casos propios (`14_*` a `21_*`). Los casos `01_*` a `13_*`
son del Hito 1 y se conservan intactos:

| Archivo | Qué cubre |
| :--- | :--- |
| `14_caminos_if.lj` | inicialización definitiva en `if/else` e `if` anidados (`--run`) |
| `15_ambito_while.lj` | ámbito nuevo en cada vuelta de `while` (`--run`) |
| `16_sombra_init.lj` | el inicializador de una variable interna ve la externa (`--run`) |
| `17_ambito_anidado.lj` | shadowing en bloques anidados (`--run`) |
| `18_e01_if_sin_else.lj` | `E01` porque un `if` sin `else` no inicializa |
| `19_e01_while.lj` | `E01` porque el cuerpo del `while` puede no ejecutarse |
| `20_multiples_errores.lj` | varios diagnósticos (`E01`, `E01`, `E04`) con `.diag` |
| `21_sintaxis_multiples.lj` | recuperación sintáctica con dos `S01` |

## 4. Reparto de trabajo

| Integrante | Archivos / etapas | Commits principales |
| :--- | :--- | :--- |
| Blanca | `semantica.[ch]`, tabla de símbolos con ámbitos y shadowing, inicialización por caminos | integración del Hito 2 en `main` |
| Edwin | `compilador.c`, `--run` con el intérprete del AST | integración del Hito 2 en `main` |
| Jimena | `tests/propias/`, `revisar.py`, diagnósticos `E01`/`E02`/`E04` y documentación | integración del Hito 2 en `main` |

## 5. Bitácora C-R-E-O (IA)

| Contexto | Rol | Especificación | Output | ¿Qué se aceptó, corrigió o rechazó? |
| :--- | :--- | :--- | :--- | :--- |
| Proyecto Lenguajito, C11 + `gcc -Werror`, solo `libc`, `tests/` intocable. | Ingeniero de compiladores experto en C. | Tabla de símbolos con ámbitos anidados, shadowing y redeclaración (`E02`); `E01` para no declarada y lectura antes de asignar; varios errores por pasada con el formato del contrato. | `semantica.[ch]`. | Se auditó contra los 5 inválidos dorados (línea y código correctos). Se corrigió el orden de revisión en `int x = x + 1;` para que el inicializador vea la variable externa antes de declarar la interna. |
| Misma base. | Ingeniero de compiladores. | Detectar `E04` incluso cuando el divisor es constante pero no un literal (`10 / (2 - 2)`). | Función `evaluar_constante()` en `ast.c`. | Aceptado; se rechazó evaluar constantes con división por cero (devuelve "no evaluable") para no perder el diagnóstico `E04` del divisor interno. |
| Pruebas del hito. | Ingeniero de pruebas. | `--run` sobre los programas válidos y salida idéntica a los `.out`; recuperación con varios errores en una pasada. | Intérprete del AST (`interprete.[ch]`) y ampliación de la suite propia con `revisar.py`. | Aceptado: `14/14` doradas y `21/21` propias. El intérprete se marca como temporal: en el Hito 4 `--run` usa el binario. |
| Corrección posterior del Hito 2. | Ingeniero de compiladores. | La inicialización debe ser definitiva por caminos: un `if` sin `else` o un `while` no inicializan una variable; solo un `if/else` que asigna en ambas ramas o una asignación incondicional. | Análisis de instantáneas de estados y fusión de caminos en `semantica.c`. | Aceptado tras probar `14/14` doradas y `21/21` propias. Se rechazó la versión anterior, que marcaba `inicializada` en cualquier asignación sin considerar el flujo. |

## 6. Demo

- [x] Preparada para 3 minutos.
- [x] Cualquier integrante puede explicar cualquier parte.
