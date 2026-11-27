# Bitácora de Requerimientos y Auditoría IA — Sesión 27

**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Indexación de Arreglos en TAC  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Edwin Armando Tuz Yeh  
**Matrícula:** 24531358  
**Track:** C 

---

## 1. Fase 1: El Artesano (Dificultad Manual)

**Reto:** Cálculo de desplazamientos base + offset.

**Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:**

> Al realizar la implementación manual, identifiqué que uno de los principales retos era calcular correctamente la posición de un elemento dentro de un arreglo. No basta con utilizar directamente el índice, porque cada elemento ocupa una cantidad determinada de bytes en memoria.
>
> Para resolverlo, primero tuve que multiplicar el índice por el tamaño de cada elemento. En los arreglos de dos dimensiones también fue necesario convertir los índices de fila y columna en un solo desplazamiento antes de calcular la dirección.
>
> Otra dificultad fue respetar el formato de las instrucciones TAC, utilizar temporales consecutivos y evitar escribir fuera de los límites del arreglo de instrucciones. Por eso fue importante controlar la cantidad máxima de instrucciones y el espacio disponible para cada línea.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal

| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Lenguaje C99, compilador GCC y bibliotecas estándar. |
| **Rol (R)** | Ingeniero de software especializado en sistemas y compiladores. |
| **Especificación (E)** | Generar instrucciones TAC para acceder a arreglos de una y dos dimensiones, calculando correctamente los desplazamientos y utilizando temporales consecutivos. |
| **Output (O)** | Código modular en C, sin función `main()`, que implemente las dos funciones solicitadas y permita analizar su complejidad. |

### 2.2 Prompt Estructurado

```text
Actúa como un ingeniero de software especializado en sistemas
y compiladores.

Necesito implementar en lenguaje C las funciones para generar
instrucciones de Código de Tres Direcciones (TAC) para acceder
a elementos de arreglos de una y dos dimensiones.

CONTEXTO:
- Utilizar C99 y bibliotecas estándar.
- El código debe compilar con GCC.
- No incluir la función main().
- Respetar las firmas declaradas en api_sesion27.h.
- Cada instrucción debe ocupar como máximo 63 caracteres
  más el terminador nulo.

REQUERIMIENTOS:

1. Implementar:
int emitir_acceso(char lineas[][64], int max,
                  const char *base, const char *indice,
                  int ancho, int *temporales);

Para un arreglo unidimensional, calcular:
offset = indice * ancho

Generar:
_t0 = indice * ancho
_t1 = base[_t0]

2. Implementar:
int emitir_acceso_2d(char lineas[][64], int max,
                     const char *base, const char *i,
                     const char *j, int filas,
                     int ancho, int *temporales);

Para un arreglo bidimensional, calcular:
posicion = i * filas + j
offset = posicion * ancho

Generar las instrucciones necesarias utilizando temporales
consecutivos y terminar con el acceso al arreglo.

3. VALIDACIONES:
- Si base es NULL, devolver 0.
- Validar los punteros necesarios.
- Comprobar que max sea suficiente.
- Validar que ancho y filas sean positivos.
- Evitar desbordamientos en el contador de temporales.
- No escribir instrucciones incompletas.
- Utilizar snprintf para generar las instrucciones.
- No modificar el contador de temporales si ocurre un error.

4. RESULTADO:
Entregar únicamente código modular en C, sin main(),
con las dos funciones completas y una explicación breve
de su complejidad temporal y espacial.

El código debe compilar sin advertencias utilizando:
gcc -std=c11 -Wall -Wextra -Werror
```

---

## 3. Código Devuelto por el Modelo

El modelo propuso utilizar `snprintf()` para construir las instrucciones TAC y arreglos temporales auxiliares para validar que todas las líneas se generen correctamente antes de copiarlas al resultado final.

**Archivo:** `ia_sesion27_c.c`

```c
#include "api_sesion27.h"
#include <stdio.h>
#include <string.h>
#include <limits.h>

int emitir_acceso(char lineas[][64], int max, const char *base,
                  const char *indice, int ancho, int *temporales)
{
    char aux[2][64];
    int t, n;

    if (!lineas || !base || !indice || !temporales ||
        max < 2 || ancho <= 0 || *temporales < 0 ||
        *temporales > INT_MAX - 2)
        return 0;

    t = *temporales;

    n = snprintf(aux[0], 64, "_t%d = %s * %d",
                 t, indice, ancho);
    if (n < 0 || n >= 64) return 0;

    n = snprintf(aux[1], 64, "_t%d = %s[_t%d]",
                 t + 1, base, t);
    if (n < 0 || n >= 64) return 0;

    memcpy(lineas, aux, sizeof(aux));
    *temporales += 2;

    return 2;
}

int emitir_acceso_2d(char lineas[][64], int max, const char *base,
                     const char *i, const char *j, int filas,
                     int ancho, int *temporales)
{
    char aux[4][64];
    int t, n;

    if (!lineas || !base || !i || !j || !temporales ||
        max < 4 || filas <= 0 || ancho <= 0 ||
        *temporales < 0 || *temporales > INT_MAX - 4)
        return 0;

    t = *temporales;

    n = snprintf(aux[0], 64, "_t%d = %s * %d",
                 t, i, filas);
    if (n < 0 || n >= 64) return 0;

    n = snprintf(aux[1], 64, "_t%d = _t%d + %s",
                 t + 1, t, j);
    if (n < 0 || n >= 64) return 0;

    n = snprintf(aux[2], 64, "_t%d = _t%d * %d",
                 t + 2, t + 1, ancho);
    if (n < 0 || n >= 64) return 0;

    n = snprintf(aux[3], 64, "_t%d = %s[_t%d]",
                 t + 3, base, t + 2);
    if (n < 0 || n >= 64) return 0;

    memcpy(lineas, aux, sizeof(aux));
    *temporales += 4;

    return 4;
}
```

### Explicación del funcionamiento

La primera función, `emitir_acceso()`, genera dos instrucciones. Primero multiplica el índice por el tamaño del elemento y después utiliza el desplazamiento calculado para acceder al arreglo.

La segunda función, `emitir_acceso_2d()`, genera cuatro instrucciones. Primero calcula la posición a partir de los índices `i` y `j`, después multiplica el resultado por el ancho del elemento y finalmente realiza el acceso al arreglo.

También se utilizan validaciones para comprobar los punteros, la capacidad disponible, los valores positivos y los límites del contador de temporales.

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)

**Pruebas ejecutadas:** Arreglos multidimensionales en TAC.

### Salida del harness

```text

=== AUDITORIA SESION 27 - Desplazamientos para arreglos 1D y 2D ===
Caso                               esperado:              obtenido:              resultado
[ 1] 1D: i * 4                          esperado: _t0 = i * 4  obtenido: _t0 = i * 4  OK
[ 2] 1D: A[_t0]                         esperado: _t1 = A[_t0] obtenido: _t1 = A[_t0] OK
[ 3] 2D: i * 3                          esperado: _t0 = i * 3  obtenido: _t0 = i * 3  OK
[ 4] 2D: offset por ancho
     esperado: _t2 = _t1 * 4
     obtenido: _t2 = _t1 * 4
     -> OK
[ 5] 2D: M[_t2]                         esperado: _t3 = M[_t2] obtenido: _t3 = M[_t2] OK
[ 6] base NULL (sin acceso)             esperado: 0            obtenido: 0            OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion27.md
```

### Comprobaciones realizadas

| Prueba | Resultado esperado | Estado |
| :--- | :--- | :--- |
| Acceso unidimensional | `_t0 = i * 4` | Correcto |
| Lectura del arreglo | `_t1 = A[_t0]` | Correcto |
| Cálculo de fila | `_t0 = i * 3` | Correcto |
| Cálculo de posición bidimensional | `_t1 = _t0 + j` | Correcto |
| Cálculo del desplazamiento y lectura | `_t2 = _t1 * 4` y `_t3 = M[_t2]` | Correcto |
| Validación de base NULL | Devolver 0 | Correcto |

* [x] Se verificó que los casos probados se ejecutaran sin provocar un Crash.
* [x] Se comprobaron los límites de las instrucciones y los temporales en los casos ejecutados.
* [x] La complejidad teórica coincide con la cantidad fija de instrucciones generadas.

### Reporte Crítico

**¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?**

> Al revisar la propuesta, consideré importante comprobar qué sucedería cuando se recibiera un puntero NULL, cuando la capacidad máxima de instrucciones fuera insuficiente o cuando el contador de temporales estuviera cerca de su límite.
>
> Para evitar problemas, se agregaron validaciones antes de generar las instrucciones. También se utilizaron arreglos auxiliares para construir primero todas las líneas y copiarlas al arreglo de salida solamente cuando la generación fue correcta.
>
> De esta manera, si ocurre un error, la función devuelve 0 y no modifica el contador de temporales. Con estas medidas se busca evitar instrucciones incompletas y escrituras fuera de los límites disponibles.

---

## Análisis de complejidad

Las dos funciones generan una cantidad fija de instrucciones, sin importar el tamaño del arreglo original.

| Función | Instrucciones | Tiempo | Espacio auxiliar |
| :--- | :---: | :---: | :---: |
| `emitir_acceso()` | 2 | O(1) | O(1) |
| `emitir_acceso_2d()` | 4 | O(1) | O(1) |

La complejidad es constante porque cada función realiza un número limitado de operaciones: generar instrucciones, validar datos y actualizar los temporales. No necesita recorrer el arreglo completo.

---

**Conclusión personal**

En esta actividad comprendí mejor cómo se realiza el cálculo de direcciones para acceder a los elementos de arreglos mediante código de tres direcciones. También pude identificar que en los arreglos de dos dimensiones primero se necesita convertir los índices en una posición lineal y después calcular el desplazamiento en memoria.

La comparación entre mi implementación manual y la propuesta de la IA me ayudó a revisar aspectos que pueden pasar desapercibidos, como las validaciones de punteros, los límites de memoria y el manejo de temporales. Finalmente, las pruebas del harness permitieron comprobar que las instrucciones generadas respetan el formato solicitado.

---

**Firma digital:** EDWINTUZYEH
