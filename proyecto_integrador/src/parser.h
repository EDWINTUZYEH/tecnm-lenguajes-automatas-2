/* parser.h - análisis sintáctico descendente recursivo de Lenguajito.
 *
 * Gramática (docs/gramatica.md, sección 3):
 *   programa   := { sentencia } EOF
 *   sentencia  := declaracion | asignacion | seleccion | iteracion
 *               | impresion | bloque
 * Los errores de sintaxis se reportan como S01 y el parser se recupera
 * sincronizando con el siguiente ';' o '}' para reportar varios errores.
 */
#ifndef PARSER_H
#define PARSER_H

#include "ast.h"
#include "diagnosticos.h"
#include "lexer.h"

/* Construye el AST del programa. Ante errores de sintaxis devuelve un árbol
 * parcial y acumula los diagnósticos S01 en `errores`. */
Nodo *parser_analizar(const ListaTokens *tokens, ListaErrores *errores);

#endif /* PARSER_H */
