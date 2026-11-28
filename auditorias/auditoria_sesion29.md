# Bitácora de Requerimientos y Auditoría IA — Sesión 29

**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Optimización: Dead Code Elimination  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Edwin Armando Tuz Yeh  
**Matrícula:** 24531358  
**Track:** C 

---

## 1. Fase 1: El Artesano (Dificultad Manual)

*Reto:* Detección de código inalcanzable.

*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*

> La principal dificultad fue controlar qué instrucciones debían eliminarse después de encontrar un GOTO o RETURN. También tuve que cuidar la compactación del arreglo para no sobrescribir instrucciones que todavía necesitaban conservarse y respetar el límite de 64 caracteres por instrucción.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal

| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C99 / GCC o Rust 2021 sin bibliotecas no estándar |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores |
| **Especificación (E)** | Análisis de flujo tras retornos y gotos |
| **Output (O)** | Solo código modular y análisis de complejidad |

### 2.2 Prompt Estructurado

```text
Actúa como un ingeniero de software especializado en compiladores y programación en C.

Necesito implementar la función eliminar_muerto() para eliminar instrucciones inalcanzables de una lista de cuádruplos TAC.

Requisitos:
- Utilizar C99 y bibliotecas estándar.
- Respetar la firma: int eliminar_muerto(char lineas[][64], int n).
- Conservar las instrucciones hasta encontrar GOTO o RETURN.
- Eliminar las instrucciones posteriores hasta encontrar una etiqueta.
- Reconocer las etiquetas que terminan en dos puntos.
- Conservar el orden original de las instrucciones.
- Compactar el arreglo original sin utilizar memoria dinámica.
- Devolver el nuevo número de instrucciones.
- Manejar correctamente una lista vacía.
- No incluir main().
- Evitar advertencias con -Wall -Wextra -Werror.

Entrega únicamente el código y explica su complejidad temporal y espacial.
```

---

## 3. Código Devuelto por el Modelo

```c
#include "api_sesion29.h"
#include <string.h>

int eliminar_muerto(char lineas[][64], int n) {
    int i, j = 0;
    int muerto = 0;

    for (i = 0; i < n; i++) {
        if (strchr(lineas[i], ':') != NULL)
            muerto = 0;

        if (!muerto) {
            if (i != j)
                strcpy(lineas[j], lineas[i]);

            j++;

            if (strncmp(lineas[i], "GOTO", 4) == 0 ||
                strncmp(lineas[i], "RETURN", 6) == 0)
                muerto = 1;
        }
    }

    return j;
}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)

*Pruebas ejecutadas:* Eliminación de bloques inalcanzables.

### Salida del harness

```text
=== AUDITORIA SESION 29 - Eliminacion de codigo inalcanzable ===
Caso                               esperado:              obtenido:              resultado
[ 1] tras GOTO: nuevo tamano       esperado: 4            obtenido: 4            OK
[ 2] tras GOTO: etiqueta viva      esperado: L1:          obtenido: L1:          OK
[ 3] tras RETURN: nuevo tamano     esperado: 4            obtenido: 4            OK
[ 4] tras RETURN: etiqueta viva    esperado: L5:          obtenido: L5:          OK
[ 5] sin codigo muerto             esperado: 3            obtenido: 3            OK
[ 6] lista vacia                   esperado: 0            obtenido: 0            OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion29.md
```

- [x] Caso base y límites superados sin *Crash*.
- [x] No existen accesos fuera de límites ni *Memory Leaks*.
- [x] La complejidad teórica coincide con la implementada.

### Reporte Crítico

*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*

> La implementación inicial debía revisarse para comprobar que reconociera correctamente las instrucciones GOTO y RETURN y que conservara las etiquetas posteriores. Se verificó mediante el harness que las instrucciones inalcanzables se eliminaran sin perder las etiquetas ni alterar el orden de las instrucciones restantes.

---

**Firma digital:** [EDWINTUZYEH]
