# Diseño del Hito 2 · Sentencias, ámbitos y diagnósticos

**Equipo:** Edwin, Blanca y Jimena
**Archivo principal:** `src/semantica.c`
**Pruebas:** `make test-hito2` y `make test-propias`

---

## 1. Objetivo

Completar el compilador de Lenguajito con:

- parser para toda la gramática: declaraciones, asignaciones, `if/else`,
  `while`, `print` y bloques;
- tabla de símbolos con ámbitos anidados y shadowing;
- diagnósticos `E01`, `E02`, `E04` y `S01` con el formato del contrato;
- recuperación para reportar varios errores en una sola pasada;
- `--run` para ejecutar los programas válidos.

El detalle del lenguaje está en [`gramatica.md`](gramatica.md). Este documento
explica **cómo** se implementó la parte semántica.

---

## 2. Flujo del compilador

```text
archivo .lj
    │
    ▼
lexer.c ─────────► tokens + S01 léxicos
    │
    ▼
parser.c ────────► AST + S01 sintácticos (recuperación con ';' y '}')
    │
    ▼
semantica.c ─────► ámbitos, shadowing, E01, E02, E04
    │
    ├── --check  ─► termina con 0/1
    ├── --run    ─► intérprete del AST (Hito 2)
    └── --tac / --asm ─► Hitos 3 y 4 (pendientes)
```

La semántica solo se ejecuta si el lexer y el parser no reportaron errores. Si
hay errores, se imprimen todos (máximo 20) y el proceso termina con código 1.

---

## 3. Tabla de símbolos

La tabla es una **pila de ámbitos**. Cada ámbito contiene un arreglo dinámico de
símbolos:

```c
typedef struct {
    char nombre[128];
    int inicializada;   /* ¿tiene valor asignado en todos los caminos? */
} Simbolo;

typedef struct {
    Simbolo *items;
    int n;
    int cap;
} Ambito;
```

Reglas:

1. El programa completo abre el ámbito global.
2. Cada bloque `{ ... }` abre un ámbito nuevo y lo cierra al terminar.
3. `buscar_local()` revisa solo el ámbito más interno; se usa para `E02`.
4. `buscar()` recorre del ámbito más interno al más externo; implementa el
   shadowing y resuelve lecturas/asignaciones.
5. Al cerrar un bloque se libera su arreglo; sus variables dejan de existir.

### Shadowing

```c
int x = 1;
{
    int x = x + 10;   // el inicializador ve la x externa
    print(x);         // 11
}
print(x);             // 1
```

El inicializador se revisa **antes** de declarar la variable interna. Así se
evita que `int x = x + 1;` se lea a sí mismo y se respeta el shadowing.

---

## 4. Inicialización por caminos

No basta con marcar una variable como inicializada en cuanto aparece una
asignación. La especificación pide que la lectura sea segura en **todos** los
caminos:

```c
int a;
if (c) { a = 1; }     // solo asigna en un camino
print(a);             // E01: no está inicializada en todos los caminos
```

La implementación usa **instantáneas** del estado de inicialización de todos los
símbolos visibles:

```c
typedef struct {
    int ambito;
    int indice;
    int inicializada;
} EstadoSimbolo;

typedef struct {
    EstadoSimbolo *items;
    int n;
} Instantanea;
```

### `if` con y sin `else`

1. Se captura el estado **antes** del `if`.
2. Se analiza la rama `entonces` y se captura su estado final.
3. Se restaura el estado anterior.
4. Si hay `else`, se analiza y se captura su estado final; si no hay, la rama
   “no” conserva el estado anterior.
5. Se fusionan los caminos:

```text
definitiva = antes || (estado_entonces && estado_else)
```

Por eso:

- `if (c) { a = 1; } else { a = 2; }` **sí** inicializa `a`;
- `if (c) { a = 1; }` **no** inicializa `a`.

### `while`

El cuerpo puede ejecutarse **cero veces**. Por eso, al terminar el ciclo se
restaura el estado anterior: solo son definitivas las inicializaciones que ya
existían antes del `while`. Dentro del cuerpo sí se analiza la secuencia normal,
de modo que `while (c) { a = 1; print(a); }` no produce `E01`.

### Bloques secuenciales

Un bloque que no es rama de `if` ni cuerpo de `while` se ejecuta siempre. Sus
asignaciones a variables externas sí se conservan; sus declaraciones internas
desaparecen al cerrar el bloque.

---

## 5. Diagnósticos

Formato exacto:

```text
archivo:línea:columna: error EXX: mensaje
```

| Código | Cuándo se emite |
| :--- | :--- |
| `S01` | error léxico o sintáctico; el parser se recupera en `;` o `}` |
| `E01` | variable no declarada, o leída antes de tener valor en todos los caminos |
| `E02` | redeclaración del mismo nombre en el mismo ámbito |
| `E04` | división entre cero con divisor constante (incluye `1 - 1`) |

`evaluar_constante()` en `ast.c` reconoce números, negaciones y operaciones
binarias constantes. Si el divisor constante vale cero, se reporta `E04` en la
posición del divisor. Una división por cero no evaluable (por ejemplo, dentro de
otra división por cero) no se marca dos veces.

---

## 6. Matriz de pruebas del Hito 2

| Tipo | Casos |
| :--- | :--- |
| Doradas válidas | `tests/validos/01` a `09` con `--run` |
| Doradas inválidas | `tests/invalidos/01` a `05` con `--check` |
| Propias válidas | `14_caminos_if`, `15_ambito_while`, `16_sombra_init`, `17_ambito_anidado` |
| Propias inválidas | `07_e01_no_declarada`, `08_asignacion_sin_declarar`, `09_leida_antes_asignar`, `11_ambito_bloque`, `12_multiples_errores`, `13_caracter_invalido`, `18_e01_if_sin_else`, `19_e01_while`, `20_multiples_errores`, `21_sintaxis_multiples` |

Resultado esperado:

```text
make test-hito2   → Hito 2: 14/14 pruebas superadas
make test-propias → Pruebas propias: 21/21 superadas
```

Los archivos `.diag` permiten comparar **todos** los diagnósticos de una pasada,
no solo el primero. Esto cubre el requisito de reportar varios errores.

---

## 7. Límites conocidos

- La inicialización es conservadora: no hay análisis de valores ni de
  alcanzabilidad. Un `while (1) { ... }` que nunca termina sigue tratando el
  estado posterior como el anterior.
- La división entre cero en tiempo de ejecución (divisor no constante) no se
  exige en el contrato; se detecta al ejecutar con `--run`.
- Los literales mayores que `INT_MAX` se truncan con `strtol`.
- `--tac` y `--asm` pertenecen a los Hitos 3 y 4.
