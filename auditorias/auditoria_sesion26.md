# Bitácora de Requerimientos y Auditoría IA — Sesión 26

**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** TAC para Llamadas a Funciones  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Edwin Armando Tuz Yeh  
**Matrícula:** [24531358]  
**Track:** (C)

---

## 1. Fase 1: El Artesano (Dificultad Manual)

*Reto:* Instrucciones param, call y return.

*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*

> Al realizar la implementación, tuve que cuidar el espacio disponible en el arreglo de instrucciones, ya que cada línea tiene una capacidad máxima de 64 caracteres. También fue necesario respetar el orden de los parámetros y comprobar cuándo un argumento tenía valor NULL para evitar generar instrucciones innecesarias.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal

| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C99 / GCC o Rust 2021 sin bibliotecas no estándar. |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores. |
| **Especificación (E)** | Generar instrucciones PARAM en el orden recibido, contar los argumentos existentes para CALL y generar RETURN con o sin valor. |
| **Output (O)** | Código modular en C, respetando las firmas establecidas y considerando límites de memoria y complejidad. |

### 2.2 Prompt Estructurado

```text
Contexto:
Estoy trabajando en la sesión 26 de Lenguajes y Autómatas II.
Necesito implementar la generación de código de tres direcciones
para llamadas a funciones y retornos en C.

Rol:
Actúa como un ingeniero de software especializado en C y
desarrollo de compiladores.

Especificación:
Implementa las funciones emitir_llamada() y emitir_return()
respetando exactamente las firmas de api_sesion26.h.
Los argumentos que no sean NULL deben generar instrucciones
PARAM en el orden a1 y a2.
La instrucción CALL debe indicar la cantidad real de parámetros.
Si resultado es NULL, CALL no debe asignar un temporal.
RETURN debe generarse con valor o sin valor.
Verifica los límites del arreglo y evita accesos fuera de memoria.
No agregues main() y utiliza snprintf para escribir las cadenas.

Output:
Entrega únicamente el código C completo, modular y compatible
con -Wall -Wextra -Werror, junto con un breve análisis
de complejidad.
```

---

## 3. Código Devuelto por el Modelo

```c
#include "api_sesion26.h"
#include <stdio.h>
#include <string.h>

int emitir_llamada(char lineas[][64], int max, int *n,
                   const char *funcion, const char *a1,
                   const char *a2, const char *resultado) {

    char temp[3][64];
    int cantidad = 0;

    if (lineas == NULL || n == NULL || funcion == NULL ||
        max < 0 || *n < 0 || *n > max)
        return 0;

    if (a1 != NULL) {
        if (snprintf(temp[cantidad], 64, "PARAM %s", a1) >= 64)
            return 0;
        cantidad++;
    }

    if (a2 != NULL) {
        if (snprintf(temp[cantidad], 64, "PARAM %s", a2) >= 64)
            return 0;
        cantidad++;
    }

    if (cantidad + 1 > max - *n)
        return 0;

    int r;

    if (resultado != NULL)
        r = snprintf(temp[cantidad], 64,
                     "%s = CALL %s, %d",
                     resultado, funcion, cantidad);
    else
        r = snprintf(temp[cantidad], 64,
                     "CALL %s, %d", funcion, cantidad);

    if (r < 0 || r >= 64)
        return 0;

    for (int i = 0; i <= cantidad; i++) {
        strcpy(lineas[*n], temp[i]);
        (*n)++;
    }

    return 1;
}

void emitir_return(char *dst, int cap, const char *valor) {

    if (dst == NULL || cap <= 0)
        return;

    if (valor != NULL)
        snprintf(dst, cap, "RETURN %s", valor);
    else
        snprintf(dst, cap, "RETURN");
}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)

*Pruebas ejecutadas:* Llamadas anidadas f(g(x)).

### Salida del harness

```text
=== AUDITORIA SESION 26 - Llamadas, parametros y retorno ===
Caso                               esperado:              obtenido:              resultado
[ 1] PARAM x                            esperado: PARAM x      obtenido: PARAM x      OK
[ 2] PARAM y                            esperado: PARAM y      obtenido: PARAM y      OK
[ 3] CALL con dos argumentos
     esperado: _t0 = CALL f, 2
     obtenido: _t0 = CALL f, 2
     -> OK
[ 4] llamada anidada f(g(x))
     esperado: _t1 = CALL f, 1
     obtenido: _t1 = CALL f, 1
     -> OK
[ 5] CALL sin argumentos
     esperado: _t0 = CALL p, 0
     obtenido: _t0 = CALL p, 0
     -> OK
[ 6] RETURN con valor                   esperado: RETURN _t0   obtenido: RETURN _t0   OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion26.md
```

- [x] Caso base y límites superados sin *Crash*.
- [ ] No existen accesos fuera de límites ni *Memory Leaks*.
- [x] La complejidad teórica coincide con la implementada.

### Reporte Crítico

*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*

> La primera implementación podía intentar escribir instrucciones sin comprobar si había suficiente espacio en el arreglo. Para evitarlo, agregué una validación de la capacidad disponible antes de copiar los parámetros y la instrucción CALL. También se contemplaron los argumentos NULL para que no se generen parámetros innecesarios.

---

**Firma digital:** [EDWINTUZYEH]
