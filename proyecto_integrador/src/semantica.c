/* semantica.c - análisis semántico de Lenguajito. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "semantica.h"

typedef struct {
    char nombre[128];
    int inicializada; /* ¿tiene valor asignado? */
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

/* Estado de inicialización de un símbolo visible, para comparar caminos. */
typedef struct {
    int ambito;
    int indice;
    int inicializada;
} EstadoSimbolo;

/* Fotografía de los estados de inicialización de todos los símbolos
 * visibles en un punto del análisis. */
typedef struct {
    EstadoSimbolo *items;
    int n;
} Instantanea;

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

/* Busca solo en el ámbito más interno. */
static Simbolo *buscar_local(Semantica *s, const char *nombre) {
    Ambito *a = &s->items[s->n - 1];
    for (int i = a->n - 1; i >= 0; i--) {
        if (strcmp(a->items[i].nombre, nombre) == 0) return &a->items[i];
    }
    return NULL;
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

/* Guarda el estado de inicialización de todos los símbolos visibles. */
static void instantanea_capturar(const Semantica *s, Instantanea *snap) {
    int total = 0;
    for (int k = 0; k < s->n; k++) total += s->items[k].n;

    snap->n = total;
    snap->items = NULL;
    if (total == 0) return;

    snap->items = malloc((size_t)total * sizeof *snap->items);
    if (snap->items == NULL) {
        fprintf(stderr, "error: memoria insuficiente\n");
        exit(2);
    }

    int p = 0;
    for (int k = 0; k < s->n; k++) {
        for (int i = 0; i < s->items[k].n; i++) {
            snap->items[p].ambito = k;
            snap->items[p].indice = i;
            snap->items[p].inicializada = s->items[k].items[i].inicializada;
            p++;
        }
    }
}

/* Restaura los estados guardados. Se usa antes de analizar la rama else y
 * al terminar un while, porque el cuerpo pudo no ejecutarse. */
static void instantanea_restaurar(Semantica *s, const Instantanea *snap) {
    for (int i = 0; i < snap->n; i++) {
        const EstadoSimbolo *e = &snap->items[i];
        s->items[e->ambito].items[e->indice].inicializada = e->inicializada;
    }
}

static void instantanea_liberar(Instantanea *snap) {
    free(snap->items);
    snap->items = NULL;
    snap->n = 0;
}

/* Une los estados de las dos ramas de un if. Una variable queda
 * definitivamente inicializada si ya lo estaba antes o si ambas ramas la
 * inicializan. Si no hay else, la rama "no" conserva el estado anterior. */
static void fusionar_caminos(Semantica *s, const Instantanea *antes,
                             const Instantanea *rama_si,
                             const Instantanea *rama_no) {
    for (int i = 0; i < antes->n; i++) {
        if (i >= rama_si->n || i >= rama_no->n) break;
        const EstadoSimbolo *e = &antes->items[i];
        int en_si = rama_si->items[i].inicializada;
        int en_no = rama_no->items[i].inicializada;
        int definitiva = e->inicializada || (en_si && en_no);
        s->items[e->ambito].items[e->indice].inicializada = definitiva;
    }
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
            Simbolo *existente = buscar_local(s, n->nombre);
            if (existente != NULL) {
                error_agregar(s->errores, n->linea, n->columna, "E02",
                              "redeclaración de '%s' en el mismo ámbito",
                              n->nombre);
            }
            if (n->tiene_init && n->expr != NULL) {
                revisar_expresion(s, n->expr);
            }
            if (existente == NULL) {
                declarar(s, n->nombre, n->tiene_init);
            }
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

        case N_SI: {
            Instantanea antes;
            instantanea_capturar(s, &antes);

            revisar_expresion(s, n->expr);

            revisar_sentencia(s, n->cuerpo);
            Instantanea fin_si;
            instantanea_capturar(s, &fin_si);

            /* La rama else debe analizarse con el estado previo al if. */
            instantanea_restaurar(s, &antes);
            if (n->sino != NULL) {
                revisar_sentencia(s, n->sino);
            }
            Instantanea fin_no;
            instantanea_capturar(s, &fin_no);

            fusionar_caminos(s, &antes, &fin_si, &fin_no);

            instantanea_liberar(&antes);
            instantanea_liberar(&fin_si);
            instantanea_liberar(&fin_no);
            break;
        }

        case N_MIENTRAS: {
            revisar_expresion(s, n->expr);

            Instantanea antes;
            instantanea_capturar(s, &antes);

            revisar_sentencia(s, n->cuerpo);

            /* El cuerpo puede ejecutarse cero veces: al salir del while solo
             * son definitivas las inicializaciones anteriores al ciclo. */
            instantanea_restaurar(s, &antes);
            instantanea_liberar(&antes);
            break;
        }

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

        case N_BIN: {
            revisar_expresion(s, n->izq);
            revisar_expresion(s, n->der);
            if (strcmp(n->operador, "/") == 0) {
                int divisor = 0;
                if (evaluar_constante(n->der, &divisor) && divisor == 0) {
                    error_agregar(s->errores, n->der->linea, n->der->columna,
                                  "E04", "división entre cero constante");
                }
            }
            break;
        }

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
