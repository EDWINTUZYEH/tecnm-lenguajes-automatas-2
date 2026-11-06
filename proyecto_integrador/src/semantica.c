/* semantica.c - análisis semántico de Lenguajito (Hito 1).
 *
 * Alcance del Hito 1 (tal como lo pide la DoD del hito):
 *   - Ámbitos anidados por bloque `{ }` con una pila propia. Al cerrar
 *     el bloque, sus símbolos dejan de existir.
 *   - Shadowing: un nombre declarado en un ámbito interno oculta al
 *     externo mientras el bloque esté activo.
 *   - E01 (variable no declarada): al leer o asignar un nombre que no
 *     existe en ningún ámbito visible.
 *   - E01 (leída antes de asignar valor): al leer un nombre declarado
 *     que nunca ha recibido un valor. Es un análisis conservador por
 *     ámbito: no distingue caminos de ejecución (si/while), así que
 *     puede aceptar un programa donde un camino deja la variable sin
 *     asignar. Esa precisión llega en el Hito 2.
 *
 * Queda para el Hito 2 (no se implementa aquí):
 *   - E02: redeclaración de un nombre en el mismo ámbito.
 *   - E04: división entre cero constante.
 *   - Análisis por caminos para la lectura antes de asignar.
 *
 * Los diagnósticos siguen el formato de docs/gramatica.md, sección 6,
 * y se acumulan hasta MAX_ERRORES (20) en una sola pasada.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "semantica.h"

#define NOMBRE_MAX 128

typedef struct {
    char nombre[NOMBRE_MAX];
    int inicializada;   /* 1 si tiene un valor asignado */
} Simbolo;

typedef struct {
    Simbolo *items;
    int n;
    int cap;
} Ambito;

typedef struct {
    Ambito *items;
    int n;
    int cap;
    ListaErrores *errores;
} Semantica;

static void ambito_apilar(Semantica *s) {
    if (s->n == s->cap) {
        int cap = (s->cap == 0) ? 8 : s->cap * 2;
        Ambito *nuevos = realloc(s->items, (size_t)cap * sizeof *nuevos);
        if (nuevos == NULL) {
            fprintf(stderr, "error: memoria insuficiente\n");
            exit(2);
        }
        s->items = nuevos;
        s->cap = cap;
    }
    Ambito *a = &s->items[s->n++];
    a->items = NULL;
    a->n = 0;
    a->cap = 0;
}

static void ambito_desapilar(Semantica *s) {
    Ambito *a = &s->items[--s->n];
    free(a->items);
}

/* Busca del ámbito más interno al más externo (shadowing). */
static Simbolo *buscar(Semantica *s, const char *nombre) {
    for (int k = s->n - 1; k >= 0; k--) {
        Ambito *a = &s->items[k];
        for (int i = a->n - 1; i >= 0; i--) {
            if (strcmp(a->items[i].nombre, nombre) == 0) return &a->items[i];
        }
    }
    return NULL;
}

static void declarar(Semantica *s, const char *nombre, int inicializada) {
    Ambito *a = &s->items[s->n - 1];
    if (a->n == a->cap) {
        int cap = (a->cap == 0) ? 8 : a->cap * 2;
        Simbolo *nuevos = realloc(a->items, (size_t)cap * sizeof *nuevos);
        if (nuevos == NULL) {
            fprintf(stderr, "error: memoria insuficiente\n");
            exit(2);
        }
        a->items = nuevos;
        a->cap = cap;
    }
    Simbolo *simbolo = &a->items[a->n++];
    snprintf(simbolo->nombre, sizeof simbolo->nombre, "%s", nombre);
    simbolo->inicializada = inicializada;
}

static void revisar_expresion(Semantica *s, const Nodo *n);

static void revisar_sentencia(Semantica *s, const Nodo *n) {
    if (s->errores->total >= MAX_ERRORES) return;

    switch (n->tipo) {
        case N_PROGRAMA:
        case N_BLOQUE:
            ambito_apilar(s);
            for (int i = 0; i < n->n_sentencias; i++) {
                revisar_sentencia(s, n->sentencias[i]);
            }
            ambito_desapilar(s);
            break;

        case N_DECLARAR: {
            /* El inicializador se revisa antes de que el nombre entre al
             * ámbito: `int x = x;` usa x sin declarar (E01), igual que
             * manda una lectura arriba-abajo. */
            if (n->tiene_init && n->expr != NULL) {
                revisar_expresion(s, n->expr);
            }
            /* Si el nombre ya existe en este ámbito, la nueva declaración
             * lo oculta para las búsquedas posteriores. E02 (redeclaración
             * en el mismo ámbito) se reporta hasta el Hito 2. */
            declarar(s, n->nombre, n->tiene_init);
            break;
        }

        case N_ASIGNAR: {
            Simbolo *simbolo = buscar(s, n->nombre);
            if (simbolo == NULL) {
                error_agregar(s->errores, n->linea, n->columna, "E01",
                              "variable no declarada '%s'", n->nombre);
            }
            if (n->expr != NULL) revisar_expresion(s, n->expr);
            if (simbolo != NULL) simbolo->inicializada = 1;
            break;
        }

        case N_SI:
            revisar_expresion(s, n->expr);
            revisar_sentencia(s, n->cuerpo);
            if (n->sino != NULL) revisar_sentencia(s, n->sino);
            break;

        case N_MIENTRAS:
            revisar_expresion(s, n->expr);
            revisar_sentencia(s, n->cuerpo);
            break;

        case N_IMPRIMIR:
            revisar_expresion(s, n->expr);
            break;

        default:
            break;
    }
}

static void revisar_expresion(Semantica *s, const Nodo *n) {
    if (s->errores->total >= MAX_ERRORES) return;

    switch (n->tipo) {
        case N_NUM:
            break;

        case N_VAR: {
            Simbolo *simbolo = buscar(s, n->nombre);
            if (simbolo == NULL) {
                error_agregar(s->errores, n->linea, n->columna, "E01",
                              "variable no declarada '%s'", n->nombre);
            } else if (!simbolo->inicializada) {
                error_agregar(s->errores, n->linea, n->columna, "E01",
                              "variable '%s' leída antes de asignar valor",
                              n->nombre);
            }
            break;
        }

        case N_NEG:
            revisar_expresion(s, n->expr);
            break;

        case N_BIN:
            revisar_expresion(s, n->izq);
            revisar_expresion(s, n->der);
            break;

        default:
            break;
    }
}

int semantica_analizar(const Nodo *programa, ListaErrores *errores) {
    Semantica s;
    s.items = NULL;
    s.n = 0;
    s.cap = 0;
    s.errores = errores;

    revisar_sentencia(&s, programa);

    while (s.n > 0) ambito_desapilar(&s);
    free(s.items);

    return errores->total > 0;
}
