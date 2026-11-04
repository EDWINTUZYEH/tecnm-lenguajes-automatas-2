/* diagnosticos.h - registro de diagnósticos (errores) del compilador.
 *
 * Formato impreso (especificado en docs/gramatica.md, sección 6):
 *   archivo:línea:columna: error EXX: mensaje
 * Se imprimen como máximo MAX_ERRORES diagnósticos.
 */
#ifndef DIAGNOSTICOS_H
#define DIAGNOSTICOS_H

#define MAX_ERRORES 20

typedef struct {
    int linea;
    int columna;
    char codigo[8];
    char mensaje[256];
} Diagnostico;

typedef struct {
    char archivo[1024];
    Diagnostico items[MAX_ERRORES];
    int total;
} ListaErrores;

void errores_iniciar(ListaErrores *errores, const char *archivo);
void error_agregar(ListaErrores *errores, int linea, int columna,
                   const char *codigo, const char *formato, ...);
void errores_imprimir(const ListaErrores *errores);

#endif /* DIAGNOSTICOS_H */
