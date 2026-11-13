/* interprete.h - ejecución directa del AST (Hito 2).
 *
 * Permite probar la semántica con --run antes de que exista el backend.
 * En el Hito 4 --run pasa a usar el binario generado.
 */
#ifndef INTERPRETE_H
#define INTERPRETE_H

#include "ast.h"

/* Ejecuta el programa y devuelve su código de salida (0 si termina bien,
 * 1 si hay un error en tiempo de ejecución, por ejemplo división entre cero). */
int interpretar(const Nodo *programa);

#endif /* INTERPRETE_H */
