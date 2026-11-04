# Entrega · Hito 1

**Equipo:** Edwin Armando Tuz Yeh  
**Repositorio:** https://github.com/EDWINTUZYEH/tecnm-lenguajes-automatas-2  
**Tag:** `v0.1-hito1`  
**Fecha:** 2026-11-04

---

## 1. Qué funciona

```bash
cd proyecto_integrador
make
make test-hito1

./lenguajito tests/validos/01_suma.lj --tokens
# 1:1 KW print
# 1:6 DELIM (
# 1:7 NUM 1
# ...
# 2:1 EOF

./lenguajito tests/hito1/01_expresion.lj --ast
# (programa (declarar x (+ (num 1) (* (num 2) (num 3)))))

./lenguajito tests/hito1/04_invalida.lj --check
# tests/hito1/04_invalida.lj:1:9: error S01: se esperaba una expresión
```

- Tokens con `LINEA:COLUMNA TIPO lexema` y token `EOF` final.
- AST exacto de la especificación para expresiones, declaraciones y
  asignaciones (4/4 pruebas doradas del Hito 1).
- Diagnósticos `S01` con el formato del contrato y recuperación: el parser
  sincroniza en `;` y `}` para reportar varios errores por pasada.
- Códigos de salida: `0` sin errores, `1` errores de compilación, `2` uso
  incorrecto (viene de `main.c`).

## 2. Qué no funciona (y por qué)

- [ ] La semántica (`E01`, `E02`, `E04`) se integra en el Hito 2; hoy `--check`
      solo valida sintaxis.
- [ ] `--tac`, `--asm` y `--run` están reservados para los Hitos 3 y 4.
- [ ] Los literales mayores que `INT_MAX` se truncan con `strtol` (el lenguaje
      base no exige otro comportamiento).

## 3. Pruebas

Salida de `make test-hito1`:

```text
Hito 1: 4/4 pruebas superadas
```

Pruebas propias (ruta y qué cubren): se agregan en `tests/propias/` a partir
del Hito 2, cuando `--run` esté disponible.

## 4. Reparto de trabajo

| Integrante | Archivos / etapas | Commits principales |
| :--- | :--- | :--- |
| Edwin Armando Tuz Yeh | `util`, `diagnosticos`, `lexer.c`, `ast.c`, `parser.c`, `compilador.c` | commit del Hito 1 |

## 5. Bitácora C-R-E-O (IA)

| Contexto | Rol | Especificación | Output | ¿Qué se aceptó, corrigió o rechazó? |
| :--- | :--- | :--- | :--- | :--- |
| Proyecto Integrador Lenguajito: C11, `gcc -Wall -Wextra -Werror`, solo `libc`; `tests/` es intocable y manda `docs/gramatica.md`. | Ingeniero de compiladores experto en C. | Lexer para los tokens de la sección 2 con línea y columna; `--tokens` con formato `LINEA:COLUMNA TIPO lexema`; errores léxicos `S01`. | `lexer.[ch]` con lista dinámica de tokens. | Aceptado tras revisar que los tipos (`KW`, `ID`, `NUM`, `OP`, `DELIM`, `EOF`) y las columnas coinciden con la especificación; se agregó el manejo de `\r` para archivos con CRLF. |
| Misma base del curso. | Ingeniero de compiladores experto en C. | Parser descendente recursivo LL(1) con la gramática EBNF de la sección 3, sin `flex`/`bison`; AST con el formato exacto de la sección 4; recuperación de errores `S01` para reportar varios por pasada. | `parser.[ch]` y `ast.[ch]`. | Se rechazó la primera idea de imprimir el AST con espacios extra: las pruebas comparan la cadena exacta. Se auditó contra `tests/hito1/*.ast` (3/3 exactos) y `04_invalida.err` (`S01` en la línea 1). |
| Cierre del hito. | Auditor. | `make test-hito1` en verde, sin warning alguno, sin modificar `tests/`. | Resumen de pruebas. | Verificado: `4/4 pruebas superadas`, `make` limpio con `-Werror`, `git status` no toca `tests/`. |

## 6. Demo

- [x] Preparada para 3 minutos.
- [x] Cualquier integrante puede explicar cualquier parte.
