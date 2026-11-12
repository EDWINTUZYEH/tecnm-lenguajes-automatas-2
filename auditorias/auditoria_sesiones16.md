
# Bitácora de Requerimientos y Auditoría IA — Sesión 16

**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Firmas de Función y Parámetros  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Edwin Armando Tuz Yeh  
**Matrícula:** 24531358  
**Track:** [C]

---

## 1. Fase 1: El Artesano (Dificultad Manual)

*Reto:* Registro de prototipos y aridad.

*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*

> Al realizar el código manualmente, la principal dificultad fue recorrer el catálogo de funciones y comparar correctamente el nombre registrado con el nombre recibido.
También fue necesario tener cuidado con los valores NULL para evitar errores al utilizar strcmp().
Otra parte importante fue distinguir entre una función que no existe y una función que sí existe, pero que tiene una cantidad incorrecta de argumentos.
Para resolverlo utilicé un ciclo for y una condición para comparar la aridad de cada función.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal

| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C99 / GCC o Rust 2021 sin bibliotecas no estándar |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores |
| **Especificación (E)** | Coincidencia estricta de parámetros |
| **Output (O)** | Solo código modular y análisis de complejidad |

### 2.2 Prompt Estructurado

```text
CONTEXTO:
Estoy desarrollando una práctica de Lenguajes y Autómatas II en lenguaje C.
El programa debe verificar las llamadas a funciones utilizando un catálogo
que almacena los nombres de las funciones y su cantidad de parámetros.

ROL:
Actúa como un ingeniero de software especializado en lenguaje C,
programación de sistemas y desarrollo de compiladores.

ESPECIFICACIÓN:
Desarrolla la función verificar_llamada() respetando exactamente
la siguiente declaración:

int verificar_llamada(const Funcion *catalogo, int total,
                      const char *nombre, int nargs);

La función debe cumplir los siguientes requisitos:

1. Buscar el nombre de la función dentro del catálogo completo.
2. Realizar una comparación exacta de los nombres.
3. Comparar la aridad registrada con el número de argumentos recibidos.
4. Devolver 1 cuando la función exista y la aridad coincida.
5. Devolver 0 cuando la función exista, pero tenga una aridad diferente.
6. Devolver -1 cuando la función no esté registrada.
7. Devolver -1 cuando el catálogo sea NULL.
8. Devolver -1 cuando el nombre sea NULL.
9. Devolver -1 cuando la cantidad de argumentos sea negativa.
10. Aceptar funciones con cero parámetros únicamente cuando se llamen
    con cero argumentos.
11. Evitar accesos inválidos a memoria.
12. No incluir main(), porque el programa será compilado junto con
    un harness externo.

OUTPUT:
Entrega código C modular, compatible con api_sesion16.h.
Debe compilar utilizando:

gcc -std=c11 -Wall -Wextra -Werror

Respeta exactamente la firma de la función y utiliza únicamente
bibliotecas estándar de C.
Incluye una explicación de la complejidad temporal y espacial.
```

---

## 3. Código Devuelto por el Modelo

```c
#include "api_sesion16.h"
#include <string.h>

int verificar_llamada(const Funcion *catalogo, int total,
                      const char *nombre, int nargs) {

    if (catalogo == NULL || nombre == NULL || nargs < 0 || total < 0) {
        return -1;
    }

    for (int i = 0; i < total; i++) {

        if (catalogo[i].nombre != NULL &&
            strcmp(catalogo[i].nombre, nombre) == 0) {

            if (catalogo[i].aridad == nargs) {
                return 1;
            }

            return 0;
        }
    }

    return -1;
}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)

*Pruebas ejecutadas:* Llamadas con número incorrecto de argumentos, funciones inexistentes, funciones sin parámetros y validación de valores NULL.

### Salida del harness

```text
=== AUDITORIA SESION 16 - Registro de prototipos y aridad ===
Caso                               esperado:              obtenido:              resultado
[ 1] suma con 3 argumentos              esperado: 1            obtenido: 1            OK
[ 2] suma con 2 argumentos              esperado: 0            obtenido: 0            OK
[ 3] suma con 4 argumentos              esperado: 0            obtenido: 0            OK
[ 4] funcion no registrada              esperado: -1           obtenido: -1           OK
[ 5] main sin argumentos                esperado: 1            obtenido: 1            OK
[ 6] nombre NULL                        esperado: -1           obtenido: -1           OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion16.md
```

* [x] Caso base y límites superados sin *Crash*.
* [x] No existen accesos fuera de límites ni *Memory Leaks*.
* [x] La complejidad teórica coincide con la implementada.

### Análisis de complejidad

**Complejidad temporal: O(n)**

En el peor caso se debe recorrer todo el catálogo para encontrar el nombre de la función.
Por eso, el tiempo de ejecución depende de la cantidad de funciones registradas.

**Complejidad espacial: O(1)**

La función utiliza únicamente variables auxiliares y no necesita crear arreglos adicionales ni reservar memoria dinámica.

### Reporte Crítico

*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*

> Al revisar el código generado por la IA, identifiqué que no contemplaba la validación
de un valor negativo en el parámetro total, que representa la cantidad de funciones registradas. 
Aunque este caso no aparece directamente en las seis pruebas del harness, es importante considerarlo para evitar trabajar con una cantidad inválida de elementos. 
Lo solucioné agregando la condición total < 0 en la validación inicial. 
También revisé el caso de las funciones con cero parámetros y comprobé que solamente deben aceptar llamadas sin argumentos.
De esta manera, la implementación contempla condiciones adicionales a las pruebas principales.

---

**Firma digital:** [EDWINTUZYEH]
