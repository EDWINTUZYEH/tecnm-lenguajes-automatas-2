
# Bitácora de Requerimientos y Auditoría IA — Sesión 18

**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Arreglos y Verificación de Límites  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Edwin Armando Tuz Yeh  
**Matrícula:** 24531358  
**Track:** C 

---

## 1. Fase 1: El Artesano (Dificultad Manual)

*Reto:* Cálculo de tamaño de arreglo en memoria

*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*

> Al realizar el código manualmente, identifiqué que era necesario conocer el tamaño que ocupa cada tipo de dato para calcular correctamente
> la memoria de un arreglo.
>  También tuve que considerar que no se deben aceptar cantidades negativas de elementos, porque no representan un tamaño válido.
>  Otro detalle fue comprobar los índices desde cero, ya que el último índice permitido siempre es el número de elementos menos uno.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal

| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C11 / GCC sin bibliotecas no estándar. |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores. |
| **Especificación (E)** | Calcular el tamaño de arreglos mediante el tipo de dato y la
cantidad de elementos. Aceptar char, short, int, float, double y puntero.
Rechazar tipos desconocidos, cantidades negativas e índices fuera del rango válido. 
|
| **Output (O)** | Código modular en C, respetando las firmas establecidas en api_sesion18.h, sin función main(), con análisis de complejidad. |

### 2.2 Prompt Estructurado

```text
Contexto:
Estoy desarrollando una práctica de Lenguajes y Autómatas II
en C11 para calcular el tamaño de arreglos y verificar
los límites de sus índices.

Rol:
Actúa como un ingeniero de software especializado en
lenguaje C y desarrollo de compiladores.

Especificación:
1. Implementa bytes_arreglo(const char *tipo, int elementos).
2. Reconoce los tipos char, short, int, float, double
   y puntero.
3. Utiliza sizeof para obtener el tamaño de cada tipo.
4. Devuelve -1 cuando el tipo sea desconocido o la
   cantidad de elementos sea negativa.
5. Devuelve cero cuando la cantidad de elementos sea cero.
6. Evita desbordamientos al multiplicar el tamaño por
   la cantidad de elementos.
7. Implementa indice_en_rango(int indice, int elementos).
8. Devuelve 1 solamente cuando el índice sea mayor o
   igual a cero y menor que el número de elementos.
9. Devuelve 0 cuando el índice esté fuera del rango.
10. Respeta exactamente las firmas del archivo
    api_sesion18.h.
11. No agregues main() y evita advertencias con
    -Wall -Wextra -Werror.

Output:
Entrega dos funciones modulares en C11, código completo,
explicación breve de su funcionamiento y complejidad
temporal y espacial.
```

---

## 3. Código Devuelto por el Modelo

```c
#include "api_sesion18.h"
#include <string.h>
#include <limits.h>

long bytes_arreglo(const char *tipo, int elementos) {
    long ancho;

    if (tipo == NULL || elementos < 0) {
        return -1;
    }

    if (strcmp(tipo, "char") == 0) {
        ancho = sizeof(char);
    }
    else if (strcmp(tipo, "short") == 0) {
        ancho = sizeof(short);
    }
    else if (strcmp(tipo, "int") == 0) {
        ancho = sizeof(int);
    }
    else if (strcmp(tipo, "float") == 0) {
        ancho = sizeof(float);
    }
    else if (strcmp(tipo, "double") == 0) {
        ancho = sizeof(double);
    }
    else if (strcmp(tipo, "puntero") == 0) {
        ancho = sizeof(void *);
    }
    else {
        return -1;
    }

    if (elementos > 0 && ancho > LONG_MAX / elementos) {
        return -1;
    }

    return ancho * elementos;
}

int indice_en_rango(int indice, int elementos) {
    if (elementos <= 0) {
        return 0;
    }

    if (indice < 0 || indice >= elementos) {
        return 0;
    }

    return 1;
}
```

**Análisis de complejidad:**

- `bytes_arreglo()`: O(1), porque realiza una cantidad fija de comparaciones y operaciones.
- `indice_en_rango()`: O(1), porque realiza comparaciones directas.
- Espacio auxiliar: O(1), porque ambas funciones utilizan una cantidad fija de variables.

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)

*Pruebas ejecutadas:* Límites estáticos y dimensiones inválidas.

### Salida del harness

```text
=== AUDITORIA SESION 18 - Tamano de arreglo y limites ===
Caso                               esperado:              obtenido:              resultado
[ 1] int[10]                       esperado: 40           obtenido: 40           OK
[ 2] double[3]                     esperado: 24           obtenido: 24           OK
[ 3] int[-4]                       esperado: -1           obtenido: -1           OK
[ 4] indice 0 de 5                 esperado: 1            obtenido: 1            OK
[ 5] indice 5 de 5                 esperado: 0            obtenido: 0            OK
[ 6] indice negativo               esperado: 0            obtenido: 0            OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion18.md
```

- [x] Caso base y límites superados sin *Crash*.
- [x] No existen accesos fuera de límites ni *Memory Leaks* en estas funciones.
- [x] La complejidad teórica coincide con la implementada.

### Reporte Crítico

*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*

> Un detalle importante que debía revisarse era el manejo de índices negativos.
>  Si solamente se comprueba que el índice sea menor que la cantidad de elementos, se pueden aceptar posiciones negativas.
>  Para evitarlo, agregué la condición `indice < 0` y también comprobé que el índice no sea igual o mayor que el número de elementos.
>
> También consideré el desbordamiento de memoria al multiplicar la cantidad de elementos por el tamaño del tipo de dato, utilizando `LONG_MAX` para evitar superar el límite del tipo long.

---

**Firma digital:** [EDWINTUZYEH]
