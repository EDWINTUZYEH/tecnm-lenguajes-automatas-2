# Bitácora de Requerimientos y Auditoría IA — Sesión 10
**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Hito 1: Mini-Evaluador de Expresiones  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [edwin armando tuz yeh ]  
**Matrícula:** [24531358]  
**Track:** (C)  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Integración AST y Tipado Estático  
*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*
Al desarrollar el evaluador manualmente, la principal dificultad fue respetar la precedencia de los operadores y el uso correcto de los paréntesis. Fue necesario separar el análisis en funciones para que las multiplicaciones y divisiones se procesaran antes que las sumas y restas.

También se identificó que el análisis debía avanzar carácter por carácter sobre la cadena de entrada, evitando leer posiciones incorrectas. Para resolverlo se utilizó un apuntador que recorre la expresión y una estructura que almacena el estado del análisis y los posibles errores.

En cuanto a la memoria, se evitó reservar memoria dinámica, ya que el evaluador trabaja directamente con la cadena recibida. El uso de llamadas recursivas permite procesar los paréntesis anidados, aunque requiere controlar correctamente los casos de sintaxis inválida.
> 

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C99 / GCC o Rust 2021 sin bibliotecas no estándar |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores |
| **Especificación (E)** | Contrato formal de Frontend Semántico |
| **Output (O)** | Solo código modular y análisis de complejidad |

### 2.2 Prompt Estructurado
```text
[Actúa como un ingeniero de software especializado en lenguaje C y
desarrollo de compiladores.

Necesito implementar un mini-evaluador de expresiones aritméticas
en lenguaje C, respetando el código base y los requisitos de la
actividad de la Sesión 10.

Requisitos:

1. Utilizar la interfaz:
   long evaluar_expresion(const char *fuente, int *error);

2. Aceptar únicamente números enteros, los operadores +, -, * y /,
   paréntesis y espacios.

3. Respetar la precedencia de operadores:
   - Multiplicación y división antes que suma y resta.
   - Los paréntesis deben modificar la precedencia.

4. No aceptar variables ni el operador unario negativo.

5. Utilizar los códigos de error:
   - 1 para división entre cero.
   - 2 para sintaxis inválida.

6. Separar el análisis en funciones para reconocer expresiones,
   términos y operaciones primarias.

7. No modificar la firma de evaluar_expresion.

8. No agregar una función main() al archivo de implementación.

9. El código debe compilar con:
   gcc -Wall -Wextra -Werror

10. Utilizar únicamente bibliotecas estándar y respetar las
    restricciones del código proporcionado.

Entrega el código completo, modular y legible. Explica también
la complejidad temporal y espacial, e identifica posibles casos
límite que deban probarse.]

```

---

## 3. Código Devuelto por el Modelo
```c
// Código devuelto por el LLM
%%writefile ia_sesion10_c.c
/* ia_sesion10_c.c - Fase 2: El Cientifico
 *
 * Pega aqui el codigo que te devolvio la IA, con la MISMA firma
 * que declara api_sesion10.h. No puede traer main().
 */
#include "api_sesion10.h"

/* TODO: pega aqui la propuesta de la IA */

#include "api_sesion10.h"
#include <ctype.h>
#include <stddef.h>

typedef struct {
    const char *s;
    int error;
} ParserIA;

static void saltar_espacios(ParserIA *p) {
    while (*p->s == ' ') {
        p->s++;
    }
}

static long expresion_ia(ParserIA *p);

static long primaria_ia(ParserIA *p) {
    long valor = 0;

    saltar_espacios(p);

    if (*p->s == '(') {
        p->s++;

        valor = expresion_ia(p);

        saltar_espacios(p);

        if (*p->s == ')') {
            p->s++;
        } else {
            p->error = 2;
        }

        return valor;
    }

    if (isdigit((unsigned char)*p->s)) {
        while (isdigit((unsigned char)*p->s)) {
            valor = valor * 10 + (*p->s - '0');
            p->s++;
        }

        return valor;
    }

    p->error = 2;
    return 0;
}

static long termino_ia(ParserIA *p) {
    long valor = primaria_ia(p);

    while (p->error == 0) {
        char operador;

        saltar_espacios(p);
        operador = *p->s;

        if (operador != '*' && operador != '/') {
            break;
        }

        p->s++;

        long derecha = primaria_ia(p);

        if (p->error != 0) {
            return 0;
        }

        if (operador == '*') {
            valor *= derecha;
        } else {
            if (derecha == 0) {
                p->error = 1;
                return 0;
            }

            valor /= derecha;
        }
    }

    return valor;
}

static long expresion_ia(ParserIA *p) {
    long valor = termino_ia(p);

    while (p->error == 0) {
        char operador;

        saltar_espacios(p);
        operador = *p->s;

        if (operador != '+' && operador != '-') {
            break;
        }

        p->s++;

        long derecha = termino_ia(p);

        if (p->error != 0) {
            return 0;
        }

        if (operador == '+') {
            valor += derecha;
        } else {
            valor -= derecha;
        }
    }

    return valor;
}

long evaluar_expresion(const char *fuente, int *error) {
    static int sin_error;

    if (error == NULL) {
        error = &sin_error;
    }

    *error = 0;

    if (fuente == NULL) {
        *error = 2;
        return 0;
    }

    ParserIA p = {fuente, 0};

    long resultado = expresion_ia(&p);

    saltar_espacios(&p);

    if (p.error == 0 && *p.s != '\0') {
        p.error = 2;
    }

    *error = p.error;

    return p.error != 0 ? 0 : resultado;
}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)
*Pruebas ejecutadas:* Precedencia, paréntesis, división entre cero y sintaxis inválida

### Salida del harness
```text
=== AUDITORIA SESION 10 - Mini-evaluador de expresiones (Hito 1) ===
Caso                               esperado:              obtenido:              resultado
[ 1] "2+3*4"                            esperado: 14           obtenido: 14           OK
[ 2] "(2+3)*4"                          esperado: 20           obtenido: 20           OK
[ 3] "10/0" -> error 1                  esperado: 1            obtenido: 1            OK
[ 4] "2+" -> error 2                    esperado: 2            obtenido: 2            OK
[ 5] "  7 "                             esperado: 7            obtenido: 7            OK
[ 6] "5-10"                             esperado: -5           obtenido: -5           OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion10.md
```

* [ *] Caso base y límites superados sin *Crash*.
* [ *] No existen accesos fuera de límites ni *Memory Leaks*.
* [* ] La complejidad teórica coincide con la implementada.

### Reporte Crítico
*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*
Durante la revisión se identificó que era necesario contemplar expresiones incompletas, paréntesis sin cerrar, caracteres no permitidos y divisiones entre cero. También se verificó que no quedaran caracteres sin procesar al finalizar la evaluación.

Para atender estos casos, se incorporaron comprobaciones del estado del analizador, validación de los paréntesis y revisión del final de la cadena. La división entre cero se identifica mediante el código de error 1, mientras que las expresiones con sintaxis incorrecta se identifican con el código 2.

Como limitación adicional, la implementación utiliza el tipo long; por ello, no incorpora una comprobación específica de desbordamiento aritmético. Este aspecto debe considerarse al evaluar expresiones con números o resultados demasiado grandes.
> 

---
**Firma digital:** [EDWINTUZYEH]
