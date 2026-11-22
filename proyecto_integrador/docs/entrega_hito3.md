# Entrega · Hito 3

**Equipo:** Edwin, Blanca y Jimena
**Repositorio:** https://github.com/EDWINTUZYEH/tecnm-lenguajes-automatas-2
**Tag:** `v0.3-hito3`
**Fecha:** 2026-11-22

---

## 1. Qué funciona

```bash
cd proyecto_integrador
make
make test-hito3     # Hito 3: 15/15 pruebas superadas
make test-propias   # Pruebas propias: 22/22 superadas

./lenguajito tests/tac/01_folding.lj --tac
# print 10

./lenguajito tests/validos/04_while.lj --tac
# i = 0
# L1:
# _t0 = i < 3
# ifFalso _t0 goto L2
# print i
# _t1 = i + 1
# i = _t1
# goto L1
# L2:
```

- `--tac` cubre expresiones, asignaciones, declaraciones con inicializador,
  `if/else`, `while`, `print` y bloques anidados.
- Temporales `_t0`, `_t1`, ... únicos y sin reutilizar; etiquetas `L1`, `L2`, ...
- **Plegado de constantes** en el AST antes de generar: no queda ninguna
  operación entre constantes.
- **Propagación de constantes a nivel TAC**: sustitución de operandos con valor
  conocido y plegado adicional. Por ejemplo, `a = 2; b = a * 3` compila a
  `a = 2; b = 6`.
- **Eliminación de código muerto**: punto fijo que borra instrucciones que
  asignan a un temporal `_tN` que nadie lee.
- El entorno de constantes se limpia en etiquetas y en `goto` para que la
  optimización sea correcta en ciclos y saltos.

## 2. Fuera del alcance del Hito 3

- `--asm` y `--run` con binario generado corresponden al Hito 4.
- No se eliminan asignaciones a variables del usuario: el contrato solo pide
  eliminar temporales sin usos.
- No se implementan CSE ni optimizaciones de bucles: no forman parte del hito.

## 3. Pruebas

`make test-hito3`:

```text
Hito 3: 15/15 pruebas superadas
```

`make test-propias`:

```text
Pruebas propias: 22/22 superadas
```

Prueba propia relacionada con TAC:

| Archivo | Qué cubre |
| :--- | :--- |
| `22_optimizacion.lj` / `.tac` | plegado, propagación y código muerto con salida exacta |

Además, la prueba dorada `tests/tac/01_folding.lj` debe imprimir `print 10`.

### Antes / después para la demo

`print(2 * 3 + 4);` sin optimización sería:

```text
_t0 = 2 * 3
_t1 = _t0 + 4
print _t1
```

Con las optimizaciones implementadas:

```text
print 10
```

`int a = 2; int b = a * 3;` produce `a = 2; b = 6;` antes de imprimir.

## 4. Reparto de trabajo

| Integrante | Archivos / etapas | Commits principales |
| :--- | :--- | :--- |
| Edwin | `tac.[ch]`, `ast_plegar_constantes()`, `compilador.c`, integración | commit del Hito 3 |
| Blanca | Revisión de propagación/eliminación de código muerto y pruebas de optimización | commit del Hito 3 |
| Jimena | `tests/propias/22_optimizacion`, documentación y demo | commit del Hito 3 |

## 5. Bitácora C-R-E-O (IA)

| Contexto | Rol | Especificación | Output | ¿Qué se aceptó, corrigió o rechazó? |
| :--- | :--- | :--- | :--- | :--- |
| Proyecto Lenguajito (Hitos 1 y 2 en verde). | Ingeniero de compiladores experto en C. | TAC del contrato §8 con temporales `_tN` únicos, etiquetas `L1`, `ifFalso`/`goto`/`print`; formato exacto. | Módulo `tac.[ch]` con generación estructural y `instr_a_texto()`. | Aceptado; el formato se verificó carácter por carácter contra los ejemplos `if` y `while` del contrato. |
| Misma base, optimización. | Ingeniero de compiladores. | Plegado de constantes (ningún `= num op num`), propagación segura en ciclos y etiquetas, eliminación de temporales sin usos. | `ast_plegar_constantes()` + `optimizar_propagacion()` + `optimizar_muertos()`. | Se rechazó la propagación ingenua a través de etiquetas (incorrecta en ciclos): el entorno se limpia en `ETIQUETA` y `GOTO`. Se verificó `tests/tac/01_folding.lj` y `tests/propias/22_optimizacion.tac`. |
| Cierre del hito. | Auditor. | `make test-hito3` y `test-propias` en verde; `tests/` intacto. | Resumen de pruebas. | `15/15` y `22/22`; `git status` no modifica `tests/` dorados (solo se agregan archivos en `tests/propias/`). |

## 6. Demo

- [x] Preparada para 3 minutos.
- [x] Cualquier integrante puede explicar cualquier parte.
