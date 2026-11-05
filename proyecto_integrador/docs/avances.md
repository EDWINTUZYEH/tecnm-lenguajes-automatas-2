# Avances del proyecto

**Equipo:** Edwin, Blanca y Jimena  
**Repositorio:** https://github.com/EDWINTUZYEH/tecnm-lenguajes-automatas-2  
**Tag actual:** `v1.0-hito4`

> Los avances se consolidaron al cierre del semestre con las referencias de
> los commits que los completaron. Cada avance tiene el formato: qué compila
> hoy (comando exacto), qué falla y qué sigue antes del hito.

---

## Avance 0 · Sesión 05 · Hito 0

1. **Qué compila hoy** (comando exacto): `make` construye `./lenguajito`;
   `docs/gramatica.md` leída y `tests/` ejecutables con `make test-hito1`.
2. **Qué falla y por qué**: el esqueleto aún no produce tokens ni AST;
   `compilador.c` respondía `compilador sin implementar`.
3. **Qué sigue**: lexer completo con línea/columna y errores léxicos `S01`.
4. **Commit**: `9154b05` (entrega del Hito 1, tag `v0.1-hito1`).

---

## Avance 1 · Sesión 08

1. **Qué compila hoy** (comando exacto):
   `./lenguajito tests/validos/01_suma.lj --tokens` imprime
   `LINEA:COLUMNA TIPO lexema` hasta `EOF`; los caracteres inválidos
   reportan `S01`.
2. **Qué falla y por qué**: `--ast` y el análisis semántico aún no están
   implementados; el parser descendente estaba en construcción.
3. **Qué sigue**: AST de expresiones con el formato exacto de la
   especificación y `make test-hito1` en verde.
4. **Commit**: `9154b05` (tag `v0.1-hito1`).

---

## Avance 2 · Sesión 15

1. **Qué compila hoy** (comando exacto):
   `./lenguajito tests/invalidos/01_no_declarada.lj --check` reporta
   `E01: variable no declarada`; `make test-hito2` → `14/14` y
   `make test-propias` → `9/9`.
2. **Qué falla y por qué**: `--tac` y `--asm` aún no existen (el contrato
   los deja para los Hitos 3 y 4); el `--run` usaba el intérprete del AST.
3. **Qué sigue**: generación de TAC con temporales únicos, plegado de
   constantes y eliminación de código muerto.
4. **Commit**: `78327e3` (tag `v0.2-hito2`).

---

## Avance 3 · Sesión 25

1. **Qué compila hoy** (comando exacto):
   `./lenguajito tests/tac/01_folding.lj --tac` produce `print 10`
   (plegado de constantes); `make test-hito3` → `15/15`.
2. **Qué falla y por qué**: el TAC de ciclos se generaba pero el backend
   x86-64 no existía; sin binario no hay ELF que enlazar.
3. **Qué sigue**: backend en AT&T (`as` + `gcc`), `--asm` y `--run` con
   binario real, y `file` para verificar el ejecutable ELF.
4. **Commit**: `1d5e6a7` (tag `v0.3-hito3`).

---

## Avance 4 · Sesión 35

1. **Qué compila hoy** (comando exacto):
   `./lenguajito tests/validos/01_suma.lj --asm` genera AT&T con `.text`,
   `.globl main` y `ret`; `make` seguido de `as --64` y `gcc` enlaza un
   ELF; `make test` → `20/20`.
2. **Qué falla y por qué**: nada pendiente del contrato base; quedan las
   extensiones del lenguaje (no implementadas por diseño: el contrato
   exige autorización previa).
3. **Qué sigue**: cierre del Hito 4, documentación final y demo de 5
   minutos.
4. **Commit**: commit del tag `v1.0-hito4`.
