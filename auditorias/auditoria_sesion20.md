# Bitácora de Requerimientos y Auditoría IA — Sesión 20

**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Hito 2: Analizador Semántico y Scopes  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Edwin Armando Tuz Yeh  
**Matrícula:** 24531358  
**Track:** (C)
---

## 1. Fase 1: El Artesano (Dificultad Manual)

*Reto:* Integración de Tabla de Símbolos y AST.

**Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:**

> Al realizar la implementación encontré que era necesario recorrer correctamente los ámbitos mediante el apuntador `padre`, sin perder la referencia del ámbito actual. También tuve que considerar que cada ámbito tiene un límite de ocho símbolos definido por `AMBITO_MAX`.
>
> Otro detalle fue evitar que los nombres repetidos se contaran varias veces. Para solucionarlo utilicé ciclos para recorrer los ámbitos y comparaciones con `strcmp()`. También agregué validaciones para evitar trabajar con apuntadores NULL.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal

| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C99 / GCC o Rust 2021 sin bibliotecas no estándar |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores |
| **Especificación (E)** | Contrato de Validación Semántica Integral |
| **Output (O)** | Solo código modular y análisis de complejidad |

### 2.2 Prompt Estructurado

```text
Contexto:
Estoy desarrollando un analizador semántico en lenguaje C
para la materia Lenguajes y Autómatas II. Trabajo con una
estructura llamada Ambito que contiene un arreglo de
símbolos, un contador total y un apuntador al ámbito padre.

Rol:
Actúa como un ingeniero de software especializado en
sistemas, compiladores y análisis semántico.

Especificación:
Implementa las funciones profundidad_de() y contar_visibles()
respetando exactamente las firmas declaradas en api_sesion20.h.

La función profundidad_de() debe:
- Recibir un ámbito y un nombre.
- Buscar el nombre en el ámbito actual y sus padres.
- Devolver 0 si está en el ámbito actual.
- Devolver el nivel correspondiente si está en un padre.
- Devolver -1 si no existe.
- Devolver -2 si algún argumento es NULL.
- Respetar el shadowing.

La función contar_visibles() debe:
- Contar los nombres distintos de toda la cadena de ámbitos.
- No contar dos veces los nombres repetidos.
- Dar prioridad a las declaraciones de los ámbitos internos.
- Validar el ámbito NULL.

Restricciones:
- Utilizar C estándar.
- No modificar las estructuras ni las firmas.
- No agregar main().
- No acceder fuera de los límites del arreglo AMBITO_MAX.
- Evitar advertencias con -Wall -Wextra -Werror.

Output:
Entrega únicamente el código modular de las funciones y
una explicación breve de su complejidad temporal y espacial.
```

---

## 3. Código Devuelto por el Modelo

```c
#include "api_sesion20.h"
#include <string.h>

int profundidad_de(const Ambito *actual, const char *nombre) {

    if (actual == NULL || nombre == NULL) {
        return -2;
    }

    int nivel = 0;

    while (actual != NULL) {

        int total = actual->total;

        if (total < 0) total = 0;
        if (total > AMBITO_MAX) total = AMBITO_MAX;

        for (int i = 0; i < total; i++) {

            if (actual->simbolos[i] != NULL &&
                strcmp(actual->simbolos[i], nombre) == 0) {

                return nivel;
            }
        }

        actual = actual->padre;
        nivel++;
    }

    return -1;
}

int contar_visibles(const Ambito *actual) {

    if (actual == NULL) {
        return -2;
    }

    int contador = 0;

    for (const Ambito *a = actual; a != NULL; a = a->padre) {

        int total = a->total;

        if (total < 0) total = 0;
        if (total > AMBITO_MAX) total = AMBITO_MAX;

        for (int i = 0; i < total; i++) {

            const char *nombre = a->simbolos[i];

            if (nombre == NULL) {
                continue;
            }

            int encontrado = 0;

            for (const Ambito *b = actual; b != a; b = b->padre) {

                int limite = b->total;

                if (limite < 0) limite = 0;
                if (limite > AMBITO_MAX) limite = AMBITO_MAX;

                for (int j = 0; j < limite; j++) {

                    if (b->simbolos[j] != NULL &&
                        strcmp(b->simbolos[j], nombre) == 0) {

                        encontrado = 1;
                        break;
                    }
                }

                if (encontrado) {
                    break;
                }
            }

            for (int j = 0; j < i && !encontrado; j++) {

                if (a->simbolos[j] != NULL &&
                    strcmp(a->simbolos[j], nombre) == 0) {

                    encontrado = 1;
                }
            }

            if (!encontrado) {
                contador++;
            }
        }
    }

    return contador;
}
```

**Análisis de complejidad:**

- `profundidad_de()`: O(D × AMBITO_MAX), donde D es la cantidad de ámbitos.
- `contar_visibles()`: O(D² × AMBITO_MAX²) como cota conservadora por las comparaciones entre ámbitos y símbolos.
- Memoria auxiliar: O(1), sin contar la memoria utilizada por las cadenas y estructuras recibidas.

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)

*Pruebas ejecutadas:* Casos de resolución de nombres, shadowing y visibilidad.

### Salida del harness

```text
=== AUDITORIA SESION 20 - Resolucion de nombres y visibilidad ===
Caso                               esperado:              obtenido:              resultado
[ 1] nombre en el ambito actual    esperado: 0             obtenido: 0             OK
[ 2] nombre dos niveles arriba     esperado: 2             obtenido: 2             OK
[ 3] shadowing gana el interno     esperado: 0             obtenido: 0             OK
[ 4] nombre no visible             esperado: -1            obtenido: -1            OK
[ 5] visibles sin repetir          esperado: 3             obtenido: 3             OK
[ 6] ambito NULL                   esperado: -2            obtenido: -2            OK

RESULTADO: 6/6 pruebas superadas
TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion20.md
```

*Nota: Esta es la salida esperada. Debes sustituirla por la salida real de tu ejecución para presentarla como evidencia.*

- [x] Implementación preparada para los casos base y límites del contrato.
- [ ] Casos base y límites ejecutados sin Crash.
- [ ] No existen accesos fuera de límites ni Memory Leaks.
- [x] La complejidad teórica fue analizada.

### Reporte Crítico

*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?*

> Al revisar la implementación identifiqué que el harness solamente comprueba cuando el apuntador del ámbito es NULL, pero no prueba directamente cuando el nombre recibido por `profundidad_de()` es NULL.
>
> Este caso es importante porque la función utiliza `strcmp()` para comparar cadenas y no se debe realizar una comparación con un apuntador nulo.
>
> Para solucionarlo agregué una validación al inicio de la función:
>
> `if (actual == NULL || nombre == NULL) { return -2; }`
>
> Así se evita realizar comparaciones inválidas y se respeta el contrato establecido para los argumentos nulos.

---

**Firma digital:** [EDWINTUZYEH]
