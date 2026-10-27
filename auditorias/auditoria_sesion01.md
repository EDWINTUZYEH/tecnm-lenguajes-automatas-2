# Bitácora de Requerimientos y Auditoría IA — Sesión 01
**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Encuadre, Diagnóstico de Punteros y Metodología IA  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
<<<<<<< EDWINTUZYEH-patch-1
**Estudiante:** [EDWIN ARMANDO TUZ YEH]  
**Matrícula:** [24531358]  
**Track:** [ C ]  
=======  
>>>>>>> main

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Inversión de buffer in-place (char*)  
*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*
> Lo más importante era hacerlo sin reservar memoria nueva, así que solo podía
> usar dos índices y un `char` temporal. Lo que tuve que cuidar fue:
> - Revisar que la cadena no fuera `NULL`, porque si la recorría directamente
>   el programa se caía.
> - Qué pasaba con la cadena vacía: como la longitud se guarda en `size_t`,
>   restarle 1 cuando vale 0 da un número enorme, así que debía revisarlo antes.
> - Dónde terminaba la cadena: el último carácter real está antes del `'\0'`,
>   y no debía intercambiarlo.
> - Cuándo detener el ciclo: cuando los dos índices se encuentran o se cruzan,
>   para no volver a invertir lo que ya estaba invertido.
> 

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C99 / GCC o Rust 2021 sin bibliotecas no estándar |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores |
| **Especificación (E)** | Punteros, O(n) tiempo, O(1) memoria |
| **Output (O)** | Solo código modular y análisis de complejidad |

### 2.2 Prompt Estructurado
```texto
Necesito entender cómo se recorre un buffer en memoria con punteros o
índices sin salirme de él. El código se compila con
gcc -std=c11 -Wall -Wextra -Werror y se prueba con un harness que ya
incluye api_sesion01.h, cuya única declaración es: void invertir(char *s);

ROL:
Actúa como programador de sistemas en C, experto en manejo seguro de
memoria, que escribe código sin asignación dinámica.

ESPECIFICACIÓN:
- Implementa void invertir(char *s) con la firma EXACTA indicada.
- Invierte la cadena in-place: sin malloc, sin arreglos auxiliares,
  solo dos índices (o punteros) y un char temporal.
- No devuelvas una copia: la misma dirección debe quedar invertida.
- invertir(NULL) debe terminar sin fallo.
- Debe funcionar con cadena vacía, de 1 carácter, de 2 y de longitud impar.
- No incluyas main().
- No debe generar advertencias con -Wall -Wextra -Werror.

OUTPUT:
Entrega solo el contenido de ia_sesion01_c.c en un único bloque de código
C, con #include "api_sesion01.h", y sin explicaciones fuera del código.
```

---

## 3. Código Devuelto por el Modelo
```c
// Código devuelto por el LLM
#include "api_sesion01.h"
#include <stddef.h>

void invertir(char *s) {
    if (s == NULL) return;

    char *fin = s;
    while (*fin != '\0') fin++;      /* fin apunta al '\0' */
    if (fin == s) return;            /* cadena vacia */
    fin--;                           /* ultimo caracter real */

    while (s < fin) {
        char tmp = *s;
        *s = *fin;
        *fin = tmp;
        s++;
        fin--;
    }
}
```

---


## 4. Fase 3: El Auditor (Resultados del Test Harness)
*Pruebas ejecutadas:* Valores NULL, buffers vacios y longitudes impares

### Salida del harness
```text
=== AUDITORIA SESION 01 - Inversion de buffer in-place ===
Caso                               esperado:              obtenido:              resultado
[ 1] invertir("HOLA")                   esperado: ALOH         obtenido: ALOH         OK
[ 2] invertir("abc")                    esperado: cba          obtenido: cba          OK
[ 3] invertir("")                       esperado:              obtenido:              OK
[ 4] invertir("AB")                     esperado: BA           obtenido: BA           OK
[ 5] invertir("a")                      esperado: a            obtenido: a            OK
[ 6] invertir(NULL)                     esperado: sin crash    obtenido: sin crash    OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion01.md
```

* [x] Caso base y límites superados sin *Crash*.
* [x] No existen accesos fuera de límites ni *Memory Leaks*.
* [x] La complejidad teórica coincide con la implementada.

### Reporte Crítico
*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*
> La IA no omitió ningún caso borde: pasó los 6 casos del harness. Su problema
> fue que incluyó código de más que no era necesario para la función. Lo
> solucioné revisando el código línea por línea y eliminando lo innecesario
> hasta dejar solo lo que pide el contrato.

---
**Firma digital:** [EDWINTUZYEH]
