/* codegen.h - generación de ensamblador x86-64 (AT&T) para Lenguajito.
 *
 * El backend traduce el AST directamente, un slot de pila de 4 bytes por
 * variable declarada. El ensamblador generado usa .text, .globl main,
 * prólogo, cuerpo y epílogo, y enlaza con printf(3).
 */
#ifndef CODEGEN_H
#define CODEGEN_H

#include "ast.h"

/* Devuelve el ensamblador como texto malloc'd (el llamador lo libera). */
char *codegen_generar(const Nodo *programa);

#endif /* CODEGEN_H */
