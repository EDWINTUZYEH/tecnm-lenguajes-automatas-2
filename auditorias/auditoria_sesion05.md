# Bitácora de Requerimientos y Auditoría IA — Sesión 05
**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Recorridos del AST y Notación Polaca  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [edwin armando tuz yeh ]  
**Matrícula:** [24531358]  
**Track:** [ C ] 

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Impresión en Postorden / RPN  
*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*
El principal reto fue escribir en un buffer de capacidad fija sin usar printf. Cada token (número u operador) debe agregarse verificando que longitud actual + separador + longitud del token no supere cap - 1, para dejar siempre espacio al terminador '\0'. Si no cabe, el recorrido se detiene para no producir una cadena en desorden ni desbordar el buffer.

Otro detalle fue el separador: el espacio solo se agrega cuando el buffer ya tiene contenido, así la cadena no empieza con espacio ni termina con uno. También hubo que inicializar buf[0] = '\0' desde el principio para que un árbol NULL produzca cadena vacía.

Por último, los números se convierten con snprintf sobre un arreglo temporal (tok[16]) y los operadores se copian directo desde n->op. Con -Wall -Wextra -Werror hubo que evitar variables sin usar y comparaciones entre int y size_t con signo distinto, por eso se castea cap a size_t.
> 

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C99 / GCC o Rust 2021 sin bibliotecas no estándar |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores |
| **Especificación (E)** | Invariantes de recorrido recursivo |
| **Output (O)** | Solo código modular y análisis de complejidad |

### 2.2 Prompt Estructurado
```text
[Curso de Lenguajes y Autómatas II. Tengo un AST en C con la estructura
  typedef enum { NODO_NUM, NODO_BINOP } TipoNodo;
  typedef struct ASTNode { TipoNodo tipo; int valor; char op;
                           struct ASTNode *izq; struct ASTNode *der; } ASTNode;
declarada en "api_sesion05.h". Compilo con
  gcc -std=c11 -Wall -Wextra -Werror
y no puedo usar bibliotecas no estándar.

ROL:
Actúa como ingeniero de software de sistemas y compiladores, experto en C
seguro (manejo de buffers y recursión).

ESPECIFICACIÓN:
Implementa exactamente esta firma:
  void postorden(ASTNode *n, char *buf, int cap);
Debe escribir en buf la notación polaca inversa (RPN) del árbol, recorriéndolo
en orden izquierdo, derecho, raíz. Requisitos e invariantes:
 1. Tokens separados por un solo espacio, sin espacio inicial ni final.
 2. NODO_NUM se escribe como entero decimal; NODO_BINOP se escribe como su
    carácter op.
 3. No uses printf ni escribas a stdout: solo escribe en buf.
 4. Nunca escribas más de cap-1 caracteres más el terminador '\0'.
 5. Un árbol NULL produce cadena vacía; buf siempre termina en '\0'.
 6. Maneja buf == NULL o cap <= 0 sin fallar.
 7. Sin variables globales y sin main().
 8. Si un token ya no cabe, detén el recorrido sin dejar la cadena corrupta.

OUTPUT:
Solo el código C del archivo, con #include "api_sesion05.h", modular
(función auxiliar static recursiva), con la firma idéntica y al final una
línea con la complejidad temporal y espacial. Sin explicaciones adicionales.]
```

---

## 3. Código Devuelto por el Modelo
```c
// Código devuelto por el LLM
#include "api_sesion05.h"
#include <stdio.h>
#include <string.h>

static void emitir(ASTNode *n, char *buf, int cap, int *pos, int *ok) {
    char tok[16];
    int len, sep;

    if (n == NULL || !*ok) return;

    emitir(n->izq, buf, cap, pos, ok);
    emitir(n->der, buf, cap, pos, ok);
    if (!*ok) return;

    if (n->tipo == NODO_NUM) {
        len = snprintf(tok, sizeof tok, "%d", n->valor);
    } else {
        tok[0] = n->op;
        tok[1] = '\0';
        len = 1;
    }

    sep = (*pos > 0) ? 1 : 0;
    if (*pos + sep + len > cap - 1) {   /* no cabe: se detiene el recorrido */
        *ok = 0;
        return;
    }
    if (sep) buf[(*pos)++] = ' ';
    memcpy(buf + *pos, tok, (size_t)len);
    *pos += len;
    buf[*pos] = '\0';
}

void postorden(ASTNode *n, char *buf, int cap) {
    int pos = 0;
    int ok = 1;

    if (buf == NULL || cap <= 0) return;
    buf[0] = '\0';
    emitir(n, buf, cap, &pos, &ok);
}

/* Complejidad: tiempo O(n) (cada nodo se visita una vez);
 * espacio O(h) por la pila de recursion, con h = altura del arbol. */
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)
*Pruebas ejecutadas:* Validación contra desbordamiento de pila
=== AUDITORIA SESION 05 - Recorrido postorden y RPN ===
Caso                               esperado:              obtenido:              resultado
[ 1] hoja 42                            esperado: 42           obtenido: 42           OK
[ 2] 3+(5*2)                            esperado: 3 5 2 * +    obtenido: 3 5 2 * +    OK
[ 3] arbol NULL                         esperado:              obtenido:              OK
[ 4] (1+2)*(3+4)
     esperado: 1 2 + 3 4 + *
     obtenido: 1 2 + 3 4 + *
     -> OK
[ 5] 8-3                                esperado: 8 3 -        obtenido: 8 3 -        OK

RESULTADO: 5/5 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion05.md

* [* ] Caso base y límites superados sin *Crash*.
* [ *] No existen accesos fuera de límites ni *Memory Leaks*.
* [* ] La complejidad teórica coincide con la implementada.

### Reporte Crítico
*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*
La IA resolvió los 5 casos del harness, pero omitió el control de capacidad del buffer (cap): es común que use strcat o sprintf sin comprobar cap-1, lo que desborda la memoria con buffers pequeños. También suele dejar espacios sobrantes al inicio o al final y no manejar buf == NULL o cap <= 0.

El harness oficial no lo detecta porque usa buffers amplios (16 a 64 bytes). Lo detecté con una prueba manual: llamé a postorden con char b[4] sobre 3+(5*2) (su RPN necesita 10 bytes) y compilé con -fsanitize=address,undefined.

La solución fue exigir en el prompt la invariante “nunca más de cap-1 caracteres” y verificar pos + sep + len > cap - 1 antes de cada escritura. Si el token no cabe, el recorrido se detiene (ok = 0) y la cadena queda válida y terminada en '\0'. El espacio separador solo se inserta cuando pos > 0, lo que evita espacios al inicio o al final.
> 

---
**Firma digital:** [EDWINTUZYEH]
