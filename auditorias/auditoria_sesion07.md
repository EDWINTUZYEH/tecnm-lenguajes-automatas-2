# Bitácora de Requerimientos y Auditoría IA — Sesión 07
**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Evaluación de Expresiones Aritméticas  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Edwin armando tuz yeh]  
**Matrícula:** [24531358]  
**Track:** [ C]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Evaluador recursivo de operaciones  
*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*

Al escribir el evaluador a mano me encontré con dos puntos delicados:
1. Hay que verificar que el divisor no sea cero **antes** de ejecutar la división o el módulo, de lo contrario el programa se cae.
2. Cuando un hijo regresa error, no se debe seguir evaluando el nodo padre; el error tiene que propagarse hacia arriba de inmediato.
También tuve que tener cuidado de que `evaluar(NULL, &error)` no provocara un segmentation fault.
> 

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C99 / GCC o Rust 2021 sin bibliotecas no estándar |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores |
| **Especificación (E)** | Manejo estricto de división entre cero |
| **Output (O)** | Solo código modular y análisis de complejidad |

### 2.2 Prompt Estructurado
```text
[Contexto: Estoy implementando un evaluador recursivo de árboles AST para expresiones aritméticas en C (curso Lenguajes y Autómatas II).

Rol: Actúa como programador experto en C y compiladores.

Especificación:
Implementa la función:
    int evaluar(ASTNode *n, int *error);

Comportamiento obligatorio:
- Si n == NULL → *error = 2 y regresa 0 (no debe caerse).
- Si el nodo es NODO_NUM → regresa n->valor y *error = 0.
- Si el nodo es NODO_BINOP:
  - Evalúa primero el hijo izquierdo. Si tiene error, propaga el error y NO evalúa el derecho ni el operador.
  - Evalúa el hijo derecho. Si tiene error, propaga el error.
  - Para + - * realiza la operación normalmente.
  - Para / y %: verifica que el divisor no sea 0 ANTES de operar. Si es 0 → *error = 1.
  - Operador desconocido → *error = 2.
- Nunca se debe ejecutar una división o módulo cuando el divisor es cero.
- El error se propaga hacia arriba sin recalcular nodos padres.

Output: Solo el código de la función evaluar (sin main), listo para compilar con el harness.]
```

---

## 3. Código Devuelto por el Modelo
```c
// Código devuelto por el LLM
%%writefile ia_sesion07_c.c
/* ia_sesion07_c.c - Fase 2: El Cientifico
 *
 * Pega aqui el codigo que te devolvio la IA, con la MISMA firma
 * que declara api_sesion07.h. No puede traer main().
 */
#include "api_sesion07.h"

/* TODO: pega aqui la propuesta de la IA */

/* ia_sesion07_c.c - Fase 2: El Científico
 * Código generado a partir del contrato C-R-E-O
 */
#include "api_sesion07.h"
#include <stddef.h>

int evaluar(ASTNode *n, int *error) {
    if (n == NULL) {
        if (error) *error = 2;
        return 0;
    }

    if (n->tipo == NODO_NUM) {
        if (error) *error = 0;
        return n->valor;
    }

    if (n->tipo != NODO_BINOP) {
        if (error) *error = 2;
        return 0;
    }

    int err_izq = 0;
    int val_izq = evaluar(n->izq, &err_izq);
    if (err_izq != 0) {
        if (error) *error = err_izq;
        return 0;
    }

    int err_der = 0;
    int val_der = evaluar(n->der, &err_der);
    if (err_der != 0) {
        if (error) *error = err_der;
        return 0;
    }

    switch (n->op) {
        case '+':
            if (error) *error = 0;
            return val_izq + val_der;
        case '-':
            if (error) *error = 0;
            return val_izq - val_der;
        case '*':
            if (error) *error = 0;
            return val_izq * val_der;
        case '/':
            if (val_der == 0) {
                if (error) *error = 1;
                return 0;
            }
            if (error) *error = 0;
            return val_izq / val_der;
        case '%':
            if (val_der == 0) {
                if (error) *error = 1;
                return 0;
            }
            if (error) *error = 0;
            return val_izq % val_der;
        default:
            if (error) *error = 2;
            return 0;
    }
}

```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)
*Pruebas ejecutadas:* Expresiones complejas y división por 0

=== AUDITORIA SESION 07 - Evaluador recursivo con deteccion de errores ===
Caso                               esperado:              obtenido:              resultado
[ 1] (2+3)*4                            esperado: 20           obtenido: 20           OK
[ 2] 7/0 -> error 1                     esperado: 1            obtenido: 1            OK
[ 3] 7%0 -> error 1                     esperado: 1            obtenido: 1            OK
[ 4] arbol NULL -> error 2              esperado: 2            obtenido: 2            OK
[ 5] 10-2-3                             esperado: 5            obtenido: 5            OK
[ 6] (8/2)+1                            esperado: 5            obtenido: 5            OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion07.md

* [ *] Caso base y límites superados sin *Crash*.
* [ *] No existen accesos fuera de límites ni *Memory Leaks*.
* [ *] La complejidad teórica coincide con la implementada.

### Reporte Crítico
*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*
La IA en la primera generación no verificaba si el puntero error era NULL antes de escribir
en él (aunque el harness siempre pasa un puntero válido). También usaba variables con nombres muy largos y un estilo demasiado “perfecto”.
Lo solucioné simplificando la versión artesano (usando if en lugar de switch y escribiendo directamente *error) para que se notara la diferencia 
entre el código hecho a mano y el generado por la IA. Ambas versiones terminaron pasando las 6 pruebas del harness.
>

---
**Firma digital:** [EDWINTUZYEH]
