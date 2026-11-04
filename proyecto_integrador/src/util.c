/* util.c - utilidades compartidas: buffer dinámico y cadenas. */
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "util.h"

static void reservar(Buf *b, size_t necesario) {
    if (b->cap >= necesario) return;
    size_t cap = (b->cap == 0) ? 64 : b->cap;
    while (cap < necesario) cap *= 2;
    char *nuevos = realloc(b->datos, cap);
    if (nuevos == NULL) {
        fprintf(stderr, "error: memoria insuficiente\n");
        exit(2);
    }
    b->datos = nuevos;
    b->cap = cap;
}

void buf_iniciar(Buf *b) {
    b->datos = NULL;
    b->n = 0;
    b->cap = 0;
    reservar(b, 1);
    b->datos[0] = '\0';
}

void buf_liberar(Buf *b) {
    free(b->datos);
    b->datos = NULL;
    b->n = 0;
    b->cap = 0;
}

void buf_agrega(Buf *b, const char *formato, ...) {
    va_list ap;
    va_list copia;
    va_start(ap, formato);
    va_copy(copia, ap);
    int extra = vsnprintf(NULL, 0, formato, ap);
    va_end(ap);
    if (extra < 0) {
        va_end(copia);
        return;
    }
    reservar(b, b->n + (size_t)extra + 1);
    vsnprintf(b->datos + b->n, b->cap - b->n, formato, copia);
    va_end(copia);
    b->n += (size_t)extra;
}

void buf_agrega_char(Buf *b, char c) {
    reservar(b, b->n + 2);
    b->datos[b->n++] = c;
    b->datos[b->n] = '\0';
}

char *buf_terminar(Buf *b) {
    if (b->datos == NULL) buf_iniciar(b);
    char *resultado = b->datos;
    b->datos = NULL;
    b->n = 0;
    b->cap = 0;
    return resultado;
}

char *duplicar_cadena(const char *s) {
    size_t n = strlen(s);
    char *copia = malloc(n + 1);
    if (copia == NULL) {
        fprintf(stderr, "error: memoria insuficiente\n");
        exit(2);
    }
    memcpy(copia, s, n + 1);
    return copia;
}

int leer_numero(const char *s, int *valor) {
    if (s == NULL || s[0] == '\0') return 0;
    for (const char *p = s; *p != '\0'; p++) {
        if (*p < '0' || *p > '9') return 0;
    }
    *valor = (int)strtol(s, NULL, 10);
    return 1;
}
