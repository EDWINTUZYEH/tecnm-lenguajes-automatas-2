/* ast.c - árbol de sintaxis abstracta de Lenguajito. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "ast.h"
#include "util.h"

static Nodo *nodo_nuevo(TipoNodo tipo, int linea, int columna) {
    Nodo *n = calloc(1, sizeof *n);
    if (n == NULL) {
        fprintf(stderr, "error: memoria insuficiente\n");
        exit(2);
    }
    n->tipo = tipo;
    n->linea = linea;
    n->columna = columna;
    return n;
}

Nodo *nodo_programa(int linea, int columna) {
    return nodo_nuevo(N_PROGRAMA, linea, columna);
}

Nodo *nodo_declarar(const char *nombre, int linea, int columna) {
    Nodo *n = nodo_nuevo(N_DECLARAR, linea, columna);
    n->nombre = duplicar_cadena(nombre);
    return n;
}

Nodo *nodo_asignar(const char *nombre, int linea, int columna) {
    Nodo *n = nodo_nuevo(N_ASIGNAR, linea, columna);
    n->nombre = duplicar_cadena(nombre);
    return n;
}

Nodo *nodo_si(int linea, int columna) {
    return nodo_nuevo(N_SI, linea, columna);
}

Nodo *nodo_mientras(int linea, int columna) {
    return nodo_nuevo(N_MIENTRAS, linea, columna);
}

Nodo *nodo_bloque(int linea, int columna) {
    return nodo_nuevo(N_BLOQUE, linea, columna);
}

Nodo *nodo_imprimir(int linea, int columna) {
    return nodo_nuevo(N_IMPRIMIR, linea, columna);
}

Nodo *nodo_bin(const char *operador, Nodo *izq, Nodo *der, int linea, int columna) {
    Nodo *n = nodo_nuevo(N_BIN, linea, columna);
    snprintf(n->operador, sizeof n->operador, "%s", operador);
    n->izq = izq;
    n->der = der;
    return n;
}

Nodo *nodo_neg(Nodo *expr, int linea, int columna) {
    Nodo *n = nodo_nuevo(N_NEG, linea, columna);
    n->expr = expr;
    return n;
}

Nodo *nodo_num(int valor, int linea, int columna) {
    Nodo *n = nodo_nuevo(N_NUM, linea, columna);
    n->numero = valor;
    return n;
}

Nodo *nodo_var(const char *nombre, int linea, int columna) {
    Nodo *n = nodo_nuevo(N_VAR, linea, columna);
    n->nombre = duplicar_cadena(nombre);
    return n;
}

void nodo_agregar_sentencia(Nodo *lista, Nodo *sentencia) {
    if (lista->n_sentencias == lista->cap_sentencias) {
        int cap = (lista->cap_sentencias == 0) ? 8 : lista->cap_sentencias * 2;
        Nodo **nuevos = realloc(lista->sentencias, (size_t)cap * sizeof *nuevos);
        if (nuevos == NULL) {
            fprintf(stderr, "error: memoria insuficiente\n");
            exit(2);
        }
        lista->sentencias = nuevos;
        lista->cap_sentencias = cap;
    }
    lista->sentencias[lista->n_sentencias++] = sentencia;
}

void nodo_liberar(Nodo *nodo) {
    if (nodo == NULL) return;
    for (int i = 0; i < nodo->n_sentencias; i++) {
        nodo_liberar(nodo->sentencias[i]);
    }
    free(nodo->sentencias);
    nodo_liberar(nodo->expr);
    nodo_liberar(nodo->cuerpo);
    nodo_liberar(nodo->sino);
    nodo_liberar(nodo->izq);
    nodo_liberar(nodo->der);
    free(nodo->nombre);
    free(nodo);
}

static void imprimir_nodo(Buf *b, const Nodo *n) {
    switch (n->tipo) {
        case N_PROGRAMA:
            buf_agrega(b, "(programa");
            for (int i = 0; i < n->n_sentencias; i++) {
                buf_agrega_char(b, ' ');
                imprimir_nodo(b, n->sentencias[i]);
            }
            buf_agrega_char(b, ')');
            break;
        case N_BLOQUE:
            buf_agrega(b, "(bloque");
            for (int i = 0; i < n->n_sentencias; i++) {
                buf_agrega_char(b, ' ');
                imprimir_nodo(b, n->sentencias[i]);
            }
            buf_agrega_char(b, ')');
            break;
        case N_DECLARAR:
            buf_agrega(b, "(declarar %s", n->nombre);
            if (n->tiene_init) {
                buf_agrega_char(b, ' ');
                imprimir_nodo(b, n->expr);
            }
            buf_agrega_char(b, ')');
            break;
        case N_ASIGNAR:
            buf_agrega(b, "(asignar %s ", n->nombre);
            imprimir_nodo(b, n->expr);
            buf_agrega_char(b, ')');
            break;
        case N_SI:
            buf_agrega(b, "(si ");
            imprimir_nodo(b, n->expr);
            buf_agrega(b, " (entonces ");
            imprimir_nodo(b, n->cuerpo);
            buf_agrega_char(b, ')');
            if (n->sino != NULL) {
                buf_agrega(b, " (si_no ");
                imprimir_nodo(b, n->sino);
                buf_agrega_char(b, ')');
            }
            buf_agrega_char(b, ')');
            break;
        case N_MIENTRAS:
            buf_agrega(b, "(mientras ");
            imprimir_nodo(b, n->expr);
            buf_agrega_char(b, ' ');
            imprimir_nodo(b, n->cuerpo);
            buf_agrega_char(b, ')');
            break;
        case N_IMPRIMIR:
            buf_agrega(b, "(imprimir ");
            imprimir_nodo(b, n->expr);
            buf_agrega_char(b, ')');
            break;
        case N_BIN:
            buf_agrega(b, "(%s ", n->operador);
            imprimir_nodo(b, n->izq);
            buf_agrega_char(b, ' ');
            imprimir_nodo(b, n->der);
            buf_agrega_char(b, ')');
            break;
        case N_NEG:
            buf_agrega(b, "(neg ");
            imprimir_nodo(b, n->expr);
            buf_agrega_char(b, ')');
            break;
        case N_NUM:
            buf_agrega(b, "(num %d)", n->numero);
            break;
        case N_VAR:
            buf_agrega(b, "(var %s)", n->nombre);
            break;
    }
}

char *ast_a_texto(const Nodo *nodo) {
    Buf b;
    buf_iniciar(&b);
    imprimir_nodo(&b, nodo);
    return buf_terminar(&b);
}
