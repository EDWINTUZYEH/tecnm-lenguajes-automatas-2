# Bitácora de Requerimientos y Auditoría IA — Sesión 28

**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Optimización: Constant Folding  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Edwin Armando Tuz Yeh  
**Matrícula:** 24531358  
**Track:** C 
---

## 1. Fase 1: El Artesano (Dificultad Manual)

*Reto:* Plegado y simplificación de constantes.

**Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:**

> Al implementar la función tuve que cuidar que los operandos fueran números enteros completos y no aceptar textos que solamente comenzaran con un número. También tuve que considerar la división entre cero para evitar errores durante la ejecución y respetar el tamaño del arreglo de destino para no escribir fuera de sus límites.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal

| Elemento C-R-E-O | Definición Técnica |
|---|---|
| **Contexto (C)** | C11 / GCC sin bibliotecas no estándar. |
| **Rol (R)** | Ingeniero de software especializado en sistemas y compiladores. |
| **Especificación (E)** | Implementar plegado de constantes e identidades algebraicas, verificando operandos enteros completos y evitando la división entre cero. |
| **Output (O)** | Función `plegar()` en C, modular, compatible con el contrato `api_sesion28.h` y sin función `main()`. |

### 2.2 Prompt Estructurado

```text
CONTEXTO:
Estoy trabajando en la sesión 28 de Lenguajes y Autómatas II.
Necesito implementar una función en C para optimizar instrucciones
de código intermedio TAC mediante Constant Folding.

ROL:
Actúa como ingeniero de software especializado en compiladores
y programación en C.

ESPECIFICACIÓN:
Implementa la función plegar() respetando exactamente esta firma:

void plegar(char *dst, int cap, const char *res,
            const char *op, const char *a, const char *b);

Requisitos:
1. Calcular operaciones entre dos enteros completos.
2. Soportar suma, resta, multiplicación y división.
3. Simplificar x + 0 a x.
4. Simplificar x * 1 a x.
5. Simplificar x * 0 a 0.
6. No realizar divisiones entre cero.
7. Si no se puede optimizar, conservar la instrucción original.
8. Utilizar snprintf para controlar el tamaño de salida.
9. Evitar advertencias con -Wall -Wextra -Werror.
10. No incluir main() ni cambiar la firma.
11. Utilizar únicamente bibliotecas estándar necesarias.

OUTPUT:
Entrega únicamente el código completo de la función,
con sus bibliotecas necesarias y un análisis de complejidad.
```

---

## 3. Código Devuelto por el Modelo

```c
#include "api_sesion28.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void plegar(char *dst, int cap, const char *res,
            const char *op, const char *a, const char *b) {

    char *fa, *fb;
    long x = strtol(a, &fa, 10);
    long y = strtol(b, &fb, 10);
    long r;
    int na = (*a && !*fa);
    int nb = (*b && !*fb);

    if (na && nb && !(strcmp(op, "/") == 0 && y == 0)) {
        if (!strcmp(op, "+")) r = x + y;
        else if (!strcmp(op, "-")) r = x - y;
        else if (!strcmp(op, "*")) r = x * y;
        else if (!strcmp(op, "/")) r = x / y;
        else goto conservar;

        snprintf(dst, cap, "%s = %ld", res, r);
    }
    else if (!strcmp(op, "+") && nb && y == 0)
        snprintf(dst, cap, "%s = %s", res, a);

    else if (!strcmp(op, "*") && nb && y == 1)
        snprintf(dst, cap, "%s = %s", res, a);

    else if (!strcmp(op, "*") && ((na && x == 0) || (nb && y == 0)))
        snprintf(dst, cap, "%s = 0", res);

    else {
        conservar:
        snprintf(dst, cap, "%s = %s %s %s", res, a, op, b);
    }
}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)

*Pruebas ejecutadas:* Simplificación de expresiones constantes.

### Salida del harness

```text
=== AUDITORIA SESION 28 - Plegado de constantes e identidades ===
Caso                               esperado:              obtenido:              resultado
[ 1] 3 + 5                              esperado: _t0 = 8      obtenido: _t0 = 8      OK
[ 2] 2 * 3                              esperado: _t0 = 6      obtenido: _t0 = 6      OK
[ 3] 7 - 10                             esperado: _t0 = -3     obtenido: _t0 = -3     OK
[ 4] x + 0                              esperado: _t0 = x      obtenido: _t0 = x      OK
[ 5] x + y (sin plegar)                 esperado: _t0 = x + y  obtenido: _t0 = x + y  OK
[ 6] 10 / 0 (no plegar)                 esperado: _t0 = 10 / 0 obtenido: _t0 = 10 / 0 OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE.
```

- [ ] Caso base y límites superados sin *Crash*.
- [ ] No existen accesos fuera de límites ni *Memory Leaks*.
- [x] La complejidad teórica coincide con la implementada.

### Reporte Crítico

*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*

> La IA debía considerar que no todos los operandos son números enteros y que una división entre cero no debe ejecutarse. Revisé la conversión con `strtol()` para comprobar que los operandos fueran enteros completos y agregué una condición para conservar la operación original cuando el divisor es cero. También se utiliza `snprintf()` para respetar la capacidad del destino.

---

**Firma digital:** [EDWINTUZYEH]
