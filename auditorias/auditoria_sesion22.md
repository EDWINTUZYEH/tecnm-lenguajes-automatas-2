# Bitácora de Requerimientos y Auditoría IA — Sesión 22

**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Generación de TAC para Expresiones  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Edwin Armando Tuz Yeh  
**Matrícula:** 24531358  
**Track:** (C)
---

## 1. Fase 1: El Artesano (Dificultad Manual)

*Reto:* Traductor de nodos AST a TAC.

**Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:**

> La principal dificultad fue implementar el recorrido del árbol AST en postorden, porque primero se deben procesar los nodos hijos y después generar la instrucción del operador. También fue necesario controlar el uso de los temporales para evitar que se repitieran y respetar los límites del arreglo de salida. En C se debe tener cuidado con los punteros, los arreglos y el tamaño máximo de 64 caracteres por línea para evitar accesos fuera de memoria.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal

| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C99 / GCC o Rust 2021 sin bibliotecas no estándar. |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores. |
| **Especificación (E)** | Conservación de precedencia de operadores mediante recorrido postorden del AST. Generar un temporal nuevo por cada operador binario, respetando los límites del arreglo. |
| **Output (O)** | Código modular en C, compatible con la API proporcionada, sin función main y con análisis de complejidad. |

### 2.2 Prompt Estructurado

```text
CONTEXTO:
Estoy desarrollando un traductor de árboles de sintaxis abstracta
(AST) a código de tres direcciones (TAC) en C para la materia
Lenguajes y Autómatas II.

ROL:
Actúa como un ingeniero de software especializado en compiladores,
estructuras de datos, punteros y programación en C.

ESPECIFICACIÓN:
Implementa la función generar_tac respetando exactamente
la siguiente firma:

int generar_tac(const Nodo *raiz, char lineas[][64], int max);

La estructura Nodo contiene:
- char tipo;
- char op;
- char valor[16];
- struct Nodo *izq;
- struct Nodo *der;

Requisitos:
1. Recorrer el árbol AST en postorden.
2. Procesar primero el hijo izquierdo y después el derecho.
3. Generar una instrucción TAC por cada operador binario.
4. Utilizar temporales consecutivos: _t0, _t1, _t2...
5. Respetar la precedencia representada por el árbol.
6. Las hojas de tipo H deben devolver su valor sin generar instrucciones.
7. Los nodos binarios de tipo B deben generar una instrucción.
8. No escribir más de max instrucciones.
9. No superar los 63 caracteres por línea.
10. Controlar punteros nulos y evitar accesos fuera de límites.
11. No incluir main(), porque el harness proporciona esa función.
12. Mantener compatibilidad con api_sesion22.h.

OUTPUT:
Entrega código C modular, compatible con GCC y las opciones
-Wall -Wextra -Werror.
Explica brevemente la complejidad temporal y espacial.
No modifiques las firmas de las funciones.
```

---

## 3. Código Devuelto por el Modelo

El modelo proporcionó una implementación modular en C utilizando recursividad, una estructura Pool para administrar los temporales y una función auxiliar para recorrer el AST.

**Archivo:** `ia_sesion22_c.c`

```c
#include "api_sesion22.h"
#include <stdio.h>

typedef struct {
    char nombre[64][16];
    int usados;
} Pool;

static const char *nuevo_temporal(Pool *p, int *contador) {
    if (p->usados >= 64) {
        return "_t?";
    }

    snprintf(
        p->nombre[p->usados],
        sizeof p->nombre[0],
        "_t%d",
        (*contador)++
    );

    return p->nombre[p->usados++];
}

static const char *traducir(
    const Nodo *nodo,
    char lineas[][64],
    int max,
    int *cantidad,
    Pool *pool,
    int *contador
) {
    const char *izquierda;
    const char *derecha;
    const char *temporal;

    if (nodo == NULL) {
        return "";
    }

    if (nodo->tipo == 'H') {
        return nodo->valor;
    }

    if (nodo->tipo != 'B') {
        return "";
    }

    izquierda = traducir(
        nodo->izq, lineas, max, cantidad, pool, contador
    );

    derecha = traducir(
        nodo->der, lineas, max, cantidad, pool, contador
    );

    if (*cantidad >= max || pool->usados >= 64) {
        return "";
    }

    temporal = nuevo_temporal(pool, contador);

    snprintf(
        lineas[*cantidad],
        64,
        "%s = %s %c %s",
        temporal,
        izquierda,
        nodo->op,
        derecha
    );

    (*cantidad)++;

    return temporal;
}

int generar_tac(const Nodo *raiz, char lineas[][64], int max) {
    Pool pool = {{{0}}, 0};
    int cantidad = 0;
    int contador = 0;

    if (raiz == NULL || lineas == NULL || max <= 0) {
        return 0;
    }

    traducir(
        raiz,
        lineas,
        max,
        &cantidad,
        &pool,
        &contador
    );

    return cantidad;
}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)

**Pruebas evaluadas:** Expresiones aritméticas anidadas, precedencia, temporales y hojas sin operaciones.

### Salida esperada del harness

```text
=== AUDITORIA SESION 22 - Traductor de AST a TAC con precedencia ===
Caso                               esperado:              obtenido:              resultado
[ 1] a + b * c                      esperado: _t0 = b * c  obtenido: _t0 = b * c  OK
[ 2] a + b * c (2a linea)
     esperado: _t1 = a + _t0
     obtenido: _t1 = a + _t0
     -> OK
[ 3] (a + b) * c
     esperado: _t1 = _t0 * c
     obtenido: _t1 = _t0 * c
     -> OK
[ 4] x * (y - z) + w
     esperado: _t2 = _t1 + w
     obtenido: _t2 = _t1 + w
     -> OK
[ 5] hoja sin operaciones          esperado: 0            obtenido: 0            OK
[ 6] (a + b) * (c - d)
     esperado: _t2 = _t0 * _t1
     obtenido: _t2 = _t0 * _t1
     -> OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion22.md
```

**Nota:** Esta es la salida esperada según los seis casos del harness. Debe sustituirse por la salida real después de ejecutar la compilación y las pruebas.

### Lista de verificación

- [ ] Caso base y límites superados sin Crash.
- [ ] No existen accesos fuera de límites ni Memory Leaks.
- [x] La complejidad teórica coincide con la implementada.

### Análisis de complejidad

**Complejidad temporal: O(n)**

El algoritmo recorre cada nodo del árbol una sola vez. Por cada operador realiza operaciones constantes para generar la instrucción TAC.

**Complejidad espacial auxiliar: O(h)**

Se utiliza memoria para las llamadas recursivas, donde h representa la altura del árbol. Además, se utiliza una estructura Pool de tamaño fijo para almacenar los temporales.

---

### Reporte Crítico

*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*

> Al revisar la implementación identifiqué que no se validan completamente los nodos binarios que tienen hijos nulos o tipos de nodo incorrectos. Aunque la función controla algunos punteros nulos y los límites del arreglo, todavía puede generar una instrucción con operandos vacíos si recibe un árbol mal formado. Este caso no está contemplado en las seis pruebas originales del harness. La mejora consiste en validar que ambos hijos sean válidos antes de generar la instrucción TAC y evitar emitir operaciones incompletas. Esto permite que el traductor sea más robusto ante entradas incorrectas.

---

**Firma digital:** [EDWINTUZYEH]
