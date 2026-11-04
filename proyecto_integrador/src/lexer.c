/* lexer.c - análisis léxico de Lenguajito. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "lexer.h"

static const char *const PALABRAS_RESERVADAS[] = {
    "int", "if", "else", "while", "print"
};
#define NUM_RESERVADAS (sizeof PALABRAS_RESERVADAS / sizeof PALABRAS_RESERVADAS[0])

static int es_letra(int c) {
    return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || c == '_';
}

static int es_digito(int c) {
    return c >= '0' && c <= '9';
}

static int es_reservada(const char *texto) {
    for (size_t i = 0; i < NUM_RESERVADAS; i++) {
        if (strcmp(texto, PALABRAS_RESERVADAS[i]) == 0) return 1;
    }
    return 0;
}

static void agregar_token(ListaTokens *lista, TipoToken tipo,
                          const char *lexema, int linea, int columna) {
    if (lista->n == lista->cap) {
        int cap = (lista->cap == 0) ? 64 : lista->cap * 2;
        Token *nuevos = realloc(lista->items, (size_t)cap * sizeof *nuevos);
        if (nuevos == NULL) {
            fprintf(stderr, "error: memoria insuficiente\n");
            exit(2);
        }
        lista->items = nuevos;
        lista->cap = cap;
    }
    Token *t = &lista->items[lista->n++];
    t->tipo = tipo;
    snprintf(t->lexema, sizeof t->lexema, "%s", lexema);
    t->linea = linea;
    t->columna = columna;
}

int lexer_analizar(const char *fuente, ListaErrores *errores, ListaTokens *salida) {
    salida->items = NULL;
    salida->n = 0;
    salida->cap = 0;

    int i = 0;
    int linea = 1;
    int columna = 1;
    int hubo_error = 0;

    while (fuente[i] != '\0') {
        int c = (unsigned char)fuente[i];

        if (c == '\n') {
            i++;
            linea++;
            columna = 1;
            continue;
        }
        if (c == ' ' || c == '\t' || c == '\r') {
            i++;
            columna++;
            continue;
        }

        /* Comentario: // hasta el final de la línea. */
        if (c == '/' && fuente[i + 1] == '/') {
            while (fuente[i] != '\0' && fuente[i] != '\n') i++;
            continue;
        }

        int inicio_linea = linea;
        int inicio_columna = columna;

        /* Identificadores y palabras reservadas. */
        if (es_letra(c)) {
            int inicio = i;
            while (es_letra((unsigned char)fuente[i]) || es_digito((unsigned char)fuente[i])) {
                i++;
                columna++;
            }
            char texto[128];
            size_t largo = (size_t)(i - inicio);
            if (largo >= sizeof texto) largo = sizeof texto - 1;
            memcpy(texto, fuente + inicio, largo);
            texto[largo] = '\0';
            agregar_token(salida, es_reservada(texto) ? TOK_KW : TOK_ID,
                          texto, inicio_linea, inicio_columna);
            continue;
        }

        /* Números enteros. */
        if (es_digito(c)) {
            int inicio = i;
            while (es_digito((unsigned char)fuente[i])) {
                i++;
                columna++;
            }
            char texto[128];
            size_t largo = (size_t)(i - inicio);
            if (largo >= sizeof texto) largo = sizeof texto - 1;
            memcpy(texto, fuente + inicio, largo);
            texto[largo] = '\0';
            agregar_token(salida, TOK_NUM, texto, inicio_linea, inicio_columna);
            continue;
        }

        /* Operadores de dos caracteres. */
        char dos[3] = { (char)c, fuente[i + 1], '\0' };
        if ((c == '<' || c == '>' || c == '=' || c == '!') && fuente[i + 1] == '=') {
            agregar_token(salida, TOK_OP, dos, inicio_linea, inicio_columna);
            i += 2;
            columna += 2;
            continue;
        }

        /* Operadores de un carácter. */
        if (c == '+' || c == '-' || c == '*' || c == '/' ||
            c == '<' || c == '>' || c == '=') {
            char uno[2] = { (char)c, '\0' };
            agregar_token(salida, TOK_OP, uno, inicio_linea, inicio_columna);
            i++;
            columna++;
            continue;
        }

        /* Delimitadores. */
        if (c == '(' || c == ')' || c == '{' || c == '}' || c == ';') {
            char uno[2] = { (char)c, '\0' };
            agregar_token(salida, TOK_DELIM, uno, inicio_linea, inicio_columna);
            i++;
            columna++;
            continue;
        }

        /* Cualquier otra cosa es error léxico S01. */
        error_agregar(errores, inicio_linea, inicio_columna, "S01",
                      "carácter inválido '%c'", c);
        hubo_error = 1;
        i++;
        columna++;
    }

    agregar_token(salida, TOK_EOF, "", linea, columna);
    return hubo_error;
}

void lexer_imprimir(const ListaTokens *lista) {
    for (int i = 0; i < lista->n; i++) {
        const Token *t = &lista->items[i];
        if (t->tipo == TOK_EOF) {
            printf("%d:%d EOF\n", t->linea, t->columna);
        } else {
            printf("%d:%d %s %s\n", t->linea, t->columna,
                   lexer_tipo_nombre(t->tipo), t->lexema);
        }
    }
}

void tokens_liberar(ListaTokens *lista) {
    free(lista->items);
    lista->items = NULL;
    lista->n = 0;
    lista->cap = 0;
}

const char *lexer_tipo_nombre(TipoToken tipo) {
    switch (tipo) {
        case TOK_EOF:   return "EOF";
        case TOK_KW:    return "KW";
        case TOK_ID:    return "ID";
        case TOK_NUM:   return "NUM";
        case TOK_OP:    return "OP";
        case TOK_DELIM: return "DELIM";
    }
    return "?";
}
