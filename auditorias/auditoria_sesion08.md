# Bitácora de Requerimientos y Auditoría IA — Sesión 08
**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Inferencia y Promoción de Tipos  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Edwin Armando Tuz Yeh  
**Matrícula:** 24531358  
**Track:** [C]
---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Reglas de casteo implícito  
*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*

Al implementar las reglas a mano el detalle que más me costó fue el orden del `enum`:
`TIPO_ERROR = 0`, `TIPO_CHAR = 1`, `TIPO_INT = 2`, `TIPO_FLOAT = 3`. Como los valores
numéricos ya coinciden con la jerarquía, la comparación `destino < origen` resuelve
`hay_perdida` directamente; sin embargo, `TIPO_ERROR` vale `0` y quedaría como el tipo
"más angosto" si no se trata antes. Por eso hay que verificar el centinela `TIPO_ERROR`
**primero**, tanto en `promover` como en `hay_perdida`, y solo después comparar rangos.

También tuve que cuidar que `nombre_tipo` cubriera todos los valores del `enum` y
agregar un `default` para evitar advertencias, ya que el harness compila con
`-Wall -Wextra -Werror` y cualquier advertencia se convierte en error.
> 

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C99 / GCC o Rust 2021 sin bibliotecas no estándar |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores |
| **Especificación (E)** | Promoción entera y ensanchamiento |
| **Output (O)** | Solo código modular y análisis de complejidad |

### 2.2 Prompt Estructurado
```text
[Contexto: Curso Lenguajes y Autómatas II, Sesión 08. Trabajo en C11 con GCC y el
harness compila con -std=c11 -Wall -Wextra -Werror, por lo que una advertencia
cuenta como error.

Rol: Ingeniero de software de sistemas y compiladores.

Especificación:
Implementa exactamente estas tres funciones declaradas en api_sesion08.h:
    Tipo promover(Tipo a, Tipo b);
    int hay_perdida(Tipo destino, Tipo origen);
    const char *nombre_tipo(Tipo t);
donde el tipo es:
    typedef enum { TIPO_ERROR = 0, TIPO_CHAR = 1, TIPO_INT = 2, TIPO_FLOAT = 3 } Tipo;

Reglas obligatorias:
- Jerarquía: CHAR < INT < FLOAT.
- promover devuelve el tipo de mayor rango entre a y b; si cualquiera de los dos
  es TIPO_ERROR, debe devolver TIPO_ERROR (nunca pierde el centinela).
- hay_perdida devuelve 1 solo cuando el destino es más angosto que el origen y 0
  en cualquier otro caso, incluido cuando aparece TIPO_ERROR.
- nombre_tipo devuelve "char", "int", "float" o "error" en minúsculas.

Output: solo el código de las tres funciones, sin main(), sin bibliotecas no
estándar, listo para compilar junto con el harness.]
```

---

## 3. Código Devuelto por el Modelo
```c
/* ia_sesion08_c.c - Fase 2: El Científico
 *
 * Código generado a partir del contrato C-R-E-O y corregido tras la auditoría.
 * Misma firma que declara api_sesion08.h. No trae main().
 */
#include "api_sesion08.h"

Tipo promover(Tipo a, Tipo b) {
    if (a == TIPO_ERROR || b == TIPO_ERROR) {
        return TIPO_ERROR;
    }
    if (a == TIPO_FLOAT || b == TIPO_FLOAT) {
        return TIPO_FLOAT;
    }
    if (a == TIPO_INT || b == TIPO_INT) {
        return TIPO_INT;
    }
    return TIPO_CHAR;
}

int hay_perdida(Tipo destino, Tipo origen) {
    if (destino == TIPO_ERROR || origen == TIPO_ERROR) {
        return 0;
    }
    return destino < origen;
}

const char *nombre_tipo(Tipo t) {
    switch (t) {
        case TIPO_CHAR:
            return "char";
        case TIPO_INT:
            return "int";
        case TIPO_FLOAT:
            return "float";
        case TIPO_ERROR:
            return "error";
        default:
            return "desconocido";
    }
}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)
*Pruebas ejecutadas:* Mezcla de tipos enteros y flotantes

### Salida del harness
```text
=== AUDITORIA SESION 08 - Reglas de promocion y perdida ===
Caso                               esperado:              obtenido:              resultado
[ 1] promover(CHAR,INT)                 esperado: int          obtenido: int          OK
[ 2] promover(INT,FLOAT)                esperado: float        obtenido: float        OK
[ 3] promover(FLOAT,FLOAT)              esperado: float        obtenido: float        OK
[ 4] promover(ERROR,INT)                esperado: error        obtenido: error        OK
[ 5] hay_perdida(CHAR,INT)              esperado: 1            obtenido: 1            OK
[ 6] hay_perdida(INT,CHAR)              esperado: 0            obtenido: 0            OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion08.md
```

* [x] Caso base y límites superados sin *Crash*.
* [x] No existen accesos fuera de límites ni *Memory Leaks*.
* [x] La complejidad teórica coincide con la implementada.

### Reporte Crítico
*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*

La primera versión que devolvió la IA omitió el centinela `TIPO_ERROR`: solo comparaba
`FLOAT`, luego `INT` y al final regresaba `CHAR`. Con eso, `promover(TIPO_ERROR, TIPO_INT)`
devolvía `int` en lugar de `error`. Al ejecutar el harness el caso 4 imprimió `FALLA`
y el resultado fue `5/6 pruebas superadas`, con código de salida distinto de cero.

Lo detecté leyendo el caso 4 del harness (`promover(ERROR,INT)` espera `error`) y
comparando esa expectativa contra la implementación generada. La corrección fue agregar
la guarda `if (a == TIPO_ERROR || b == TIPO_ERROR) return TIPO_ERROR;` al inicio de
`promover`, y de forma análoga devolver `0` en `hay_perdida` cuando aparece `TIPO_ERROR`
para no confundir el centinela (`0`) con el tipo más angosto. Tras el ajuste, tanto la
versión artesano como la de IA pasan las 6 pruebas con código de salida 0.
> 

---
**Firma digital:** EDWINTUZYEH
