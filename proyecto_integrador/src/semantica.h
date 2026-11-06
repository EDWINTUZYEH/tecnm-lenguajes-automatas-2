/* semantica.h - análisis semántico de Lenguajito (Hito 1).
 *
 * Alcance del Hito 1: ámbitos anidados por bloque y diagnóstico E01
 * (variable no declarada o leída antes de asignar valor).
 * Los demás diagnósticos (E02, E04) llegan en el Hito 2.
 */
#ifndef SEMANTICA_H
#define SEMANTICA_H

#include "ast.h"
#include "diagnosticos.h"

/* Revisa el programa y acumula diagnósticos en `errores`.
 * Devuelve 1 si se encontró al menos un error, 0 en caso contrario. */
int semantica_analizar(const Nodo *programa, ListaErrores *errores);

#endif /* SEMANTICA_H */
