# Bitácora de Requerimientos y Auditoría IA — Sesión 24

**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Control de Flujo: Sentencia if-else  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Edwin Armando Tuz Yeh  
**Matrícula:** [No. de Control]  
**Track:** C (el harness evalúa C; la versión en Rust es opcional y no se califica con este harness).

---

## 1. Fase 1: El Artesano (Dificultad Manual)

**Reto:** Saltos condicionales y evaluación booleana.

Al realizar la implementación manual identifiqué que era necesario controlar correctamente la cantidad de instrucciones generadas y respetar el espacio disponible en el arreglo de cadenas.

Una de las dificultades fue distinguir el comportamiento de los operadores AND y OR, ya que cada uno necesita un tipo de salto diferente. También fue necesario considerar el caso en que el segundo operando fuera NULL, para evitar generar una instrucción innecesaria.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal

| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Lenguaje C11, compilador GCC y biblioteca estándar de C. |
| **Rol (R)** | Ingeniero de software especializado en sistemas y compiladores. |
| **Especificación (E)** | Generar saltos condicionales para expresiones lógicas AND y OR, respetando el cortocircuito, los límites del arreglo y los casos donde el segundo operando sea NULL. |
| **Output (O)** | Función modular `emitir_condicion()`, compatible con `api_sesion24.h`, sin función `main()` y con análisis de complejidad. |

### 2.2 Prompt Estructurado

```text
CONTEXTO:
Estoy desarrollando una práctica de Lenguajes y Autómatas II
en lenguaje C11, utilizando GCC.

ROL:
Actúa como un ingeniero de software especializado en
compiladores y generación de código intermedio.

ESPECIFICACIÓN:
Implementa la función emitir_condicion() con la siguiente firma:

int emitir_condicion(char lineas[][64], int max,
                     const char *a, const char *b,
                     char op, const char *etiqueta);

Requisitos:
1. Para el operador '&' genera saltos IFFALSE.
2. Para el operador '|' genera saltos IFTRUE.
3. Todos los saltos deben dirigirse a la etiqueta recibida.
4. Si b es NULL, genera únicamente el salto del primer operando.
5. Respeta el límite máximo de instrucciones.
6. Valida los argumentos necesarios.
7. Utiliza snprintf para evitar desbordamientos
   al escribir en las cadenas.
8. No incluyas main().
9. Mantén exactamente la firma solicitada.
10. El código debe compilar con:
    gcc -std=c11 -Wall -Wextra -Werror.

OUTPUT:
Entrega únicamente la implementación modular en C,
con comentarios breves y un análisis de complejidad.
```

---

## 3. Código Devuelto por el Modelo

Archivo: `ia_sesion24_c.c`

```c
#include "api_sesion24.h"
#include <stdio.h>

int emitir_condicion(char lineas[][64], int max,
                     const char *a, const char *b,
                     char op, const char *etiqueta) {

    const char *salto;
    int total = 0;

    if (lineas == NULL || a == NULL ||
        etiqueta == NULL || max <= 0) {
        return 0;
    }

    switch (op) {
        case '&':
            salto = "IFFALSE";
            break;

        case '|':
            salto = "IFTRUE";
            break;

        default:
            return 0;
    }

    int escritos = snprintf(lineas[total], 64,
                             "%s %s GOTO %s",
                             salto, a, etiqueta);

    if (escritos < 0 || escritos >= 64) {
        return 0;
    }

    total++;

    if (b != NULL && total < max) {

        escritos = snprintf(lineas[total], 64,
                            "%s %s GOTO %s",
                            salto, b, etiqueta);

        if (escritos < 0 || escritos >= 64) {
            return total;
        }

        total++;
    }

    return total;
}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)

**Pruebas ejecutadas:** Condiciones compuestas con AND y OR.

### Salida del harness

```text
PENDIENTE: pegar aquí la salida real de ejecución.

Resultado esperado:
RESULTADO: 6/6 pruebas superadas
TODO EN VERDE.
```

### Lista de verificación

- [x] Caso base y límites superados sin Crash (pendiente de ejecución).
- [x] No existen accesos fuera de límites ni Memory Leaks (pendiente de verificar).
- [x] La complejidad teórica coincide con la implementada.

### Análisis de complejidad

La función genera como máximo dos instrucciones, una para cada operando.

- **Tiempo:** O(1), porque se procesa como máximo un número fijo de dos operandos. La escritura de cadenas depende de su longitud, que está limitada por el tamaño del búfer.
- **Espacio auxiliar:** O(1), porque utiliza una cantidad fija de variables auxiliares.
- **Memoria de salida:** Como máximo dos posiciones del arreglo proporcionado por el usuario.

### Reporte Crítico

Un caso borde importante es cuando el segundo operando tiene valor NULL. Una implementación que no contemple esta situación podría intentar generar una instrucción con un operando inexistente.

Se solucionó mediante una condición que comprueba si `b` es diferente de NULL antes de generar el segundo salto.

También se identificó la importancia de respetar el parámetro `max`, ya que representa la cantidad máxima de instrucciones que pueden escribirse en el arreglo.

De esta manera se evita intentar utilizar posiciones que no están disponibles.

---

**Conclusión:**

La implementación permite generar instrucciones de salto condicional para operadores AND y OR, respetando la etiqueta de salida y el mecanismo de cortocircuito.

La función conserva la interfaz establecida por el docente y está diseñada para trabajar con el harness de la Sesión 24.

**Estado de auditoría:** Pendiente de incorporar la evidencia real de ejecución.

---

**Firma digital:** [Usuario de GitHub]
