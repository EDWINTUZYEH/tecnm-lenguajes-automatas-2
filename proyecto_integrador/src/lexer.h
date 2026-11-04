/* lexer.h - análisis léxico de Lenguajito.
 *
 * Convierte el texto fuente en una lista de tokens con línea y columna.
 * Los caracteres inválidos producen un diagnóstico S01 y el análisis continúa.
 */
#ifndef LEXER_H
#define LEXER_H

#include "diagnosticos.h"

typedef enum {
    TOK_EOF,
    TOK_KW,    /* int, if, else, while, print */
    TOK_ID,    /* identificadores */
    TOK_NUM,   /* literales enteros */
    TOK_OP,    /* + - * / < <= > >= == != = */
    TOK_DELIM  /* ( ) { } ; */
} TipoToken;

typedef struct {
    TipoToken tipo;
    char lexema[128];
    int linea;
    int columna;
} Token;

typedef struct {
    Token *items;
    int n;
    int cap;
} ListaTokens;

/* Tokeniza `fuente`; los errores léxicos se acumulan en `errores`.
 * Devuelve 1 si hubo errores léxicos, 0 si no. */
int lexer_analizar(const char *fuente, ListaErrores *errores, ListaTokens *salida);

/* Imprime los tokens con el formato LINEA:COLUMNA TIPO lexema. */
void lexer_imprimir(const ListaTokens *lista);

void tokens_liberar(ListaTokens *lista);

const char *lexer_tipo_nombre(TipoToken tipo);

#endif /* LEXER_H */
