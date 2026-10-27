# Bitácora de Requerimientos y Auditoría IA — Sesión 02
**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Gestión en GitHub Web y Nodos Dinámicos  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [edwin armndo tuz yeh]  
**Matrícula:** [24531358]  
**Track:** [C]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Lista enlazada de tokens en Heap  
*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*
Lo más difícil fue manejar la memoria dinámica sin perder referencias. Identifiqué tres restricciones:

Paso por doble puntero: agregar_token recibe NodoToken **cabeza porque, si la lista está vacía, la función debe modificar la cabeza que vive en quien la llama. Con un puntero simple, el cambio se perdería.
Use-after-free al liberar: si se hace free(actual) y luego actual = actual->siguiente, se lee memoria ya liberada. Hay que guardar siguiente en una variable temporal antes del free.
Cadenas en char lexema[16]: strncpy no garantiza el '\0' cuando el texto llena el buffer, así que forcé el terminador en la última posición.

También debí manejar NULL en contar_tokens y liberar_lista, y el caso malloc devuelve NULL.
> 

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C99 / GCC o Rust 2021 sin bibliotecas no estándar |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores |
| **Especificación (E)** | Gestión de memoria dinámica C99/Rust |
| **Output (O)** | Solo código modular y análisis de complejidad |

### 2.2 Prompt Estructurado
```text
Necesito una lista enlazada de tokens
en el heap, con esta estructura: typedef struct NodoToken { char lexema[16];
struct NodoToken *siguiente; } NodoToken;. Se compila con gcc -Wall -Wextra
-Werror, sin bibliotecas no estándar.

Rol: Actúa como ingeniero de software de sistemas y compiladores, en
manejo seguro de memoria dinámica en C.

Especificación: Implementa exactamente estas firmas:
NodoToken *crear_nodo(const char *lexema);
void agregar_token(NodoToken **cabeza, const char *lexema);
int contar_tokens(NodoToken *cabeza);
void liberar_lista(NodoToken *cabeza);
Cada nodo se reserva con malloc, sin arreglos globales. El siguiente del
último nodo debe ser NULL. contar_tokens(NULL) devuelve 0 y liberar_lista(NULL)
no debe fallar. Al liberar, guarda el siguiente antes de hacer free, para
evitar use-after-free. No incluyas main().

Output: Solo el código modular en un archivo .c, con #include "api_sesion02.h"
y un breve análisis de complejidad de cada función.
```

---

## 3. Código Devuelto por el Modelo
```c
/* artesano_sesion02_c.c - Fase 1: El Artesano (sin IA)
 * Lista enlazada de tokens en heap.
 */
#include "api_sesion02.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

NodoToken *crear_nodo(const char *lexema) {
    NodoToken *nodo = (NodoToken *)malloc(sizeof(NodoToken));
    if (nodo == NULL) {
        return NULL;
    }
    if (lexema == NULL) {
        nodo->lexema[0] = '\0';
    } else {
        strncpy(nodo->lexema, lexema, sizeof(nodo->lexema) - 1);
        nodo->lexema[sizeof(nodo->lexema) - 1] = '\0';
    }
    nodo->siguiente = NULL;
    return nodo;
}

void agregar_token(NodoToken **cabeza, const char *lexema) {
    if (cabeza == NULL) {
        return;
    }
    NodoToken *nuevo = crear_nodo(lexema);
    if (nuevo == NULL) {
        return;
    }
    if (*cabeza == NULL) {
        *cabeza = nuevo;
        return;
    }
    NodoToken *actual = *cabeza;
    while (actual->siguiente != NULL) {
        actual = actual->siguiente;
    }
    actual->siguiente = nuevo;
}

int contar_tokens(NodoToken *cabeza) {
    int cuenta = 0;
    NodoToken *actual = cabeza;
    while (actual != NULL) {
        cuenta++;
        actual = actual->siguiente;
    }
    return cuenta;
}

void liberar_lista(NodoToken *cabeza) {
    NodoToken *actual = cabeza;
    while (actual != NULL) {
        NodoToken *siguiente = actual->siguiente; /* guardar antes de free */
        free(actual);
        actual = siguiente;
    }
}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)
*Pruebas ejecutadas:* Prevención de Use-After-Free y cadenas nulas
[ 1] crear_nodo("if")->lexema           esperado: if           obtenido: if           OK
[ 2] contar_tokens(3 tokens)            esperado: 3            obtenido: 3            OK
[ 3] orden: segundo token               esperado: dos          obtenido: dos          OK
[ 4] ultimo->siguiente == NULL          esperado: 1            obtenido: 1            OK
[ 5] contar_tokens(NULL)                esperado: 0            obtenido: 0            OK
[ 6] liberar_lista(NULL)                esperado: sin crash    obtenido: sin crash    OK

RESULTADO: 6/6 pruebas superadas

* [ *] Caso base y límites superados sin *Crash*.
* [ *] No existen accesos fuera de límites ni *Memory Leaks*.
* [ *] La complejidad teórica coincide con la implementada.

### Reporte Crítico
*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*
La IA pasó los 6 casos, pero tiene un problema: si el lexema tiene más de 15 caracteres, lo corta sin avisar. Lo probé con "identificador_muy_largo" y lo que se guardó fue identificador_m, o sea que el token queda distinto al original y nadie se entera. Tampoco avisa si malloc falla, porque agregar_token devuelve void. No cambié las firmas porque son parte del contrato; lo dejé anotado como limitación y como mejora (devolver un código de error o usar un buffer más grande). Valgrind marcó fugas, pero eran del harness, que no libera sus listas; liberar_lista está bien.
> 

---
**Firma digital:** [EDWINTUZYEH]
