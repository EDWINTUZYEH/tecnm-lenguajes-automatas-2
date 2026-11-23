# Bitácora de Requerimientos y Auditoría IA — Sesión 01

**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Encuadre, Diagnóstico de Punteros y Metodología IA  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Edwin Armando Tuz Yeh  
**Matrícula:** 24531358  
**Track:** (C)
---

## 1. Fase 1: El Artesano (Dificultad Manual)

*Reto:* Inversión de buffer in-place (`char*`).

**Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:**

> La principal dificultad fue recorrer la cadena desde ambos extremos sin salirme de los límites del buffer. También tuve que considerar que en C las cadenas terminan con el carácter nulo `\0`, por lo que no debía intercambiarlo como si fuera un carácter normal.
>
> Para resolverlo utilicé dos índices: uno que comienza en la posición cero y otro que comienza en el último carácter de la cadena. Después intercambié los caracteres utilizando una variable temporal de tipo `char`.
>
> Otra restricción importante fue no utilizar memoria adicional, por lo que la inversión se realizó directamente sobre la cadena original. También agregué una condición para comprobar si el puntero es `NULL` y evitar errores de ejecución.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal

| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C99 / GCC o Rust 2021 sin bibliotecas no estándar. |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores. |
| **Especificación (E)** | Utilizar punteros e índices, complejidad temporal O(n) y memoria auxiliar O(1). |
| **Output (O)** | Código modular en C y análisis de complejidad. |

### 2.2 Prompt Estructurado

```text
CONTEXTO:
Estoy desarrollando una práctica de Lenguajes y Autómatas II
en lenguaje C. Necesito implementar una función que invierta
una cadena de caracteres directamente en su memoria original.

ROL:
Actúa como un ingeniero de software especializado en C,
manejo de punteros y desarrollo de compiladores.

ESPECIFICACIÓN:
Implementa una función llamada invertir que reciba un puntero
de tipo char.

La función debe cumplir los siguientes requisitos:

1. Invertir los caracteres directamente en el buffer original.
2. No utilizar malloc ni reservar memoria adicional.
3. Utilizar dos índices y una variable temporal de tipo char.
4. Comprobar si el puntero recibido es NULL.
5. Manejar correctamente cadenas vacías y de un carácter.
6. No modificar el carácter terminador '\0'.
7. Mantener exactamente la firma void invertir(char *s).
8. No incluir la función main().
9. Utilizar complejidad temporal O(n) y espacial O(1).
10. El código debe compilar con GCC utilizando:
    -std=c11 -Wall -Wextra -Werror.

OUTPUT:
Proporciona el código completo de la función en C,
con comentarios breves y una explicación de su complejidad.
No cambies la firma de la función ni agregues archivos
o dependencias innecesarias.
```

---

## 3. Código Devuelto por el Modelo

```c
/* ia_sesion01_c.c - Fase 2: El Cientifico
 * Inversión de buffer in-place.
 */

#include "api_sesion01.h"
#include <string.h>

void invertir(char *s) {

    if (s == NULL) {
        return;
    }

    size_t inicio = 0;
    size_t fin = strlen(s);

    if (fin == 0) {
        return;
    }

    fin--;

    while (inicio < fin) {

        char temporal = s[inicio];

        s[inicio] = s[fin];
        s[fin] = temporal;

        inicio++;
        fin--;
    }
}
```

**Análisis de complejidad:**

- Tiempo: O(n), porque se recorre la cadena para obtener su longitud y después se realizan los intercambios hasta llegar al centro.
- Espacio auxiliar: O(1), porque solamente se utilizan dos índices y una variable temporal.
- Memoria dinámica: No se utiliza `malloc` ni se crea una copia de la cadena.

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)

*Pruebas ejecutadas:* Valores NULL, buffers vacíos y longitudes impares y pares.

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

### Criterios de aceptación

- [x] Caso base y límites superados sin Crash.
- [x] No existen accesos fuera de límites en los casos probados ni se utiliza memoria dinámica.
- [x] La complejidad teórica coincide con la implementada.

### Reporte Crítico

*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*

> Al revisar la implementación, el caso más importante que debía comprobar era cuando la función recibía un puntero `NULL`. Si se intenta calcular la longitud de una cadena sin verificar primero el puntero, se puede producir un error de segmentación.
>
> Para evitarlo se agregó una condición al inicio de la función que comprueba si `s == NULL` y termina inmediatamente cuando no existe una cadena válida.
>
> También se verificó el comportamiento con una cadena vacía y otra de un solo carácter. Estos casos permiten comprobar que los índices no intenten acceder a posiciones inexistentes.
>
> Después de ejecutar el harness, los seis casos terminaron correctamente. La implementación cumplió con el contrato y no necesitó reservar memoria adicional.

---

**Firma digital:** [EDWINTUZYEH]
