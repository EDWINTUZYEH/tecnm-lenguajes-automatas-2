/* tac.c - generación de código de tres direcciones optimizado.
 *
 * Pipeline:
 *   1. Plegado de constantes sobre el AST (ast_plegar_constantes).
 *   2. Generación estructural de instrucciones TAC (lista dinámica).
 *   3. Propagación de constantes a nivel TAC (sustitución + plegado).
 *   4. Eliminación de código muerto: temporales _t asignados que nadie lee
 *      se eliminan (punto fijo).
 *   5. Serialización al formato de la sección 8 del contrato.
 *
 * En las etiquetas y en los saltos se limpia el entorno de constantes:
 * el control puede llegar desde varios caminos, así que propagar ahí no
 * sería correcto.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "tac.h"
#include "diagnosticos.h"
#include "util.h"

#define TAM_NOMBRE 128
#define MAX_ENTRADAS_ENV 256

typedef enum {
    TAC_COPIA,     /* destino = a */
    TAC_BIN,       /* destino = a op b */
    TAC_NEG,       /* destino = -a */
    TAC_GOTO,      /* goto Lx */
    TAC_IF_FALSO,  /* ifFalso a goto Lx */
    TAC_ETIQUETA,  /* Lx: */
    TAC_PRINT      /* print a */
} TipoInstr;

typedef struct {
    TipoInstr tipo;
    char destino[TAM_NOMBRE];
    char a[TAM_NOMBRE];
    char b[TAM_NOMBRE];
    char op[3];
    int etiqueta;
} Instr;

typedef struct {
    Instr *items;
    int n;
    int cap;
    int sig_temp;
    int sig_etiqueta;
} TAC;

typedef struct {
    int es_num;
    int valor;
    char nombre[TAM_NOMBRE];
} Operando;

static Operando operando_num(int valor) {
    Operando op;
    op.es_num = 1;
    op.valor = valor;
    op.nombre[0] = '\0';
    return op;
}

static Operando operando_nombre(const char *nombre) {
    Operando op;
    op.es_num = 0;
    op.valor = 0;
    snprintf(op.nombre, sizeof op.nombre, "%s", nombre);
    return op;
}

static void tac_emitir(TAC *t, Instr instr) {
    if (t->n == t->cap) {
        int cap = (t->cap == 0) ? 64 : t->cap * 2;
        Instr *nuevos = realloc(t->items, (size_t)cap * sizeof *nuevos);
        if (nuevos == NULL) {
            fprintf(stderr, "error: memoria insuficiente\n");
            exit(2);
        }
        t->items = nuevos;
        t->cap = cap;
    }
    t->items[t->n++] = instr;
}

static int tac_nueva_etiqueta(TAC *t) {
    return ++t->sig_etiqueta;
}

static Operando tac_nuevo_temp(TAC *t) {
    char nombre[TAM_NOMBRE];
    snprintf(nombre, sizeof nombre, "_t%d", t->sig_temp++);
    return operando_nombre(nombre);
}

static void emitir_simple(TAC *t, TipoInstr tipo, const char *destino, const char *a) {
    Instr i;
    memset(&i, 0, sizeof i);
    i.tipo = tipo;
    snprintf(i.destino, sizeof i.destino, "%s", destino);
    snprintf(i.a, sizeof i.a, "%s", a);
    tac_emitir(t, i);
}

static void emitir_bin(TAC *t, const char *destino,
                       const Operando *a, const Operando *b, const char *op) {
    Instr i;
    memset(&i, 0, sizeof i);
    i.tipo = TAC_BIN;
    snprintf(i.destino, sizeof i.destino, "%s", destino);
    if (a->es_num) snprintf(i.a, sizeof i.a, "%d", a->valor);
    else snprintf(i.a, sizeof i.a, "%s", a->nombre);
    if (b->es_num) snprintf(i.b, sizeof i.b, "%d", b->valor);
    else snprintf(i.b, sizeof i.b, "%s", b->nombre);
    snprintf(i.op, sizeof i.op, "%s", op);
    tac_emitir(t, i);
}

static void emitir_operando(TAC *t, TipoInstr tipo, const char *a, int etiqueta) {
    Instr i;
    memset(&i, 0, sizeof i);
    i.tipo = tipo;
    if (a != NULL) snprintf(i.a, sizeof i.a, "%s", a);
    i.etiqueta = etiqueta;
    tac_emitir(t, i);
}

static void operando_a_cadena(const Operando *op, char destino[TAM_NOMBRE]) {
    if (op->es_num) snprintf(destino, TAM_NOMBRE, "%d", op->valor);
    else snprintf(destino, TAM_NOMBRE, "%s", op->nombre);
}

static Operando gen_expr(Nodo *n, TAC *t);
static void gen_sentencia(Nodo *n, TAC *t);

static int calcular_bin(int a, int b, const char *op, int *resultado) {
    if (strcmp(op, "+") == 0) { *resultado = a + b; return 1; }
    if (strcmp(op, "-") == 0) { *resultado = a - b; return 1; }
    if (strcmp(op, "*") == 0) { *resultado = a * b; return 1; }
    if (strcmp(op, "/") == 0) {
        if (b == 0) return 0;
        *resultado = a / b;
        return 1;
    }
    if (strcmp(op, "<") == 0)  { *resultado = a < b;  return 1; }
    if (strcmp(op, "<=") == 0) { *resultado = a <= b; return 1; }
    if (strcmp(op, ">") == 0)  { *resultado = a > b;  return 1; }
    if (strcmp(op, ">=") == 0) { *resultado = a >= b; return 1; }
    if (strcmp(op, "==") == 0) { *resultado = a == b; return 1; }
    if (strcmp(op, "!=") == 0) { *resultado = a != b; return 1; }
    return 0;
}

static Operando gen_expr(Nodo *n, TAC *t) {
    switch (n->tipo) {
        case N_NUM:
            return operando_num(n->numero);

        case N_VAR:
            return operando_nombre(n->nombre);

        case N_NEG: {
            Operando e = gen_expr(n->expr, t);
            if (e.es_num) return operando_num(-e.valor);
            Operando temp = tac_nuevo_temp(t);
            Instr i;
            memset(&i, 0, sizeof i);
            i.tipo = TAC_NEG;
            snprintf(i.destino, sizeof i.destino, "%s", temp.nombre);
            snprintf(i.a, sizeof i.a, "%s", e.nombre);
            tac_emitir(t, i);
            return temp;
        }

        case N_BIN: {
            Operando izq = gen_expr(n->izq, t);
            Operando der = gen_expr(n->der, t);
            if (izq.es_num && der.es_num) {
                int resultado = 0;
                if (calcular_bin(izq.valor, der.valor, n->operador, &resultado)) {
                    return operando_num(resultado);
                }
            }
            Operando temp = tac_nuevo_temp(t);
            emitir_bin(t, temp.nombre, &izq, &der, n->operador);
            return temp;
        }

        default:
            return operando_num(0);
    }
}

static void gen_sentencia(Nodo *n, TAC *t) {
    switch (n->tipo) {
        case N_PROGRAMA:
        case N_BLOQUE:
            for (int i = 0; i < n->n_sentencias; i++) {
                gen_sentencia(n->sentencias[i], t);
            }
            break;

        case N_DECLARAR:
            if (n->tiene_init && n->expr != NULL) {
                Operando e = gen_expr(n->expr, t);
                char texto[TAM_NOMBRE];
                operando_a_cadena(&e, texto);
                emitir_simple(t, TAC_COPIA, n->nombre, texto);
            }
            break;

        case N_ASIGNAR: {
            Operando e = gen_expr(n->expr, t);
            char texto[TAM_NOMBRE];
            operando_a_cadena(&e, texto);
            emitir_simple(t, TAC_COPIA, n->nombre, texto);
            break;
        }

        case N_SI: {
            Operando cond = gen_expr(n->expr, t);
            char texto[TAM_NOMBRE];
            operando_a_cadena(&cond, texto);
            if (n->sino != NULL) {
                int etiqueta_sino = tac_nueva_etiqueta(t);
                int etiqueta_fin = tac_nueva_etiqueta(t);
                emitir_operando(t, TAC_IF_FALSO, texto, etiqueta_sino);
                gen_sentencia(n->cuerpo, t);
                emitir_operando(t, TAC_GOTO, NULL, etiqueta_fin);
                Instr etiqueta;
                memset(&etiqueta, 0, sizeof etiqueta);
                etiqueta.tipo = TAC_ETIQUETA;
                etiqueta.etiqueta = etiqueta_sino;
                tac_emitir(t, etiqueta);
                gen_sentencia(n->sino, t);
                memset(&etiqueta, 0, sizeof etiqueta);
                etiqueta.tipo = TAC_ETIQUETA;
                etiqueta.etiqueta = etiqueta_fin;
                tac_emitir(t, etiqueta);
            } else {
                int etiqueta_fin = tac_nueva_etiqueta(t);
                emitir_operando(t, TAC_IF_FALSO, texto, etiqueta_fin);
                gen_sentencia(n->cuerpo, t);
                Instr etiqueta;
                memset(&etiqueta, 0, sizeof etiqueta);
                etiqueta.tipo = TAC_ETIQUETA;
                etiqueta.etiqueta = etiqueta_fin;
                tac_emitir(t, etiqueta);
            }
            break;
        }

        case N_MIENTRAS: {
            int etiqueta_inicio = tac_nueva_etiqueta(t);
            int etiqueta_fin = tac_nueva_etiqueta(t);
            Instr etiqueta;
            memset(&etiqueta, 0, sizeof etiqueta);
            etiqueta.tipo = TAC_ETIQUETA;
            etiqueta.etiqueta = etiqueta_inicio;
            tac_emitir(t, etiqueta);
            Operando cond = gen_expr(n->expr, t);
            char texto[TAM_NOMBRE];
            operando_a_cadena(&cond, texto);
            emitir_operando(t, TAC_IF_FALSO, texto, etiqueta_fin);
            gen_sentencia(n->cuerpo, t);
            emitir_operando(t, TAC_GOTO, NULL, etiqueta_inicio);
            memset(&etiqueta, 0, sizeof etiqueta);
            etiqueta.tipo = TAC_ETIQUETA;
            etiqueta.etiqueta = etiqueta_fin;
            tac_emitir(t, etiqueta);
            break;
        }

        case N_IMPRIMIR: {
            Operando e = gen_expr(n->expr, t);
            char texto[TAM_NOMBRE];
            operando_a_cadena(&e, texto);
            Instr i;
            memset(&i, 0, sizeof i);
            i.tipo = TAC_PRINT;
            snprintf(i.a, sizeof i.a, "%s", texto);
            tac_emitir(t, i);
            break;
        }

        default:
            break;
    }
}

/* ------------------------------------------------------------------ */
/* Optimización                                                        */
/* ------------------------------------------------------------------ */

typedef struct {
    char nombre[TAM_NOMBRE];
    int definido;
    int valor;
} EntradaEnv;

typedef struct {
    EntradaEnv items[MAX_ENTRADAS_ENV];
    int n;
} Env;

static EntradaEnv *env_buscar(Env *env, const char *nombre) {
    for (int i = 0; i < env->n; i++) {
        if (strcmp(env->items[i].nombre, nombre) == 0) return &env->items[i];
    }
    return NULL;
}

static void env_fijar(Env *env, const char *nombre, int definido, int valor) {
    EntradaEnv *e = env_buscar(env, nombre);
    if (!definido) {
        if (e != NULL) {
            env->items[e - env->items] =
                env->items[env->n - 1]; /* borrado por intercambio */
            env->n--;
        }
        return;
    }
    if (e != NULL) {
        e->definido = 1;
        e->valor = valor;
        return;
    }
    if (env->n == MAX_ENTRADAS_ENV) return; /* lleno: no registrar */
    snprintf(env->items[env->n].nombre, TAM_NOMBRE, "%s", nombre);
    env->items[env->n].definido = 1;
    env->items[env->n].valor = valor;
    env->n++;
}

static void env_limpiar(Env *env) {
    env->n = 0;
}

/* Si `campo` contiene un nombre con constante conocida, lo sustituye por
 * el literal. */
static void env_sustituir(Env *env, char campo[TAM_NOMBRE]) {
    int dummy;
    if (leer_numero(campo, &dummy)) return; /* ya es literal */
    EntradaEnv *e = env_buscar(env, campo);
    if (e != NULL && e->definido) {
        snprintf(campo, TAM_NOMBRE, "%d", e->valor);
    }
}

static void optimizar_propagacion(TAC *t) {
    Env env;
    env.n = 0;

    for (int i = 0; i < t->n; i++) {
        Instr *instr = &t->items[i];
        switch (instr->tipo) {
            case TAC_ETIQUETA:
            case TAC_GOTO:
                env_limpiar(&env);
                break;

            case TAC_COPIA:
                env_sustituir(&env, instr->a);
                {
                    int v;
                    if (leer_numero(instr->a, &v)) {
                        env_fijar(&env, instr->destino, 1, v);
                    } else {
                        env_fijar(&env, instr->destino, 0, 0);
                    }
                }
                break;

            case TAC_BIN: {
                env_sustituir(&env, instr->a);
                env_sustituir(&env, instr->b);
                int a, b, resultado;
                if (leer_numero(instr->a, &a) && leer_numero(instr->b, &b) &&
                    calcular_bin(a, b, instr->op, &resultado)) {
                    instr->tipo = TAC_COPIA;
                    snprintf(instr->a, sizeof instr->a, "%d", resultado);
                    instr->b[0] = '\0';
                    env_fijar(&env, instr->destino, 1, resultado);
                } else {
                    env_fijar(&env, instr->destino, 0, 0);
                }
                break;
            }

            case TAC_NEG:
                env_sustituir(&env, instr->a);
                {
                    int v;
                    if (leer_numero(instr->a, &v)) {
                        instr->tipo = TAC_COPIA;
                        snprintf(instr->a, sizeof instr->a, "%d", -v);
                        env_fijar(&env, instr->destino, 1, -v);
                    } else {
                        env_fijar(&env, instr->destino, 0, 0);
                    }
                }
                break;

            case TAC_IF_FALSO:
            case TAC_PRINT:
                env_sustituir(&env, instr->a);
                break;
        }
    }
}

static int es_temporal(const char *nombre) {
    return nombre[0] == '_' && nombre[1] == 't';
}

static int nombre_leido(const TAC *t, const char *nombre) {
    for (int i = 0; i < t->n; i++) {
        const Instr *instr = &t->items[i];
        switch (instr->tipo) {
            case TAC_COPIA:
            case TAC_NEG:
            case TAC_IF_FALSO:
            case TAC_PRINT:
                if (strcmp(instr->a, nombre) == 0) return 1;
                break;
            case TAC_BIN:
                if (strcmp(instr->a, nombre) == 0) return 1;
                if (strcmp(instr->b, nombre) == 0) return 1;
                break;
            default:
                break;
        }
    }
    return 0;
}

static void optimizar_muertos(TAC *t) {
    for (;;) {
        int alguno = 0;
        int j = 0;
        for (int i = 0; i < t->n; i++) {
            const Instr *instr = &t->items[i];
            int escribe = (instr->tipo == TAC_COPIA ||
                           instr->tipo == TAC_BIN ||
                           instr->tipo == TAC_NEG);
            if (escribe && es_temporal(instr->destino) &&
                !nombre_leido(t, instr->destino)) {
                alguno = 1;
                continue; /* no copiar: se elimina */
            }
            t->items[j++] = t->items[i];
        }
        t->n = j;
        if (!alguno) break;
    }
}

/* ------------------------------------------------------------------ */

static void instr_a_texto(const Instr *instr, Buf *b) {
    switch (instr->tipo) {
        case TAC_COPIA:
            buf_agrega(b, "%s = %s\n", instr->destino, instr->a);
            break;
        case TAC_BIN:
            buf_agrega(b, "%s = %s %s %s\n",
                       instr->destino, instr->a, instr->op, instr->b);
            break;
        case TAC_NEG:
            buf_agrega(b, "%s = -%s\n", instr->destino, instr->a);
            break;
        case TAC_GOTO:
            buf_agrega(b, "goto L%d\n", instr->etiqueta);
            break;
        case TAC_IF_FALSO:
            buf_agrega(b, "ifFalso %s goto L%d\n", instr->a, instr->etiqueta);
            break;
        case TAC_ETIQUETA:
            buf_agrega(b, "L%d:\n", instr->etiqueta);
            break;
        case TAC_PRINT:
            buf_agrega(b, "print %s\n", instr->a);
            break;
    }
}

static void tac_liberar(TAC *t) {
    free(t->items);
    t->items = NULL;
    t->n = 0;
    t->cap = 0;
}

char *tac_generar(Nodo *programa) {
    ast_plegar_constantes(programa);

    TAC t;
    memset(&t, 0, sizeof t);
    t.sig_temp = 0;
    t.sig_etiqueta = 0; /* la primera etiqueta será L1 */

    gen_sentencia(programa, &t);
    optimizar_propagacion(&t);
    optimizar_muertos(&t);

    Buf b;
    buf_iniciar(&b);
    for (int i = 0; i < t.n; i++) {
        instr_a_texto(&t.items[i], &b);
    }
    tac_liberar(&t);
    return buf_terminar(&b);
}
