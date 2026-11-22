/* tac.h - generación de código de tres direcciones (TAC) optimizado.
 *
 * El formato y las optimizaciones (plegado de constantes y eliminación de
 * código muerto) están especificados en docs/gramatica.md, sección 8.
 * Temporales: _t0, _t1, ... (únicos, no se reutilizan).
 */
#ifndef TAC_H
#define TAC_H

#include "ast.h"

/* Genera el TAC optimizado y lo devuelve como texto malloc'd
 * (el llamador lo libera). La AST se pliega de constantes previamente. */
char *tac_generar(Nodo *programa);

#endif /* TAC_H */
