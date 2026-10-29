# Bitácora de Requerimientos y Auditoría IA — Sesión 06
**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Sistema de Tipos Primitivos  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Edwin armando tuz yeh]  
**Matrícula:** [ 24531358]  
**Track:** [ C]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Chequeo de compatibilidad de tipos  
*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*
> El enum asigna TIPO_ERROR = 0, el valor más bajo de la jerarquía. Al comparar
> directamente con `destino >= origen`, `compatible(INT, ERROR)` daría 1
> (2 >= 0), que es incorrecto. Tuve que poner una guarda previa que rechaza
> TIPO_ERROR en cualquier posición (destino u origen). También cuidé que
> `nombre_tipo` nunca devolviera NULL, porque el harness lo trata como falla, y
> que el `switch` sin `default` no generara el warning de "control reaches end
> of non-void function" bajo `-Wall -Wextra -Werror`.
> 

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C99 / GCC o Rust 2021 sin bibliotecas no estándar |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores |
| **Especificación (E)** | Matriz de compatibilidad estática |
| **Output (O)** | Solo código modular y análisis de complejidad |

### 2.2 Prompt Estructurado
```text
[Contexto: Estoy construyendo la verificación semántica de un compilador en C11,
compilado con gcc -std=c11 -Wall -Wextra -Werror. Existe un enum
Tipo { TIPO_ERROR=0, TIPO_CHAR=1, TIPO_INT=2, TIPO_FLOAT=3 } declarado en
api_sesion06.h.

Rol: Actúa como ingeniero de software de sistemas y compiladores que escribe
C estricto y defensivo.

Especificación: Implementa
  int compatible(Tipo destino, Tipo origen);
  const char *nombre_tipo(Tipo t);
La jerarquía es CHAR < INT < FLOAT. Asignar a un tipo más angosto se rechaza
(requiere cast explícito). TIPO_ERROR nunca es compatible con nada, ni como
destino ni como origen. nombre_tipo devuelve "char", "int", "float" o "error",
y nunca NULL. Usa una matriz de compatibilidad estática.

Output: Solo el código C, sin main(), con las firmas exactas de api_sesion06.h,
más una línea indicando la complejidad temporal y espacial.]
```

---

## 3. Código Devuelto por el Modelo
```c
//

#include "api_sesion06.h"

/* Matriz de compatibilidad: TABLA[destino][origen]
 * Indices: 0=ERROR, 1=CHAR, 2=INT, 3=FLOAT
 */
static const int TABLA[4][4] = {
    /* origen:  ERR CHR INT FLT */
    /* ERR */ {  0,  0,  0,  0 },
    /* CHR */ {  0,  1,  0,  0 },
    /* INT */ {  0,  1,  1,  0 },
    /* FLT */ {  0,  1,  1,  1 }
};

int compatible(Tipo destino, Tipo origen) {
    if ((int)destino < 0 || (int)destino > 3) return 0;
    if ((int)origen  < 0 || (int)origen  > 3) return 0;
    return TABLA[destino][origen];
}

const char *nombre_tipo(Tipo t) {
    switch (t) {
        case TIPO_CHAR:  return "char";
        case TIPO_INT:   return "int";
        case TIPO_FLOAT: return "float";
        case TIPO_ERROR: return "error";
    }
    return "desconocido";
}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)
*Pruebas ejecutadas:* Rechazo de asignaciones incompatibles
[ 1] compatible(INT,INT)                esperado: 1            obtenido: 1            OK
[ 2] compatible(FLOAT,INT)              esperado: 1            obtenido: 1            OK
[ 3] compatible(INT,FLOAT)              esperado: 0            obtenido: 0            OK
[ 4] compatible(INT,ERROR)              esperado: 0            obtenido: 0            OK
[ 5] nombre_tipo(INT)                   esperado: int          obtenido: int          OK
[ 6] nombre_tipo(ERROR)                 esperado: error        obtenido: error        OK

RESULTADO: 6/6 pruebas superadas

* [*] Caso base y límites superados sin *Crash*.
* [*] No existen accesos fuera de límites ni *Memory Leaks*.
* [*] La complejidad teórica coincide con la implementada.

### Reporte Crítico
*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*
 Los 6 casos del harness pasan, pero no cubren todo el contrato. Agregué
 temporalmente casos extra: `compatible(ERROR,ERROR)`, `compatible(ERROR,INT)`,
 `compatible(CHAR,INT)`, `compatible(FLOAT,CHAR)` y `compatible((Tipo)7,INT)`.
 El caso borde clave es TIPO_ERROR como destino: una versión con
 `destino >= origen` sin guardas devuelve 1 para `ERROR→ERROR`. La propuesta
 lo evita con la fila y columna de ERROR en ceros, y valida el rango antes de
 indexar para no leer fuera de la matriz. Contrapartida: la tabla es menos
 mantenible, ya que un tipo nuevo exige ampliar la matriz y los límites a mano.
>

---
**Firma digital:** [EDWINTUZYEH]
