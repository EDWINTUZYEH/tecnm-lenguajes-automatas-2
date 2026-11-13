/* interprete.c - ejecución directa del AST (Hito 2). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "interprete.h"

typedef struct {
    char nombre[128];
    int valor;
} Variable;

typedef struct {
    Variable *items;
    int n;
    int cap;
} AmbitoValores;

typedef struct {
    AmbitoValores *items;
    int n;
    int cap;
    int error_runtime;
} Interprete;

static void ambito_apilar(Interprete *it) {
    if (it->n == it->cap) {
        int cap = (it->cap == 0) ? 8 : it->cap * 2;
        AmbitoValores *nuevos = realloc(it->items, (size_t)cap * sizeof *nuevos);
        if (nuevos == NULL) {
            fprintf(stderr, "error: memoria insuficiente\n");
            exit(2);
        }
        it->items = nuevos;
        it->cap = cap;
    }
    AmbitoValores *a = &it->items[it->n++];
    a->items = NULL;
    a->n = 0;
    a->cap = 0;
}

static void ambito_desapilar(Interprete *it) {
    AmbitoValores *a = &it->items[--it->n];
    free(a->items);
}

static Variable *buscar(Interprete *it, const char *nombre) {
    for (int k = it->n - 1; k >= 0; k--) {
        AmbitoValores *a = &it->items[k];
        for (int i = a->n - 1; i >= 0; i--) {
            if (strcmp(a->items[i].nombre, nombre) == 0) return &a->items[i];
        }
    }
    return NULL;
}

static void declarar(Interprete *it, const char *nombre, int valor) {
    AmbitoValores *a = &it->items[it->n - 1];
    if (a->n == a->cap) {
        int cap = (a->cap == 0) ? 8 : a->cap * 2;
        Variable *nuevos = realloc(a->items, (size_t)cap * sizeof *nuevos);
        if (nuevos == NULL) {
            fprintf(stderr, "error: memoria insuficiente\n");
            exit(2);
        }
        a->items = nuevos;
        a->cap = cap;
    }
    Variable *v = &a->items[a->n++];
    snprintf(v->nombre, sizeof v->nombre, "%s", nombre);
    v->valor = valor;
}

static int evaluar(Interprete *it, const Nodo *n) {
    switch (n->tipo) {
        case N_NUM:
            return n->numero;

        case N_VAR: {
            Variable *v = buscar(it, n->nombre);
            return (v != NULL) ? v->valor : 0;
        }

        case N_NEG:
            return -evaluar(it, n->expr);

        case N_BIN: {
            int a = evaluar(it, n->izq);
            int b = evaluar(it, n->der);
            const char *op = n->operador;
            if (strcmp(op, "+") == 0) return a + b;
            if (strcmp(op, "-") == 0) return a - b;
            if (strcmp(op, "*") == 0) return a * b;
            if (strcmp(op, "/") == 0) {
                if (b == 0) {
                    fprintf(stderr, "error en tiempo de ejecución: "
                                    "división entre cero\n");
                    it->error_runtime = 1;
                    return 0;
                }
                return a / b;
            }
            if (strcmp(op, "<") == 0) return a < b;
            if (strcmp(op, "<=") == 0) return a <= b;
            if (strcmp(op, ">") == 0) return a > b;
            if (strcmp(op, ">=") == 0) return a >= b;
            if (strcmp(op, "==") == 0) return a == b;
            if (strcmp(op, "!=") == 0) return a != b;
            return 0;
        }

        default:
            return 0;
    }
}

static void ejecutar_sentencia(Interprete *it, const Nodo *n) {
    if (it->error_runtime) return;

    switch (n->tipo) {
        case N_PROGRAMA:
        case N_BLOQUE:
            ambito_apilar(it);
            for (int i = 0; i < n->n_sentencias; i++) {
                ejecutar_sentencia(it, n->sentencias[i]);
            }
            ambito_desapilar(it);
            break;

        case N_DECLARAR: {
            int valor = 0;
            if (n->tiene_init && n->expr != NULL) valor = evaluar(it, n->expr);
            declarar(it, n->nombre, valor);
            break;
        }

        case N_ASIGNAR: {
            int valor = evaluar(it, n->expr);
            Variable *v = buscar(it, n->nombre);
            if (v != NULL) v->valor = valor;
            break;
        }

        case N_SI:
            if (evaluar(it, n->expr) != 0) {
                ejecutar_sentencia(it, n->cuerpo);
            } else if (n->sino != NULL) {
                ejecutar_sentencia(it, n->sino);
            }
            break;

        case N_MIENTRAS:
            while (!it->error_runtime && evaluar(it, n->expr) != 0) {
                ejecutar_sentencia(it, n->cuerpo);
            }
            break;

        case N_IMPRIMIR:
            printf("%d\n", evaluar(it, n->expr));
            break;

        default:
            break;
    }
}

int interpretar(const Nodo *programa) {
    Interprete it;
    it.items = NULL;
    it.n = 0;
    it.cap = 0;
    it.error_runtime = 0;

    ejecutar_sentencia(&it, programa);

    while (it.n > 0) ambito_desapilar(&it);
    free(it.items);

    if (it.error_runtime) return 1;
    return 0;
}
