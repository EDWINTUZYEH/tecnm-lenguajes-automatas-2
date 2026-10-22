# Bitácora de Requerimientos y Auditoría IA — Sesión 01
**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Encuadre, Diagnóstico de Punteros y Metodología IA  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
<<<<<<< EDWINTUZYEH-patch-1
**Estudiante:** [EDWIN ARMANDO TUZ YEH ]  
**Matrícula:** [24531358]  
**Track:** [ C ]  
=======
**Estudiante:** [Nombre Completo]  
**Matrícula:** [No. de Control]  
**Track:** C (el harness evalúa C; la versión en Rust es opcional y no se califica con este harness)  
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

<<<<<<< EDWINTUZYEH-patch-1
* [*] Caso base y límites superados sin *Crash*.
* [*] No existen accesos fuera de límites ni *Memory Leaks*.
* [*] La complejidad teórica coincide con la implementada.
=======
### Salida del harness
```text
Pega aquí la salida de la celda del harness. Debe terminar con:
RESULTADO: n/n pruebas superadas
```

* [ ] Caso base y límites superados sin *Crash*.
* [ ] No existen accesos fuera de límites ni *Memory Leaks*.
* [ ] La complejidad teórica coincide con la implementada.
>>>>>>> main

### Reporte Crítico
*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*

Que en cierta forma ponia codigos demas y que no era muy funcional y la solucion fue ir revisando y eliminar lo inecesario.
> 

---
**Firma digital:** [EDWINTUZYEH]
