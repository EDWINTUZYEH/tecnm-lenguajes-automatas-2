# Entrega · Hito 1

**Equipo:** Edwin, Blanca y Jimena
**Repositorio:** https://github.com/EDWINTUZYEH/tecnm-lenguajes-automatas-2
**Tag:** `v0.1-hito1`
**Fecha:** 2026-11-05

---

## 1. Qué funciona

Comandos exactos que se pueden ejecutar (desde `proyecto_integrador/`):

```bash
make                                      # construye ./lenguajito (sin warnings, -Wall -Wextra -Werror)
make test-hito1                           # Hito 1: 4/4 pruebas superadas
python3 tests/propias/revisar.py          # pruebas propias: 13/13
./lenguajito tests/validos/01_suma.lj --tokens
./lenguajito tests/hito1/01_expresion.lj --ast
./lenguajito tests/hito1/04_invalida.lj --check
```

Salidas verificadas en esta entrega:

```console
$ ./lenguajito tests/propias/01_comentarios.lj --tokens
2:1 KW int
2:5 ID a
2:7 OP =
2:9 NUM 1
2:10 DELIM ;
3:1 KW int
3:5 ID b
3:7 OP =
3:9 NUM 2
3:10 DELIM ;
5:1 KW print
5:6 DELIM (
5:7 ID a
5:9 OP +
5:11 ID b
5:12 DELIM )
5:13 DELIM ;
6:1 EOF

$ ./lenguajito tests/hito1/01_expresion.lj --ast
(programa (declarar x (+ (num 1) (* (num 2) (num 3)))))
$ ./lenguajito tests/hito1/02_asignacion.lj --ast
(programa (asignar x (* (+ (num 1) (num 2)) (num 3))))
$ ./lenguajito tests/hito1/03_sin_init.lj --ast
(programa (declarar y))

$ ./lenguajito tests/hito1/04_invalida.lj --check
tests/hito1/04_invalida.lj:1:9: error S01: se esperaba una expresión
(código de salida 1)

$ ./lenguajito tests/propias/11_ambito_bloque.lj --check
tests/propias/11_ambito_bloque.lj:5:7: error E01: variable no declarada 'y'
(código de salida 1)

$ ./lenguajito tests/propias/12_multiples_errores.lj --check
tests/propias/12_multiples_errores.lj:1:7: error E01: variable no declarada 'a'
tests/propias/12_multiples_errores.lj:2:7: error E01: variable no declarada 'b'
(código de salida 1)
```

- `--tokens`: `LINEA:COLUMNA TIPO lexema`, un token por línea, con línea
  `EOF` al final; comentarios `//`, espacios, tabuladores y CRLF se
  ignoran; carácter inválido → `S01`.
- `--ast`: formato exacto de la especificación (sección 4); precedencia
  y asociatividad izquierda según la gramática.
- `--check`: `S01` léxico y sintáctico con recuperación (varios errores
  por pasada, máximo 20); `E01` por **variable no declarada** (lectura o
  asignación) y por **leída antes de asignar valor**, con ámbitos
  anidados por bloque y shadowing. Diagnósticos con el formato
  `archivo:línea:columna: error EXX: mensaje` y código de salida 1.

## 2. Qué no funciona (y por qué)

- [ ] `E02` (redeclaración en el mismo ámbito) y `E04` (división entre
      cero constante): son diagnóstico del **Hito 2** (la DoD del Hito 1
      pide `S01`/`E01`); el compilador no los reporta todavía.
- [ ] Lectura antes de asignar **por caminos** (`if`/`while`): el
      análisis actual es conservador por ámbito, no por camino; el caso
      estático completo llega con el análisis semántico del Hito 2.
- [ ] `--tac`, `--asm` y `--run` responden
      `modo ... aún no implementado (llega en un hito posterior)`;
      son de los Hitos 3 y 4.
- [ ] `make test` (suite completa) no está en verde: incluye las pruebas
      doradas de los Hitos 2, 3 y 4. La evidencia del Hito 1 es
      `make test-hito1`.
- [ ] Los literales enteros mayores que `INT_MAX` se truncan con `strtol`.

## 3. Pruebas

Salida de `make test-hito1` (tal como la imprime el runner):

```text
Hito 1: 4/4 pruebas superadas
```

Salida de `python3 tests/propias/revisar.py`:

```text
Hito 1 propias: 13/13 pruebas superadas
```

Las pruebas doradas (`tests/`) no se modificaron: `git status` y el diff
de este entregable no tocan `tests/validos/`, `tests/invalidos/`,
`tests/hito1/`, `tests/tac/` ni `tests/run.py`.

Pruebas propias agregadas (ruta y qué cubren), en `tests/propias/`:

- `01_comentarios.lj` + `.tokens`: `--tokens` con comentarios `//`,
  columnas exactas y línea `EOF`.
- `02_precedencia.lj` + `.ast`: precedencia `* /` sobre `+ -`,
  asociatividad izquierda.
- `03_comparaciones.lj` + `.ast`: comparaciones dentro de declaración.
- `04_unario_parentesis.lj` + `.ast`: menos unario, más unario y
  paréntesis anidados.
- `05_si_si_no.lj` + `.ast`: `if/else` con bloques (formato `(si ...)`).
- `06_mientras.lj` + `.ast`: `while` con bloque y asignación.
- `07_e01_no_declarada.lj` + `.err`: `E01` al leer una variable no
  declarada (`print(z);`).
- `08_asignacion_sin_declarar.lj` + `.err`: `E01` al asignar a una
  variable no declarada (`x = 5;`).
- `09_leida_antes_asignar.lj` + `.err`: `E01` al leer una variable
  declarada que nunca recibió valor (`int x; print(x);`).
- `10_sombra_ok.lj`: shadowing en bloque anidado; `--check` sin errores.
- `11_ambito_bloque.lj` + `.err`: las variables de un bloque mueren al
  cerrarlo; reutilizarlas fuera es `E01`.
- `12_multiples_errores.lj` + `.err`: varios diagnósticos `E01` en una
  sola pasada.
- `13_caracter_invalido.lj` + `.err`: carácter inválido → `S01` léxico.

## 4. Reparto de trabajo

| Integrante | Archivos / etapas | Commits principales |
| :--- | :--- | :--- |
| Edwin | `util`, `lexer`, `parser`, `ast`, `compilador` (léxico, sintaxis, AST, CLI) | Hito 1 (tag `v0.1-hito1`) |
| Blanca | `diagnosticos`, `semantica` (ámbito y E01), `tests/propias/` | Hito 1 (tag `v0.1-hito1`) |
| Jimena | Documentación del entregable (`README`, `docs/avances.md`, `docs/entrega_hito1.md`) y preparación de la demo | Hito 1 (tag `v0.1-hito1`) |

## 5. Bitácora C-R-E-O 

| Contexto | Rol | Especificación | Output | ¿Qué se aceptó, corrigió o rechazó? |
| :--- | :--- | :--- | :--- | :--- |
| Hito 1: lexer con `LINEA:COLUMNA` y errores léxicos. | Ingeniero de compiladores experto en C. | `docs/gramatica.md` §2 (tokens y formato `--tokens`); `-Wall -Wextra -Werror`, solo libc. | `lexer.[ch]` | **Aceptada** tras auditar tipos (`KW`, `ID`, `NUM`, `OP`, `DELIM`, `EOF`), columnas y el manejo de CRLF; se verificó `6:1 EOF` en archivos con comentario final. |
| Hito 1: parser descendente y AST exacto. | Ingeniero de compiladores experto en C. | `docs/gramatica.md` §3 (EBNF LL(1)) y §4 (formato del AST); sin flex/bison. | `parser.[ch]`, `ast.[ch]` | **Rechazada** la primera versión que imprimía el AST con saltos/espacios extra (las pruebas doradas comparan la cadena exacta). **Aceptada** tras comparar la salida con `tests/hito1/*.ast` (3/3 exactos) y `04_invalida.err` (`S01` en línea 1). |
| Hito 1: `--check` semántico básico. | Ingeniero de compiladores experto en C. | `docs/gramatica.md` §5–6 (declaración obligatoria, ámbitos, formato de diagnósticos). | `semantica.[ch]` (pila de ámbitos, shadowing, `E01`) | **Aceptada** tras comprobar que los 9 programas de `tests/validos/` pasan `--check` sin errores; se limitó el alcance a `E01` y se documentó que `E02`/`E04` y el análisis por caminos llegan en el Hito 2. |
| Cierre del entregable. | Auditor. | Rúbrica del hito y checklist de 10 puntos; `tests/` intocable. | `make`, `make test-hito1` (4/4), `tests/propias/revisar.py` (13/13) | **Aceptada** la entrega: sin warnings con `-Werror`, doradas sin modificar (`git status`), diagnósticos con el formato exacto de `docs/gramatica.md` §6. |
