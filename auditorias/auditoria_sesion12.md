# Bitácora de Requerimientos y Auditoría IA — Sesión 12

**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Atributos de Símbolos y Memoria  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [edwin armando tuz yeh]  
**Matrícula:** [24531358]  
**Track:** C  

---

## 1. Fase 1: El Artesano (Dificultad Manual)

*Reto:* Estructura de registro de símbolos  
*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*

> El principal problema que identifiqué fue la **alineación natural**. No basta con sumar el tamaño del tipo anterior; hay que redondear
> el cursor hacia arriba al múltiplo del ancho del tipo actual.  
>  
Ejemplo concreto: después de un `char` (`cursor = 1`), al colocar un `int` (`ancho = 4`) el offset no puede ser `1`, debe ser `4`.  
> La fórmula correcta es:  
> `alineado = ((cursor + ancho - 1) / ancho) * ancho`  
>  
> También tuve que cuidar el caso de registro `NULL` y cursor negativo para no escribir memoria inválida, así como devolver `-1` cuando el tipo no existe.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal

| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C99 / GCC o Rust 2021 sin bibliotecas no estándar |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores |
| **Especificación (E)** | Cálculo de desplazamientos y alineación |
| **Output (O)** | Solo código modular y análisis de complejidad |

### 2.2 Prompt Estructurado

```text
Contexto: Estoy implementando la tabla de símbolos de un compilador simple en C (C11). Necesito dos funciones que respeten exactamente el contrato de api_sesion12.h.

Rol: Actúa como un ingeniero de compiladores experimentado que escribe código limpio, seguro y sin dependencias externas.

Especificación:
1. int ancho_de_tipo(const char *tipo);
   - Devuelve el tamaño en bytes de: char=1, short=2, int=4, float=4, double=8, puntero=8
   - Cualquier otro tipo o NULL -> -1

2. int asignar_offset(Simbolo *simbolo, int cursor);
   - Si simbolo es NULL o cursor < 0 -> -1
   - Calcula el offset alineado al múltiplo del ancho del tipo (alineación natural)
   - Guarda el offset en simbolo->offset
   - Devuelve el cursor donde empezará la siguiente variable (offset + ancho)
   - No debe escribir memoria si el registro es NULL

Output: Solo las dos funciones implementadas, sin main(), usando la firma exacta de api_sesion12.h. Incluye los includes necesarios (string.h). Código listo para compilar con -Wall -Wextra -Werror.
```

### 2.3 Código Devuelto por el Modelo

```c
#include "api_sesion12.h"
#include <string.h>
#include <limits.h>

int ancho_de_tipo(const char *tipo) {
    if (tipo == NULL) return -1;
    if (strcmp(tipo, "char") == 0)    return 1;
    if (strcmp(tipo, "short") == 0)   return 2;
    if (strcmp(tipo, "int") == 0)     return 4;
    if (strcmp(tipo, "float") == 0)   return 4;
    if (strcmp(tipo, "double") == 0)  return 8;
    if (strcmp(tipo, "puntero") == 0) return 8;
    return -1;
}

int asignar_offset(Simbolo *simbolo, int cursor) {
    if (simbolo == NULL || cursor < 0) return -1;
    int ancho = ancho_de_tipo(simbolo->tipo);
    if (ancho < 0) return -1;
    /* Evita desbordamiento de int al redondear y sumar el ancho */
    if (cursor > INT_MAX - (ancho - 1)) return -1;
    int alineado = ((cursor + ancho - 1) / ancho) * ancho;
    if (alineado > INT_MAX - ancho) return -1;
    simbolo->offset = alineado;
    return alineado + ancho;
}
```

---

## 3. Fase 3: El Auditor (Resultados del Test Harness)

*Pruebas ejecutadas:* Alineación de tipos y tamaños en bytes  

### Salida del harness

```text
=== AUDITORIA SESION 12 - Registro de simbolo y offsets alineados ===
Caso                               esperado:              obtenido:              resultado
[ 1] ancho_de_tipo("int")               esperado: 4            obtenido: 4            OK
[ 2] ancho_de_tipo("double")            esperado: 8            obtenido: 8            OK
[ 3] int en cursor 0                    esperado: 4            obtenido: 4            OK
[ 4] char e int: offset de b            esperado: 4            obtenido: 4            OK
[ 5] double desde cursor 4              esperado: 8            obtenido: 8            OK
[ 6] registro NULL                      esperado: -1           obtenido: -1           OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion12.md
```

- [x] Caso base y límites superados sin Crash.
- [x] No existen accesos fuera de límites ni Memory Leaks.
- [x] La complejidad teórica coincide con la implementada ($O(1)$ en ambas funciones).

### Reporte Crítico

*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*

* **Cobertura completa del harness:** La IA no omitió ningún caso del harness; todas las 6 pruebas pasaron exitosamente.
* **Protección adicional:** La versión generada añadió validaciones extra contra desbordamiento de enteros (`INT_MAX`) mediante `<limits.h>`, las cuales el harness
* no evalúa directamente pero previenen comportamiento indefinido.
* **Manejo de punteros nulos:** El caso borde más crítico (`simbolo == NULL` y `tipo == NULL`) está correctamente protegido en ambas funciones, evitando escrituras o lecturas en memoria inválida.
* **Entradas fuera de rango:** Se validan adecuadamente los tipos desconocidos y valores de `cursor < 0`, devolviendo `-1` en ambos escenarios.

**Conclusión:** La IA generó una solución correcta, limpia y más defensiva que el mínimo requerido. 
No fue necesario modificar el código para superar las pruebas.

---

**Firma digital:** `[EDWINTUZYEH]`
