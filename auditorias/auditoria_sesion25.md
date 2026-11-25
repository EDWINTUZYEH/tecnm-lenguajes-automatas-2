# Bitácora de Requerimientos y Auditoría IA — Sesión 25

**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Control de Flujo: Bucles while y for  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Edwin Armando Tuz Yeh  
**Matrícula:** 24531358  
**Track:** C

---

## 1. Fase 1: El Artesano (Dificultad Manual)

**Reto:** Estructura de ciclo en instrucciones TAC.

**Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:**

> Al realizar esta parte me di cuenta de que tenía que llevar un buen control de las etiquetas para que los ciclos no utilizaran los mismos nombres. También tuve que cuidar que las instrucciones no pasaran del límite de 64 caracteres y que el contador indicara correctamente la siguiente posición del arreglo. En el ciclo for, una de las partes que más debía cuidar era colocar la actualización del iterador antes del GOTO, porque de lo contrario el ciclo no seguiría el orden esperado.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal

| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Lenguaje C11 utilizando GCC y bibliotecas estándar. |
| **Rol (R)** | Programador con conocimientos de C y desarrollo de compiladores. |
| **Especificación (E)** | Crear las funciones while y for, controlar las etiquetas, respetar el orden de las instrucciones y permitir argumentos NULL cuando corresponda. |
| **Output (O)** | Código en C, separado por funciones, sin main() y que pueda compilar con el harness. |

### 2.2 Prompt Estructurado

```text
Actúa como un programador con experiencia en lenguaje C
y desarrollo de compiladores.

CONTEXTO:
Estoy trabajando en la Sesión 25 de Lenguajes y Autómatas II.
Necesito generar instrucciones TAC para los ciclos while y for.

ROL:
Ayúdame como un programador que conoce C11 y el manejo de arreglos.

ESPECIFICACIÓN:
Implementa las funciones emitir_while() y emitir_for()
respetando las firmas del archivo api_sesion25.h.

Para while necesito:
- Etiqueta de inicio.
- Condición con IFFALSE.
- GOTO para regresar al inicio.
- Etiqueta de fin.

Para for necesito:
- Inicialización si no es NULL.
- Etiqueta de inicio.
- Evaluación de la condición.
- Actualización si no es NULL.
- GOTO de regreso.
- Etiqueta de fin.

Cada ciclo debe utilizar dos etiquetas nuevas.
Utiliza snprintf para generar las instrucciones.
Comprueba que exista espacio en el arreglo antes de escribir.
Evita modificar las firmas y no agregues main().

El código debe compilar con:
-std=c11 -Wall -Wextra -Werror

OUTPUT:
Dame el código completo de las funciones, de manera
ordenada y sin agregar explicaciones innecesarias.
```

---

## 3. Código Devuelto por el Modelo

El modelo proporcionó una implementación de las dos funciones solicitadas. El código utiliza `snprintf()` para formar las instrucciones y `memcpy()` para agregarlas al arreglo.

Se conservaron las firmas originales y se agregaron validaciones para revisar los punteros, el espacio disponible y el contador de etiquetas.

```c
#include "api_sesion25.h"
#include <stdio.h>
#include <string.h>
#include <limits.h>

void emitir_while(char lineas[][64], int max, int *n,
                  const char *cond, int *etiquetas) {
    char temp[4][64];
    int inicio, fin;

    if (!lineas || !n || !cond || !etiquetas ||
        max < 0 || *n < 0 || *n > max ||
        max - *n < 4 || *etiquetas < 0 ||
        *etiquetas > INT_MAX - 2)
        return;

    inicio = *etiquetas;
    fin = inicio + 1;

    if (snprintf(temp[0], 64, "L%d:", inicio) >= 64 ||
        snprintf(temp[1], 64, "IFFALSE %s GOTO L%d", cond, fin) >= 64 ||
        snprintf(temp[2], 64, "GOTO L%d", inicio) >= 64 ||
        snprintf(temp[3], 64, "L%d:", fin) >= 64)
        return;

    memcpy(lineas + *n, temp, sizeof(temp));
    *n += 4;
    *etiquetas += 2;
}

void emitir_for(char lineas[][64], int max, int *n,
                const char *inicio, const char *cond,
                const char *post, int *etiquetas) {
    char temp[6][64];
    int total = 0, etiqueta_inicio, etiqueta_fin;

    if (!lineas || !n || !cond || !etiquetas ||
        max < 0 || *n < 0 || *n > max ||
        *etiquetas < 0 || *etiquetas > INT_MAX - 2)
        return;

    etiqueta_inicio = *etiquetas;
    etiqueta_fin = etiqueta_inicio + 1;

    if (inicio != NULL) {
        if (snprintf(temp[total], 64, "%s", inicio) >= 64)
            return;
        total++;
    }

    if (snprintf(temp[total], 64, "L%d:", etiqueta_inicio) >= 64)
        return;
    total++;

    if (snprintf(temp[total], 64, "IFFALSE %s GOTO L%d",
                 cond, etiqueta_fin) >= 64)
        return;
    total++;

    if (post != NULL) {
        if (snprintf(temp[total], 64, "%s", post) >= 64)
            return;
        total++;
    }

    if (snprintf(temp[total], 64, "GOTO L%d",
                 etiqueta_inicio) >= 64)
        return;
    total++;

    if (snprintf(temp[total], 64, "L%d:", etiqueta_fin) >= 64)
        return;
    total++;

    if (max - *n < total)
        return;

    memcpy(lineas + *n, temp, (size_t)total * sizeof(temp[0]));
    *n += total;
    *etiquetas += 2;
}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)

**Pruebas ejecutadas:** Comprobación de las etiquetas, condiciones, inicialización, actualización del iterador y uso de NULL en el argumento `post`.

### Salida del harness

```text
=== AUDITORIA SESION 25 - Esqueleto TAC de while y for ===
[ 1] while: marca de inicio             esperado: L0:          obtenido: L0:          OK
[ 2] while: condicion
     esperado: IFFALSE a < b GOTO L1
     obtenido: IFFALSE a < b GOTO L1
     -> OK
[ 3] dos ciclos sin colision             esperado: L2:          obtenido: L2:          OK
[ 4] for: inicializacion                esperado: i = 0        obtenido: i = 0        OK
[ 5] for: actualizacion                 esperado: i = i + 1    obtenido: i = i + 1    OK
[ 6] for sin post (NULL)                esperado: 5            obtenido: 5            OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE.
```

### Lista de verificación

- [x] Las funciones while y for generan las instrucciones solicitadas.
- [x] Se utilizan etiquetas diferentes para evitar que los ciclos se repitan con los mismos nombres.
- [x] Se contempla el caso donde `post` tiene valor NULL.
- [x] Se utiliza `snprintf()` para formar las instrucciones.
- [x] Se comprueba el espacio disponible antes de copiar las instrucciones.
- [ ] Se probaron todos los casos de límites y entradas incorrectas sin provocar errores.
- [ ] Se comprobó la ausencia de accesos fuera de los límites mediante pruebas adicionales.
- [x] Se revisó la complejidad de las funciones.

### Reporte Crítico

**¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?**

> Uno de los casos que había que cuidar era cuando el argumento `post` llegaba como NULL. En ese caso no se debe agregar la actualización del iterador, pero tampoco se deben alterar las demás instrucciones del ciclo. Para solucionarlo se agregó una condición que revisa si `post` tiene un valor antes de escribirlo en el arreglo. También se agregaron comprobaciones para revisar que exista espacio suficiente antes de copiar las instrucciones. De esta manera se evita modificar posiciones que no corresponden y se mantiene el orden correcto del ciclo.

---

**Firma digital:** [EDWINTUZYEH]
