# Entrega · Hito 2

**Equipo:** Edwin Armando Tuz Yeh  
**Repositorio:** https://github.com/EDWINTUZYEH/tecnm-lenguajes-automatas-2  
**Tag:** `v0.2-hito2`  
**Fecha:** 2026-11-04

---

## 1. Qué funciona

```bash
cd proyecto_integrador
make
make test-hito2     # Hito 2: 14/14 pruebas superadas
make test-propias   # Pruebas propias: 8/8 superadas

./lenguajito tests/validos/08_anidado.lj --run
# 1 2 4 3 6 9

./lenguajito tests/invalidos/02_redeclaracion.lj --check
# tests/invalidos/02_redeclaracion.lj:2:5: error E02: redeclaración de 'x' en el mismo ámbito
```

- Parser completo: declaraciones, asignaciones, `if/else`, `while`, `print` y
  bloques anidados.
- Tabla de símbolos con ámbitos anidados y shadowing; la redeclaración en el
  mismo ámbito se reporta como `E02`.
- `E01` para variable no declarada y para lectura antes de asignar valor.
- `E04` para división entre cero constante, incluida una expresión constante
  como `k / (1 - 1)`.
- Se reportan varios errores en una pasada (máximo 20) y el proceso sale con
  código 1.
- `--run` ejecuta los 9 programas válidos interpretando el AST (permitido en
  este hito por la guía).

## 2. Qué no funciona (y por qué)

- [ ] `--tac` y `--asm` llegan en los Hitos 3 y 4.
- [ ] `--run` aún no usa el binario generado: se sustituye por el backend en el
      Hito 4, como pide el contrato.
- [ ] La división entre cero en tiempo de ejecución (no constante) no se exige;
      el intérprete la detecta y termina con código 1 sin abortar.

## 3. Pruebas

`make test-hito2`:

```text
Hito 2: 14/14 pruebas superadas
```

`make test-propias`:

```text
Pruebas propias: 8/8 superadas
```

Pruebas propias agregadas (`tests/propias/`):

| Archivo | Qué cubre |
| :--- | :--- |
| `01_negativos.lj` | unario `-` combinado con `*`, `+` y paréntesis |
| `02_anidado.lj` | `while` con `if/else` interno |
| `03_shadowing_anidado.lj` | shadowing en tres niveles de bloques |
| `04_comparaciones.lj` | los seis operadores de comparación |
| `05_division_entera.lj` | división entera y precedencia |
| `06_lectura_antes.lj` | `E01` al leer antes de asignar (caso inválido) |
| `07_redeclaracion_misma.lj` | `E02` en el mismo ámbito (caso inválido) |
| `08_div_cero_expresion.lj` | `E04` con divisor constante `(1 - 1)` (caso inválido) |

## 4. Reparto de trabajo

| Integrante | Archivos / etapas | Commits principales |
| :--- | :--- | :--- |
| Edwin Armando Tuz Yeh | `semantica.[ch]`, `interprete.[ch]`, `compilador.c`, `tests/propias/` | commit del Hito 2 |

## 5. Bitácora C-R-E-O (IA)

| Contexto | Rol | Especificación | Output | ¿Qué se aceptó, corrigió o rechazó? |
| :--- | :--- | :--- | :--- | :--- |
| Proyecto Lenguajito, C11 + `gcc -Werror`, solo `libc`, `tests/` intocable. | Ingeniero de compiladores experto en C. | Tabla de símbolos con ámbitos anidados, shadowing y redeclaración (`E02`); `E01` para no declarada y lectura antes de asignar; varios errores por pasada con el formato del contrato. | `semantica.[ch]`. | Se auditó contra los 5 inválidos dorados (línea y código correctos). Se corrigió el orden de revisión en `int x = x + 1;` para que el inicializador vea la variable externa antes de declarar la interna. |
| Misma base. | Ingeniero de compiladores. | Detectar `E04` incluso cuando el divisor es constante pero no un literal (`10 / (2 - 2)`). | Función `evaluar_constante()` en `ast.c`. | Aceptado; se rechazó evaluar constantes con división por cero (devuelve "no evaluable") para no perder el diagnóstico `E04` del divisor interno. |
| Pruebas del hito. | Ingeniero de pruebas. | `--run` sobre los programas válidos y salida idéntica a los `.out`; recuperación con varios errores en una pasada. | Intérprete del AST (`interprete.[ch]`) y suite propia `tests/propias/` con `revisar.py`. | Aceptado: `14/14` doradas y `8/8` propias. El intérprete se marca como temporal: en el Hito 4 `--run` usa el binario. |

## 6. Demo

- [x] Preparada para 3 minutos.
- [x] Cualquier integrante puede explicar cualquier parte.
