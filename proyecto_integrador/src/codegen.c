/* codegen.c - generación de ensamblador x86-64 (AT&T).
 *
 * Layout de la pila: %rbp apunta a la base del marco y cada variable
 * declarada ocupa un slot de 4 bytes en %rbp - 4, %rbp - 8, ...
 * El tamaño del marco se redondea a múltiplo de 16 para que las llamadas
 * a printf cumplan la ABI (%rsp % 16 == 0 en el `call`).
 *
 * Las expresiones se evalúan dejando el resultado en %eax; los subárboles
 * conservan el orden de evaluación del lenguaje (izquierda, luego derecha).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "codegen.h"
#include "util.h"

#define TAM_NOMBRE 128

typedef struct {
    char nombre[TAM_NOMBRE];
    int offset; /* desplazamiento negativo respecto a %rbp */
} Slot;

typedef struct {
    Slot *items;
    int n;
    int cap;
} Ambito;

typedef struct {
    Ambito *ambitos;
    int n;
    int cap;
    int sig_slot;
    int sig_etiqueta;
    Buf cuerpo;
} Codegen;

static void ambito_apilar(Codegen *cg) {
    if (cg->n == cg->cap) {
        int cap = (cg->cap == 0) ? 8 : cg->cap * 2;
        Ambito *nuevos = realloc(cg->ambitos, (size_t)cap * sizeof *nuevos);
        if (nuevos == NULL) {
            fprintf(stderr, "error: memoria insuficiente\n");
            exit(2);
        }
        cg->ambitos = nuevos;
        cg->cap = cap;
    }
    Ambito *a = &cg->ambitos[cg->n++];
    a->items = NULL;
    a->n = 0;
    a->cap = 0;
}

static void ambito_desapilar(Codegen *cg) {
    Ambito *a = &cg->ambitos[--cg->n];
    free(a->items);
}

static int buscar_slot(const Codegen *cg, const char *nombre) {
    for (int k = cg->n - 1; k >= 0; k--) {
        const Ambito *a = &cg->ambitos[k];
        for (int i = a->n - 1; i >= 0; i--) {
            if (strcmp(a->items[i].nombre, nombre) == 0) {
                return a->items[i].offset;
            }
        }
    }
    return 0; /* no debería ocurrir: la semántica ya validó */
}

static int declarar_slot(Codegen *cg, const char *nombre) {
    Ambito *a = &cg->ambitos[cg->n - 1];
    if (a->n == a->cap) {
        int cap = (a->cap == 0) ? 8 : a->cap * 2;
        Slot *nuevos = realloc(a->items, (size_t)cap * sizeof *nuevos);
        if (nuevos == NULL) {
            fprintf(stderr, "error: memoria insuficiente\n");
            exit(2);
        }
        a->items = nuevos;
        a->cap = cap;
    }
    cg->sig_slot++;
    int offset = -4 * cg->sig_slot;
    snprintf(a->items[a->n].nombre, TAM_NOMBRE, "%s", nombre);
    a->items[a->n].offset = offset;
    a->n++;
    return offset;
}

static int nueva_etiqueta(Codegen *cg) {
    return ++cg->sig_etiqueta;
}

static void gen_expresion(Codegen *cg, const Nodo *n);
static void gen_sentencia(Codegen *cg, const Nodo *n);

static const char *comparacion_a_set(const char *op) {
    if (strcmp(op, "<") == 0)  return "setl";
    if (strcmp(op, "<=") == 0) return "setle";
    if (strcmp(op, ">") == 0)  return "setg";
    if (strcmp(op, ">=") == 0) return "setge";
    if (strcmp(op, "==") == 0) return "sete";
    if (strcmp(op, "!=") == 0) return "setne";
    return "sete";
}

static void gen_expresion(Codegen *cg, const Nodo *n) {
    switch (n->tipo) {
        case N_NUM:
            buf_agrega(&cg->cuerpo, "    movl $%d, %%eax\n", n->numero);
            break;

        case N_VAR:
            buf_agrega(&cg->cuerpo, "    movl %d(%%rbp), %%eax\n",
                       buscar_slot(cg, n->nombre));
            break;

        case N_NEG:
            gen_expresion(cg, n->expr);
            buf_agrega(&cg->cuerpo, "    negl %%eax\n");
            break;

        case N_BIN: {
            gen_expresion(cg, n->izq);
            buf_agrega(&cg->cuerpo, "    pushq %%rax\n");
            gen_expresion(cg, n->der);
            buf_agrega(&cg->cuerpo, "    movl %%eax, %%r11d\n");
            buf_agrega(&cg->cuerpo, "    popq %%rcx\n");
            buf_agrega(&cg->cuerpo, "    movl %%ecx, %%eax\n"); /* eax = izquierda */
            const char *op = n->operador;
            if (strcmp(op, "+") == 0) {
                buf_agrega(&cg->cuerpo, "    addl %%r11d, %%eax\n");
            } else if (strcmp(op, "-") == 0) {
                buf_agrega(&cg->cuerpo, "    subl %%r11d, %%eax\n");
            } else if (strcmp(op, "*") == 0) {
                buf_agrega(&cg->cuerpo, "    imull %%r11d, %%eax\n");
            } else if (strcmp(op, "/") == 0) {
                buf_agrega(&cg->cuerpo, "    cltd\n");
                buf_agrega(&cg->cuerpo, "    idivl %%r11d\n");
            } else { /* comparaciones */
                buf_agrega(&cg->cuerpo, "    cmpl %%r11d, %%eax\n");
                buf_agrega(&cg->cuerpo, "    %s %%al\n", comparacion_a_set(op));
                buf_agrega(&cg->cuerpo, "    movzbl %%al, %%eax\n");
            }
            break;
        }

        default:
            break;
    }
}

static void gen_sentencia(Codegen *cg, const Nodo *n) {
    switch (n->tipo) {
        case N_PROGRAMA:
        case N_BLOQUE:
            ambito_apilar(cg);
            for (int i = 0; i < n->n_sentencias; i++) {
                gen_sentencia(cg, n->sentencias[i]);
            }
            ambito_desapilar(cg);
            break;

        case N_DECLARAR:
            if (n->tiene_init && n->expr != NULL) {
                gen_expresion(cg, n->expr);
            }
            {
                int offset = declarar_slot(cg, n->nombre);
                if (n->tiene_init && n->expr != NULL) {
                    buf_agrega(&cg->cuerpo, "    movl %%eax, %d(%%rbp)\n", offset);
                }
            }
            break;

        case N_ASIGNAR:
            gen_expresion(cg, n->expr);
            buf_agrega(&cg->cuerpo, "    movl %%eax, %d(%%rbp)\n",
                       buscar_slot(cg, n->nombre));
            break;

        case N_SI:
            if (n->sino != NULL) {
                int id_sino = nueva_etiqueta(cg);
                int id_fin = nueva_etiqueta(cg);
                gen_expresion(cg, n->expr);
                buf_agrega(&cg->cuerpo, "    testl %%eax, %%eax\n");
                buf_agrega(&cg->cuerpo, "    je .L%d\n", id_sino);
                gen_sentencia(cg, n->cuerpo);
                buf_agrega(&cg->cuerpo, "    jmp .L%d\n", id_fin);
                buf_agrega(&cg->cuerpo, ".L%d:\n", id_sino);
                gen_sentencia(cg, n->sino);
                buf_agrega(&cg->cuerpo, ".L%d:\n", id_fin);
            } else {
                int id_fin = nueva_etiqueta(cg);
                gen_expresion(cg, n->expr);
                buf_agrega(&cg->cuerpo, "    testl %%eax, %%eax\n");
                buf_agrega(&cg->cuerpo, "    je .L%d\n", id_fin);
                gen_sentencia(cg, n->cuerpo);
                buf_agrega(&cg->cuerpo, ".L%d:\n", id_fin);
            }
            break;

        case N_MIENTRAS: {
            int id_inicio = nueva_etiqueta(cg);
            int id_fin = nueva_etiqueta(cg);
            buf_agrega(&cg->cuerpo, ".L%d:\n", id_inicio);
            gen_expresion(cg, n->expr);
            buf_agrega(&cg->cuerpo, "    testl %%eax, %%eax\n");
            buf_agrega(&cg->cuerpo, "    je .L%d\n", id_fin);
            gen_sentencia(cg, n->cuerpo);
            buf_agrega(&cg->cuerpo, "    jmp .L%d\n", id_inicio);
            buf_agrega(&cg->cuerpo, ".L%d:\n", id_fin);
            break;
        }

        case N_IMPRIMIR:
            gen_expresion(cg, n->expr);
            buf_agrega(&cg->cuerpo, "    movl %%eax, %%esi\n");
            buf_agrega(&cg->cuerpo, "    leaq .LC0(%%rip), %%rdi\n");
            buf_agrega(&cg->cuerpo, "    movl $0, %%eax\n");
            buf_agrega(&cg->cuerpo, "    call printf\n");
            break;

        default:
            break;
    }
}

char *codegen_generar(const Nodo *programa) {
    Codegen cg;
    memset(&cg, 0, sizeof cg);
    cg.sig_slot = 0;
    cg.sig_etiqueta = 0;
    buf_iniciar(&cg.cuerpo);

    gen_sentencia(&cg, programa);

    int marco = cg.sig_slot * 4;
    if (marco % 16 != 0) marco += 16 - (marco % 16);

    Buf out;
    buf_iniciar(&out);
    buf_agrega(&out, "    .text\n");
    buf_agrega(&out, "    .globl main\n");
    buf_agrega(&out, "main:\n");
    buf_agrega(&out, "    pushq %%rbp\n");
    buf_agrega(&out, "    movq %%rsp, %%rbp\n");
    if (marco > 0) buf_agrega(&out, "    subq $%d, %%rsp\n", marco);
    buf_agrega(&out, "%s", cg.cuerpo.datos);
    buf_agrega(&out, "    movl $0, %%eax\n");
    buf_agrega(&out, "    leave\n");
    buf_agrega(&out, "    ret\n");
    buf_agrega(&out, "\n    .section .rodata\n");
    buf_agrega(&out, ".LC0:\n");
    buf_agrega(&out, "    .string \"%%d\\n\"\n");

    buf_liberar(&cg.cuerpo);
    while (cg.n > 0) ambito_desapilar(&cg);
    free(cg.ambitos);

    return buf_terminar(&out);
}
