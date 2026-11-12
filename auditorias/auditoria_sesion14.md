# Bitácora de Requerimientos y Auditoría IA — Sesión 14
**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Declaración vs Uso de Variables  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Edwin Armando Tuz Yeh  
**Matrícula:** 24531358  
**Track:** C 

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Detección de variables no declaradas  
*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*
> La principal dificultad fue controlar los nombres almacenados en la tabla y evitar que se registraran dos veces. También tuve que considerar que el arreglo tiene una capacidad máxima de 16 elementos.
>  Para resolverlo utilicé un ciclo para recorrer los nombres registrados y strcmp() para comparar los nombres completos,
>  evitando confundir variables como "x" y "xy". Además, agregué validaciones para evitar trabajar con punteros nulos y nombres vacíos.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C99 / GCC o Rust 2021 sin bibliotecas no estándar |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores |
| **Especificación (E)** | Invariante de definición previa: implementar declarar() para insertar nombres nuevos sin duplicados y usar() para comprobar si un nombre ya fue declarado.
Validar punteros nulos, nombres vacíos y capacidad máxima de la tabla. |
| **Output (O)** | Solo código modular y análisis de complejidad |

### 2.2 Prompt Estructurado
```text
CONTEXTO:
Estoy desarrollando una tabla de símbolos para la materia
Lenguajes y Autómatas II utilizando C99 y GCC.

ROL:
Actúa como un ingeniero de software especializado en
programación de sistemas y desarrollo de compiladores.

ESPECIFICACIÓN:
Implementa las funciones declarar() y usar() respetando
exactamente las firmas del archivo api_sesion14.h.

La función declarar():
- Devuelve 1 si inserta un nombre nuevo.
- Devuelve 0 si el nombre ya estaba registrado.
- Devuelve -1 si recibe NULL, un nombre vacío o la tabla
  está llena.
- No debe permitir declaraciones duplicadas.
- Debe respetar TABLA_MAX.

La función usar():
- Devuelve 1 si el nombre ya fue declarado.
- Devuelve 0 si el nombre no existe o recibe datos inválidos.

Utiliza strcmp() para comparar nombres completos.
No modifiques la estructura Tabla.
No cambies las firmas de las funciones.
No agregues main().
Evita advertencias con -Wall -Wextra -Werror.

OUTPUT:
Entrega código C modular y una explicación breve
de la complejidad temporal y espacial.
```

---

## 3. Código Devuelto por el Modelo
```c
#include "api_sesion14.h"
#include <string.h>

int declarar(Tabla *tabla, const char *nombre) {

    if (tabla == NULL || nombre == NULL || nombre[0] == '\0') {
        return -1;
    }

    if (tabla->total < 0 || tabla->total > TABLA_MAX) {
        return -1;
    }

    for (int i = 0; i < tabla->total; i++) {
        if (strcmp(tabla->nombres[i], nombre) == 0) {
            return 0;
        }
    }

    if (tabla->total >= TABLA_MAX) {
        return -1;
    }

    tabla->nombres[tabla->total] = nombre;
    tabla->total++;

    return 1;
}

int usar(const Tabla *tabla, const char *nombre) {

    if (tabla == NULL || nombre == NULL || nombre[0] == '\0') {
        return 0;
    }

    if (tabla->total < 0 || tabla->total > TABLA_MAX) {
        return 0;
    }

    for (int i = 0; i < tabla->total; i++) {
        if (strcmp(tabla->nombres[i], nombre) == 0) {
            return 1;
        }
    }

    return 0;
}
```

**Análisis de complejidad:**
- Tiempo: O(n), porque se recorre la tabla para buscar un nombre.
- Espacio auxiliar: O(1), porque no se crean estructuras adicionales.
- Almacenamiento: O(1) por inserción, porque se guarda un puntero en el arreglo existente.

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)
*Pruebas ejecutadas:* Uso antes de declarar y redeclaración

### Salida del harness
```text
=== AUDITORIA SESION 14 - Declaracion previa y redeclaracion ===
Caso                               esperado:              obtenido:              resultado
[ 1] usar sin declarar                  esperado: 0            obtenido: 0            OK
[ 2] usar despues de declarar           esperado: 1            obtenido: 1            OK
[ 3] redeclarar el mismo nombre         esperado: 0            obtenido: 0            OK
[ 4] total tras redeclarar              esperado: 1            obtenido: 1            OK
[ 5] prefijo no es el mismo nombre      esperado: 0            obtenido: 0            OK
[ 6] declarar nombre vacio              esperado: -1           obtenido: -1           OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion14.md
```

* [x] Caso base y límites superados sin *Crash*.
* [x] No existen accesos fuera de límites ni *Memory Leaks*.
* [x] La complejidad teórica coincide con la implementada.

### Reporte Crítico
*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*
> La propuesta inicial debía contemplar algunos casos adicionales que no aparecen directamente en las pruebas del harness,
> como recibir un puntero NULL, un nombre vacío o una tabla llena.
> Para solucionarlo agregué validaciones al inicio de las funciones y una comprobación de la capacidad máxima antes de insertar un nuevo nombre.
>  También revisé que la redeclaración no aumentara el contador de símbolos.
> De esta manera se evitan inserciones incorrectas y se mantiene el contenido de la tabla dentro de sus límites.

---
**Firma digital:** [EDWINTUZYEH]
