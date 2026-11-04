/* compilador.c - punto de entrada del compilador de Lenguajito.
 *
 * Hito 1: lectura del archivo, análisis léxico, análisis sintáctico y AST.
 * Hito 2: análisis semántico con ámbitos y ejecución con --run.
 */
#define _POSIX_C_SOURCE 200809L /* mkdtemp, rmdir */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

#include "ast.h"
#include "codegen.h"
#include "compilador.h"
#include "diagnosticos.h"
#include "lexer.h"
#include "parser.h"
#include "semantica.h"
#include "tac.h"

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

/* Escribe el ensamblador en un directorio temporal, lo ensambla y enlaza
 * con `as` y `gcc`, ejecuta el binario y reenvía su salida. Devuelve el
 * código de salida del programa ejecutado. */
static int ejecutar_binario(const char *ensamblador) {
    char dir[] = "/tmp/lenguajitoXXXXXX";
    if (mkdtemp(dir) == NULL) {
        fprintf(stderr, "error: no se pudo crear el directorio temporal\n");
        return 1;
    }

    char ruta_s[256], ruta_o[256], ruta_bin[256];
    snprintf(ruta_s, sizeof ruta_s, "%s/programa.s", dir);
    snprintf(ruta_o, sizeof ruta_o, "%s/programa.o", dir);
    snprintf(ruta_bin, sizeof ruta_bin, "%s/programa", dir);

    FILE *f = fopen(ruta_s, "wb");
    if (f == NULL) {
        fprintf(stderr, "error: no se pudo escribir %s\n", ruta_s);
        rmdir(dir);
        return 1;
    }
    fputs(ensamblador, f);
    fclose(f);

    char comando[2048];
    snprintf(comando, sizeof comando,
             "as --64 -o '%s' '%s' && gcc -o '%s' '%s' && '%s'",
             ruta_o, ruta_s, ruta_bin, ruta_o, ruta_bin);
    int estado = system(comando);

    remove(ruta_s);
    remove(ruta_o);
    remove(ruta_bin);
    rmdir(dir);

    if (estado < 0) {
        fprintf(stderr, "error: no se pudo ejecutar el binario\n");
        return 1;
    }
    if (WIFEXITED(estado)) return WEXITSTATUS(estado);
    return 1;
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

    if (errores.total == 0) {
        semantica_analizar(programa, &errores);
    }

    if (errores.total > 0) {
        errores_imprimir(&errores);
        nodo_liberar(programa);
        return 1;
    }

    if (strcmp(modo, "--check") == 0) {
        nodo_liberar(programa);
        return 0;
    }

    if (strcmp(modo, "--tac") == 0) {
        char *tac = tac_generar(programa);
        fputs(tac, stdout);
        free(tac);
        nodo_liberar(programa);
        return 0;
    }

    if (strcmp(modo, "--asm") == 0) {
        char *asm_texto = codegen_generar(programa);
        fputs(asm_texto, stdout);
        free(asm_texto);
        nodo_liberar(programa);
        return 0;
    }

    if (strcmp(modo, "--run") == 0) {
        char *asm_texto = codegen_generar(programa);
        int estado = ejecutar_binario(asm_texto);
        free(asm_texto);
        nodo_liberar(programa);
        return estado;
    }

    fprintf(stderr, "modo %s aún no implementado\n", modo);
    nodo_liberar(programa);
    return 1;
}
