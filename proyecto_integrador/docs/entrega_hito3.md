# Entrega · Hito 3

**Equipo:** Edwin, Blanca y Jimena  
**Repositorio:** https://github.com/EDWINTUZYEH/tecnm-lenguajes-automatas-2  
**Tag:** `v0.3-hito3`  
**Fecha:** 2026-11-04

---

## 1. Qué funciona

```bash
cd proyecto_integrador
make
make test-hito3     # Hito 3: 15/15 pruebas superadas
make test-propias   # Pruebas propias: 9/9 superadas

./lenguajito tests/tac/01_folding.lj --tac
# print 10

./lenguajito tests/validos/04_while.lj --tac
# L1:
# _t0 = i < 3
# ifFalso _t0 goto L2
# print i
# _t1 = i + 1
# i = _t1
# goto L1
# L2:
```

- `--tac` cubre expresiones, asignaciones, `declarar` con inicializador,
  `if/else`, `while`, `print` y bloques.
- Temporales `_t0`, `_t1`, ... únicos y sin reutilizar; etiquetas `L1`, `L2`, ...
- **Plegado de constantes** en el AST antes de generar (no queda ninguna
  operación entre constantes).
- **Propagación de constantes a nivel TAC**: sustitución de operandos con
  valor conocido y plegado adicional (por ejemplo, `a = 2; b = a * 3`
  compila a `a = 2; b = 6`).
- **Eliminación de código muerto**: punto fijo que borra instrucciones que
  asignan a un temporal `_t` que nadie lee (`_t0 = 6` desaparece si `_t0`
  no se usa).
- El entorno de constantes se limpia en etiquetas y en `goto` para que la
  optimización sea correcta en ciclos y saltos.

## 2. Qué no funciona (y por qué)

- [ ] `--asm` y `--run` con binario llegan en el Hito 4.
- [ ] No se hace eliminación de código muerto de stores a variables del
      usuario (solo temporales, como pide el contrato) ni `CSE` (no es parte
      del alcance del hito).

## 3. Pruebas

`make test-hito3`:

```text
Hito 3: 15/15 pruebas superadas
```

`make test-propias`:

```text
Pruebas propias: 9/9 superadas
```

Pruebas propias relacionadas con TAC (`tests/propias/`):

| Archivo | Qué cubre |
| :--- | :--- |
| `09_optimizacion.lj` / `09_optimizacion.tac` | plegado + propagación + código muerto con salida exacta |

Además `tests/tac/01_folding.lj` (dorado) imprime `print 10`.

### Antes / después para la demo

`print(2 * 3 + 4);` sin optimización sería:

```text
_t0 = 2 * 3
_t1 = _t0 + 4
print _t1
```

con las optimizaciones implementadas:

```text
print 10
```

`int a = 2; int b = a * 3;` produce `a = 2` + `_t0 = a * 3` + `b = _t0`
antes de optimizar, y `a = 2; b = 6;` después.

## 4. Reparto de trabajo

| Integrante | Archivos / etapas | Commits principales |
| :--- | :--- | :--- |
| Jimena | `tac.[ch]`, propagación de constantes y eliminación de código muerto | commit del Hito 3 |
| Edwin | `ast_plegar_constantes()` en `ast.c`, `compilador.c` (`--tac`) | commit del Hito 3 |
| Blanca | `tests/propias/revisar.py`, verificación de `09_optimizacion.lj` | commit del Hito 3 |

## 5. Bitácora C-R-E-O (IA)

| Contexto | Rol | Especificación | Output | ¿Qué se aceptó, corrigió o rechazó? |
| :--- | :--- | :--- | :--- | :--- |
| Proyecto Lenguajito (Hitos 1 y 2 en verde). | Ingeniero de compiladores experto en C. | TAC del contrato §8 con temporales `_tN` únicos, etiquetas `L1`, `ifFalso`/`goto`/`print`; formato exacto. | Módulo `tac.[ch]` con generación estructural y `instr_a_texto()`. | Aceptado; el formato se verificó carácter por carácter contra los ejemplos `if` y `while` del contrato. |
| Misma base, optimización. | Ingeniero de compiladores. | Plegado de constantes (ningún `= num op num`), propagación segura en ciclos y etiquetas, eliminación de temporales sin usos. | `ast_plegar_constantes()` + `optimizar_propagacion()` + `optimizar_muertos()`. | Se rechazó la propagación ingenua a través de etiquetas (incorrecta en ciclos): el entorno se limpia en `ETIQUETA` y `GOTO`. Se verificó `tests/tac/01_folding.lj` y `tests/propias/09_optimizacion.tac`. |
| Cierre del hito. | Auditor. | `make test-hito3` y `test-propias` en verde; `tests/` intacto. | Resumen de pruebas. | `15/15` y `9/9`; `git status` no modifica `tests/` dorados (solo se agregan archivos en `tests/propias/`). |

## 6. Demo

- [x] Preparada para 3 minutos.
- [x] Cualquier integrante puede explicar cualquier parte.
