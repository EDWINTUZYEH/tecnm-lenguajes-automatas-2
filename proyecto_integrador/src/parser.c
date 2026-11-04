/* parser.c - análisis sintáctico descendente recursivo de Lenguajito. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "parser.h"

typedef struct {
    const ListaTokens *tokens;
    int pos;
    ListaErrores *errores;
    int panico; /* evita cascadas de errores dentro de una sentencia */
} Parser;

static const Token *actual(const Parser *p) {
    return &p->tokens->items[p->pos];
}

static void avanzar(Parser *p) {
    if (p->tokens->items[p->pos].tipo != TOK_EOF) p->pos++;
}

static int es_lexema(const Token *t, const char *lexema) {
    return strcmp(t->lexema, lexema) == 0;
}

static void error_sintaxis(Parser *p, const char *mensaje) {
    if (p->panico) return;
    const Token *t = actual(p);
    error_agregar(p->errores, t->linea, t->columna, "S01", "%s", mensaje);
    p->panico = 1;
}

/* Si el token actual es `lexema` lo consume; si no, reporta S01. */
static int consumir(Parser *p, const char *lexema) {
    if (es_lexema(actual(p), lexema)) {
        avanzar(p);
        return 1;
    }
    char mensaje[128];
    snprintf(mensaje, sizeof mensaje, "se esperaba '%s'", lexema);
    error_sintaxis(p, mensaje);
    return 0;
}

/* Descarta tokens hasta después del siguiente ';' (sin salir del bloque). */
static void sincronizar(Parser *p) {
    while (actual(p)->tipo != TOK_EOF) {
        if (es_lexema(actual(p), ";")) {
            avanzar(p);
            return;
        }
        if (es_lexema(actual(p), "}")) return;
        avanzar(p);
    }
}

static Nodo *parse_expresion(Parser *p);
static Nodo *parse_bloque(Parser *p);
static Nodo *parse_sentencia(Parser *p);

static Nodo *parse_primaria(Parser *p) {
    const Token *t = actual(p);
    if (t->tipo == TOK_NUM) {
        int valor = (int)strtol(t->lexema, NULL, 10);
        avanzar(p);
        return nodo_num(valor, t->linea, t->columna);
    }
    if (t->tipo == TOK_ID) {
        avanzar(p);
        return nodo_var(t->lexema, t->linea, t->columna);
    }
    if (t->tipo == TOK_DELIM && es_lexema(t, "(")) {
        avanzar(p);
        Nodo *e = parse_expresion(p);
        consumir(p, ")");
        return e;
    }
    error_sintaxis(p, "se esperaba una expresión");
    return nodo_num(0, t->linea, t->columna);
}

static Nodo *parse_unaria(Parser *p) {
    const Token *t = actual(p);
    if (t->tipo == TOK_OP && es_lexema(t, "-")) {
        avanzar(p);
        Nodo *e = parse_primaria(p);
        return nodo_neg(e, t->linea, t->columna);
    }
    if (t->tipo == TOK_OP && es_lexema(t, "+")) {
        avanzar(p);
        return parse_primaria(p);
    }
    return parse_primaria(p);
}

static Nodo *parse_multiplicativa(Parser *p) {
    Nodo *izq = parse_unaria(p);
    for (;;) {
        const Token *t = actual(p);
        if (t->tipo == TOK_OP && (es_lexema(t, "*") || es_lexema(t, "/"))) {
            avanzar(p);
            Nodo *der = parse_unaria(p);
            izq = nodo_bin(t->lexema, izq, der, t->linea, t->columna);
        } else {
            return izq;
        }
    }
}

static Nodo *parse_aditiva(Parser *p) {
    Nodo *izq = parse_multiplicativa(p);
    for (;;) {
        const Token *t = actual(p);
        if (t->tipo == TOK_OP && (es_lexema(t, "+") || es_lexema(t, "-"))) {
            avanzar(p);
            Nodo *der = parse_multiplicativa(p);
            izq = nodo_bin(t->lexema, izq, der, t->linea, t->columna);
        } else {
            return izq;
        }
    }
}

static Nodo *parse_comparacion(Parser *p) {
    Nodo *izq = parse_aditiva(p);
    const Token *t = actual(p);
    if (t->tipo == TOK_OP &&
        (es_lexema(t, "<") || es_lexema(t, "<=") || es_lexema(t, ">") ||
         es_lexema(t, ">=") || es_lexema(t, "==") || es_lexema(t, "!="))) {
        avanzar(p);
        Nodo *der = parse_aditiva(p);
        return nodo_bin(t->lexema, izq, der, t->linea, t->columna);
    }
    return izq;
}

static Nodo *parse_expresion(Parser *p) {
    return parse_comparacion(p);
}

static Nodo *parse_declaracion(Parser *p) {
    avanzar(p); /* consume "int" */
    const Token *t = actual(p);
    if (t->tipo != TOK_ID) {
        error_sintaxis(p, "se esperaba un identificador después de 'int'");
        return NULL;
    }
    Nodo *n = nodo_declarar(t->lexema, t->linea, t->columna);
    avanzar(p);
    if (es_lexema(actual(p), "=")) {
        avanzar(p);
        n->tiene_init = 1;
        n->expr = parse_expresion(p);
    }
    consumir(p, ";");
    return n;
}

static Nodo *parse_asignacion(Parser *p) {
    const Token *t = actual(p);
    Nodo *n = nodo_asignar(t->lexema, t->linea, t->columna);
    avanzar(p);
    if (!consumir(p, "=")) return n;
    n->expr = parse_expresion(p);
    consumir(p, ";");
    return n;
}

static Nodo *parse_seleccion(Parser *p) {
    const Token *t = actual(p);
    avanzar(p); /* consume "if" */
    Nodo *n = nodo_si(t->linea, t->columna);
    consumir(p, "(");
    n->expr = parse_expresion(p);
    consumir(p, ")");
    n->cuerpo = parse_bloque(p);
    if (es_lexema(actual(p), "else")) {
        avanzar(p);
        n->sino = parse_bloque(p);
    }
    return n;
}

static Nodo *parse_iteracion(Parser *p) {
    const Token *t = actual(p);
    avanzar(p); /* consume "while" */
    Nodo *n = nodo_mientras(t->linea, t->columna);
    consumir(p, "(");
    n->expr = parse_expresion(p);
    consumir(p, ")");
    n->cuerpo = parse_bloque(p);
    return n;
}

static Nodo *parse_impresion(Parser *p) {
    const Token *t = actual(p);
    avanzar(p); /* consume "print" */
    Nodo *n = nodo_imprimir(t->linea, t->columna);
    consumir(p, "(");
    n->expr = parse_expresion(p);
    consumir(p, ")");
    consumir(p, ";");
    return n;
}

static Nodo *parse_bloque(Parser *p) {
    const Token *t = actual(p);
    Nodo *bloque = nodo_bloque(t->linea, t->columna);
    if (!consumir(p, "{")) return bloque;

    while (actual(p)->tipo != TOK_EOF && !es_lexema(actual(p), "}") &&
           p->errores->total < MAX_ERRORES) {
        Nodo *s = parse_sentencia(p);
        if (s != NULL) {
            nodo_agregar_sentencia(bloque, s);
        } else {
            if (!p->panico) {
                error_agregar(p->errores, actual(p)->linea, actual(p)->columna,
                              "S01", "sentencia inesperada");
            }
            sincronizar(p);
        }
        p->panico = 0;
    }

    if (actual(p)->tipo == TOK_EOF) {
        error_sintaxis(p, "se esperaba '}'");
    } else {
        avanzar(p); /* consume "}" */
    }
    return bloque;
}

static Nodo *parse_sentencia(Parser *p) {
    const Token *t = actual(p);
    if (t->tipo == TOK_KW) {
        if (es_lexema(t, "int")) return parse_declaracion(p);
        if (es_lexema(t, "if")) return parse_seleccion(p);
        if (es_lexema(t, "while")) return parse_iteracion(p);
        if (es_lexema(t, "print")) return parse_impresion(p);
    }
    if (t->tipo == TOK_ID) return parse_asignacion(p);
    if (t->tipo == TOK_DELIM && es_lexema(t, "{")) return parse_bloque(p);
    return NULL;
}

Nodo *parser_analizar(const ListaTokens *tokens, ListaErrores *errores) {
    Parser p;
    p.tokens = tokens;
    p.pos = 0;
    p.errores = errores;
    p.panico = 0;

    Nodo *programa = nodo_programa(1, 1);
    while (actual(&p)->tipo != TOK_EOF && errores->total < MAX_ERRORES) {
        if (es_lexema(actual(&p), "}")) {
            error_agregar(errores, actual(&p)->linea, actual(&p)->columna,
                          "S01", "llave '}' sin bloque abierto");
            avanzar(&p);
            continue;
        }
        Nodo *s = parse_sentencia(&p);
        if (s != NULL) {
            nodo_agregar_sentencia(programa, s);
        } else {
            if (!p.panico) {
                error_agregar(errores, actual(&p)->linea, actual(&p)->columna,
                              "S01", "sentencia inesperada");
            }
            sincronizar(&p);
        }
        p.panico = 0;
    }
    return programa;
}
