# Bitácora de Requerimientos y Auditoría IA — Sesión 09
**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Reporte Formal de Errores Semánticos  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [edwin armando tuz yeh]  
**Matrícula:** [24531358]  
**Track:** [C]
---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Diagnóstico con línea y columna  
*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*
> El reto principal fue respetar que el buffer pertenece al llamador. La función
> no puede escribir más de `cap-1` caracteres y el resultado siempre debe quedar
> terminado en `'\0'`. Usar `sprintf` habría desbordado el buffer en el caso 4
> (`cap=10`, mensaje de 37 caracteres), así que usé `snprintf(salida, (size_t)cap, ...)`,
> que trunca y termina la cadena por sí mismo. También identifiqué tres entradas
> peligrosas: `salida == NULL`, `cap <= 0` (no se puede escribir ni el `'\0'`) y
> punteros `archivo`/`mensaje` nulos, que con `%s` provocan comportamiento
> indefinido. Los valida antes de formatear. Otra restricción fue el formato:
> `archivo:línea:columna: error: mensaje`, sin espacios extra ni punto final.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C11 / GCC (`-std=c11 -Wall -Wextra -Werror`), sin bibliotecas no estándar; el `main()` lo aporta el harness |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores, experto en programación defensiva y manejo seguro de buffers |
| **Especificación (E)** | Estructura estándar de errores GCC: `archivo:línea:columna: error: mensaje`, máximo `cap-1` caracteres, siempre terminado en `'\0'`, manejo de `cap <= 0` y punteros `NULL` |
| **Output (O)** | Solo código modular con la firma exacta de `api_sesion09.h` y análisis de complejidad |

### 2.2 Prompt Estructurado
```text
CONTEXTO: Estoy construyendo un compilador en C11. Mi código se compila con
gcc -std=c11 -Wall -Wextra -Werror junto con un harness que ya contiene main().
No puedes usar bibliotecas no estándar.

ROL: Actúa como ingeniero de software de sistemas y compiladores, experto en
programación defensiva y manejo seguro de buffers.

ESPECIFICACIÓN: Implementa exactamente esta firma, sin modificarla:
void reportar(const char *archivo, int linea, int columna,
              const char *mensaje, char *salida, int cap);
Debe escribir en `salida` el diagnóstico con el formato de GCC:
archivo:linea:columna: error: mensaje
Sin espacios extra ni punto final. Reglas obligatorias:
1. Nunca escribir más de cap-1 caracteres (el buffer es del llamador).
2. El resultado siempre termina en '\0'.
3. Si cap <= 0 o salida es NULL, no escribir nada.
4. Tratar archivo o mensaje NULL sin comportamiento indefinido.
5. Aceptar línea y columna 0 (se imprimen como 0).
6. No incluir main().

OUTPUT: Entrega solo el código C, sin explicaciones, y al final indica en una
línea la complejidad en tiempo y espacio.
```

---

## 3. Código Devuelto por el Modelo
```c
// Código devuelto por el LLM
#include "api_sesion09.h"
#include <stdio.h>

void reportar(const char *archivo, int linea, int columna, const char *mensaje, char *salida, int cap) {
    if (salida == NULL || cap <= 0) return;
    if (archivo == NULL) archivo = "(desconocido)";
    if (mensaje == NULL) mensaje = "";
    snprintf(salida, (size_t)cap, "%s:%d:%d: error: %s",
             archivo, linea, columna, mensaje);
}
// Complejidad: O(n) en tiempo, con n = longitud total de archivo + mensaje
// (acotada por cap); O(1) en espacio adicional.
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)
*Pruebas ejecutadas:* Múltiples errores sin abortar parser

### Salida del harness
```text
=== AUDITORIA SESION 09 - Diagnostico con linea y columna ===
Caso                               esperado:              obtenido:              resultado
[ 1] main.c:14:5
     esperado: main.c:14:5: error: tipo incompatible
     obtenido: main.c:14:5: error: tipo incompatible
     -> OK
[ 2] a.c:1:1
     esperado: a.c:1:1: error: x
     obtenido: a.c:1:1: error: x
     -> OK
[ 3] linea 0
     esperado: x.c:0:0: error: y
     obtenido: x.c:0:0: error: y
     -> OK
[ 4] cap=10 trunca                      esperado: main.c:14    obtenido: main.c:14    OK

RESULTADO: 4/4 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion09.md
```

* [x] Caso base y límites superados sin *Crash*.
* [x] No existen accesos fuera de límites ni *Memory Leaks*.
* [x] La complejidad teórica coincide con la implementada.

### Reporte Crítico
*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*
>  p. ej. usó `sprintf` en lugar de
> `snprintf`, no validó `cap <= 0`, o no trató `archivo`/`mensaje` nulos].
> Lo detecté revisando el código línea por línea / ejecutando `prueba_extra.c`
> con `cap=0`, `cap=1` y `mensaje=NULL`]. Lo solucioné cambiando a `snprintf`
> con `(size_t)cap` / agregando la guarda inicial / sustituyendo los NULL.

---
**Firma digital:** [EDWINTUZYEH]
