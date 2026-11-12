
# Bitácora de Requerimientos y Auditoría IA — Sesión 15
**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Bloques Anidados y Ciclo de Vida  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Edwin Armando Tuz Yeh  
**Matrícula:** 24531358  
**Track:** C   

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Operaciones Push y Pop de ámbito  

*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*

> Al realizar el ejercicio tuve que comprender cómo funcionan los punteros y la memoria dinámica en C. 
La principal dificultad fue reservar espacio para crear un nuevo ámbito y enlazarlo correctamente con el ámbito anterior.
También tuve que considerar que no se deben utilizar punteros NULL y que 
el ámbito raíz no debe liberarse, porque representa el entorno global del programa.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal

| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Lenguaje C, estándar C11, utilizando GCC, estructuras, punteros y memoria dinámica. |
| **Rol (R)** | Ingeniero de software especializado en sistemas y desarrollo de compiladores. |
| **Especificación (E)** | Implementar las funciones push_ambito() y pop_ambito(). La función push debe reservar memoria para un nuevo ámbito, guardar su nombre y enlazarlo con el ámbito actual. La función pop debe liberar únicamente el ámbito actual y devolver el puntero de su padre. Se deben validar los punteros NULL y proteger el ámbito raíz. |
| **Output (O)** | Código modular en C, compatible con api_sesion15.h, sin función main(), con manejo correcto de memoria dinámica y explicación de su funcionamiento y complejidad. |

### 2.2 Prompt Estructurado

```text
CONTEXTO:
Estoy desarrollando una práctica de Lenguajes y Autómatas II
en lenguaje C. Necesito implementar un sistema de ámbitos
anidados para representar los bloques de un programa.

ROL:
Actúa como un ingeniero de software especializado en lenguaje C,
administración de memoria y desarrollo de compiladores.

ESPECIFICACIÓN:
Implementa las funciones push_ambito() y pop_ambito()
respetando exactamente las siguientes firmas:

Ambito *push_ambito(Ambito *actual, const char *nombre);
Ambito *pop_ambito(Ambito *actual);

La estructura Ambito está definida de la siguiente manera:

typedef struct Ambito {
    const char *nombre;
    struct Ambito *padre;
} Ambito;

Requisitos:
1. push_ambito() debe comprobar que actual no sea NULL.
2. También debe comprobar que nombre no sea NULL.
3. Debe reservar memoria utilizando malloc().
4. Debe guardar el nombre recibido.
5. Debe enlazar el nuevo ámbito con el ámbito actual.
6. Debe devolver el nuevo ámbito creado.
7. pop_ambito() debe devolver el padre del ámbito actual.
8. Debe liberar únicamente el ámbito que recibe.
9. No debe liberar el ámbito raíz.
10. Debe manejar correctamente los casos de memoria insuficiente.
11. El código no debe contener main().
12. Debe compilar utilizando -Wall -Wextra -Werror.

OUTPUT:
Entrega el código modular en C, respetando la interfaz
api_sesion15.h. Incluye una explicación breve de su
funcionamiento y complejidad algorítmica.
```

---

## 3. Código Devuelto por el Modelo

```c
#include "api_sesion15.h"
#include <stdlib.h>

Ambito *push_ambito(Ambito *actual, const char *nombre) {
    if (actual == NULL || nombre == NULL) {
        return NULL;
    }

    Ambito *nuevo = malloc(sizeof(Ambito));

    if (nuevo == NULL) {
        return NULL;
    }

    nuevo->nombre = nombre;
    nuevo->padre = actual;

    return nuevo;
}

Ambito *pop_ambito(Ambito *actual) {
    if (actual == NULL || actual->padre == NULL) {
        return NULL;
    }

    Ambito *padre = actual->padre;
    free(actual);

    return padre;
}
```

### Explicación del funcionamiento

- **push_ambito():** Comprueba que los argumentos sean válidos, reserva memoria para un nuevo ámbito y guarda el nombre y el enlace hacia su padre.
- **pop_ambito():** Comprueba que el ámbito actual no sea NULL ni la raíz. Después guarda el puntero al padre, libera el ámbito actual y devuelve el padre.
- **malloc():** Reserva memoria dinámica para crear un ámbito.
- **free():** Libera la memoria del ámbito que deja de utilizarse.
- **Complejidad:** Ambas operaciones tienen complejidad temporal O(1), porque realizan una cantidad constante de operaciones.

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)

*Pruebas ejecutadas:* Comprobación de nombres, profundidad de ámbitos, devolución del padre y protección del ámbito raíz.

### Salida del harness

```text
=== AUDITORIA SESION 15 - Push y pop de ambitos ===
Caso                               esperado:              obtenido:              resultado
[ 1] nombre del ambito nuevo       esperado: if           obtenido: if           OK
[ 2] profundidad con dos push      esperado: 3            obtenido: 3            OK
[ 3] pop devuelve el padre         esperado: 1            obtenido: 1            OK
[ 4] pop sobre la raiz             esperado: 1            obtenido: 1            OK
[ 5] push con padre NULL           esperado: 1            obtenido: 1            OK
[ 6] profundidad tras pop          esperado: 2            obtenido: 2            OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion15.md
```

### Lista de comprobación

- [x] Caso base y límites contemplados sin provocar un Crash.
- [x] Se comprueba que los punteros recibidos no sean NULL cuando corresponde.
- [x] Se libera únicamente el ámbito actual y se conserva el padre.
- [x] Se protege el ámbito raíz para evitar liberar memoria que no pertenece a la función.
- [x] La complejidad teórica coincide con la implementación.

### Reporte Crítico

*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*

> Al revisar el código generado por la IA, identifiqué que la función push_ambito() conserva directamente el puntero del nombre recibido, en
lugar de realizar una copia de la cadena. 
Esto significa que el nombre debe seguir existiendo mientras se utilice el ámbito.
>
> También observé que es necesario comprobar el caso en el que el ámbito actual sea la raíz, porque no debe liberarse su memoria.
La función pop_ambito() resuelve esta situación comprobando si el campo padre es NULL antes de ejecutar free().
>
> Para esta práctica se conserva el comportamiento establecido en api_sesion15.h y se utilizan nombres que permanecen disponibles durante las pruebas. 
Como mejora futura, se podría implementar una copia dinámica del nombre y liberarla al cerrar el ámbito.

---

**Firma digital:** [EDWINTUZYEH]
