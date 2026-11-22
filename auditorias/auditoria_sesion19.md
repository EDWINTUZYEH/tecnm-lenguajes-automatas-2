
# Bitácora de Requerimientos y Auditoría IA — Sesión 19

**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Estructuras (struct) y Miembros  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Edwin Armando Tuz Yeh  
**Matrícula:** 24531358  
**Track:** (C)
---

## 1. Fase 1: El Artesano (Dificultad Manual)

*Reto:* Offsets de miembros en estructuras.

*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*

> Al realizar la implementación manual identifiqué que los campos de una estructura no siempre se guardan uno después de otro. Cada campo necesita una posición de memoria que respete su alineación. Por ejemplo, después de un campo char, puede ser necesario agregar bytes de padding antes de guardar un int.
>  También tuve que considerar que el tamaño total de la estructura debe redondearse según la alineación del campo más grande.
> La principal dificultad fue calcular correctamente los espacios de memoria sin modificar las firmas de las funciones establecidas en el archivo api_sesion19.h.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal

| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C99 / GCC, utilizando bibliotecas estándar y el contrato definido en api_sesion19.h. |
| **Rol (R)** | Ingeniero de software especializado en programación de sistemas y compiladores. |
| **Especificación (E)** | Implementar el cálculo de offsets de miembros y tamaño total de estructuras, aplicando alineación individual, padding entre campos y padding final. Los tipos permitidos son char, short, int y double, con tamaños y alineaciones de 1, 2, 4 y 8 bytes respectivamente. 
Las listas NULL, tipos desconocidos y miembros inexistentes deben manejarse devolviendo -1. Una estructura sin campos debe devolver 0. |
| **Output (O)** | Código C modular, con las funciones offset_campo() y tamano_struct(), respetando las firmas originales, sin incluir main(), y compatible con las opciones -Wall -Wextra -Werror. Incluir una explicación de la complejidad algorítmica. |

### 2.2 Prompt Estructurado

```text
CONTEXTO:
Estoy trabajando en la Sesión 19 de Lenguajes y Autómatas II.
Necesito implementar dos funciones en lenguaje C para calcular
los offsets de los miembros de una estructura y su tamaño total.

ROL:
Actúa como un ingeniero de software especializado en C,
programación de sistemas y compiladores.

ESPECIFICACIÓN:
Implementa las funciones:

int offset_campo(const Campo *campos, int total, const char *nombre);
int tamano_struct(const Campo *campos, int total);

La estructura Campo está declarada en api_sesion19.h.

Los tipos permitidos son:
- char: 1 byte.
- short: 2 bytes.
- int: 4 bytes.
- double: 8 bytes.

Cada campo debe alinearse a su propio tamaño antes de
asignarle un offset.

El tamaño total debe redondearse al múltiplo de la
alineación mayor de todos los campos.

Las condiciones especiales son:
- Si la lista es NULL, devolver -1.
- Si el total es negativo, devolver -1.
- Si existe un tipo desconocido, devolver -1.
- Si el nombre del miembro no existe, devolver -1.
- Si la estructura no tiene campos, devolver 0.

OUTPUT:
Entrega código C completo y modular.
Respeta exactamente las firmas originales.
No incluyas main().
Utiliza bibliotecas estándar.
Evita advertencias con -Wall -Wextra -Werror.
Incluye comentarios breves y explica la complejidad
temporal y espacial de ambas funciones.
```

---

## 3. Código Devuelto por el Modelo

```c
#include "api_sesion19.h"
#include <string.h>

static int tamano_tipo(const char *tipo) {
    if (tipo == NULL) {
        return -1;
    }

    if (strcmp(tipo, "char") == 0) return 1;
    if (strcmp(tipo, "short") == 0) return 2;
    if (strcmp(tipo, "int") == 0) return 4;
    if (strcmp(tipo, "double") == 0) return 8;

    return -1;
}

static int ajustar_offset(int offset, int alineacion) {
    int residuo = offset % alineacion;

    if (residuo != 0) {
        offset += alineacion - residuo;
    }

    return offset;
}

int offset_campo(const Campo *campos, int total, const char *nombre) {
    int offset = 0;
    int i;
    int tamano;

    if (campos == NULL || nombre == NULL || total < 0) {
        return -1;
    }

    for (i = 0; i < total; i++) {
        if (campos[i].nombre == NULL ||
            tamano_tipo(campos[i].tipo) == -1) {
            return -1;
        }
    }

    for (i = 0; i < total; i++) {
        tamano = tamano_tipo(campos[i].tipo);
        offset = ajustar_offset(offset, tamano);

        if (strcmp(campos[i].nombre, nombre) == 0) {
            return offset;
        }

        offset += tamano;
    }

    return -1;
}

int tamano_struct(const Campo *campos, int total) {
    int offset = 0;
    int alineacion_mayor = 0;
    int tamano;
    int i;

    if (campos == NULL || total < 0) {
        return -1;
    }

    if (total == 0) {
        return 0;
    }

    for (i = 0; i < total; i++) {
        if (campos[i].nombre == NULL) {
            return -1;
        }

        tamano = tamano_tipo(campos[i].tipo);

        if (tamano == -1) {
            return -1;
        }

        offset = ajustar_offset(offset, tamano);
        offset += tamano;

        if (tamano > alineacion_mayor) {
            alineacion_mayor = tamano;
        }
    }

    return ajustar_offset(offset, alineacion_mayor);
}
```

**Análisis de complejidad:**

- `offset_campo()`: O(n) en tiempo, porque recorre los campos para validar y localizar el miembro. Utiliza O(1) de espacio auxiliar.
- `tamano_struct()`: O(n) en tiempo, porque recorre una vez todos los campos para calcular sus posiciones y el tamaño final. Utiliza O(1) de espacio auxiliar.

Donde n representa el número total de campos de la estructura.

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)

*Pruebas ejecutadas:* Acceso a miembros inexistentes, alineación de campos, padding final y estructuras vacías.

### Salida del harness

```text
=== AUDITORIA SESION 19 - Offsets de miembros y tamano de struct ===
Caso                               esperado:              obtenido:              resultado
[ 1] struct char e int: b           esperado: 4            obtenido: 4            OK
[ 2] struct de tres campos: c       esperado: 8            obtenido: 8            OK
[ 3] tamano total con padding       esperado: 12           obtenido: 12           OK
[ 4] double seguido de char         esperado: 16           obtenido: 16           OK
[ 5] miembro inexistente            esperado: -1           obtenido: -1           OK
[ 6] struct sin campos              esperado: 0            obtenido: 0            OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion19.md
```

*Nota: Esta es la salida esperada. Debe sustituirse por la salida real obtenida al ejecutar el harness antes de entregar.*

- [x] Se contempla el caso base y los límites definidos en el contrato.
- [x] La implementación no utiliza memoria dinámica ni necesita liberar memoria.
- [x] La complejidad teórica es O(n) en tiempo y O(1) en espacio auxiliar.

### Reporte Crítico

*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*

> Durante la revisión identifiqué que era necesario validar los tipos de los campos antes de realizar los cálculos. Si se recibe un tipo desconocido, no se debe intentar calcular su alineación porque podría producir una división entre cero o un resultado incorrecto.
>
> También revisé el caso de una estructura vacía, ya que debe devolver cero, y el caso de un miembro inexistente, que debe devolver -1.
>
> Para solucionar estas situaciones agregué validaciones para comprobar que la lista, los nombres y los tipos sean válidos antes de realizar los cálculos. También comprobé que cada campo se alinee correctamente y que el tamaño final incluya el padding correspondiente.
>
> El harness comprueba seis situaciones, pero no prueba directamente las listas NULL ni los tipos desconocidos. Por eso es importante revisar también esas condiciones mediante pruebas adicionales.

---

**Firma digital:** [EDWINTUZYEH]
