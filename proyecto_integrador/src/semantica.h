/* semantica.h - análisis semántico de Lenguajito.
 *
 * Tabla de símbolos con ámbitos anidados y shadowing. Diagnósticos:
 *   E01  variable no declarada o leída antes de asignar valor
 *   E02  redeclaración en el mismo ámbito
 *   E04  división entre cero constante
 * Se reportan varios errores por pasada (máximo MAX_ERRORES).
 */
#ifndef SEMANTICA_H
#define SEMANTICA_H

#include "ast.h"
#include "diagnosticos.h"

/* Analiza `programa` y agrega los diagnósticos a `errores`.
 * Devuelve 1 si hubo errores semánticos, 0 si no. */
int semantica_analizar(const Nodo *programa, ListaErrores *errores);

#endif /* SEMANTICA_H */
