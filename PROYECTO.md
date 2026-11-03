# Proyecto Integrador · Lenguajito

**Lenguajes y Autómatas II (SCD-1016)** · TecNM Cancún · 30% de la calificación

Este documento son las **reglas y los requisitos** del proyecto. El lenguaje que
debes compilar está especificado en
[`proyecto_integrador/docs/gramatica.md`](proyecto_integrador/docs/gramatica.md).
Si es tu primera vez, empieza por la guía operativa:
[`proyecto_integrador/docs/guia-proyecto.md`](proyecto_integrador/docs/guia-proyecto.md).

---

## 1. Qué vas a construir

Un **compilador** para *Lenguajito*, un lenguaje mínimo de variables enteras,
asignaciones, `if/else`, `while` y `print`. El compilador lee un archivo `.lj` y
puede:

- mostrar los tokens (`--tokens`),
- mostrar el árbol sintáctico (`--ast`),
- revisar la semántica y reportar errores (`--check`),
- generar código de tres direcciones (`--tac`),
- generar ensamblador x86-64 (`--asm`),
- compilar, enlazar y ejecutar el programa (`--run`).

No es una aplicación con interfaz gráfica ni un lenguaje nuevo inventado por ti:
es el compilador de **este** lenguaje, con **esta** gramática.

### Lo que ya sabes hacer

Cada etapa del compilador corresponde a laboratorios que ya trabajaste:

| Etapa | Laboratorios |
| :--- | :--- |
| Tokens y AST | 01–05 |
| Tipos y evaluación | 06–08 |
| Diagnósticos | 09 |
| Tabla de símbolos y ámbitos | 11–20 |
| TAC y optimización | 21–29 |
| Ensamblador y enlace | 31–38 |

**El proyecto no agrega temas nuevos: integra los que ya viste.** Si un laboratorio
te quedó flojo, ese es el momento de recuperarlo.

---

## 2. Equipos y roles

- Equipos de **3 o 4 personas**. Un solo repositorio por equipo (fork del repo del
  curso), todo dentro de `proyecto_integrador/`.
- Roles sugeridos (pueden rotar en cada hito): léxico/sintaxis, semántica, TAC,
  backend y pruebas.
- **Todos programan.** En la demo cualquier integrante puede ser cuestionado sobre
  cualquier parte; si no la explica, esa parte no cuenta como entregada.
- El trabajo se reparte en el `README` del proyecto con nombre y archivos por
  persona. Los commits deben reflejar ese reparto.

---

## 3. Arquitectura esperada

```text
proyecto_integrador/
├── Makefile              # make, make test, make clean
├── src/
│   ├── main.c            # interfaz de línea de comandos (ya viene)
│   ├── compilador.h
│   ├── lexer.c           # tokens, línea y columna
│   ├── parser.c          # análisis descendente + AST
│   ├── ast.c             # construcción e impresión del AST
│   ├── semantica.c       # tabla de símbolos, ámbitos, diagnósticos
│   ├── tac.c             # generación y optimización de TAC
│   └── codegen.c         # ensamblador x86-64
├── docs/                 # gramática y decisiones de diseño
└── tests/                # programas de prueba (no se modifican)
```

Puedes reorganizar archivos, pero mantén la separación por etapas: se evalúa que
cada una se pueda explicar y probar por separado.

---

## 4. Hitos

Cuatro entregas, **7.5 puntos cada una** (30 en total). Cada hito tiene una
definición de terminado (DoD) que es lo que se revisa.

### Hito 1 · Sesión 10 · Léxico, sintaxis y AST de expresiones

**Objetivo:** leer el archivo, producir tokens y el AST de expresiones,
declaraciones y asignaciones.

**DoD**
- [ ] `--tokens` imprime `linea:columna TIPO lexema`, un token por línea.
- [ ] `--ast` produce el formato de la especificación para 3 programas.
- [ ] `--check` acepta los programas válidos y reporta `S01`/`E01` en los inválidos.
- [ ] `make test-hito1` en verde.
- [ ] `README` con "qué funciona / qué no".
- [ ] Demo de 3 minutos.

**Entregable:** tag `v0.1-hito1`, `make test-hito1` en verde, `README` actualizado.

### Hito 2 · Sesión 20 · Sentencias, ámbitos y diagnósticos

**Objetivo:** gramática completa (bloques, `if/else`, `while`, `print`) y análisis
semántico con tabla de símbolos.

**DoD**
- [ ] El parser acepta la gramática completa y rechaza lo inválido con `S01`.
- [ ] Tabla de símbolos con ámbitos anidados, shadowing, redeclaración (`E02`),
      variable no declarada (`E01`) y lectura antes de asignar (`E01`).
- [ ] Los diagnósticos usan el formato y los códigos de la especificación.
- [ ] Se reportan **varios** errores en una pasada (recuperación).
- [ ] `--run` ya puede ejecutar los programas (interpretando el AST está permitido
      en este hito).
- [ ] `make test-hito2` en verde y demo.

**Entregable:** tag `v0.2-hito2`, pruebas en verde, `README`.

### Hito 3 · Sesión 30 · TAC y optimización

**Objetivo:** generar código de tres direcciones para todas las construcciones y
aplicar dos optimizaciones.

**DoD**
- [ ] `--tac` genera TAC para expresiones, asignaciones, `if/else`, `while` y
      `print`, con temporales únicos (`_t0`, `_t1`, ...).
- [ ] **Plegado de constantes:** `2 * 3 + 4` no debe aparecer como operación entre
      constantes en el TAC.
- [ ] **Eliminación de código muerto:** no deben quedar temporales asignados que
      nadie use.
- [ ] `--tac` de dos programas se explica en la demo (antes/después).
- [ ] `make test` completo en verde.
- [ ] Demo de 3 minutos.

**Entregable:** tag `v0.3-hito3`, TAC de los dos programas, `README`.

### Hito 4 · Sesión 40 · Backend y binario ELF

**Objetivo:** generar ensamblador x86-64, enlazarlo y ejecutar el binario.

**DoD**
- [ ] `--asm` genera ensamblador AT&T con `.text`, `.globl main`, prólogo,
      cuerpo y epílogo.
- [ ] `--run` ejecuta el **binario generado** con `as` y `gcc` (no un intérprete).
- [ ] `file` o `readelf` muestran un ELF ejecutable.
- [ ] `make test` completo en verde, incluidos los 9 programas válidos.
- [ ] Demo final de 5 minutos: un programa con anidamiento, uno con errores y uno
      con optimización visible.

**Entregable:** tag `v1.0-hito4`, binario, `README` final y demo.

---

## 5. Avances

Entre hito y hito hay un **avance** de 2 minutos (3 bullets + commit). Se documenta
en `proyecto_integrador/docs/avances.md`. No lleva calificación propia, pero es
requisito para el hito siguiente: si falta, el hito siguiente vale **10% menos**.

| Sesión | Qué se presenta |
| :---: | :--- |
| 05 | Hito 0: repo, `Makefile`, gramática leída, primer programa de prueba |
| 08 | Lexer: tokens de un programa y errores léxicos |
| 15 | Parser de sentencias en progreso + tabla de símbolos inicial |
| 25 | TAC de expresiones y de un `if` |
| 35 | `--asm` de una expresión y primer binario que corre |

Formato del avance:

```text
1. Qué compila hoy (comando exacto).
2. Qué falla y por qué.
3. Qué sigue antes del hito.
```

---

## 6. Rúbrica (por hito, 7.5 puntos)

| Criterio | Puntos | Qué se mira |
| :--- | :---: | :--- |
| **Funciona** | 3.0 | Los programas del hito producen la salida o los errores esperados |
| **Pruebas** | 1.5 | `make test` en verde y pruebas propias además de las doradas |
| **Claridad y demo** | 1.5 | Código modular, sin warnings, `README` claro, cualquier integrante explica su parte |
| **Auditoría e IA** | 1.5 | Bitácora C-R-E-O de lo que pidieron a la IA, qué aceptaron y qué rechazaron |

Un hito sin demo vale como máximo 50%. Un hito con `make test` en rojo pierde
completos los 3 puntos de "Funciona".

---

## 7. Reglas

1. **Repositorio:** un fork del repo del curso por equipo. El proyecto vive en
   `proyecto_integrador/`. No se aceptan enlaces a repos externos.
2. **Lenguaje y herramientas:** C11 y `gcc` (mismas banderas de los laboratorios).
   El analizador es **descendente recursivo escrito a mano**: no se permite
   `flex`, `bison`, `yacc`, `ANTLR` ni generadores de parsers.
3. **Bibliotecas:** solo `libc` estándar. Nada de bibliotecas de terceros.
4. **Pruebas doradas:** `proyecto_integrador/tests/` no se modifica. Si cambias un
   programa o una salida esperada, el criterio "Pruebas" vale 0.
5. **IA:** permitida como en los laboratorios: contrato **C-R-E-O**, y la respuesta
   se audita antes de integrarla. Cada hito incluye la bitácora de lo usado. Sin
   bitácora, se pierden los 1.5 puntos de auditoría.
6. **Atrasos:** −10% por día, hasta 3 días. Después de eso el hito vale 0, salvo
   causa justificada por escrito antes de la fecha.
7. **Integridad:** copiar código de otro equipo, o de un compilador existente, es
   calificación 0 en el proyecto y reporte a la coordinación. Compartir pruebas
   propias entre equipos sí está permitido; compartir implementación, no.
8. **Extensiones:** hasta **+1 punto** sobre los 30, con autorización previa y demo.
   Candidatas: `for`, `do-while`, arreglos, funciones, `float`, `break`/`continue`.
   Una extensión no puede romper la gramática base ni las pruebas doradas.

---

## 8. Calendario

| Semana | Sesión | Entregable |
| :---: | :---: | :--- |
| 1 | 05 | Hito 0 (repo y `make`) — requisito |
| 2 | 08 | Avance: lexer |
| 3 | 10 | **Hito 1** |
| 5 | 15 | Avance: parser y tabla de símbolos |
| 6 | 20 | **Hito 2** |
| 8 | 25 | Avance: TAC |
| 9 | 30 | **Hito 3** |
| 11 | 35 | Avance: asm y enlace |
| 12 | 40 | **Hito 4** y demo final |

---

## 9. Preguntas frecuentes

**¿Puedo reutilizar el parser del laboratorio 10?**
Sí, es tuyo. Tendrás que ampliarlo para aceptar la gramática completa.

**¿Tengo que implementar un intérprete antes del backend?**
No es obligatorio, pero es la forma más rápida de probar la semántica en el Hito 2.
En el Hito 4 el `--run` debe usar el binario generado.

**¿Puedo usar el código de la IA tal cual?**
Puedes usarlo si pasa las pruebas y lo auditás. La bitácora debe decir qué pediste,
qué te devolvió y qué corregiste o rechazaste.

**¿Cuántas líneas debe tener?**
No hay métrica. Un compilador de este lenguaje bien hecho ronda las 1,500–2,500
líneas de C, pero lo que se califica es el comportamiento y la claridad.

**¿Y si mi equipo va muy bien y quiere más?**
Pide una extensión antes del Hito 3. Se evalúa en la demo final y suma hasta 1 punto.

**¿La gramática se puede cambiar?**
No en la parte base. Los programas de prueba dependen de ella. Cualquier cambio es
una extensión autorizada por escrito.
