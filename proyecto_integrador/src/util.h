/* util.h - utilidades compartidas: buffer dinámico y cadenas. */
#ifndef UTIL_H
#define UTIL_H

#include <stddef.h>

/* Buffer de texto dinámico terminado en '\0'. */
typedef struct {
    char *datos;
    size_t n;
    size_t cap;
} Buf;

void buf_iniciar(Buf *b);
void buf_liberar(Buf *b);
void buf_agrega(Buf *b, const char *formato, ...);
void buf_agrega_char(Buf *b, char c);
char *buf_terminar(Buf *b); /* devuelve la cadena y libera la estructura */

char *duplicar_cadena(const char *s);

/* Devuelve 1 y escribe `valor` si `s` es un entero decimal. */
int leer_numero(const char *s, int *valor);

#endif /* UTIL_H */
