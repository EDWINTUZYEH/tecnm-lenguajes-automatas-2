# Bitácora de Requerimientos y Auditoría IA — Sesión 25

**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Control de Flujo: Bucles while y for  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** Edwin Armando Tuz Yeh  
**Matrícula:** [24531358]  
**Track:** (C)

---

## 1. Fase 1: El Artesano (Dificultad Manual)

**Reto:** Estructura de ciclo en instrucciones TAC.

**Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:**

> Al implementar los ciclos identifiqué que era necesario controlar correctamente las etiquetas de inicio y fin para evitar que dos ciclos utilizaran los mismos nombres. También tuve que considerar el tamaño máximo de 64 caracteres por instrucción y la posición del contador `n` para evitar escribir fuera del arreglo. Otro detalle fue colocar la actualización del iterador antes del salto GOTO en el ciclo for.

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal

| Elemento C-R-E-O | Definición Técnica |
|---|---|
| **Contexto (C)** | Lenguaje C11, GCC y biblioteca estándar. |
| **Rol (R)** | Ingeniero de software especializado en sistemas y compiladores. |
| **Especificación (E)** | Implementar `emitir_while()` y `emitir_for()`, respetando las firmas originales, generando etiquetas únicas, validando límites y permitiendo argumentos NULL opcionales. |
| **Output (O)** | Código modular en C, sin función main, compatible con el harness y análisis de complejidad. |

### 2.2 Prompt Estructurado

```text
Actúa como un ingeniero de software especializado en C y compiladores.

CONTEXTO:
Estoy desarrollando un generador de código de tres direcciones (TAC)
para la materia Lenguajes y Autómatas II.

ROL:
Actúa como un programador experto en C11 y manejo seguro de memoria.

ESPECIFICACIÓN:
Implementa las funciones emitir_while() y emitir_for()
respetando exactamente las firmas declaradas en api_sesion25.h.

El while debe generar cuatro instrucciones:
1. Etiqueta de inicio.
2. Salto condicional IFFALSE hacia el fin.
3. GOTO hacia el inicio.
4. Etiqueta de fin.

El for debe generar:
1. Inicialización, si no es NULL.
2. Etiqueta de inicio.
3. Salto condicional.
4. Actualización, si no es NULL.
5. GOTO hacia el inicio.
6. Etiqueta de fin.

Utiliza snprintf para generar las instrucciones.
Valida los límites del arreglo y evita escrituras fuera de memoria.
Cada ciclo debe consumir dos etiquetas únicas.
No agregues main().
El código debe compilar con:
-std=c11 -Wall -Wextra -Werror

OUTPUT:
Entrega únicamente código C modular y funcional,
sin modificar las firmas originales.
```

## 3. Código Devuelto por el Modelo

Se generaron las funciones `emitir_while()` y `emitir_for()` utilizando C11.

La implementación utiliza:
- `snprintf()` para construir las instrucciones TAC.
- `memcpy()` para copiar las instrucciones al arreglo.
- Validaciones de punteros y límites.
- Dos etiquetas por ciclo.
- Control de argumentos NULL.

Archivos utilizados:

- `artesano_sesion25_c.c`
- `ia_sesion25_c.c`
- `api_sesion25.h`

## 4. Fase 3: El Auditor (Resultados del Test Harness)

**Pruebas ejecutadas:** Validación de etiquetas, condiciones, inicialización, actualización y argumento NULL.

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


- [x] Caso base y límites superados sin Crash 
- [x] No existen accesos fuera de límites ni Memory Leaks.
- [x] La complejidad de generación es O(1), ya que cada ciclo genera una cantidad fija de instrucciones.

### Reporte Crítico

**¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?**

> Un caso importante fue cuando el argumento post tiene valor NULL. Si no se controla correctamente, se puede generar una instrucción vacía o alterar la posición de las demás instrucciones. Se solucionó agregando una condición que verifica si post es diferente de NULL antes de generar la actualización. También se agregaron validaciones para comprobar que exista espacio suficiente en el arreglo y evitar escrituras fuera de sus límites.

---

**Firma digital:** [EDWINTUZYEH]
