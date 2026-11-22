# Diseño del Hito 4 · Backend x86-64 y binario ELF

**Equipo:** Edwin, Blanca y Jimena
**Archivo principal:** `src/codegen.c`
**Pruebas:** `make test-hito4` y `make test`

---

## 1. Objetivo

Cerrar el compilador con un backend real:

- generar ensamblador **x86-64 AT&T** con `--asm`;
- ensamblar, enlazar y ejecutar el **binario generado** con `--run`;
- producir un ejecutable **ELF de 64 bits** para Linux;
- dejar `make test` completo en verde.

A partir de este hito, `--run` ya **no** interpreta el AST.

---

## 2. Flujo

```text
archivo .lj
    │
    ▼
lexer → parser → AST → semantica
    │
    ├── --check ─────────────► 0/1
    ├── --tac ───────────────► TAC optimizado (Hito 3)
    ├── --asm ───────────────► ensamblador AT&T
    └── --run
          │
          ▼
      codegen_generar()  →  /tmp/lenguajitoXXXXXX/programa.s
          │
          ▼
      as --64  →  programa.o
          │
          ▼
      gcc      →  programa (ELF)
          │
          ▼
      ejecutar y reenviar salida / código de salida
```

---

## 3. Modelo de generación

### Variables y marco de pila

- Cada declaración reserva un slot de 4 bytes: `-4(%rbp)`, `-8(%rbp)`, ...
- Los ámbitos anidados se manejan con una pila de tablas de slots; al cerrar
  un bloque sus nombres dejan de resolverse.
- El tamaño del marco se redondea a múltiplo de 16 para cumplir la ABI antes
  de `call printf` (`%rsp % 16 == 0`).

### Prólogo y epílogo

```asm
    .text
    .globl main
main:
    pushq %rbp
    movq %rsp, %rbp
    subq $N, %rsp
    ...
    movl $0, %eax
    leave
    ret
```

### Expresiones

- El resultado queda en `%eax`.
- Los subárboles se evalúan de izquierda a derecha.
- Para binarias: se evalúa la izquierda, se guarda con `pushq %rax`, se evalúa
  la derecha, se recupera la izquierda y se aplica la operación.
- Divisiones: `cltd` + `idivl`.
- Comparaciones: `cmpl` + `setl/setle/setg/setge/sete/setne` +
  `movzbl %al, %eax`.

### Sentencias

- `declarar` con inicializador: evalúa y guarda en el slot.
- `asignar`: evalúa y guarda en el slot resuelto por ámbito.
- `if/else`: `testl` + `je` a etiquetas `.L1`, `.L2`, ...
- `while`: etiqueta de inicio, condición, salto de salida, cuerpo y salto de
  vuelta.
- `print`: `printf("%d\n", e)` usando `.LC0` en `.rodata`.

---

## 4. `--asm` y `--run`

- `--asm` imprime el ensamblador completo por `stdout`; no crea archivos.
- `--run` escribe el ensamblador en un directorio temporal creado con
  `mkdtemp`, ejecuta:

  ```bash
  as --64 -o programa.o programa.s
  gcc -o programa programa.o
  ./programa
  ```

  y reenvía la salida y el código de salida del programa. Después elimina los
  archivos temporales.

El binario resultante es un **ELF 64-bit LSB pie executable, x86-64**,
verificado con `file` y `readelf -h`.

---

## 5. Pruebas

| Tipo | Casos |
| :--- | :--- |
| Doradas válidas | 9 programas con `--run` comparado contra `.out` |
| Doradas inválidas | 5 programas con `--check` |
| Doradas de AST | 4 programas del Hito 1 |
| Doradas de TAC | `tests/tac/01_folding.lj` |
| Dorada de backend | `--asm` del primer válido: exige `.globl` y `ret` |
| Propias | `23_asm_suma` (`--asm` exacto y `--run`) |

Resultado esperado:

```text
make test-hito4   → Hito 4: 16/16 pruebas superadas
make test         → todos: 20/20 pruebas superadas
make test-propias → Pruebas propias: 23/23 superadas
```

---

## 6. Límites conocidos

- El binario es para Linux x86-64; no se genera para otras plataformas.
- La división entre cero en tiempo de ejecución no se detecta en compilación
  salvo el caso constante `E04`; el binario recibe la señal del sistema.
- No hay optimizaciones de backend (registros, peephole): el objetivo del
  hito es un backend correcto y verificable.
