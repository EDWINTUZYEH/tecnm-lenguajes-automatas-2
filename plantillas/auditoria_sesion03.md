# Bitácora de Requerimientos y Auditoría IA — Sesión 03
**Materia:** Lenguajes y Autómatas II (SCD-1016)  
**Tema:** Google Colab, Mágicos y Flujo de Entrega  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Edwin atamndo tuz yeh]  
**Matrícula:** [24531358]  
**Track:** [ C]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Manipulación de archivos y llamadas OS  
*Describe qué problema o restricción de memoria/sintaxis identificaste al codificar a mano:*
  Al empezar no sabía cómo abrir y escribir un archivo en C, ni qué devolvían las
> funciones cuando algo fallaba. Me atoré principalmente en tres puntos:
> 1. No sabía que `fopen` devuelve `NULL` si no puede abrir el archivo, y que
>    sin revisar eso el programa puede abortar al usar un puntero inválido.
> 2. No tenía claro que hay que cerrar el archivo con `fclose` en todos los
>    caminos, porque un archivo abierto es un recurso que se queda sin liberar.
>    y si se me complica un poco en codificar a manopero si se puede solucionar.
> 

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | C99 / GCC o Rust 2021 sin bibliotecas no estándar |
| **Rol (R)** | Ingeniero de software de sistemas y compiladores |
| **Especificación (E)** | Salida estándar y códigos de retorno ABI |
| **Output (O)** | Solo código modular y análisis de complejidad |

### 2.2 Prompt Estructurado
```text
[ESPECIFICACIÓN:
Implementa exactamente estas firmas, sin cambiarlas:

  int escribir_texto(const char *ruta, const char *texto);
  int contar_lineas(const char *ruta);
  int ejecutar(const char *comando);

Comportamiento:
- escribir_texto: abre el archivo en modo escritura, escribe el texto y lo cierra.
  Devuelve 0 si todo salió bien y -1 si hubo cualquier error.
- contar_lineas: devuelve el número de líneas del archivo. Debe contar la última
  línea aunque no termine en '\n'. Si el archivo no se puede abrir, devuelve -1
  (sin abortar el programa).
- ejecutar: ejecuta el comando con system() y devuelve el código de salida REAL
  del proceso usando WEXITSTATUS, no el estado crudo que entrega system().
  "true" debe dar 0 y "false" debe dar 1.
- El archivo debe cerrarse en todos los caminos de ejecución.

OUTPUT:
Entrégame únicamente el código completo del archivo ia_sesion03_c.c, con las
firmas idénticas, listo para compilar. Después del código, agrega un análisis
breve de complejidad en tiempo y memoria de cada función. Sin otras explicaciones.]
```

---

## 3. Código Devuelto por el Modelo
```c
#include "api_sesion03.h"
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>

int escribir_texto(const char *ruta, const char *texto) {
    if (ruta == NULL || texto == NULL) return -1;
    FILE *f = fopen(ruta, "w");
    if (f == NULL) return -1;
    int rc = (fputs(texto, f) == EOF) ? -1 : 0;
    if (fclose(f) != 0) rc = -1;
    return rc;
}

int contar_lineas(const char *ruta) {
    if (ruta == NULL) return -1;
    FILE *f = fopen(ruta, "r");
    if (f == NULL) return -1;
    int lineas = 0, c, ultimo = '\n';
    while ((c = fgetc(f)) != EOF) {
        if (c == '\n') lineas++;
        ultimo = c;
    }
    if (ultimo != '\n') lineas++;
    fclose(f);
    return lineas;
}

int ejecutar(const char *comando) {
    if (comando == NULL) return -1;
    int estado = system(comando);
    if (estado == -1) return -1;
    if (WIFEXITED(estado)) return WEXITSTATUS(estado);
    return -1;
}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness)
*Pruebas ejecutadas:* Detección de errores de compilación GCC

* [* ] Caso base y límites superados sin *Crash*.
* [*] No existen accesos fuera de límites ni *Memory Leaks*.
* [*] La complejidad teórica coincide con la implementada.

### Reporte Crítico
*¿Qué caso borde o problema omitió la IA y cómo lo solucionaste?
 en cierta forma la ia si ayuda en ciertas lineas de codigo, entonces la solucion es eliminar los codigos demas y verificar que realmente funcione. 

---
**Firma digital:** [EDWINTUZYEH]
