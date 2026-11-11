
# Bitácora de Requerimientos y Auditoría IA — Sesión 13

**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Manejo de Ámbitos (Scope Global/Local)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Edwin Armando Tuz Yeh  
**Matrícula:** 24531358  
**Track:** [C]

---

## 1. Fase 1: El Artesano (Dificultad Manual)

**Reto:** Pila de tablas de símbolos (Stack Scopes).

**Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:**

Al realizar el código manualmente, una de las principales dificultades fue controlar correctamente la cantidad de nombres que puede guardar cada ámbito. La estructura tiene un límite de 8 elementos definido mediante `AMBITO_MAX`, por lo que fue necesario revisar que no se intentara guardar información cuando el espacio estuviera lleno.

También tuve que comprender cómo funciona el apuntador `padre`, ya que permite recorrer los diferentes ámbitos hasta llegar al global. Otro detalle importante fue evitar registrar dos veces el mismo identificador dentro de un mismo ámbito, sin impedir que se utilice el mismo nombre en otro nivel.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal

| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Lenguaje C, estándar C11, utilizando GCC y las bibliotecas estándar. |
| **Rol (R)** | Ingeniero de software especializado en programación de sistemas y compiladores. |
| **Especificación (E)** | Implementar una pila de ámbitos enlazados. La función declarar() debe registrar identificadores únicamente en el ámbito actual. La función buscar() debe recorrer el ámbito actual y sus padres hasta encontrar el identificador, respetando el ocultamiento de variables (Shadowing). Debe validar entradas nulas, nombres vacíos, duplicados y capacidad máxima. |
| **Output (O)** | Código C modular, sin función main(), respetando las firmas de api_sesion13.h y compatible con -Wall -Wextra -Werror. Incluir explicación de complejidad temporal y espacial. |

### 2.2 Prompt Estructurado

```text
CONTEXTO:
Estoy trabajando en una práctica de Lenguajes y Autómatas II.
Necesito implementar una pila de ámbitos enlazados en lenguaje C.
La estructura Ambito ya está definida en api_sesion13.h y contiene:
nombre, nombres, total y padre. La capacidad máxima es AMBITO_MAX.

ROL:
Actúa como un ingeniero de software especializado en C y
desarrollo de compiladores.

ESPECIFICACIÓN:
Implementa dos funciones:

1. int declarar(Ambito *ambito, const char *nombre);

- Devuelve 1 cuando registra correctamente un nombre.
- Devuelve 0 si el nombre ya existe en el ámbito actual.
- Devuelve -1 si recibe NULL, un nombre vacío o si el ámbito
  está lleno.
- No debe buscar ni modificar los ámbitos padres.
- No debe superar AMBITO_MAX.

2. const char *buscar(const Ambito *ambito, const char *nombre);

- Busca primero en el ámbito actual.
- Si no encuentra el identificador, continúa con el padre.
- Debe respetar el Shadowing.
- Devuelve el nombre del ámbito donde encontró el identificador.
- Devuelve NULL si no encuentra el identificador.

OUTPUT:
Entrega únicamente código C modular, sin main(), utilizando
las bibliotecas estándar necesarias.
Respeta exactamente las firmas originales.
El código debe compilar con:
gcc -std=c11 -Wall -Wextra -Werror

Explica también la complejidad temporal de las funciones.
```

---

## 3. Código Devuelto por el Modelo

```c
/* ia_sesion13_c.c - Fase 2: El Cientifico
 * Pila de ambitos y busqueda jerarquica.
 */

#include "api_sesion13.h"
#include <string.h>

int declarar(Ambito *ambito, const char *nombre) {
    int i;

    if (ambito == NULL || nombre == NULL || nombre[0] == '\0') {
        return -1;
    }

    if (ambito->total < 0 || ambito->total > AMBITO_MAX) {
        return -1;
    }

    for (i = 0; i < ambito->total; i++) {
        if (ambito->nombres[i] != NULL &&
            strcmp(ambito->nombres[i], nombre) == 0) {
            return 0;
        }
    }

    if (ambito->total == AMBITO_MAX) {
        return -1;
    }

    ambito->nombres[ambito->total] = nombre;
    ambito->total++;

    return 1;
}

const char *buscar(const Ambito *ambito, const char *nombre) {
    int i;

    if (nombre == NULL || nombre[0] == '\0') {
        return NULL;
    }

    while (ambito != NULL) {
        if (ambito->total < 0 || ambito->total > AMBITO_MAX) {
            return NULL;
        }

        for (i = 0; i < ambito->total; i++) {
            if (ambito->nombres[i] != NULL &&
                strcmp(ambito->nombres[i], nombre) == 0) {
                return ambito->nombre;
            }
        }

        ambito = ambito->padre;
    }

    return NULL;
}
```

**Análisis de complejidad:**

- `declarar()`: O(n), porque revisa los nombres registrados en el ámbito actual.
- `buscar()`: O(d × n), porque recorre los diferentes ámbitos y revisa sus identificadores.
- Espacio adicional: O(1), porque utiliza una cantidad constante de variables auxiliares y no reserva memoria dinámica.

Donde n representa la cantidad de identificadores por ámbito y d representa la cantidad de niveles de la jerarquía.

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)

**Pruebas ejecutadas:** Búsqueda jerárquica de identificadores.

### Salida del harness

```text
=== AUDITORIA SESION 13 - Pila de ambitos y busqueda jerarquica ===
Caso                               esperado:              obtenido:              resultado
[ 1] declarar(&g, "x")                  esperado: 1            obtenido: 1            OK
[ 2] buscar en el mismo ambito          esperado: global       obtenido: global       OK
[ 3] buscar subiendo al padre           esperado: global       obtenido: global       OK
[ 4] shadowing en el hijo               esperado: bloque       obtenido: bloque       OK
[ 5] tres niveles hasta la raiz         esperado: raiz         obtenido: raiz         OK
[ 6] nombre no declarado                esperado: (nulo)       obtenido: (nulo)       OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion13.md
```

### Lista de verificación

- [x] Caso base y límites de las seis pruebas del harness superados sin Crash.
- [x] Se revisaron las condiciones para evitar accesos fuera de los límites del arreglo.
- [x] No se utiliza memoria dinámica, por lo que no se generan Memory Leaks por asignaciones dinámicas.
- [x] La complejidad teórica coincide con las operaciones implementadas.

### Reporte Crítico

**¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?**

Al revisar la propuesta de la IA, observé que las seis pruebas del harness no comprueban todos los casos posibles.
Por ejemplo, no se prueba directamente qué sucede cuando se intenta declarar un identificador repetido en el mismo ámbito, 
cuando se alcanza la capacidad máxima de ocho elementos o cuando se reciben argumentos nulos.

Para atender estos casos revisé las condiciones de las funciones. La función declarar() comprueba si el ámbito o el nombre son nulos, 
si el nombre está vacío, si ya existe y si se alcanzó el límite de almacenamiento.
También se verifica que buscar() no recorra posiciones fuera del arreglo y que pueda regresar NULL cuando el identificador no existe.

Con esta revisión se complementan los seis casos del harness con las condiciones adicionales establecidas en el contrato de la actividad.

---

**Firma digital:** [EDWINTUZYEH]
