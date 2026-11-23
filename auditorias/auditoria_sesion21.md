**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Fundamentos de Código de 3 Direcciones  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Edwin Armando Tuz Yeh  
**Matrícula:** 24531358  
**Track:** (C)
---

## 1. Fase 1: El Artesano (Dificultad Manual)

*Reto:* Representación en Cuádruplos (op,a,b,r)

*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*

> Al realizar la implementación manual identifiqué que era importante respetar el tamaño del buffer para evitar escribir fuera de sus límites.
>  También tuve que cuidar el formato de los cuádruplos y comprobar que los argumentos NULL se representaran con un guion bajo (_).
>  Otro detalle fue incrementar correctamente el contador después de generar cada temporal para evitar repetir nombres.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal

| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C99 / GCC o Rust 2021 sin bibliotecas no estándar |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores |
| **Especificación (E)** | Generación de temporales únicos (_t0..) |
| **Output (O)** | Solo código modular y análisis de complejidad |

### 2.2 Prompt Estructurado

```text
Contexto:
Estoy trabajando en la Sesión 21 de Lenguajes y Autómatas II.
Necesito implementar código de tres direcciones (TAC) en lenguaje C,
utilizando temporales únicos y representación mediante cuádruplos.

Rol:
Actúa como un ingeniero de software especializado en programación
de sistemas y compiladores, con conocimientos de C y GCC.

Especificación:
Implementa las funciones nuevo_temporal() y emitir_cuadruplo()
respetando exactamente las siguientes firmas:

void nuevo_temporal(char *dst, int cap, int *contador);

void emitir_cuadruplo(char *dst, int cap, const char *op,
                      const char *a1, const char *a2, const char *res);

La función nuevo_temporal debe generar nombres como _t0, _t1, _t2,
utilizando el contador recibido y aumentándolo después de cada llamada.

La función emitir_cuadruplo debe generar el formato:
(op, a1, a2, res).

Cuando algún argumento sea NULL, debe sustituirse por un guion bajo (_).

Se debe respetar la capacidad del buffer, no utilizar memoria global,
no reservar memoria dinámica y no agregar una función main().

El código debe compilar con:
gcc -std=c11 -Wall -Wextra -Werror

Output:
Devuelve únicamente el código C modular completo, con las dos funciones
implementadas y una breve explicación de su complejidad.
```

---

## 3. Código Devuelto por el Modelo

```c
#include "api_sesion21.h"
#include <stdio.h>

void nuevo_temporal(char *dst, int cap, int *contador) {
    if (dst == NULL || cap <= 0 || contador == NULL) {
        return;
    }

    (void)snprintf(dst, (size_t)cap, "_t%d", *contador);
    (*contador)++;
}

void emitir_cuadruplo(char *dst, int cap, const char *op,
                      const char *a1, const char *a2, const char *res) {
    if (dst == NULL || cap <= 0) {
        return;
    }

    (void)snprintf(dst, (size_t)cap, "(%s, %s, %s, %s)",
                   op != NULL ? op : "_",
                   a1 != NULL ? a1 : "_",
                   a2 != NULL ? a2 : "_",
                   res != NULL ? res : "_");
}
```

**Análisis de complejidad:**

- `nuevo_temporal()`: O(log n) respecto al valor del contador, por la conversión numérica a texto.
- `emitir_cuadruplo()`: O(L), donde L es la longitud total de las cadenas formateadas.
- Memoria auxiliar: O(1), sin reservar memoria dinámica.

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)

*Pruebas ejecutadas:* Generación de temporales y representación de cuádruplos.

### Salida del harness

```text
=== AUDITORIA SESION 21 - Cuadruplos y temporales unicos ===
Caso                               esperado:              obtenido:              resultado
[ 1] nuevo_temporal(_t0)                esperado: _t0          obtenido: _t0          OK
[ 2] nuevo_temporal(_t7)                esperado: _t7          obtenido: _t7          OK
[ 3] cuadruplo de a + b
     esperado: (+, a, b, _t0)
     obtenido: (+, a, b, _t0)
     -> OK
[ 4] cuadruplo de _t0 * c
     esperado: (*, _t0, c, _t1)
     obtenido: (*, _t0, c, _t1)
     -> OK
[ 5] asignacion simple                  esperado: (=, a, _, x) obtenido: (=, a, _, x) OK
[ 6] goto sin operandos
     esperado: (goto, L1, _, _)
     obtenido: (goto, L1, _, _)
     -> OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion21.md
```

- [x] Caso base y límites superados sin Crash.
- [x] No existen accesos fuera de límites en las pruebas realizadas ni Memory Leaks por asignación dinámica.
- [x] La complejidad teórica coincide con la implementada.

### Reporte Crítico

*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*

> Un caso importante que debía revisarse era el manejo de argumentos NULL al generar los cuádruplos. Si no se comprueba cada argumento, la salida puede ser incorrecta. Se solucionó agregando una condición para sustituir los valores NULL por un guion bajo (_). También se agregó una validación para comprobar que el buffer exista y tenga capacidad positiva antes de escribir. Finalmente, se verificó el resultado mediante los seis casos del harness.

---

**Firma digital:** [EDWINTUZYEH]
