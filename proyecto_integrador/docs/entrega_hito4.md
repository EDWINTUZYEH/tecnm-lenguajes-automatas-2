# Entrega · Hito 4

**Equipo:** Edwin Armando Tuz Yeh  
**Repositorio:** https://github.com/EDWINTUZYEH/tecnm-lenguajes-automatas-2  
**Tag:** `v1.0-hito4`  
**Fecha:** 2026-11-04

---

## 1. Qué funciona

```bash
cd proyecto_integrador
make
make test          # todos: 20/20 pruebas superadas
make test-hito4    # Hito 4: 16/16 pruebas superadas

./lenguajito tests/validos/08_anidado.lj --run
# 1 2 4 3 6 9   (ejecutado desde el binario generado)

./lenguajito tests/validos/01_suma.lj --asm
#     .text
#     .globl main
# main:
#     pushq %rbp
#     movq %rsp, %rbp
#     ...
#     ret
```

- `--asm` genera ensamblador **x86-64 AT&T**: `.text`, `.globl main`,
  prólogo (`pushq %rbp; movq %rsp, %rbp; subq $N, %rsp`), cuerpo y epílogo
  (`movl $0, %eax; leave; ret`).
- `print(e)` se traduce a `printf("%d\n", e)`; el formato vive en `.rodata`
  (`.LC0`) y se referencia con `leaq .LC0(%rip), %rdi`.
- `--run` **ya no interpreta el AST**: escribe el ensamblador, lo ensambla
  con `as --64`, lo enlaza con `gcc` y ejecuta el binario resultante,
  reenviando su salida y su código de salida.
- El ejecutable generado es un ELF de 64 bits verificado con `file`:

```text
/tmp/anidado: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV),
dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=...
```

- Las 9 pruebas válidas producen exactamente los `.out` esperados
  (`make test` → `20/20`).

## 2. Qué no funciona (y por qué)

- [ ] División entre cero en tiempo de ejecución (divisor no constante): la
      especificación no la exige; la semántica solo detecta el caso `E04`.
- [ ] El binario es para Linux x86-64; no se verifica en otras plataformas.

## 3. Pruebas

`make test`:

```text
Hito 4: 16/16 pruebas superadas
todos: 20/20 pruebas superadas
```

`make test-propias`:

```text
Pruebas propias: 9/9 superadas
```

`file` sobre el binario producido a partir de `tests/validos/08_anidado.lj`:
`ELF 64-bit LSB pie executable, x86-64`.

## 4. Reparto de trabajo

| Integrante | Archivos / etapas | Commits principales |
| :--- | :--- | :--- |
| Edwin Armando Tuz Yeh | `codegen.[ch]`, `compilador.c` (modo `--asm`, `ejecutar_binario()`), eliminación del intérprete | commit del Hito 4 |

## 5. Bitácora C-R-E-O (IA)

| Contexto | Rol | Especificación | Output | ¿Qué se aceptó, corrigió o rechazó? |
| :--- | :--- | :--- | :--- | :--- |
| Proyecto Lenguajito, Hito final (Hitos 1–3 en verde). | Ingeniero de compiladores experto en ensamblador x86-64. | AT&T: `.text`, `.globl main`, prólogo, cuerpo, epílogo; `print` con `printf(3)`; `ret` al final (el test lo exige). | `codegen.[ch]`: walk del AST con slots de pila de 4 bytes por variable y marco redondeado a 16. | Aceptado tras verificar que las 9 salidas de `--run` coinciden con los `.out`. Se corrigió la alineación de pila antes de `call printf` (marco múltiple de 16 con `%rsp % 16 == 0`). |
| Enlace y ejecución. | Ingeniero de compiladores. | `--run` debe usar el binario generado con `as` y `gcc`, no un intérprete. | `ejecutar_binario()`: directorio temporal `mkstemp`-like (`mkdtemp`), ensamblado, enlace, ejecución, limpieza y propagación del código de salida. | Se rechazó cualquier fallback al intérprete (violaría el DoD del hito). Se verificó `file`/`readelf` → ELF x86-64. |
| Cierre del hito. | Auditor. | `make test` completo en verde; `tests/` sin tocar. | Resumen de pruebas. | `20/20`; `readelf -h` muestra `Class: ELF64`, `Machine: Advanced Micro Devices X86-64`; `tests/` dorados intactos. |

## 6. Demo

- [x] Preparada para 5 minutos: (1) programa anidado
      (`tests/validos/08_anidado.lj`), (2) programa con errores
      (`tests/invalidos/02_redeclaracion.lj --check`), (3) optimización
      visible (`tests/tac/01_folding.lj --tac` → `print 10`).
- [x] Cualquier integrante puede explicar cualquier parte.
