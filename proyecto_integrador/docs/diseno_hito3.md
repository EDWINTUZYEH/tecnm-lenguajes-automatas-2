# Diseño del Hito 3 · TAC y optimización

**Equipo:** Edwin, Blanca y Jimena
**Archivo principal:** `src/tac.c`
**Pruebas:** `make test-hito3` y `make test-propias`

---

## 1. Objetivo

Generar **código de tres direcciones** (TAC) a partir del AST, con el formato
de la sección 8 de [`gramatica.md`](gramatica.md), y aplicar dos
optimizaciones:

- plegado y propagación de constantes;
- eliminación de código muerto para temporales.

El TAC se imprime con `--tac` y es la entrada conceptual del backend del
Hito 4.

---

## 2. Flujo

```text
archivo .lj
    │
    ▼
lexer → parser → AST
    │
    ▼
semantica.c  (E01, E02, E04)
    │
    ▼
ast_plegar_constantes()      ← plegado sobre el AST
    │
    ▼
tac_generar()
    ├── generación estructural de instrucciones
    ├── propagación de constantes a nivel TAC
    ├── eliminación de temporales sin usos
    └── serialización al formato del contrato
    │
    ▼
--tac
```

La semántica se ejecuta antes: si hay errores, no se genera TAC y el proceso
sale con código 1.

---

## 3. Formato generado

| Forma | Significado |
| :--- | :--- |
| `x = a op b` | operación binaria |
| `x = a` | copia |
| `x = -a` | negación |
| `goto L1` | salto incondicional |
| `ifFalso a goto L1` | salta si `a` vale 0 |
| `L1:` | etiqueta |
| `print a` | impresión |

- Temporales `_t0`, `_t1`, ... únicos y sin reutilizar.
- Etiquetas `L1`, `L2`, ... únicas.
- Las variables del usuario conservan su nombre.

Ejemplo real de `while (i < 3) { print(i); i = i + 1; }`:

```text
i = 0
L1:
_t0 = i < 3
ifFalso _t0 goto L2
print i
_t1 = i + 1
i = _t1
goto L1
L2:
```

---

## 4. Generación estructural

`gen_sentencia()` recorre el AST:

- `N_DECLARAR` con inicializador → copia del valor a la variable.
- `N_ASIGNAR` → evalúa la expresión y emite una copia.
- `N_SI` → `ifFalso` a la etiqueta del `else` (o al final), cuerpo, `goto` al
  final y etiquetas.
- `N_MIENTRAS` → etiqueta de inicio, condición, `ifFalso` de salida, cuerpo y
  `goto` de vuelta.
- `N_IMPRIMIR` → `print` del operando.

`gen_expr()` devuelve un operando (constante o temporal) y emite instrucciones
solo cuando hace falta.

---

## 5. Optimizaciones

### Plegado en el AST

`ast_plegar_constantes()` sustituye `N_BIN` y `N_NEG` constantes por un
`N_NUM`. Por eso `print(2 * 3 + 4);` produce directamente:

```text
print 10
```

### Propagación de constantes en TAC

Se mantiene un entorno `nombre → valor` mientras se recorre la lista:

- una copia de un literal registra el valor;
- una operación con ambos operandos constantes se pliega;
- las variables conservan su valor hasta que se redefinen.

El entorno se **limpia en etiquetas y en `goto`**, porque el control puede
llegar desde varios caminos y propagar ahí sería incorrecto en ciclos y saltos.

Ejemplo:

```c
int a = 2;
int b = a * 3;
print(b);
```

```text
a = 2
b = 6
print 6
```

### Eliminación de código muerto

Se repite hasta punto fijo: si una instrucción escribe un temporal `_tN` que
nadie lee, se elimina. Solo se eliminan temporales, como pide el contrato; no
se tocan asignaciones a variables del usuario.

---

## 6. Pruebas

| Tipo | Casos |
| :--- | :--- |
| Doradas del Hito 3 | `tests/tac/01_folding.lj` → `print 10` |
| Doradas de Hitos 1 y 2 | válidos, inválidos y AST |
| Propias | `22_optimizacion` (plegado + propagación + código muerto) |

Resultado esperado:

```text
make test-hito3   → Hito 3: 15/15 pruebas superadas
make test-propias → Pruebas propias: 22/22 superadas
```

---

## 7. Límites conocidos

- No hay optimizaciones de bucles, CSE ni eliminación de variables del
  usuario: fuera del alcance del hito.
- La propagación es local al bloque lineal entre etiquetas.
- El TAC no se ejecuta: solo se genera y se imprime. La ejecución real llega
  con el backend del Hito 4.
