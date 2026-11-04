/* diagnosticos.c - registro de diagnósticos (errores) del compilador. */
#include <stdarg.h>
#include <stdio.h>
#include <string.h>

#include "diagnosticos.h"

void errores_iniciar(ListaErrores *errores, const char *archivo) {
    errores->total = 0;
    snprintf(errores->archivo, sizeof errores->archivo, "%s", archivo);
}

void error_agregar(ListaErrores *errores, int linea, int columna,
                   const char *codigo, const char *formato, ...) {
    if (errores->total >= MAX_ERRORES) return;

    Diagnostico *d = &errores->items[errores->total];
    d->linea = linea;
    d->columna = columna;
    snprintf(d->codigo, sizeof d->codigo, "%s", codigo);

    va_list ap;
    va_start(ap, formato);
    vsnprintf(d->mensaje, sizeof d->mensaje, formato, ap);
    va_end(ap);

    errores->total++;
}

void errores_imprimir(const ListaErrores *errores) {
    for (int i = 0; i < errores->total; i++) {
        const Diagnostico *d = &errores->items[i];
        printf("%s:%d:%d: error %s: %s\n",
               errores->archivo, d->linea, d->columna, d->codigo, d->mensaje);
    }
}
