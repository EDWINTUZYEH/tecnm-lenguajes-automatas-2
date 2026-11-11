# Bitácora de Requerimientos y Auditoría IA — Sesión 11
**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Arquitectura de la Tabla de Símbolos  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [edwin armando tuz yeh]  
**Matrícula:** [24531358]  
**Track:** C 

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Tabla Hash con encadenamiento  
*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*
>  algunas de las dificultades  en este ejercicio:
> - Con -Werror, el esqueleto no compilaba si quedaban parámetros sin usar.
> - Al recorrer la cadena, necesité guardar el puntero al último nodo para enlazar el nuevo.
> - Olvidé el terminador '\0' al copiar el nombre en un arreglo de 16 bytes.
> - Dudé entre insertar al inicio o al final de la cadena.
> Conserva solo las que sean ciertas en tu caso.]

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C11 / GCC con `-Wall -Wextra -Werror`, sin bibliotecas no estándar. Tabla de símbolos con encadenamiento según `api_sesion11.h` |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores |
| **Especificación (E)** | Función de dispersión djb2 y manejo de colisiones por cadena, O(1) promedio |
| **Output (O)** | Solo código modular y análisis de complejidad |

### 2.2 Prompt Estructurado
```text
Contexto: Estoy implementando la tabla de símbolos de un compilador en C11.
Se compila con gcc -std=c11 -Wall -Wextra -Werror y la interfaz está fijada
en api_sesion11.h (struct Simbolo con nombre[16], tipo, offset y sig).

Rol: Actúa como ingeniero de software de sistemas y compiladores.

Especificación: Implementa exactamente estas firmas, sin modificarlas:
  unsigned int hash_djb2(const char *clave);
  int insertar_simbolo(Simbolo *tabla[], unsigned int cubetas,
                       const char *nombre, int tipo, int offset);
- hash_djb2 inicia en 5381 y por cada byte hace hash = hash * 33 + c.
  hash_djb2("") = 5381 y hash_djb2("abc") = 193485963.
- insertar_simbolo calcula el índice como hash % cubetas.
- Devuelve 1 si insertó, 0 si el nombre ya existe en esa cadena,
  -1 si tabla es NULL, nombre es NULL o cubetas es 0.
- Una colisión se encadena; nunca se sobrescribe una entrada existente.
- No incluyas main().

Output: Solo el archivo .c completo, más un breve análisis de complejidad
(caso promedio y peor caso).
```

---

## 3. Código Devuelto por el Modelo
```c
#include "api_sesion11.h"
#include <stdlib.h>
#include <string.h>

unsigned int hash_djb2(const char *clave) {
    unsigned int h = 5381u;
    if (clave == NULL) {
        return h;
    }
    for (const unsigned char *c = (const unsigned char *)clave; *c != '\0'; c++) {
        h = h * 33u + *c;
    }
    return h;
}

int insertar_simbolo(Simbolo *tabla[], unsigned int cubetas, const char *nombre, int tipo, int offset) {
    if (tabla == NULL || nombre == NULL || cubetas == 0u) {
        return -1;
    }

    unsigned int i = hash_djb2(nombre) % cubetas;

    for (Simbolo *p = tabla[i]; p != NULL; p = p->sig) {
        if (strncmp(p->nombre, nombre, sizeof(p->nombre) - 1) == 0) {
            return 0;
        }
    }

    Simbolo *nuevo = malloc(sizeof(Simbolo));
    if (nuevo == NULL) {
        return -1;
    }
    strncpy(nuevo->nombre, nombre, sizeof(nuevo->nombre) - 1);
    nuevo->nombre[sizeof(nuevo->nombre) - 1] = '\0';
    nuevo->tipo = tipo;
    nuevo->offset = offset;
    nuevo->sig = tabla[i];
    tabla[i] = nuevo;
    return 1;
}
```

Análisis de complejidad: inserción O(1) en promedio (factor de carga acotado) y O(n) en el peor caso, cuando todas las claves caen en una cubeta.

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)
*Pruebas ejecutadas:* Manejo de claves duplicadas y colisiones

### Salida del harness
```text

=== AUDITORIA SESION 11 - Tabla hash con encadenamiento ===
[ 1] hash_djb2("")                      esperado: 5381         obtenido: 5381         OK
[ 2] hash_djb2("abc")                   esperado: 193485963    obtenido: 193485963    OK
[ 3] insertar x dos veces               esperado: 0            obtenido: 0            OK
[ 4] dos claves, una cubeta             esperado: 2            obtenido: 2            OK
[ 5] offset de beta en cadena           esperado: 4            obtenido: 4            OK
[ 6] insertar en tabla NULL             esperado: -1           obtenido: -1           OK

RESULTADO: 6/6 pruebas superadas
```

* [x] Caso base y límites superados sin *Crash*.
* [ ] No existen accesos fuera de límites ni *Memory Leaks*. *
* [x] La complejidad teórica coincide con la implementada (O(1) promedio, O(n) peor caso).

### Reporte Crítico
*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*
> La IA no consideró que `nombre[16]` solo guarda 15 caracteres.
>  El hash se calcula con el nombre completo, pero el nodo guarda una versión truncada.
> Dos identificadores largos que compartan los primeros 15 caracteres (por ejemplo `contador_global_1` y `contador_global_2`) producen hashes distintos y pueden caer en cubetas diferentes, así que ambos se insertarían como si fueran símbolos distintos aunque en la tabla se vean iguales.
>  Lo detecté al revisar que el tamaño del campo en la cabecera no coincide con la longitud arbitraria de la entrada. Solución propuesta: calcular el hash solo sobre los primeros 15 caracteres, o rechazar con -1 los nombres de más de 15 caracteres.
>
> Además, el contrato no incluye una función para liberar la tabla, por lo que los nodos creados con `malloc` nunca se liberan. El harness no lo detecta, pero `valgrind` lo reportaría como memoria no liberada.

---
**Firma digital:** [EDWINTUZYEH]
