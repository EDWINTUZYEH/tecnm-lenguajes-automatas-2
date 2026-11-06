# Avances del proyecto

**Equipo:** Edwin, Blanca y Jimena
**Repositorio:** https://github.com/EDWINTUZYEH/tecnm-lenguajes-automatas-2
**Tag actual:** `v0.1-hito1`

Formato de cada avance: qué compila hoy (comando exacto), qué falla y por
qué, qué sigue, y el commit. Los avances de los Hitos 2, 3 y 4 se
documentarán en las sesiones 15, 25 y 35 respectivamente; aún no existen.

---

## Avance 0 · Sesión 05 · Hito 0

1. **Qué compila hoy** (comando exacto): `make` construye `./lenguajito`
   a partir del esqueleto del curso (fork del repo del curso,
   `proyecto_integrador/` en la raíz, sin tocar `tests/`).
2. **Qué falla y por qué**: el `compilar()` del esqueleto respondía
   `compilador sin implementar`; aún no había lexer ni AST.
3. **Qué sigue**: lexer completo con línea/columna y errores léxicos
   `S01` (avance 1, sesión 08).
4. **Commit**: material del fork (`4fdd0f2`); el primer commit del equipo
   sobre `proyecto_integrador/` es `9154b05` (Hito 1).

---

## Avance 1 · Sesión 08

1. **Qué compila hoy** (comando exacto):
   `./lenguajito tests/validos/01_suma.lj --tokens` imprime
   `LINEA:COLUMNA TIPO lexema` hasta la línea `EOF`; los caracteres
   inválidos reportan `S01`.
2. **Qué falla y por qué**: `--ast` y `--check` seguían en construcción
   (el parser descendente recursivo y el AST se cerraron junto con el
   Hito 1).
3. **Qué sigue**: `--ast` con el formato de la especificación, `--check`
   con `S01`/`E01` básico y `make test-hito1` en verde para la sesión 10.
4. **Commit**: `9154b05` (Hito 1, tag `v0.1-hito1`, `make test-hito1` →
   4/4). El cierre del entregable se consolida en el commit del tag
   `v0.1-hito1` re-creado al terminar la verificación de esta entrega.

---

## Avance 2 · Sesión 15

⏳ **Pendiente.** Se documentará en la sesión 15 (análisis semántico
completo, `E02`/`E04`, ámbitos y recuperación). El Hito 2 no ha sido
trabajado todavía.

---

## Avance 3 · Sesión 25

⏳ **Pendiente.** Se documentará en la sesión 25 (TAC de expresiones y de
un `if`). El Hito 3 no ha sido trabajado todavía.

---

## Avance 4 · Sesión 35

⏳ **Pendiente.** Se documentará en la sesión 35 (`--asm` de una
expresión y primer binario). El Hito 4 no ha sido trabajado todavía.
