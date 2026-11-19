# Bitácora de Requerimientos y Auditoría IA — Sesión 17

**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Comprobación Semántica de Retornos  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Edwin Armando Tuz Yeh  
**Matrícula:** 24531358  
**Track:** C 

---

## 1. Fase 1: El Artesano (Dificultad Manual)

*Reto:* Validación de tipo de sentencia return.

*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*

> Al realizar la implementación manual, tuve dificultad para organizar las condiciones que permiten comprobar si el tipo de retorno es compatible con el tipo declarado en la función. También tuve que cuidar el orden de las validaciones, porque primero se debe revisar la compatibilidad de tipos y después comprobar que todas las rutas tengan un return. Otro detalle fue evitar errores de sintaxis al utilizar punteros, funciones como strcmp() y las llaves de cierre de la función.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal

| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C11 / GCC, utilizando bibliotecas estándar y respetando la interfaz definida en api_sesion17.h. |
| **Rol (R)** | Ingeniero de software especializado en programación en C y desarrollo de compiladores. |
| **Especificación (E)** | Comprobar la compatibilidad entre el tipo de retorno de una función y el tipo de expresión devuelta. Validar que todas las rutas de ejecución tengan return cuando corresponda. Detectar parámetros NULL y conteos de rutas incorrectos. |
| **Output (O)** | Código modular en C, respetando la firma original, sin función main(), con funciones auxiliares y análisis de complejidad. |

### 2.2 Prompt Estructurado

```text
CONTEXTO:
Estoy desarrollando un analizador semántico en C para la materia
Lenguajes y Autómatas II. Necesito implementar una función que
compruebe la compatibilidad de los tipos de retorno y verifique
que todas las rutas de ejecución de una función tengan return.

ROL:
Actúa como un ingeniero de software especializado en C y compiladores.

ESPECIFICACIÓN:
Implementa la función diagnosticar_retorno() respetando exactamente
la siguiente firma:

int diagnosticar_retorno(
    const char *tipo_funcion,
    const char *tipo_expresion,
    int rutas_totales,
    int rutas_con_return
);

Reglas que debe cumplir:

1. Retornar 0 cuando todo sea correcto.
2. Retornar 1 cuando exista incompatibilidad de tipos.
3. Retornar 2 cuando exista una ruta sin retorno.
4. Retornar -1 cuando haya parámetros NULL o conteos incoherentes.
5. Una función void no puede devolver un valor.
6. Una conversión solamente se acepta cuando el tipo destino
   es igual o más amplio que el tipo de origen.
7. La compatibilidad de tipos debe comprobarse antes que
   las rutas de retorno.
8. No modificar la firma original.
9. No agregar main().
10. Utilizar bibliotecas estándar de C.
11. El código debe compilar con -Wall -Wextra -Werror.

OUTPUT:
Entrega el código completo, modular y con funciones auxiliares
si son necesarias. Explica brevemente la lógica y la complejidad
del algoritmo.
```

---

## 3. Código Devuelto por el Modelo

```c
#include "api_sesion17.h"
#include <string.h>

static int nivel_tipo(const char *tipo) {

    if (tipo == NULL) return -1;

    if (strcmp(tipo, "char") == 0) return 1;

    if (strcmp(tipo, "short") == 0 ||
        strcmp(tipo, "short int") == 0) return 2;

    if (strcmp(tipo, "int") == 0) return 3;

    if (strcmp(tipo, "long") == 0 ||
        strcmp(tipo, "long int") == 0) return 4;

    if (strcmp(tipo, "long long") == 0 ||
        strcmp(tipo, "long long int") == 0) return 5;

    if (strcmp(tipo, "float") == 0) return 6;

    if (strcmp(tipo, "double") == 0) return 7;

    if (strcmp(tipo, "long double") == 0) return 8;

    return -1;
}

int diagnosticar_retorno(
    const char *tipo_funcion,
    const char *tipo_expresion,
    int rutas_totales,
    int rutas_con_return
) {

    int destino;
    int origen;

    if (tipo_funcion == NULL || tipo_expresion == NULL) {
        return -1;
    }

    if (rutas_totales <= 0 ||
        rutas_con_return < 0 ||
        rutas_con_return > rutas_totales) {
        return -1;
    }

    if (strcmp(tipo_funcion, "void") == 0) {
        return strcmp(tipo_expresion, "void") == 0 ? 0 : 1;
    }

    if (strcmp(tipo_expresion, "void") == 0) {
        return 1;
    }

    destino = nivel_tipo(tipo_funcion);
    origen = nivel_tipo(tipo_expresion);

    if (destino == -1 || origen == -1) {
        return 1;
    }

    if (destino < origen) {
        return 1;
    }

    if (rutas_con_return < rutas_totales) {
        return 2;
    }

    return 0;
}
```

**Análisis de complejidad:**

- Tiempo: O(1) respecto al número de rutas, porque solamente se realizan comparaciones de tipos y conteos, sin recorrer las rutas individualmente.
- Espacio: O(1), porque utiliza únicamente dos variables auxiliares y no reserva memoria dinámica.

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)

*Pruebas ejecutadas:* Funciones sin retorno o retornos mixtos.

### Salida del harness

```text
=== AUDITORIA SESION 17 - Validacion de retornos y rutas ===
Caso                               esperado:              obtenido:              resultado
[ 1] int con int y dos rutas            esperado: 0            obtenido: 0            OK
[ 2] void devuelve valor                esperado: 1            obtenido: 1            OK
[ 3] ruta sin retorno                   esperado: 2            obtenido: 2            OK
[ 4] double acepta int                  esperado: 0            obtenido: 0            OK
[ 5] int no acepta double               esperado: 1            obtenido: 1            OK
[ 6] cero rutas de ejecucion            esperado: -1           obtenido: -1           OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion17.md
```

- [x] Caso base y límites superados sin Crash.
- [x] No existen accesos fuera de límites ni Memory Leaks.
- [x] La complejidad teórica coincide con la implementada.

### Reporte Crítico

*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*

> Durante la revisión identifiqué que era importante comprobar explícitamente el caso en el que una función que devuelve un valor recibe una expresión de tipo void. Por ejemplo, una función int no puede devolver una expresión void, porque los tipos son incompatibles. También se debe comprobar que una función void solamente acepte una expresión void.
>
> Para solucionar estos casos agregué comparaciones con strcmp() antes de revisar las rutas de retorno. Además, verifiqué que los tipos desconocidos no sean aceptados y que los conteos de rutas sean válidos. Finalmente, ejecuté el harness y comprobé que las seis pruebas proporcionadas fueran superadas.

---

**Firma digital:** [EDWINTUZYEH]
