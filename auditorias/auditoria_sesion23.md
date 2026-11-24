# Bitácora de Requerimientos y Auditoría IA — Sesión 23

**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Etiquetas y Saltos Incondicionales  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Edwin Armando Tuz Yeh  
**Matrícula:** [24531358] 
**Track:** (C)

---

## 1. Fase 1: El Artesano (Dificultad Manual)

**Reto:** Generador de etiquetas e instrucciones GOTO.

Al realizar la implementación manual identifiqué que era necesario controlar correctamente el contador para generar etiquetas consecutivas y únicas, comenzando desde L0.

También tuve que considerar las restricciones de memoria al escribir cadenas en los búferes. El tamaño disponible puede ser limitado, por lo que utilicé `snprintf()` para evitar escribir fuera de la capacidad establecida.

Otra dificultad fue validar los parámetros recibidos, especialmente cuando la etiqueta es NULL, para evitar errores de segmentación y accesos inválidos a memoria.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal

| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C11 / GCC, utilizando bibliotecas estándar de C. |
| **Rol (R)** | Ingeniero de software especializado en sistemas y compiladores. |
| **Especificación (E)** | Generar etiquetas consecutivas y emitir instrucciones de salto incondicional o marcas de destino, respetando los límites de memoria y las firmas establecidas. |
| **Output (O)** | Código C modular, compatible con el contrato `api_sesion23.h`, sin función `main()` y con análisis de complejidad. |

### 2.2 Prompt Estructurado

```text
CONTEXTO:
Estoy desarrollando un proyecto en C para la materia
Lenguajes y Autómatas II. Necesito implementar un
generador de etiquetas y saltos incondicionales.

ROL:
Actúa como un ingeniero de software especializado
en sistemas, compiladores y programación en C.

ESPECIFICACIÓN:
Implementa las siguientes funciones:

void nueva_etiqueta(char *dst, int cap, int *contador);
void emitir_flujo(char *dst, int cap,
                  const char *etiqueta, int es_salto);

La función nueva_etiqueta debe generar etiquetas
consecutivas como L0, L1, L2 y avanzar el contador.

La función emitir_flujo debe escribir "GOTO Lx"
cuando es_salto sea distinto de cero y "Lx:"
cuando sea cero.

Considera los siguientes requisitos:
1. Respetar exactamente las firmas originales.
2. No utilizar main().
3. Validar los punteros NULL.
4. Evitar escribir fuera de los límites de dst.
5. Utilizar únicamente bibliotecas estándar de C.
6. Una etiqueta NULL debe producir una cadena vacía.
7. El código debe compilar con:
   gcc -std=c11 -Wall -Wextra -Werror.

OUTPUT:
Entrega únicamente el código C modular,
con comentarios breves y un análisis de complejidad.
No modifiques las firmas de las funciones.
```

---

## 3. Código Devuelto por el Modelo

```c
#include "api_sesion23.h"
#include <stdio.h>

void nueva_etiqueta(char *dst, int cap, int *contador) {
    if (dst == NULL || cap <= 0) {
        return;
    }

    dst[0] = '\0';

    if (contador == NULL || *contador < 0) {
        return;
    }

    snprintf(dst, (size_t)cap, "L%d", *contador);
    (*contador)++;
}

void emitir_flujo(char *dst, int cap,
                  const char *etiqueta, int es_salto) {
    if (dst == NULL || cap <= 0) {
        return;
    }

    dst[0] = '\0';

    if (etiqueta == NULL) {
        return;
    }

    if (es_salto != 0) {
        snprintf(dst, (size_t)cap, "GOTO %s", etiqueta);
    } else {
        snprintf(dst, (size_t)cap, "%s:", etiqueta);
    }
}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)

**Pruebas ejecutadas:** Generación de etiquetas, emisión de GOTO, marcas de destino y validación de etiqueta NULL.

### Salida del harness

```text
=== AUDITORIA SESION 23 - Etiquetas y saltos incondicionales ===
Caso                               esperado:              obtenido:              resultado
[ 1] nueva_etiqueta(L0)                 esperado: L0           obtenido: L0           OK
[ 2] nueva_etiqueta(L5)                 esperado: L5           obtenido: L5           OK
[ 3] emitir_flujo(GOTO L2)              esperado: GOTO L2      obtenido: GOTO L2      OK
[ 4] emitir_flujo(marca L2)             esperado: L2:          obtenido: L2:          OK
[ 5] emitir_flujo(NULL)                 esperado:              obtenido:              OK
[ 6] nueva_etiqueta(L10)                esperado: L10          obtenido: L10          OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion23.md
```

### Criterios de aceptación

- [x] Caso base y límites superados sin Crash en los seis casos evaluados.
- [x] Se utilizaron funciones de escritura limitada para evitar desbordamientos del búfer.
- [x] No se realizan asignaciones dinámicas de memoria, por lo que no hay Memory Leaks atribuibles a estas funciones.
- [x] La complejidad teórica es lineal respecto al tamaño de la cadena generada.

### Reporte Crítico

**¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?**

Un caso importante que debía considerarse era recibir una etiqueta NULL en la función `emitir_flujo()`. Si se intentara utilizar directamente con `snprintf()` sin validarla, podría producirse un comportamiento incorrecto.

Para solucionar este problema se agregó una validación que comprueba si la etiqueta es NULL antes de construir la instrucción. También se inicializa el búfer de destino como una cadena vacía para evitar conservar información anterior.

Además, se utilizó `snprintf()` para limitar la escritura a la capacidad disponible del búfer y prevenir desbordamientos de memoria.

**Análisis de complejidad:**

- `nueva_etiqueta()`: O(d), donde d es la cantidad de dígitos del contador.
- `emitir_flujo()`: O(n), donde n es la longitud de la etiqueta.
- Espacio auxiliar: O(1), sin memoria dinámica.

---

**Firma digital:** [EDWINTUZYEH]
