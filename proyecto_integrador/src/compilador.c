/* compilador.c - punto de entrada del compilador de Lenguajito.
 *
 * Hito 1: lectura del archivo, análisis léxico, análisis sintáctico,
 * AST y análisis semántico básico (E01, variable no declarada).
 * Los demás modos se habilitan en los hitos siguientes.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "ast.h"
#include "compilador.h"
#include "diagnosticos.h"
#include "lexer.h"
#include "parser.h"
#include "semantica.h"

/* Lee el archivo completo. Devuelve NULL si no se puede abrir. */
static char *leer_archivo(const char *ruta) {
    FILE *f = fopen(ruta, "rb");
    if (f == NULL) return NULL;

    size_t cap = 4096;
    size_t n = 0;
    char *datos = malloc(cap);
    if (datos == NULL) {
        fclose(f);
        return NULL;
    }
    for (;;) {
        if (n + 1024 + 1 > cap) {
            cap *= 2;
            char *nuevos = realloc(datos, cap);
            if (nuevos == NULL) {
                free(datos);
                fclose(f);
                return NULL;
            }
            datos = nuevos;
        }
        size_t leidos = fread(datos + n, 1, 1024, f);
        n += leidos;
        if (leidos < 1024) break;
    }
    fclose(f);
    datos[n] = '\0';
    return datos;
}

int compilar(const char *ruta, const char *modo) {
    char *fuente = leer_archivo(ruta);
    if (fuente == NULL) {
        fprintf(stderr, "%s: no se pudo abrir el archivo\n", ruta);
        return 1;
    }

    ListaErrores errores;
    errores_iniciar(&errores, ruta);

    ListaTokens tokens;
    lexer_analizar(fuente, &errores, &tokens);
    free(fuente);

    if (strcmp(modo, "--tokens") == 0) {
        lexer_imprimir(&tokens);
        errores_imprimir(&errores);
        int hubo_error = (errores.total > 0);
        tokens_liberar(&tokens);
        return hubo_error ? 1 : 0;
    }

    Nodo *programa = parser_analizar(&tokens, &errores);
    tokens_liberar(&tokens);

    if (strcmp(modo, "--ast") == 0) {
        if (errores.total > 0) {
            errores_imprimir(&errores);
            nodo_liberar(programa);
            return 1;
        }
        char *texto = ast_a_texto(programa);
        puts(texto);
        free(texto);
        nodo_liberar(programa);
        return 0;
    }

    /* De aquí en adelante solo queda --check; los demás modos llegan en
     * los hitos siguientes. Si hubo errores de sintaxis ya se reportaron
     * arriba y el AST no es confiable. */
    if (strcmp(modo, "--check") == 0) {
        if (errores.total == 0) {
            semantica_analizar(programa, &errores);
        }
        if (errores.total > 0) {
            errores_imprimir(&errores);
            nodo_liberar(programa);
            return 1;
        }
        nodo_liberar(programa);
        return 0;
    }

    if (errores.total > 0) {
        errores_imprimir(&errores);
        nodo_liberar(programa);
        return 1;
    }

    fprintf(stderr, "modo %s aún no implementado (llega en un hito posterior)\n",
            modo);
    nodo_liberar(programa);
    return 1;
}
