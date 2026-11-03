# Guía de C para los laboratorios

**Lenguajes y Autómatas II (SCD-1016)** · TecNM Cancún

Esta guía no es un curso de C: es el C **que los laboratorios te van a pedir**. Cada
tema trae lo mínimo para escribir la función del día, el error que casi todos cometen
y las sesiones donde aparece. Léela antes de la sesión correspondiente y vuelve a ella
cuando el compilador te regañe.

> **Regla de oro:** si el compilador se queja, la respuesta casi siempre está en la
> sección 11 (los errores de gcc). Búscalo ahí primero.

---

## Índice

0. [Cómo se lee un laboratorio](#0-cómo-se-lee-un-laboratorio)
1. [Tipos, variables y `const`](#1-tipos-variables-y-const)
2. [Funciones: por valor y por puntero](#2-funciones-por-valor-y-por-puntero)
3. [Punteros](#3-punteros)
4. [Arreglos y cadenas](#4-arreglos-y-cadenas)
5. [`struct`, `typedef` y `enum`](#5-struct-typedef-y-enum)
6. [Memoria dinámica y listas](#6-memoria-dinámica-y-listas)
7. [Arreglos 2D y `char lineas[][64]`](#7-arreglos-2d-y-char-lineas64)
8. [Recursión](#8-recursión)
9. [Archivos y códigos de salida](#9-archivos-y-códigos-de-salida)
10. [`switch`, ciclos y operadores](#10-switch-ciclos-y-operadores)
11. [Los errores de gcc que más vas a ver](#11-los-errores-de-gcc-que-más-vas-a-ver)
12. [Mapa: qué necesitas en cada sesión](#12-mapa-qué-necesitas-en-cada-sesión)
13. [Ejercicios de calentamiento](#13-ejercicios-de-calentamiento)

---

## 0. Cómo se lee un laboratorio

Cada libreta te da tres cosas antes de pedirte código:

**1. Un contrato (la cabecera).** El archivo `api_sesionNN.h` declara las funciones que
el *harness* sabe probar. Si cambias la firma, el *harness* no compila. Por eso tu
archivo **no lleva `main()`**: el `main()` es del *harness*.

```c
/* api_sesion01.h */
#ifndef API_SESION01_H
#define API_SESION01_H

void invertir(char *s);

#endif
```

**2. Un esqueleto.** Tu archivo `artesano_sesionNN_c.c` incluye la cabecera y trae la
firma con un `TODO`. Tú completas el cuerpo; no cambias la firma.

```c
#include "api_sesion01.h"

void invertir(char *s) {
    (void)s; /* TODO: aquí va tu código */
}
```

**3. Un examen.** El *harness* compila tu archivo junto con el suyo, ejecuta cada caso
y compara el resultado contra lo esperado:

```bash
gcc -std=c11 -Wall -Wextra -Werror harness_sesion01_c.c artesano_sesion01_c.c -o test
./test
```

- `-Wall -Wextra` activan los avisos; `-Werror` convierte cada aviso en **error**.
- Si todo pasa, termina con `RESULTADO: n/n pruebas superadas` y código de salida 0.
- Si algo falla, imprime `FALLA` en ese caso y termina con código 1.

Mientras no implementes nada, la salida es roja. Eso es normal: el *harness* no regala
aprobados.

### Cómo pedirle a la IA: el contrato C-R-E-O

En la Fase 2 no se le pide código "a ver qué sale": se le da un contrato. El formato
del curso es **C-R-E-O**:

- **C — Contexto:** lenguaje, compilador, archivos que ya existen y prohibiciones.
- **R — Rol:** qué especialista debe ser el modelo.
- **E — Especificación:** las firmas exactas de `api_sesionNN.h` y las reglas del reto,
  copiadas tal cual.
- **O — Output:** qué debe entregar (solo el `.c`, sin `main`, sin `printf` de depuración).

Ejemplo para la sesión 03:

```text
C — Contexto: C11, gcc -Wall -Wextra -Werror, Linux. El archivo api_sesion03.h
    ya existe y no se puede modificar. Prohibido usar system().
R — Rol: ingeniero de compiladores con experiencia en C y manejo de archivos.
E — Especificación: implementa exactamente
      int escribir_texto(const char *ruta, const char *texto);
      int contar_lineas(const char *ruta);
    Reglas: escribir_texto devuelve 0 si pudo escribir y -1 si no; contar_lineas
    devuelve -1 si el archivo no abre, cuenta la última línea sin salto y devuelve 0
    para un archivo vacío. Cierra el archivo en todos los caminos.
O — Output: solo el contenido de artesano_sesion03_c.c, con
    #include "api_sesion03.h", sin main() y sin printf.
```

Después compílalo: si no respeta la firma, el *harness* no compila; si la respeta pero
falla un caso, el *harness* te dice exactamente cuál.

---

## 1. Tipos, variables y `const`

**En una frase:** cada dato tiene un tipo que dice cuánto ocupa y qué operaciones
admite. `const` significa "esto no se modifica".

```c
int    cuenta = 0;        /* entero, normalmente 32 bits */
long   total = 0L;        /* entero más grande, 64 bits en x86-64 */
char   letra = 'A';       /* un solo carácter entre comillas simples */
size_t longitud = 0;      /* entero sin signo, el que devuelve strlen */

const char *mensaje = "HOLA";   /* apunta a texto que NO puedes modificar */
char copia[] = "HOLA";          /* copia modificable: 5 bytes, incluido '\0' */
```

**El detalle que más importa:** un `char` es un número pequeño (0–255) que también se
puede comparar como letra. Por eso `letra == 'A'` y `letra == 65` son lo mismo, y por
eso `'0'` (el carácter cero, valor 48) no es lo mismo que `0` (el número cero).

**El error clásico**

```c
char *s = "HOLA";
s[0] = 'X';          /* ¡error! el literal vive en memoria de solo lectura */
```

En ejecución termina con **`Segmentation fault`**. Si necesitas modificar el texto,
cópialo primero a un arreglo: `char s[] = "HOLA";`.

**Dónde aparece:** 01, 09, 18 (tamaños y tipos), 31–40 (`long`).

---

## 2. Funciones: por valor y por puntero

**En una frase:** C pasa los argumentos **por valor** (una copia). Para que una función
modifique algo de quien la llama, hay que pasarle la **dirección** con `&`.

```c
#include <stdio.h>

void dividir(int a, int b, int *cociente, int *resto) {
    *cociente = a / b;
    *resto    = a % b;
}

int main(void) {
    int c = 0, r = 0;
    dividir(17, 5, &c, &r);       /* pasas direcciones */
    printf("%d y %d\n", c, r);    /* 3 y 2 */
    return 0;
}
```

- `int *cociente` es "un puntero a entero": la función recibe la **dirección** de una
  variable y escribe en ella con `*cociente = ...`.
- Esto se llama **parámetro de salida** y el curso lo usa mucho (`int *error`, `int *n`,
  `int *contadores`).

**El error clásico**

```c
int error = 0;
evaluar(nodo, error);      /* mal: pasas el valor (una copia) */
evaluar(nodo, &error);     /* bien: pasas la dirección */
```

El compilador avisa: `warning: passing argument 2 ... makes pointer from integer without a cast`
(y con `-Werror`, se vuelve error).

**Dónde aparece:** 07 (`int *error`), 12, 25–27 (`int *n`, `int *etiquetas`).

---

## 3. Punteros

**En una frase:** un puntero guarda una **dirección de memoria**, no un valor.

```c
int x = 42;
int *p = &x;      /* p guarda la dirección de x */
printf("%d\n", *p);   /* 42: *p significa "lo que hay en la dirección p" */
*p = 7;               /* modifica x a través del puntero */
```

Tres operaciones y ya:

| Símbolo | Nombre | Qué hace |
| :--- | :--- | :--- |
| `&x` | dirección de | te da un puntero a `x` |
| `*p` | desreferencia | el valor que está en la dirección `p` |
| `p->campo` | acceso | atajo de `(*p).campo` para structs |

**Puntero a puntero.** `NodoToken **cabeza` significa "la dirección de un puntero a
nodo". Se usa cuando la función puede **cambiar el puntero original** (por ejemplo, al
insertar al inicio). En la sesión 02 ya no lo necesitas: `agregar_token` devuelve la
cabeza nueva. Pero lo verás en la teoría y en la 11, así que conviene reconocerlo:

Suponiendo `typedef struct Nodo { int valor; struct Nodo *sig; } Nodo;`:

```c
void insertar_al_inicio(Nodo **cabeza, int valor) {
    Nodo *nuevo = malloc(sizeof *nuevo);
    if (nuevo == NULL) return;
    nuevo->valor = valor;
    nuevo->sig = *cabeza;   /* el primer nodo actual */
    *cabeza = nuevo;        /* la cabeza ahora es el nuevo */
}
```

**El error clásico**

```c
int *p = NULL;
printf("%d\n", *p);   /* Segmentation fault */
```

Siempre comprueba `if (p == NULL)` antes de desreferenciar. Y si un puntero no apunta a
nada válido todavía, inicialízalo en `NULL`, no lo dejes "basura".

**Dónde aparece:** 01, 02, 11 (puntero a puntero), 13, 15, 20 (recorrer ámbitos).

---

## 4. Arreglos y cadenas

**En una frase:** un arreglo es una fila de elementos contiguos; una cadena en C es un
arreglo de `char` que termina en el byte `'\0'`.

```c
char saludo[] = "HOLA";   /* ocupa 5 bytes: H O L A \0 */
/*  saludo[0]='H' ... saludo[3]='A', saludo[4]='\0'  */

int largo = 0;
while (saludo[largo] != '\0') largo++;   /* strlen escrito a mano */
```

- `'\0'` es el número 0, no el carácter `'0'` (que vale 48).
- El largo **no** se guarda en ningún lado: se cuenta hasta encontrar `'\0'`.
- En una función, `char *s` y `char s[]` son lo mismo: reciben la dirección del primer
  carácter.

**Funciones de `<string.h>` que vas a usar**

| Función | Para qué | Ojo |
| :--- | :--- | :--- |
| `strlen(s)` | largo sin contar `'\0'` | recorre toda la cadena |
| `strcmp(a, b)` | comparar: `0` si son iguales | **no** uses `==` con cadenas |
| `strncpy(dst, src, n)` | copiar con límite | puede no terminar en `'\0'` |
| `snprintf(dst, cap, fmt, ...)` | formatear con límite | devuelve lo que *quiso* escribir |

```c
char buffer[32];
snprintf(buffer, sizeof buffer, "%s = %d", "x", 42);   /* "x = 42" */
```

**El error clásico**

```c
char destino[8];
strcpy(destino, "un texto demasiado largo");   /* desborda el buffer */
```

Con `snprintf` nunca te pasas del tamaño, y siempre queda `'\0'`:

```c
snprintf(destino, sizeof destino, "%s", "un texto demasiado largo");
```

**Dónde aparece:** 01, 05, 09, 11, 21–30 (`snprintf` para emitir líneas TAC).

---

## 5. `struct`, `typedef` y `enum`

**En una frase:** `struct` agrupa varios datos bajo un nombre; `typedef` le pone un
alias; `enum` define un conjunto de constantes con nombre.

```c
typedef enum { NODO_NUM, NODO_BINOP } TipoNodo;   /* 0 y 1 */

typedef struct ASTNode {
    TipoNodo tipo;
    int valor;
    char op;
    struct ASTNode *izq;   /* dentro del struct se usa "struct ASTNode" */
    struct ASTNode *der;
} ASTNode;                 /* alias: ya puedes escribir "ASTNode" */
```

Acceso: con `.` si tienes el struct, con `->` si tienes un puntero.

```c
ASTNode n;
n.valor = 5;              /* punto: variable directa */
ASTNode *p = &n;
p->valor = 7;             /* flecha: a través de un puntero */
```

**El error clásico**

```c
struct Punto { int x; int y; }   /* falta el ';' después de la llave */
```

gcc: `error: expected ';' after struct definition`. Y el otro clásico:

```c
ASTNode *p = crear_numero(3);
p.valor = 3;       /* mal: p es puntero */
p->valor = 3;      /* bien */
```

**Dónde aparece:** 02, 04, 11–20 (tabla de símbolos), 22, 30 (AST).

---

## 6. Memoria dinámica y listas

**En una frase:** `malloc` pide memoria en el *heap* en tiempo de ejecución; `free` la
devuelve. Todo lo que pides, lo devuelves.

```c
#include <stdlib.h>

NodoToken *nuevo = malloc(sizeof *nuevo);   /* tamaño de un nodo */
if (nuevo == NULL) {
    return NULL;                            /* no hay memoria */
}
nuevo->siguiente = NULL;
/* ... */
free(nuevo);                                /* devuélvela cuando ya no la uses */
```

- `sizeof *nuevo` es mejor que `sizeof(NodoToken)`: si cambias el tipo, sigue bien.
- `free(NULL)` es válido y no hace nada.
- Después de `free(p)`, `p` sigue guardando la misma dirección, pero ya no es tuya:
  **no la uses** (eso es *use-after-free*).

**Recorrer una lista**

```c
int contar(NodoToken *nodo) {
    int total = 0;
    while (nodo != NULL) {
        total++;
        nodo = nodo->siguiente;   /* avanza al siguiente */
    }
    return total;
}
```

**Agregar al final sin puntero a puntero** (lo que hace la sesión 02):

```c
#include <stdio.h>
#include <stdlib.h>

NodoToken *agregar(NodoToken *cabeza, const char *lexema) {
    NodoToken *nuevo = malloc(sizeof *nuevo);
    if (nuevo == NULL) return cabeza;

    /* copia el lexema con límite y termina en '\0' */
    snprintf(nuevo->lexema, sizeof nuevo->lexema, "%s", lexema);
    nuevo->siguiente = NULL;

    if (cabeza == NULL) return nuevo;   /* la lista estaba vacía */

    NodoToken *p = cabeza;
    while (p->siguiente != NULL) p = p->siguiente;
    p->siguiente = nuevo;
    return cabeza;                       /* la cabeza no cambió */
}
```

**El error clásico**

```c
NodoToken *p = cabeza;
while (p != NULL) {
    free(p);
    p = p->siguiente;   /* ¡p ya fue liberado! */
}
```

Primero guarda el siguiente, luego libera:

```c
while (cabeza != NULL) {
    NodoToken *siguiente = cabeza->siguiente;
    free(cabeza);
    cabeza = siguiente;
}
```

**Dónde aparece:** 02, 04 (árbol), 11, 15 (ámbitos).

---

## 7. Arreglos 2D y `char lineas[][64]`

**En una frase:** `char lineas[][64]` es un arreglo de filas de 64 caracteres; cada
`lineas[i]` es una fila que puedes pasar a `snprintf`.

**Cómo se ve en memoria:** imagina 3 filas de 64 bytes, una detrás de otra:

```
lineas[0] -> " _t0 = b * c "  (64 bytes)
lineas[1] -> " _t1 = a + _t0 "
lineas[2] -> ...
```

```c
#include <stdio.h>

void llenar(char lineas[][64], int max) {
    for (int i = 0; i < max; i++) {
        snprintf(lineas[i], 64, "linea %d", i);   /* escribe en la fila i */
    }
}
```

- En el parámetro **sí** se pone el `64` de la segunda dimensión; la primera se omite
  porque el compilador necesita saber cuánto mide cada fila para calcular `lineas[i]`.
- `lineas[i]` es un `char *` a la fila `i`: se usa como cualquier cadena.
- **No** es lo mismo que `char **`: ahí cada fila vive en otro lugar y tú tendrías que
  reservar cada una. `char lineas[][64]` es un bloque contiguo.

**El error clásico**

```c
void f(char **lineas);        /* no es lo que tienes */
void f(char lineas[][64]);    /* correcto */
```

gcc: `warning: passing argument 1 ... from incompatible pointer type`.

**Dónde aparece:** 22–30 (emisión de TAC).

---

## 8. Recursión

**En una frase:** una función recursiva se llama a sí misma con un problema **más
pequeño**, y tiene un caso base que la detiene.

```c
int evaluar(ASTNode *n) {
    if (n == NULL) return 0;              /* caso base 1: árbol vacío */
    if (n->tipo == NODO_NUM) return n->valor;   /* caso base 2: hoja */

    int a = evaluar(n->izq);   /* resuelve el subárbol izquierdo */
    int b = evaluar(n->der);   /* resuelve el subárbol derecho */
    switch (n->op) {
        case '+': return a + b;
        case '-': return a - b;
        case '*': return a * b;
        default:  return 0;
    }
}
```

Cada llamada guarda su estado en la **pila de llamadas**. Si el caso base no llega
nunca, la pila se desborda (*stack overflow*).

**Recorrido postorden** (primero hijos, después el nodo): es el orden natural para
calcular y para emitir TAC.

```c
void postorden(ASTNode *n, char *buf, int cap) {
    if (n == NULL) return;
    postorden(n->izq, buf, cap);
    postorden(n->der, buf, cap);
    /* aquí ya puedes usar el valor de n */
}
```

**El error clásico**

```c
int factorial(int n) {
    return n * factorial(n - 1);   /* falta el caso base: nunca termina */
}
```

**Dónde aparece:** 04, 05, 07, 10 (analizador), 22, 30, 40.

---

## 9. Archivos y códigos de salida

**En una frase:** un archivo se abre, se lee o escribe, y **siempre** se cierra. El
código de salida le dice al sistema si el programa terminó bien.

```c
#include <stdio.h>

int contar_lineas(const char *ruta) {
    FILE *f = fopen(ruta, "r");
    if (f == NULL) return -1;        /* no se pudo abrir */

    int lineas = 0;
    int c;
    int ultimo = '\n';
    while ((c = fgetc(f)) != EOF) {
        if (c == '\n') lineas++;
        ultimo = c;
    }
    if (ultimo != '\n') lineas++;    /* última línea sin salto */
    fclose(f);
    return lineas;
}
```

- `"r"` = leer, `"w"` = escribir (borra lo que había), `"a"` = agregar.
- `fopen` devuelve `NULL` si falla: compruébalo.
- `fgets(buffer, tam, f)` lee una línea y devuelve `NULL` al llegar al final.
- `fclose` devuelve 0 si todo salió bien.

**Códigos de salida:** `return 0` en `main` = éxito; cualquier otro número = error. Los
scripts y GitHub Actions usan ese número para decidir si siguen.

**El error clásico**

```c
FILE *f = fopen("datos.txt", "r");
char linea[100];
while (fgets(linea, sizeof linea, f) != NULL) {   /* f puede ser NULL */
    /* ... */
}
```

Comprueba `f` antes del bucle. Y no olvides `fclose(f)` en **todos** los caminos.

**Dónde aparece:** 03, 09 (diagnósticos), 39 (bitácoras).

---

## 10. `switch`, ciclos y operadores

**En una frase:** `switch` elige entre casos; `for`/`while` repiten; los operadores
tienen precedencia y `%` da el residuo.

Suponiendo que `error` es un parámetro `int *`:

```c
switch (n->op) {
    case '+': return a + b;
    case '-': return a - b;
    case '*': return a * b;
    case '/':
        if (b == 0) { *error = 1; return 0; }
        return a / b;
    default:
        *error = 2;
        return 0;
}
```

- Cada `case` termina en `break` o en `return`; si no, "cae" al siguiente.
- `default` atrapa lo que no encaja.
- `%` es el residuo: `17 % 5 == 2`. Con negativos, C trunca hacia cero.

**El error clásico**

```c
switch (op) {
    case '+': resultado = a + b;   /* sin break: sigue al case '-' */
    case '-': resultado = a - b; break;
}
```

**Dónde aparece:** 04, 06–08, 28, 31, 36.

---

## 11. Los errores de gcc que más vas a ver

| Mensaje (resumido) | Qué significa | Cómo se arregla |
| :--- | :--- | :--- |
| `expected ';' before ...` | falta un `;` en la línea anterior | cuéntalo; suele ser después de un `struct` o de una declaración |
| `'x' undeclared` | usaste una variable que no existe en ese bloque | declárala antes o revisa el nombre |
| `implicit declaration of function 'f'` | llamaste a `f` sin declararla | incluye la cabecera o declara el prototipo |
| `passing argument 2 ... makes pointer from integer` | pasaste un valor donde iba una dirección | usa `&variable` |
| `assignment to 'char *' from incompatible pointer type` | mezclaste `char *` con `char **` o similar | revisa el tipo de la firma |
| `control reaches end of non-void function` | una función con retorno no devuelve nada en algún camino | agrega `return` en todos los caminos |
| `unused parameter 'x'` | no usaste un parámetro y `-Werror` lo castiga | úsalo o escribe `(void)x;` (solo mientras desarrollas) |
| `format '%d' expects argument of type 'int'` | el formato no coincide con el tipo | usa `%ld` para `long`, `%s` para cadenas |
| `undefined reference to 'f'` | el enlazador no encuentra la función | ¿olvidaste implementarla o el archivo al compilar? |
| `Segmentation fault` (al ejecutar) | tocaste memoria que no es tuya: `NULL`, fuera de límites, ya liberada | revisa índices y punteros |

**Cómo leer el error:** gcc te da `archivo:línea:columna: error: mensaje`. Ve a esa
línea; el error real muchas veces está en la anterior.

---

## 12. Mapa: qué necesitas en cada sesión

| Sesión | Tema | C que necesitas |
| :---: | :--- | :--- |
| 01 | Punteros y metodología | §1, §3, §4 (recorrer hasta `'\0'`) |
| 02 | Lista de tokens | §5, §6 (`malloc`, lista, recorrer) |
| 03 | Archivos | §9 (`FILE*`, `fgets`/`fgetc`, `fclose`) |
| 04 | AST | §5 (`struct`/`enum`), §6 (`malloc`), §8, §10 (`switch`) |
| 05 | Recorridos | §4 (`snprintf`), §5, §8 (postorden) |
| 06 | Tipos | §5 (`enum`), §10 (`switch`) |
| 07 | Evaluación | §8 (recursión), §2 (`int *error`), §10 |
| 08 | Promoción | §5 (`enum`), §2 |
| 09 | Diagnósticos | §4 (`snprintf` y capacidad) |
| 10 | Mini-evaluador | §3, §4, §8 (analizador recursivo) |
| 11 | Tabla de símbolos | §5, §6 (`malloc`), §4 (`strcmp`) |
| 12 | Atributos y offsets | §5, §1 (`sizeof`) |
| 13 | Ámbitos | §5, §6, §3 |
| 14 | Declaración vs uso | §5, §4 (`strcmp`) |
| 15 | Bloques y ciclo de vida | §6 (`malloc`/`free`), §3 |
| 16 | Firmas y parámetros | §2, §5 (arreglo de structs) |
| 17 | Retornos | §4, §10 (rutas y `switch`) |
| 18 | Arreglos y límites | §1 (`sizeof`), §10 (`%`) |
| 19 | `struct` y offsets | §5, §1 |
| 20 | Hito 2 | §5, §6, §4 |
| 21 | Cuádruplos | §4 (`snprintf`), §2 (`int *contador`) |
| 22 | AST → TAC | §7 (`char lineas[][64]`), §8 (postorden) |
| 23 | Etiquetas y saltos | §4 (`snprintf`), §2 |
| 24 | `if`/`else` | §7, §10 |
| 25 | `while`/`for` | §7, §2 (`int *n`) |
| 26 | Llamadas | §7, §2, §4 |
| 27 | Arreglos en TAC | §7, §2 (`int *temporales`) |
| 28 | Plegado | §4, §10, §8 |
| 29 | Código muerto | §7, §4 (`strcmp`) |
| 30 | Hito 3 | §7, §8, §4 |
| 31 | Ensamblador | §4 (`strcmp`), §10 (`switch`) |
| 32 | Registros | §10 (arreglos e índices) |
| 33 | Spilling | §10, §2 (`const int *`) |
| 34 | Marco de pila | §1 (`%`, alineación) |
| 35 | Argumentos | §5 (`char` como selector), §2 |
| 36 | Comparaciones | §4, §10 |
| 37 | Pipeline | §4 (`snprintf`), §9 (formato de `.s`) |
| 38 | Enlace y ELF | §4 (recorrido de texto), §10 (`& 0xFF`) |
| 39 | Auditoría | §5, §4, §10 |
| 40 | Hito 4 | §7, §8, §4 (analizar texto) |

---

## 13. Ejercicios de calentamiento

Sin *harness* y sin entregar: son para calentar la mano antes del laboratorio. La
solución está plegada; intenta primero.

### 13.1 Invertir una cadena en su lugar

```c
void invertir(char *s);   /* "HOLA" -> "ALOH", sin malloc */
```

<details>
<summary>Solución</summary>

```c
void invertir(char *s) {
    if (s == NULL) return;
    int n = 0;
    while (s[n] != '\0') n++;
    for (int i = 0, j = n - 1; i < j; i++, j--) {
        char tmp = s[i];
        s[i] = s[j];
        s[j] = tmp;
    }
}
```

</details>

### 13.2 Contar sin `strlen`

```c
int largo(const char *s);   /* "abc" -> 3, NULL -> 0 */
```

<details>
<summary>Solución</summary>

```c
int largo(const char *s) {
    if (s == NULL) return 0;
    int n = 0;
    while (s[n] != '\0') n++;
    return n;
}
```

</details>

### 13.3 Un `struct` con función por puntero

```c
typedef struct { int x; int y; } Punto;
void mover(Punto *p, int dx, int dy);   /* mueve el punto original */
```

<details>
<summary>Solución</summary>

```c
void mover(Punto *p, int dx, int dy) {
    if (p == NULL) return;
    p->x += dx;
    p->y += dy;
}
```

</details>

### 13.4 Reservar un arreglo en el heap

```c
int *crear_ceros(int n);   /* devuelve n enteros en 0, o NULL */
void destruir(int *p);
```

<details>
<summary>Solución</summary>

```c
#include <stdlib.h>

int *crear_ceros(int n) {
    if (n <= 0) return NULL;
    int *p = malloc((size_t)n * sizeof *p);
    if (p == NULL) return NULL;
    for (int i = 0; i < n; i++) p[i] = 0;
    return p;
}

void destruir(int *p) {
    free(p);
}
```

</details>

### 13.5 Llenar un arreglo 2D de líneas

```c
void llenar(char lineas[][64], int max);   /* "linea 0", "linea 1", ... */
```

<details>
<summary>Solución</summary>

```c
#include <stdio.h>

void llenar(char lineas[][64], int max) {
    for (int i = 0; i < max; i++) {
        snprintf(lineas[i], 64, "linea %d", i);
    }
}
```

</details>

### 13.6 Recursión sobre un árbol

```c
int contar_nodos(ASTNode *n);   /* NULL -> 0 */
```

<details>
<summary>Solución</summary>

```c
int contar_nodos(ASTNode *n) {
    if (n == NULL) return 0;
    return 1 + contar_nodos(n->izq) + contar_nodos(n->der);
}
```

</details>

---

## Antes de cada laboratorio: checklist de 60 segundos

1. ¿Entendí **qué recibe** y **qué devuelve** la función del contrato?
2. ¿Mi archivo incluye `api_sesionNN.h` y **no** tiene `main()`?
3. ¿Inicialicé en `NULL` los punteros y comprobé los `malloc`?
4. ¿Cierro los archivos y libero la memoria que pido?
5. ¿Compila sin avisos? (Si hay un aviso, con `-Werror` es un error.)

Si algo no cuadra, vuelve a la sección del mapa (12) y lee el tema correspondiente.
