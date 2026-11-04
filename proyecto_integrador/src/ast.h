/* ast.h - árbol de sintaxis abstracta de Lenguajito.
 *
 * El formato de impresión está especificado en docs/gramatica.md, sección 4.
 */
#ifndef AST_H
#define AST_H

typedef enum {
    N_PROGRAMA,
    N_DECLARAR,
    N_ASIGNAR,
    N_SI,
    N_MIENTRAS,
    N_BLOQUE,
    N_IMPRIMIR,
    N_BIN,
    N_NEG,
    N_NUM,
    N_VAR
} TipoNodo;

typedef struct Nodo {
    TipoNodo tipo;
    int linea;
    int columna;

    int numero;             /* N_NUM */
    char operador[3];       /* N_BIN: + - * / < <= > >= == != */
    char *nombre;           /* N_DECLARAR, N_ASIGNAR, N_VAR */
    int tiene_init;         /* N_DECLARAR */

    struct Nodo *expr;      /* condición, expresión, inicializador */
    struct Nodo *cuerpo;    /* sentencia de `entonces` o del cuerpo de while */
    struct Nodo *sino;      /* rama `else` (puede ser NULL) */
    struct Nodo *izq;       /* N_BIN: hijo izquierdo */
    struct Nodo *der;       /* N_BIN: hijo derecho */

    struct Nodo **sentencias; /* N_PROGRAMA y N_BLOQUE */
    int n_sentencias;
    int cap_sentencias;
} Nodo;

Nodo *nodo_programa(int linea, int columna);
Nodo *nodo_declarar(const char *nombre, int linea, int columna);
Nodo *nodo_asignar(const char *nombre, int linea, int columna);
Nodo *nodo_si(int linea, int columna);
Nodo *nodo_mientras(int linea, int columna);
Nodo *nodo_bloque(int linea, int columna);
Nodo *nodo_imprimir(int linea, int columna);
Nodo *nodo_bin(const char *operador, Nodo *izq, Nodo *der, int linea, int columna);
Nodo *nodo_neg(Nodo *expr, int linea, int columna);
Nodo *nodo_num(int valor, int linea, int columna);
Nodo *nodo_var(const char *nombre, int linea, int columna);

void nodo_agregar_sentencia(Nodo *lista, Nodo *sentencia);
void nodo_liberar(Nodo *nodo);

/* Impresión en una sola línea con el formato de la especificación.
 * Devuelve una cadena reservada con malloc que el llamador debe liberar. */
char *ast_a_texto(const Nodo *nodo);

/* Devuelve 1 y escribe `valor` si la expresión es constante (números,
 * negación y operaciones con ambos lados constantes). Una división entre
 * cero constante no es evaluable: devuelve 0. */
int evaluar_constante(const Nodo *expr, int *valor);

#endif /* AST_H */
