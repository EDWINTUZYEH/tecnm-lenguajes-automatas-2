# Bitácora de Requerimientos y Auditoría IA — Sesión 04
**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Anatomía de un Árbol Sintáctico (AST)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [edwin armnado tuz yeh ]  
**Matrícula:** [24531358]  
**Track:** [ C]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Estructura de nodo binario (ASTNode)  
*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*
Al programar a mano, identifiqué que debía reservar memoria para cada nodo utilizando malloc() y comprobar que la reserva fuera correcta. También tuve que cuidar que los nodos numéricos no tuvieran hijos y que los nodos de operación guardaran correctamente el operador y sus hijos izquierdo y derecho. Otro detalle importante fue evaluar los nodos de forma recursiva y comprobar que un árbol vacío no provocara un error.
> 

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C99 / GCC o Rust 2021 sin bibliotecas no estándar |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores |
| **Especificación (E)** | Gramática E -> E + T | T con tipos de nodo |
| **Output (O)** | Solo código modular y análisis de complejidad |

### 2.2 Prompt Estructurado
```text
[Actúa como un ingeniero de software especializado en compiladores
y estructuras de datos. Implementa un árbol sintáctico abstracto
(AST) en lenguaje C11.

Respeta las funciones declaradas en api_sesion04.h:

ASTNode *crear_numero(int v);
ASTNode *crear_binario(char op, ASTNode *izq, ASTNode *der);
int evaluar(ASTNode *n);

Requisitos:
1. crear_numero debe reservar memoria y guardar el valor recibido.
2. crear_binario debe reservar memoria y enlazar correctamente
   el operador y los hijos izquierdo y derecho.
3. evaluar debe devolver el valor de un nodo numérico.
4. Debe evaluar recursivamente las operaciones +, - y *.
5. Si recibe NULL, debe devolver -1 sin provocar una falla
   de segmentación.
6. Comprobar que malloc no devuelva NULL antes de utilizar
   la memoria reservada.
7. No cambiar las firmas ni incluir main().
8. Utilizar bibliotecas estándar de C.
9. El código debe compilar con:
   gcc -std=c11 -Wall -Wextra -Werror

Entrega el código modular y explica su complejidad temporal
y espacial.]
```

---

## 3. Código Devuelto por el Modelo
```c
// Código devuelto por el LLM
#include "api_sesion04.h"
#include <stdlib.h>

ASTNode *crear_numero(int v) {
    ASTNode *n = malloc(sizeof(ASTNode));

    if (n == NULL) {
        return NULL;
    }

    n->tipo = NODO_NUM;
    n->valor = v;
    n->op = '\0';
    n->izq = NULL;
    n->der = NULL;

    return n;
}

ASTNode *crear_binario(char op, ASTNode *izq, ASTNode *der) {
    ASTNode *n = malloc(sizeof(ASTNode));

    if (n == NULL) {
        return NULL;
    }

    n->tipo = NODO_BINOP;
    n->valor = 0;
    n->op = op;
    n->izq = izq;
    n->der = der;

    return n;
}

int evaluar(ASTNode *n) {
    int izquierdo;
    int derecho;

    if (n == NULL) {
        return -1;
    }

    if (n->tipo == NODO_NUM) {
        return n->valor;
    }

    if (n->tipo != NODO_BINOP) {
        return -1;
    }

    if (n->izq == NULL || n->der == NULL) {
        return -1;
    }

    izquierdo = evaluar(n->izq);
    derecho = evaluar(n->der);

    switch (n->op) {
        case '+':
            return izquierdo + derecho;
        case '-':
            return izquierdo - derecho;
        case '*':
            return izquierdo * derecho;
        default:
            return -1;
    }
}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)
*Pruebas ejecutadas:* Árbol vacío y evaluación de nodo raíz

* [ *] Caso base y límites superados sin *Crash*.
* [* ] No existen accesos fuera de límites ni *Memory Leaks*.
* [ *] La complejidad teórica coincide con la implementada.

### Reporte Crítico
*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*
> 

---
**Firma digital:** [EDWINTUZYE]
