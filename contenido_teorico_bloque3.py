# contenido_teorico_bloque3.py
# Base de conocimiento conceptual: Unidad 3: Código Intermedio y Optimización (Sesiones 21 a 30)
# Materia: Lenguajes y Autómatas II (SCD-1016)
# Docente Titular: MCC. Iván Márquez Larios (ijmarquezl)

TEORIA_BLOQUE_3 = {21: {'tema': 'Fundamentos de Código de Tres Direcciones (TAC)',
      'unidad': 'Unidad 3: Código Intermedio y Optimización',
      'teoria_principal': {'titulo': 'La Representación Intermedia Lineal y Cuádruplos',
                           'lead': 'El código intermedio desacopla el frontend (análisis sintáctico/semántico) del backend (arquitectura '
                                   'de hardware objetivo).',
                           'tarjetas': [('01. Estructura de 3 Direcciones',
                                         "Instrucciones de la forma 'x = y op z', donde cada paso involucra a lo sumo dos operandos y un "
                                         'resultado.',
                                         'Simplifica expresiones complejas anidadas convirtiéndolas en una secuencia lineal de pasos '
                                         'atómicos.'),
                                        ('02. Representación en Cuádruplos',
                                         'Tupla formal de 4 campos: (operador, argumento1, argumento2, resultado).',
                                         'Permite almacenar las instrucciones intermedias en un arreglo o lista enlazada homogénea.'),
                                        ('03. Generación de Temporales Únicos',
                                         'El compilador asigna variables sintéticas autoincrementales (_t0, _t1, _t2...) para guardar '
                                         'resultados parciales.',
                                         'Facilita el análisis de vida de variables (Liveness Analysis) en fases posteriores de asignación '
                                         'de registros.')]},
      'arquitectura_memoria': {'titulo': 'Estructura de Datos de la Lista de Cuádruplos',
                               'descripcion': 'Modelado de instrucciones intermedias en memoria dinámica:',
                               'tarjetas': [('Estructura Quad',
                                             'struct Quad { OpCode op; char arg1[32]; char arg2[32]; char res[32]; struct Quad *sig; };',
                                             'Cada cuádruplo se encadena en una lista lineal de instrucciones emitida por el traductor de '
                                             'AST.'),
                                            ('Ventaja sobre Triplos',
                                             'Los cuádruplos desacoplan el identificador del resultado de la posición física del arreglo.',
                                             'Permite mover, reordenar y eliminar instrucciones durante la optimización sin invalidar '
                                             'referencias cruzadas.')]},
      'casos_borde': {'titulo': 'Antipatrones en Generación de TAC',
                      'items': ['Reutilizar nombres de temporales antes de que expire su tiempo de vida, corrompiendo datos en '
                                'subexpresiones.',
                                'Omitir el operador de asignación simple (x = y) intentando forzar un operador binario ficticio.',
                                "Punteros nulos en argumentos no utilizados en operaciones unarias (ej. negación '_t0 = -a')."]},
      'contexto': {'pregunta': '¿Cómo se convierte una expresión en una lista de instrucciones tan simples que cualquier procesador pueda '
                               'ejecutarlas?',
                   'objetivo': 'Entender qué es el código de tres direcciones y representar operaciones como cuádruplos, generando '
                               'temporales únicos que no se pisen entre sí.',
                   'por_que': 'El backend no entiende árboles ni paréntesis: solo sabe ejecutar instrucciones con un operador y dos '
                              'operandos. El TAC es el contrato entre el frontend y el backend; si los temporales se repiten o un '
                              'cuádruplo queda mal formado, el ensamblador recibe basura y el error aparece lejos de su causa.',
                   'conceptos': [('Código de tres direcciones',
                                  'Representación intermedia donde cada instrucción hace una sola operación con, como máximo, dos '
                                  'operandos y un resultado.',
                                  "Como una receta paso a paso: en lugar de decir 'licúa todo', cada línea indica exactamente qué mezclar "
                                  'y dónde guardarlo.'),
                                 ('Cuádruplo',
                                  'Registro de cuatro campos (operador, argumento 1, argumento 2, resultado) que describe una instrucción '
                                  'intermedia.',
                                  'Como el renglón de un formulario bancario: operación, cuenta origen, cuenta destino y monto, siempre en '
                                  'el mismo orden.'),
                                 ('Temporal',
                                  'Variable sintética que guarda el resultado parcial de una operación para usarlo en la siguiente.',
                                  'Como el plato donde dejas la mezcla mientras preparas el siguiente ingrediente: tiene nombre propio '
                                  'para no confundirla.'),
                                 ('Representación intermedia',
                                  'Formato del programa entre el análisis y la generación de código, independiente del hardware objetivo.',
                                  'Como el plano de una casa antes de elegir los materiales: sirve para revisar la estructura sin '
                                  'comprometerse con un proveedor.')],
                   'resultado': 'Dos funciones en C que generan nombres de temporales únicos y formatean cuádruplos, verificadas por un '
                                'harness con seis casos.'},
      'lab': {'reto': 'Cuádruplos y temporales únicos',
              'entregable': 'tus funciones nuevo_temporal() y emitir_cuadruplo() en artesano_sesion21_c.c, el harness en verde y la '
                            'bitácora en auditorias/auditoria_sesion21.md',
              'explicacion': 'Recibes un contador y los campos de una instrucción; debes escribir el nombre del siguiente temporal o el '
                             'cuádruplo completo en un buffer de texto. Las funciones no imprimen: escriben en dst, respetan la capacidad '
                             'y dejan el contador actualizado.',
              'reglas': ['El contador se usa y después se incrementa: la primera llamada siempre produce _t0.',
                         'Un argumento NULL se escribe como guion bajo en el cuádruplo; no se omite ni se inventa.',
                         'Escribe siempre en el buffer recibido: no reserves memoria ni uses variables globales.'],
              'api': {'header': 'api_sesion21.h',
                      'decls': ['void nuevo_temporal(char *dst, int cap, int *contador);',
                                'void emitir_cuadruplo(char *dst, int cap, const char *op, const char *a1, const char *a2, const char '
                                '*res);']},
              'stub': 'void nuevo_temporal(char *dst, int cap, int *contador) {\n'
                      '          (void)dst; (void)cap; (void)contador; /* TODO: escribe _tK y avanza el contador */\n'
                      '      }\n'
                      '      \n'
                      '      void emitir_cuadruplo(char *dst, int cap, const char *op, const char *a1, const char *a2, const char *res) {\n'
                      '          (void)dst; (void)cap; (void)op; (void)a1; (void)a2; (void)res; /* TODO: formatea el cuadruplo */\n'
                      '      }',
              'casos': [{'caso': 'nuevo_temporal(_t0)',
                         'codigo': 'int c = 0;\n      char b[32] = "";\n      nuevo_temporal(b, 32, &c);',
                         'var': 'b',
                         'esperado': '_t0',
                         'tipo': 'str'},
                        {'caso': 'nuevo_temporal(_t7)',
                         'codigo': 'int c = 7;\n      char b[32] = "";\n      nuevo_temporal(b, 32, &c);',
                         'var': 'b',
                         'esperado': '_t7',
                         'tipo': 'str'},
                        {'caso': 'cuadruplo de a + b',
                         'codigo': 'char b[64] = "";\n      emitir_cuadruplo(b, 64, "+", "a", "b", "_t0");',
                         'var': 'b',
                         'esperado': '(+, a, b, _t0)',
                         'tipo': 'str'},
                        {'caso': 'cuadruplo de _t0 * c',
                         'codigo': 'char b[64] = "";\n      emitir_cuadruplo(b, 64, "*", "_t0", "c", "_t1");',
                         'var': 'b',
                         'esperado': '(*, _t0, c, _t1)',
                         'tipo': 'str'},
                        {'caso': 'asignacion simple',
                         'codigo': 'char b[64] = "";\n      emitir_cuadruplo(b, 64, "=", "a", NULL, "x");',
                         'var': 'b',
                         'esperado': '(=, a, _, x)',
                         'tipo': 'str'},
                        {'caso': 'goto sin operandos',
                         'codigo': 'char b[64] = "";\n      emitir_cuadruplo(b, 64, "goto", "L1", NULL, NULL);',
                         'var': 'b',
                         'esperado': '(goto, L1, _, _)',
                         'tipo': 'str'}],
              'criterios': ['nuevo_temporal() produce _t0, _t7 y _t10 a partir del contador y lo deja incrementado.',
                            'emitir_cuadruplo() respeta el formato (op, a1, a2, res) incluso cuando faltan argumentos.',
                            'Los seis casos del harness salen OK con código de salida 0.']}},
 22: {'tema': 'Generación de TAC para Expresiones Aritmético-Lógicas',
      'unidad': 'Unidad 3: Código Intermedio y Optimización',
      'teoria_principal': {'titulo': 'Aplanado Recursivo del AST en Instrucciones TAC',
                           'lead': 'El recorrido postorden del AST sintetiza nombres de variables temporales para aplanar la jerarquía de '
                                   'operadores.',
                           'tarjetas': [('01. Recorrido Postorden Generador',
                                         'Evalúa recursivamente las ramas izquierda y derecha, obteniendo sus nombres de retorno, y emite '
                                         'el cuádruplo del operador.',
                                         'Garantiza que los operandos estén calculados antes de utilizarlos.'),
                                        ('02. Conservación de Precedencia',
                                         'La estructura jerárquica del AST dicta el orden de emisión en TAC sin necesidad de paréntesis '
                                         'explícitos.',
                                         "La expresión 'a + b * c' se convierte estrictamente en: '_t0 = b * c' seguido de '_t1 = a + "
                                         "_t0'."),
                                        ('03. Expresiones Booleanas como Enteros',
                                         "Las comparaciones ('<', '==', '!=') generan cuádruplos de asignación condicional o banderas "
                                         'booleanas (0 o 1).',
                                         'Permite tratar condiciones lógicas con la misma infraestructura que las operaciones '
                                         'aritméticas.')]},
      'arquitectura_memoria': {'titulo': "Sintetización del Atributo 'Lugar' (Place)",
                               'descripcion': 'Propagación ascendente de identificadores durante la traducción:',
                               'tarjetas': [('Atributo char* lugar',
                                             "Cada llamada a 'generar_tac(nodo)' retorna una cadena con el nombre de la variable o "
                                             'temporal donde reside el resultado.',
                                             "Las hojas devuelven su propio lexema ('x', '42'); los nodos internos devuelven su nuevo "
                                             "temporal ('_t0')."),
                                            ('Generador de Nombres (new_temp)',
                                             'Función atómica que incrementa un contador global: \'sprintf(buffer, "_t%d", contador++)\'.',
                                             'Garantiza unicidad de identificadores temporales en toda la unidad de traducción.')]},
      'casos_borde': {'titulo': 'Puntos de Falla en Expresiones',
                      'items': ["Inversión del orden de argumentos en operadores asimétricos: emitir '_t0 = b - a' para 'a - b'.",
                                'Desbordamiento de buffer al formatear nombres de temporales con números altos (>10,000).',
                                'Pérdida de la variable temporal devuelta por una rama en llamadas recursivas profundas.']},
      'contexto': {'pregunta': '¿Cómo se traduce un árbol de expresión a una lista plana de instrucciones sin perder la precedencia?',
                   'objetivo': 'Recorrer un AST en postorden y emitir una instrucción TAC por cada operador, devolviendo el nombre del '
                               'temporal o de la hoja que contiene el resultado.',
                   'por_que': 'El AST conserva la jerarquía, pero el backend necesita una secuencia lineal. El recorrido postorden '
                              'garantiza que los operandos ya estén calculados cuando se emite el operador, y el atributo lugar conecta '
                              'cada subexpresión con la siguiente instrucción.',
                   'conceptos': [('Recorrido postorden',
                                  'Visitar primero el hijo izquierdo, luego el derecho y al final el nodo actual.',
                                  'Como armar un mueble: primero preparas las patas y el tablero, y solo al final unes las piezas.'),
                                 ('Atributo lugar',
                                  'Nombre de la variable o temporal donde quedó guardado el resultado de una subexpresión.',
                                  'Como el número de caja donde el cajero deja tu pedido mientras atiende lo demás.'),
                                 ('Aplanado',
                                  'Convertir una estructura jerárquica en una secuencia de pasos lineales.',
                                  'Como pasar un organigrama a una lista de órdenes: sigues las relaciones, pero el resultado se lee de '
                                  'arriba a abajo.'),
                                 ('Temporal',
                                  'Variable sintética que guarda el resultado de una operación para la siguiente instrucción.',
                                  'Como una libreta de notas intermedia: no forma parte del resultado final, pero sin ella perderías los '
                                  'cálculos parciales.')],
                   'resultado': 'Un traductor en C que convierte un árbol binario en líneas TAC y respeta la precedencia con temporales '
                                '_t0, _t1, ...'},
      'lab': {'reto': 'Traductor de AST a TAC con precedencia',
              'entregable': 'tu traductor en artesano_sesion22_c.c, el harness en verde y la bitácora',
              'explicacion': 'Recibes la raíz de un árbol con hojas y operadores binarios. Debes escribir una línea TAC por operador en el '
                             'arreglo lineas y devolver cuántas líneas emitiste. Los temporales ya están resueltos: úsalos con '
                             'nuevo_temporal.',
              'reglas': ['Primero se calculan los hijos y después se emite el operador: el recorrido es postorden.',
                         'Cada operador usa un temporal nuevo: llama a nuevo_temporal, no inventes el nombre.',
                         'Nunca escribas más de max líneas ni más de 63 caracteres por línea.'],
              'api': {'header': 'api_sesion22.h',
                      'tipos': ['typedef struct Nodo {',
                                '    char tipo;',
                                '    char op;',
                                '    char valor[16];',
                                '    struct Nodo *izq;',
                                '    struct Nodo *der;',
                                '} Nodo;'],
                      'decls': ['int generar_tac(const Nodo *raiz, char lineas[][64], int max);']},
              'stub': '/* Los temporales ya estan resueltos: usalos tal cual. */\n'
                      'typedef struct {\n'
                      '    char nombre[64][16];\n'
                      '    int usados;\n'
                      '} Pool;\n'
                      '\n'
                      'const char *nuevo_temporal(Pool *p, int *contador) {\n'
                      '    if (p->usados >= 64) return "_t?";\n'
                      '    snprintf(p->nombre[p->usados], sizeof p->nombre[0], "_t%d", (*contador)++);\n'
                      '    return p->nombre[p->usados++];\n'
                      '}\n'
                      '\n'
                      'int generar_tac(const Nodo *raiz, char lineas[][64], int max) {\n'
                      '    /* TODO: postorden; por cada operador escribe lineas[n] = "_tX = a op b" */\n'
                      '    (void)raiz; (void)lineas; (void)max;\n'
                      '    return 0;\n'
                      '}',
              'casos': [{'caso': 'a + b * c',
                         'codigo': 'Nodo a = {.tipo=\'H\', .valor="a"};\n'
                                   '      Nodo b = {.tipo=\'H\', .valor="b"};\n'
                                   '      Nodo c = {.tipo=\'H\', .valor="c"};\n'
                                   "      Nodo m = {.tipo='B', .op='*', .izq=&b, .der=&c};\n"
                                   "      Nodo s = {.tipo='B', .op='+', .izq=&a, .der=&m};\n"
                                   '      char l[8][64] = {{0}};\n'
                                   '      generar_tac(&s, l, 8);',
                         'var': 'l[0]',
                         'esperado': '_t0 = b * c',
                         'tipo': 'str'},
                        {'caso': 'a + b * c (2a linea)',
                         'codigo': 'Nodo a = {.tipo=\'H\', .valor="a"};\n'
                                   '      Nodo b = {.tipo=\'H\', .valor="b"};\n'
                                   '      Nodo c = {.tipo=\'H\', .valor="c"};\n'
                                   "      Nodo m = {.tipo='B', .op='*', .izq=&b, .der=&c};\n"
                                   "      Nodo s = {.tipo='B', .op='+', .izq=&a, .der=&m};\n"
                                   '      char l[8][64] = {{0}};\n'
                                   '      generar_tac(&s, l, 8);',
                         'var': 'l[1]',
                         'esperado': '_t1 = a + _t0',
                         'tipo': 'str'},
                        {'caso': '(a + b) * c',
                         'codigo': 'Nodo a = {.tipo=\'H\', .valor="a"};\n'
                                   '      Nodo b = {.tipo=\'H\', .valor="b"};\n'
                                   '      Nodo c = {.tipo=\'H\', .valor="c"};\n'
                                   "      Nodo s = {.tipo='B', .op='+', .izq=&a, .der=&b};\n"
                                   "      Nodo m = {.tipo='B', .op='*', .izq=&s, .der=&c};\n"
                                   '      char l[8][64] = {{0}};\n'
                                   '      generar_tac(&m, l, 8);',
                         'var': 'l[1]',
                         'esperado': '_t1 = _t0 * c',
                         'tipo': 'str'},
                        {'caso': 'x * (y - z) + w',
                         'codigo': 'Nodo x = {.tipo=\'H\', .valor="x"};\n'
                                   '      Nodo y = {.tipo=\'H\', .valor="y"};\n'
                                   '      Nodo z = {.tipo=\'H\', .valor="z"};\n'
                                   '      Nodo w = {.tipo=\'H\', .valor="w"};\n'
                                   "      Nodo r = {.tipo='B', .op='-', .izq=&y, .der=&z};\n"
                                   "      Nodo m = {.tipo='B', .op='*', .izq=&x, .der=&r};\n"
                                   "      Nodo s = {.tipo='B', .op='+', .izq=&m, .der=&w};\n"
                                   '      char l[8][64] = {{0}};\n'
                                   '      generar_tac(&s, l, 8);',
                         'var': 'l[2]',
                         'esperado': '_t2 = _t1 + w',
                         'tipo': 'str'},
                        {'caso': 'hoja sin operaciones',
                         'codigo': 'Nodo a = {.tipo=\'H\', .valor="x"};\n'
                                   '      char l[4][64] = {{0}};\n'
                                   '      int n = generar_tac(&a, l, 4);',
                         'var': 'n',
                         'esperado': 0,
                         'tipo': 'int'},
                        {'caso': '(a + b) * (c - d)',
                         'codigo': 'Nodo a = {.tipo=\'H\', .valor="a"};\n'
                                   '      Nodo b = {.tipo=\'H\', .valor="b"};\n'
                                   '      Nodo c = {.tipo=\'H\', .valor="c"};\n'
                                   '      Nodo d = {.tipo=\'H\', .valor="d"};\n'
                                   "      Nodo s1 = {.tipo='B', .op='+', .izq=&a, .der=&b};\n"
                                   "      Nodo s2 = {.tipo='B', .op='-', .izq=&c, .der=&d};\n"
                                   "      Nodo m = {.tipo='B', .op='*', .izq=&s1, .der=&s2};\n"
                                   '      char l[8][64] = {{0}};\n'
                                   '      generar_tac(&m, l, 8);',
                         'var': 'l[2]',
                         'esperado': '_t2 = _t0 * _t1',
                         'tipo': 'str'}],
              'criterios': ['Cada operador genera exactamente una línea y las hojas no generan ninguna.',
                            'Los temporales se numeran en orden y no se reutilizan.',
                            'El orden de las líneas respeta la precedencia del árbol.']}},
 23: {'tema': 'Etiquetas y Saltos Incondicionales (Goto)',
      'unidad': 'Unidad 3: Código Intermedio y Optimización',
      'teoria_principal': {'titulo': 'Modelado del Grafo de Flujo de Control (CFG)',
                           'lead': 'Las estructuras de control estructuradas se transforman en una red lineal de etiquetas (Labels) y '
                                   'bifurcaciones.',
                           'tarjetas': [('01. Instrucción Label',
                                         "Marca un punto de destino en el flujo de ejecución: 'LABEL L0'.",
                                         'No consume ciclos de hardware en sí misma; actúa como marcador de dirección en memoria.'),
                                        ('02. Salto Incondicional (Goto)',
                                         "Transfiere la ejecución directamente a una etiqueta destino: 'GOTO L1'.",
                                         'Rompe la ejecución secuencial lineal de la lista de cuádruplos.'),
                                        ('03. Bloques Básicos (Basic Blocks)',
                                         'Secuencia continua de instrucciones con una sola entrada (al inicio) y una sola salida (al '
                                         'final).',
                                         'La unidad fundamental sobre la cual operan los optimizadores de código.')]},
      'arquitectura_memoria': {'titulo': 'Generador de Etiquetas y Punteros a Bloques',
                               'descripcion': 'Estructura de gestión de etiquetas simbólicas:',
                               'tarjetas': [('Generador new_label()',
                                             "Retorna identificadores únicos de destino: 'L0', 'L1', 'L2'...",
                                             'Permite anidar estructuras de control complejas sin colisión de nombres.'),
                                            ('Cuádruplos de Salto',
                                             'Cuádruplo con operador OP_GOTO y arg1 apuntando a la cadena de la etiqueta destino.',
                                             "El backend traduce estas instrucciones directamente a 'jmp' en x86-64.")]},
      'casos_borde': {'titulo': 'Antipatrones en Saltos',
                      'items': ['Saltos a etiquetas no declaradas o inexistentes en la tabla de cuádruplos.',
                                'Etiquetas huérfanas sin instrucciones posteriores asociadas.',
                                'Bucles infinitos no intencionados por etiquetas mal colocadas al cerrar funciones.']},
      'contexto': {'pregunta': '¿Cómo se le dice al procesador que continúe en otra parte del programa sin perder el orden lógico?',
                   'objetivo': 'Generar etiquetas únicas y las dos formas de un salto incondicional: la marca de destino y el GOTO que la '
                               'usa.',
                   'por_que': 'Una vez que el programa se convierte en una lista lineal, la única forma de representar decisiones y ciclos '
                              'es cortar esa línea con saltos. Las etiquetas son los puntos de reunión; sin nombres únicos, dos '
                              'estructuras anidadas se saltarían entre sí y el flujo quedaría corrupto.',
                   'conceptos': [('Etiqueta',
                                  'Marca simbólica que identifica una instrucción concreta dentro de la lista de cuádruplos.',
                                  'Como el número de un andén: no mueve el tren, solo indica dónde debe detenerse.'),
                                 ('Salto incondicional',
                                  'Instrucción que transfiere el control a una etiqueta sin evaluar ninguna condición.',
                                  "Como un letrero de 'continúe por la puerta B': no pregunta nada, solo desvía."),
                                 ('Bloque básico',
                                  'Tramo de instrucciones que se ejecuta completo, con una sola entrada y una sola salida.',
                                  'Como un vagón de metro: entras por una puerta y sales por la siguiente, sin bajarte a mitad de camino.'),
                                 ('Generador de etiquetas',
                                  'Contador global que produce nombres únicos L0, L1, L2... para evitar colisiones.',
                                  'Como un talonario de fichas numeradas: cada quien toma la siguiente y nadie repite número.')],
                   'resultado': 'Dos funciones en C: una que emite etiquetas L0, L1... y otra que escribe un GOTO o la marca de destino, '
                                'probadas con seis casos.'},
      'lab': {'reto': 'Etiquetas y saltos incondicionales',
              'entregable': 'tus funciones nueva_etiqueta() y emitir_flujo() en artesano_sesion23_c.c, el harness en verde y la bitácora '
                            'en auditorias/auditoria_sesion23.md',
              'explicacion': 'Recibes un contador de etiquetas y, según el modo, debes escribir GOTO Lx o Lx:. La función no imprime: '
                             'escribe en dst y, cuando corresponde, avanza el contador.',
              'reglas': ['nueva_etiqueta() usa el valor actual y después lo incrementa: la primera etiqueta es L0.',
                         'emitir_flujo() con es_salto distinto de cero escribe GOTO; con cero escribe la marca con dos puntos.',
                         'Una etiqueta NULL produce cadena vacía; nunca escribas fuera de cap.'],
              'api': {'header': 'api_sesion23.h',
                      'decls': ['void nueva_etiqueta(char *dst, int cap, int *contador);',
                                'void emitir_flujo(char *dst, int cap, const char *etiqueta, int es_salto);']},
              'stub': 'void nueva_etiqueta(char *dst, int cap, int *contador) {\n'
                      '          (void)dst; (void)cap; (void)contador; /* TODO: escribe LK y avanza el contador */\n'
                      '      }\n'
                      '      \n'
                      '      void emitir_flujo(char *dst, int cap, const char *etiqueta, int es_salto) {\n'
                      '          (void)dst; (void)cap; (void)etiqueta; (void)es_salto; /* TODO: GOTO o marca de destino */\n'
                      '      }',
              'casos': [{'caso': 'nueva_etiqueta(L0)',
                         'codigo': 'int c = 0;\n      char b[32] = "";\n      nueva_etiqueta(b, 32, &c);',
                         'var': 'b',
                         'esperado': 'L0',
                         'tipo': 'str'},
                        {'caso': 'nueva_etiqueta(L5)',
                         'codigo': 'int c = 5;\n      char b[32] = "";\n      nueva_etiqueta(b, 32, &c);',
                         'var': 'b',
                         'esperado': 'L5',
                         'tipo': 'str'},
                        {'caso': 'emitir_flujo(GOTO L2)',
                         'codigo': 'char b[32] = "";\n      emitir_flujo(b, 32, "L2", 1);',
                         'var': 'b',
                         'esperado': 'GOTO L2',
                         'tipo': 'str'},
                        {'caso': 'emitir_flujo(marca L2)',
                         'codigo': 'char b[32] = "";\n      emitir_flujo(b, 32, "L2", 0);',
                         'var': 'b',
                         'esperado': 'L2:',
                         'tipo': 'str'},
                        {'caso': 'emitir_flujo(NULL)',
                         'codigo': 'char b[32] = "";\n      emitir_flujo(b, 32, NULL, 1);',
                         'var': 'b',
                         'esperado': '',
                         'tipo': 'str'},
                        {'caso': 'nueva_etiqueta(L10)',
                         'codigo': 'int c = 10;\n      char b[32] = "";\n      nueva_etiqueta(b, 32, &c);',
                         'var': 'b',
                         'esperado': 'L10',
                         'tipo': 'str'}],
              'criterios': ['Las etiquetas generadas son únicas y consecutivas: L0, L1, L2...',
                            'GOTO y la marca de destino usan exactamente el mismo nombre de etiqueta.',
                            'Una etiqueta NULL no provoca fallo de segmentación y produce cadena vacía.']}},
 24: {'tema': 'Control de Flujo: Sentencias If e If-Else',
      'unidad': 'Unidad 3: Código Intermedio y Optimización',
      'teoria_principal': {'titulo': 'Saltos Condicionales y Evaluación de Cortocircuito',
                           'lead': 'La bifurcación condicional bifurca el flujo según el valor de verdad de una expresión booleana.',
                           'tarjetas': [('01. Instrucción ifFalse / ifTrue',
                                         "Evalúa un temporal booleano y salta si la condición se cumple o no: 'IFFALSE _t0 GOTO L_else'.",
                                         "Permite saltar sobre el bloque 'then' cuando la condición es falsa."),
                                        ('02. Estructura TAC de If-Else',
                                         "Patrón estándar: 'Condición -> IFFALSE L_else -> Cuerpo_Then -> GOTO L_fin -> LABEL L_else -> "
                                         "Cuerpo_Else -> LABEL L_fin'.",
                                         'Garantiza la exclusión mutua estricta entre ambas ramas.'),
                                        ('03. Evaluación de Cortocircuito (Short-Circuit)',
                                         "En 'A && B', si A es falso, no se evalúa B; en 'A || B', si A es verdadero, no se evalúa B.",
                                         'Ahorra tiempo de cómputo y evita fallos de ejecución como desreferenciación nula en '
                                         'condiciones.')]},
      'arquitectura_memoria': {'titulo': 'Plantilla de Emisión para Nodos If-Else',
                               'descripcion': 'Secuencia determinista de generación de etiquetas:',
                               'tarjetas': [('Reserva de Etiquetas al Iniciar',
                                             "Se reservan dos etiquetas: 'L_else = new_label()' y 'L_fin = new_label()'.",
                                             'Evita colisiones con etiquetas generadas recursivamente dentro del cuerpo del if.'),
                                            ('Salto de Escape (Bypass)',
                                             "Al final del bloque 'then', es obligatorio emitir 'GOTO L_fin' para no ejecutar "
                                             "accidentalmente el bloque 'else'.",
                                             'El generador debe enlazar correctamente ambos flujos.')]},
      'casos_borde': {'titulo': 'Fallas Críticas en If-Else',
                      'items': ["Olvidar el 'GOTO L_fin' al final del bloque 'then', provocando que se ejecuten ambas ramas "
                                'consecutivamente.',
                                'Evaluación estricta en lugar de cortocircuito cuando la condición contiene efectos secundarios.',
                                "Etiquetas 'fin' duplicadas en sentencias if anidadas."]},
      'contexto': {'pregunta': '¿Cómo ejecuta el programa una rama y evita la otra si solo sabe avanzar instrucción por instrucción?',
                   'objetivo': 'Traducir una condición booleana a saltos condicionales con cortocircuito, usando una etiqueta de salida '
                               'común.',
                   'por_que': 'Un if no existe en el repertorio del procesador: se construye con una comparación y un salto que se dispara '
                              'cuando la condición falla. Con && y || el orden importa, porque el segundo operando no debe evaluarse si el '
                              'primero ya decidió el resultado.',
                   'conceptos': [('Condición de guardia',
                                  'Expresión booleana que decide si un bloque se ejecuta o se salta.',
                                  'Como el torniquete del metro: si no tienes saldo, no pasas; no hace falta que el tren se detenga.'),
                                 ('Salto condicional',
                                  'Instrucción que salta solo si una bandera o temporal tiene cierto valor de verdad.',
                                  'Como un semáforo: la misma calle, pero solo cruzas cuando la luz está en verde.'),
                                 ('Cortocircuito',
                                  'Detener la evaluación de una condición en cuanto el resultado ya es definitivo.',
                                  'Como una fila de trámites: si el primer requisito no se cumple, no tiene caso formarse en la segunda '
                                  'ventanilla.'),
                                 ('Etiqueta de salida',
                                  'Destino común al que saltan todas las evaluaciones que ya decidieron el resultado.',
                                  'Como la salida de emergencia del edificio: sin importar por dónde empezaste, todas las rutas terminan '
                                  'en la misma puerta.')],
                   'resultado': 'Una función en C que emite el esqueleto de saltos de una condición compuesta y respeta el cortocircuito.'},
      'lab': {'reto': 'Saltos condicionales con cortocircuito',
              'entregable': 'tu función emitir_condicion() en artesano_sesion24_c.c, el harness en verde y la bitácora en '
                            'auditorias/auditoria_sesion24.md',
              'explicacion': 'Recibes dos operandos, un operador lógico (& para AND, | para OR) y una etiqueta de salida. Debes escribir '
                             'los saltos que evalúan el primer operando y, solo si hace falta, el segundo.',
              'reglas': ['Para & usa IFFALSE: si el operando es falso, se salta a la etiqueta de salida.',
                         'Para | usa IFTRUE: si el operando es verdadero, se salta a la etiqueta de salida.',
                         'Si el segundo operando es NULL, emite un solo salto; no inventes una comparación.'],
              'api': {'header': 'api_sesion24.h',
                      'decls': ['int emitir_condicion(char lineas[][64], int max, const char *a, const char *b, char op, const char '
                                '*etiqueta);']},
              'stub': 'int emitir_condicion(char lineas[][64], int max, const char *a, const char *b, char op, const char *etiqueta) {\n'
                      '          (void)lineas; (void)max; (void)a; (void)b; (void)op; (void)etiqueta; /* TODO: saltos con cortocircuito '
                      '*/\n'
                      '          return 0;\n'
                      '      }',
              'casos': [{'caso': 'a && b (primer salto)',
                         'codigo': 'char l[8][64] = {{0}};\n      emitir_condicion(l, 8, "a", "b", \'&\', "L9");',
                         'var': 'l[0]',
                         'esperado': 'IFFALSE a GOTO L9',
                         'tipo': 'str'},
                        {'caso': 'a && b (segundo salto)',
                         'codigo': 'char l[8][64] = {{0}};\n      emitir_condicion(l, 8, "a", "b", \'&\', "L9");',
                         'var': 'l[1]',
                         'esperado': 'IFFALSE b GOTO L9',
                         'tipo': 'str'},
                        {'caso': 'a && b (dos saltos)',
                         'codigo': 'char l[8][64] = {{0}};\n      int n = emitir_condicion(l, 8, "a", "b", \'&\', "L9");',
                         'var': 'n',
                         'esperado': 2,
                         'tipo': 'int'},
                        {'caso': 'a || b (primer salto)',
                         'codigo': 'char l[8][64] = {{0}};\n      emitir_condicion(l, 8, "a", "b", \'|\', "L9");',
                         'var': 'l[0]',
                         'esperado': 'IFTRUE a GOTO L9',
                         'tipo': 'str'},
                        {'caso': 'a || b (segundo salto)',
                         'codigo': 'char l[8][64] = {{0}};\n      emitir_condicion(l, 8, "a", "b", \'|\', "L9");',
                         'var': 'l[1]',
                         'esperado': 'IFTRUE b GOTO L9',
                         'tipo': 'str'},
                        {'caso': 'condicion simple (b NULL)',
                         'codigo': 'char l[4][64] = {{0}};\n      emitir_condicion(l, 4, "a", NULL, \'&\', "L0");',
                         'var': 'l[0]',
                         'esperado': 'IFFALSE a GOTO L0',
                         'tipo': 'str'}],
              'criterios': ['AND emite IFFALSE y OR emite IFTRUE, siempre hacia la etiqueta recibida.',
                            'El segundo operando se evalúa con un salto propio y no se mezcla con el primero.',
                            'Una condición sin segundo operando emite una sola instrucción y no se cae.']}},
 25: {'tema': 'Control de Flujo: Bucles While y For',
      'unidad': 'Unidad 3: Código Intermedio y Optimización',
      'teoria_principal': {'titulo': 'Estructuras Cíclicas, Invariantes y Salidas Múltiples',
                           'lead': 'Los ciclos repiten la ejecución de un bloque hasta que una condición de guardia se invalide.',
                           'tarjetas': [('01. Estructura TAC de Bucle While',
                                         "Patrón: 'LABEL L_inicio -> Evaluar_Condicion -> IFFALSE L_fin -> Cuerpo -> GOTO L_inicio -> "
                                         "LABEL L_fin'.",
                                         'Garantiza que la condición se evalúe antes de cada iteración.'),
                                        ('02. Desugaring de Bucle For',
                                         "Un bucle 'for (init; cond; post) { body }' se transforma internamente en: 'init; while(cond) { "
                                         "body; post; }'.",
                                         'Simplifica el compilador al reutilizar la misma rutina de generación para ambos ciclos.'),
                                        ('03. Sentencias Break y Continue',
                                         "'break' emite un 'GOTO L_fin'; 'continue' emite un 'GOTO L_inicio' o salto a la sección 'post'.",
                                         'Requiere mantener una pila de etiquetas de bucles activos para resolver destinos.')]},
      'arquitectura_memoria': {'titulo': 'Pila de Contexto de Bucles (Loop Stack)',
                               'descripcion': "Gestión de destinos para 'break' y 'continue' anidados:",
                               'tarjetas': [('Estructura LoopContext',
                                             "Contiene 'char label_inicio[32]' y 'char label_fin[32]' del bucle activo.",
                                             "Se empuja a una pila en 'push_loop()' y se retira en 'pop_loop()' al cerrar el ciclo."),
                                            ('Validación de Break Huérfano',
                                             "Si se encuentra una sentencia 'break' y la pila de bucles está vacía, emitir error semántico "
                                             'fatal.',
                                             'Previene saltos ilegales fuera de contextos de bucle o switch.')]},
      'casos_borde': {'titulo': 'Antipatrones en Ciclos',
                      'items': ["Olvidar actualizar la variable de paso (post-incremento) en la transformación de bucles 'for'.",
                                "Resolver un 'break' hacia el bucle exterior en ciclos anidados por no usar una pila LIFO.",
                                'Emisión de la etiqueta de inicio después de la condición, impidiendo la reevaluación del ciclo.']},
      'contexto': {'pregunta': '¿Cómo se representa un ciclo que se repite sin saber de antemano cuántas veces?',
                   'objetivo': 'Construir el esqueleto TAC de while y for con etiquetas de inicio y fin, y ubicar correctamente la '
                               'actualización del iterador.',
                   'por_que': "El procesador no tiene una instrucción 'repetir': el ciclo es un salto hacia atrás condicionado. Si la "
                              'etiqueta de inicio queda después de la condición o si el post-incremento se pierde al desazucarar el for, '
                              'el programa entra en un bucle infinito o nunca itera.',
                   'conceptos': [('Etiqueta de inicio',
                                  'Punto al que vuelve el flujo al terminar cada iteración.',
                                  'Como la línea de salida de una vuelta en una pista: cada vez que completas el recorrido, regresas al '
                                  'mismo punto.'),
                                 ('Condición de guardia',
                                  'Expresión que se evalúa antes de cada vuelta y decide si el ciclo continúa.',
                                  'Como el portero de un antro: cada persona que quiere entrar se somete a la misma revisión.'),
                                 ('Desazucarado (desugaring)',
                                  'Transformar una construcción compleja, como for, en otra más simple que el compilador ya sabe generar.',
                                  'Como convertir una receta para horno en una versión para olla express: cambias la forma, no el '
                                  'resultado.'),
                                 ('Pila de bucles',
                                  'Estructura que guarda las etiquetas del ciclo activo para resolver break y continue anidados.',
                                  'Como los post-its de la puerta del refrigerador: el último que pegaste es el primero que ves y el que '
                                  'corresponde al ciclo actual.')],
                   'resultado': 'Dos funciones en C que emiten el esqueleto TAC de un while y de un for, con etiquetas únicas y el '
                                'iterador en su lugar.'},
      'lab': {'reto': 'Esqueleto TAC de while y for',
              'entregable': 'tus funciones emitir_while() y emitir_for() en artesano_sesion25_c.c, el harness en verde y la bitácora en '
                            'auditorias/auditoria_sesion25.md',
              'explicacion': 'Ambas funciones agregan líneas al arreglo en la posición *n y avanzan ese contador; las etiquetas se toman '
                             'de *etiquetas. Un argumento NULL en inicio o post significa que esa instrucción no se emite.',
              'reglas': ['El while emite cuatro líneas: marca de inicio, salto condicional, GOTO de regreso y marca de fin.',
                         'El for emite init, marca, salto condicional, post, GOTO y marca de fin; si post es NULL, se omite la '
                         'actualización.',
                         'Cada ciclo consume dos etiquetas y las agrega a *etiquetas; no reutilices nombres.'],
              'api': {'header': 'api_sesion25.h',
                      'decls': ['void emitir_while(char lineas[][64], int max, int *n, const char *cond, int *etiquetas);',
                                'void emitir_for(char lineas[][64], int max, int *n, const char *inicio, const char *cond, const char '
                                '*post, int *etiquetas);']},
              'stub': 'void emitir_while(char lineas[][64], int max, int *n, const char *cond, int *etiquetas) {\n'
                      '          (void)lineas; (void)max; (void)n; (void)cond; (void)etiquetas; /* TODO: cuatro lineas del while */\n'
                      '      }\n'
                      '      \n'
                      '      void emitir_for(char lineas[][64], int max, int *n, const char *inicio, const char *cond, const char *post, '
                      'int *etiquetas) {\n'
                      '          (void)lineas; (void)max; (void)n; (void)inicio; (void)cond; (void)post; (void)etiquetas; /* TODO: '
                      'desazucarar */\n'
                      '      }',
              'casos': [{'caso': 'while: marca de inicio',
                         'codigo': 'char l[16][64] = {{0}};\n      int n = 0, e = 0;\n      emitir_while(l, 16, &n, "a < b", &e);',
                         'var': 'l[0]',
                         'esperado': 'L0:',
                         'tipo': 'str'},
                        {'caso': 'while: condicion',
                         'codigo': 'char l[16][64] = {{0}};\n      int n = 0, e = 0;\n      emitir_while(l, 16, &n, "a < b", &e);',
                         'var': 'l[1]',
                         'esperado': 'IFFALSE a < b GOTO L1',
                         'tipo': 'str'},
                        {'caso': 'dos ciclos sin colision',
                         'codigo': 'char l[16][64] = {{0}};\n'
                                   '      int n = 0, e = 0;\n'
                                   '      emitir_while(l, 16, &n, "a < b", &e);\n'
                                   '      emitir_while(l, 16, &n, "c < d", &e);',
                         'var': 'l[4]',
                         'esperado': 'L2:',
                         'tipo': 'str'},
                        {'caso': 'for: inicializacion',
                         'codigo': 'char l[16][64] = {{0}};\n'
                                   '      int n = 0, e = 0;\n'
                                   '      emitir_for(l, 16, &n, "i = 0", "i < 10", "i = i + 1", &e);',
                         'var': 'l[0]',
                         'esperado': 'i = 0',
                         'tipo': 'str'},
                        {'caso': 'for: actualizacion',
                         'codigo': 'char l[16][64] = {{0}};\n'
                                   '      int n = 0, e = 0;\n'
                                   '      emitir_for(l, 16, &n, "i = 0", "i < 10", "i = i + 1", &e);',
                         'var': 'l[3]',
                         'esperado': 'i = i + 1',
                         'tipo': 'str'},
                        {'caso': 'for sin post (NULL)',
                         'codigo': 'char l[16][64] = {{0}};\n'
                                   '      int n = 0, e = 0;\n'
                                   '      emitir_for(l, 16, &n, "j = 0", "j < 3", NULL, &e);',
                         'var': 'n',
                         'esperado': 5,
                         'tipo': 'int'}],
              'criterios': ['El GOTO de regreso apunta a la marca de inicio y el salto condicional a la marca de fin.',
                            'El for coloca la actualización del iterador antes del GOTO de regreso.',
                            'Dos ciclos seguidos usan etiquetas distintas (L0/L1 y L2/L3).']}},
 26: {'tema': 'TAC para Llamadas a Funciones y Retornos',
      'unidad': 'Unidad 3: Código Intermedio y Optimización',
      'teoria_principal': {'titulo': 'Protocolo de Invocación, Parámetros y Cuádruplos Call',
                           'lead': 'El código intermedio desacopla el paso de argumentos preparando la secuencia de instrucciones de '
                                   'invocación.',
                           'tarjetas': [('01. Instrucción PARAM',
                                         "Emite cada argumento antes de la llamada: 'PARAM arg1', 'PARAM arg2'...",
                                         'En C, los parámetros se evalúan típicamente de derecha a izquierda o de izquierda a derecha.'),
                                        ('02. Instrucción CALL',
                                         "Invoca la función especificando el nombre y el número de argumentos: '_t0 = CALL funcion, N'.",
                                         'El número N permite al backend saber cuántos parámetros limpiar de la pila si aplica.'),
                                        ('03. Instrucción RETURN',
                                         "Emite 'RETURN expr' para funciones con valor o 'RETURN' para funciones void.",
                                         'Marca la salida del flujo de control de la rutina actual.')]},
      'arquitectura_memoria': {'titulo': 'Llamadas Anidadas y Preservación de Temporales',
                               'descripcion': "Resolución de expresiones como 'f(g(x), h(y))':",
                               'tarjetas': [('Evaluación Recursiva de Argumentos',
                                             "Primero se evalúa 'g(x)' y se guarda en '_t0'; luego 'h(y)' en '_t1'; finalmente 'PARAM "
                                             "_t0', 'PARAM _t1', 'CALL f, 2'.",
                                             'Garantiza que los temporales de llamadas internas no se sobrescriban.'),
                                            ('Asignación del Resultado',
                                             'Si la función retorna valor, el cuádruplo asigna el resultado directamente a un nuevo '
                                             'temporal.',
                                             "Permite encadenar llamadas en expresiones matemáticas: 'x = f() + 5'.")]},
      'casos_borde': {'titulo': 'Fallas Críticas en Invocaciones',
                      'items': ['Discrepancia entre la aridad del CALL y el número real de cuádruplos PARAM emitidos.',
                                'Sobrescribir temporales de retorno al encadenar múltiples llamadas en la misma línea.',
                                'No emitir instrucción RETURN al final de funciones que finalizan sin bloque explícito.']},
      'contexto': {'pregunta': '¿Qué instrucciones intermedias hacen falta para llamar a una función y recoger su resultado?',
                   'objetivo': 'Emitir la secuencia PARAM ... CALL ... RETURN que representa una invocación, incluyendo llamadas anidadas '
                               'y funciones sin valor de retorno.',
                   'por_que': 'Llamar a una función no es una sola operación: hay que evaluar y pasar argumentos, transferir el control, '
                              'recibir el valor y regresar. El TAC hace explícito cada paso para que el backend sepa cuántos parámetros '
                              'hay y dónde queda el resultado.',
                   'conceptos': [('Parámetro (PARAM)',
                                  'Instrucción que deja un argumento listo para la llamada, en el orden en que la función lo espera.',
                                  'Como los ingredientes que pones sobre la mesa antes de cocinar: cada uno se prepara y se coloca en su '
                                  'lugar antes de encender el fuego.'),
                                 ('CALL',
                                  'Instrucción que transfiere el control a una función e indica cuántos argumentos recibió.',
                                  'Como marcar un número telefónico: necesitas el destino y saber cuántas extensiones vas a pedir.'),
                                 ('RETURN',
                                  'Instrucción que termina la función y, si hay valor, lo entrega a quien llamó.',
                                  'Como el mesero que regresa con tu plato: cierra el pedido y te entrega el resultado.'),
                                 ('Llamada anidada',
                                  'Invocación dentro de otra, donde el resultado temporal de la primera se usa como argumento de la '
                                  'segunda.',
                                  'Como pedir un café que primero necesita que alguien prepare la leche: el segundo paso no empieza hasta '
                                  'que el primero termina.')],
                   'resultado': 'Dos funciones en C que emiten la secuencia de una llamada y la instrucción de retorno, verificadas con '
                                'seis casos.'},
      'lab': {'reto': 'Llamadas, parámetros y retorno',
              'entregable': 'tus funciones emitir_llamada() y emitir_return() en artesano_sesion26_c.c, el harness en verde y la bitácora '
                            'en auditorias/auditoria_sesion26.md',
              'explicacion': 'emitir_llamada() agrega a lineas los PARAM necesarios y la instrucción CALL, actualizando *n. '
                             'emitir_return() escribe en dst el retorno con o sin valor.',
              'reglas': ['Cada argumento no NULL genera un PARAM, en el orden a1, a2.',
                         'El número que acompaña a CALL es la cantidad real de PARAM emitidos.',
                         'Si resultado es NULL, el CALL no asigna; si el valor de retorno es NULL, escribe solo RETURN.'],
              'api': {'header': 'api_sesion26.h',
                      'decls': ['int emitir_llamada(char lineas[][64], int max, int *n, const char *funcion, const char *a1, const char '
                                '*a2, const char *resultado);',
                                'void emitir_return(char *dst, int cap, const char *valor);']},
              'stub': 'int emitir_llamada(char lineas[][64], int max, int *n, const char *funcion, const char *a1, const char *a2, const '
                      'char *resultado) {\n'
                      '          (void)lineas; (void)max; (void)n; (void)funcion; (void)a1; (void)a2; (void)resultado; /* TODO: PARAM y '
                      'CALL */\n'
                      '          return 0;\n'
                      '      }\n'
                      '      \n'
                      '      void emitir_return(char *dst, int cap, const char *valor) {\n'
                      '          (void)dst; (void)cap; (void)valor; /* TODO: RETURN con o sin valor */\n'
                      '      }',
              'casos': [{'caso': 'PARAM x',
                         'codigo': 'char l[16][64] = {{0}};\n      int n = 0;\n      emitir_llamada(l, 16, &n, "f", "x", "y", "_t0");',
                         'var': 'l[0]',
                         'esperado': 'PARAM x',
                         'tipo': 'str'},
                        {'caso': 'PARAM y',
                         'codigo': 'char l[16][64] = {{0}};\n      int n = 0;\n      emitir_llamada(l, 16, &n, "f", "x", "y", "_t0");',
                         'var': 'l[1]',
                         'esperado': 'PARAM y',
                         'tipo': 'str'},
                        {'caso': 'CALL con dos argumentos',
                         'codigo': 'char l[16][64] = {{0}};\n      int n = 0;\n      emitir_llamada(l, 16, &n, "f", "x", "y", "_t0");',
                         'var': 'l[2]',
                         'esperado': '_t0 = CALL f, 2',
                         'tipo': 'str'},
                        {'caso': 'llamada anidada f(g(x))',
                         'codigo': 'char l[16][64] = {{0}};\n'
                                   '      int n = 0;\n'
                                   '      emitir_llamada(l, 16, &n, "g", "x", NULL, "_t0");\n'
                                   '      emitir_llamada(l, 16, &n, "f", "_t0", NULL, "_t1");',
                         'var': 'l[3]',
                         'esperado': '_t1 = CALL f, 1',
                         'tipo': 'str'},
                        {'caso': 'CALL sin argumentos',
                         'codigo': 'char l[8][64] = {{0}};\n      int n = 0;\n      emitir_llamada(l, 8, &n, "p", NULL, NULL, "_t0");',
                         'var': 'l[0]',
                         'esperado': '_t0 = CALL p, 0',
                         'tipo': 'str'},
                        {'caso': 'RETURN con valor',
                         'codigo': 'char b[32] = "";\n      emitir_return(b, 32, "_t0");',
                         'var': 'b',
                         'esperado': 'RETURN _t0',
                         'tipo': 'str'}],
              'criterios': ['Los PARAM se emiten en el mismo orden en que se declararon los argumentos.',
                            'El entero del CALL coincide con el número de PARAM realmente emitidos.',
                            'Una llamada anidada conserva el temporal de la llamada interna y no lo sobrescribe.']}},
 27: {'tema': 'Indexación de Arreglos en Código Intermedio',
      'unidad': 'Unidad 3: Código Intermedio y Optimización',
      'teoria_principal': {'titulo': 'Aplanado de Direcciones y Acceso Indexado',
                           'lead': "En TAC, el acceso a arreglos 'A[i]' se descompone en un cálculo de desplazamiento y una lectura "
                                   'indexada.',
                           'tarjetas': [('01. Cálculo del Desplazamiento Lineal',
                                         "Multiplica el índice por el ancho del tipo: '_t0 = i * sizeof(T)'.",
                                         'Convierte el índice abstracto a un offset físico de memoria en bytes.'),
                                        ('02. Lectura Indexada (Array Read)',
                                         "Instrucción de acceso indirecto: '_t1 = A[_t0]'.",
                                         "Carga en un temporal el valor ubicado en la dirección 'Base(A) + _t0'."),
                                        ('03. Escritura Indexada (Array Write)',
                                         "Instrucción de asignación a memoria: 'A[_t0] = valor'.",
                                         'Modifica el contenido del arreglo en memoria sin asignar a temporales intermediarios.')]},
      'arquitectura_memoria': {'titulo': 'Aplanado de Arreglos Multidimensionales',
                               'descripcion': 'Cálculo de matrices bidimensionales A[N][M]:',
                               'tarjetas': [('Fórmula de Aplanado',
                                             "Para 'A[i][j]', calcula: '_t0 = i * M', '_t1 = _t0 + j', '_t2 = _t1 * sizeof(T)', '_t3 = "
                                             "A[_t2]'.",
                                             'Reduce accesos multidimensionales a un único cálculo de dirección lineal.'),
                                            ('Optimización por Desplazamientos Constantes',
                                             "Si 'i' y 'j' son constantes numéricas conocidas, el offset total se calcula en tiempo de "
                                             'compilación.',
                                             'Elimina todas las multiplicaciones intermedias en runtime.')]},
      'casos_borde': {'titulo': 'Antipatrones en Indexación TAC',
                      'items': ['Olvidar multiplicar el índice por el tamaño del elemento en bytes (sizeof).',
                                "Confundir la lectura indexada con la escritura en sentencias de asignación 'A[i] = B[j]'.",
                                'Desbordamiento de entero en el cálculo de offsets para arreglos tridimensionales grandes.']},
      'contexto': {'pregunta': '¿Cómo se convierte un acceso A[i] en una dirección de memoria concreta?',
                   'objetivo': 'Calcular el desplazamiento de un índice, sumarlo a la base y emitir las instrucciones TAC de lectura '
                               'indexada para arreglos de una y dos dimensiones.',
                   'por_que': 'El procesador no entiende índices: entiende direcciones. El compilador debe multiplicar el índice por el '
                              'ancho del elemento y sumarlo a la base; si olvida el ancho o el orden de las dimensiones, lee la celda '
                              'equivocada sin avisar.',
                   'conceptos': [('Desplazamiento (offset)',
                                  'Distancia en bytes desde el inicio del arreglo hasta el elemento que se quiere leer.',
                                  'Como los kilómetros en una carretera: la base es el punto de partida y el offset te dice cuánto '
                                  'avanzar.'),
                                 ('Base',
                                  'Dirección donde empieza el arreglo en memoria.',
                                  'Como la primera casa de una calle: todas las demás se ubican a partir de ella.'),
                                 ('Ancho de elemento',
                                  'Cantidad de bytes que ocupa un elemento del arreglo, por ejemplo 4 para un int.',
                                  'Como el tamaño de los cajones de un estacionamiento: si cada cajón mide lo mismo, el número de cajón se '
                                  'convierte en distancia.'),
                                 ('Aplanado',
                                  'Transformar un índice multidimensional en un único desplazamiento lineal.',
                                  'Como numerar los asientos de un estadio fila por fila: dos números, fila y asiento, se convierten en un '
                                  'solo número de butaca.')],
                   'resultado': 'Dos funciones en C que emiten el cálculo de offset y la lectura indexada para arreglos 1D y 2D.'},
      'lab': {'reto': 'Desplazamientos para arreglos 1D y 2D',
              'entregable': 'tus funciones emitir_acceso() y emitir_acceso_2d() en artesano_sesion27_c.c, el harness en verde y la '
                            'bitácora en auditorias/auditoria_sesion27.md',
              'explicacion': 'Para un arreglo 1D emites la multiplicación del índice por el ancho y la lectura base[_tK]. Para uno 2D '
                             'primero aplanas i * filas + j, luego multiplicas por el ancho y lees. Los temporales se numeran desde '
                             '*temporales.',
              'reglas': ['Multiplica siempre el índice por el ancho del elemento antes de usarlo como offset.',
                         'En 2D respeta el orden i * filas + j; intercambiar dimensiones lee otra celda.',
                         'Cada temporal nuevo incrementa *temporales; no repitas nombres.'],
              'api': {'header': 'api_sesion27.h',
                      'decls': ['int emitir_acceso(char lineas[][64], int max, const char *base, const char *indice, int ancho, int '
                                '*temporales);',
                                'int emitir_acceso_2d(char lineas[][64], int max, const char *base, const char *i, const char *j, int '
                                'filas, int ancho, int *temporales);']},
              'stub': 'int emitir_acceso(char lineas[][64], int max, const char *base, const char *indice, int ancho, int *temporales) {\n'
                      '          (void)lineas; (void)max; (void)base; (void)indice; (void)ancho; (void)temporales; /* TODO: offset y '
                      'lectura */\n'
                      '          return 0;\n'
                      '      }\n'
                      '      \n'
                      '      int emitir_acceso_2d(char lineas[][64], int max, const char *base, const char *i, const char *j, int filas, '
                      'int ancho, int *temporales) {\n'
                      '          (void)lineas; (void)max; (void)base; (void)i; (void)j; (void)filas; (void)ancho; (void)temporales; /* '
                      'TODO: aplanar y leer */\n'
                      '          return 0;\n'
                      '      }',
              'casos': [{'caso': '1D: i * 4',
                         'codigo': 'char l[8][64] = {{0}};\n      int t = 0;\n      emitir_acceso(l, 8, "A", "i", 4, &t);',
                         'var': 'l[0]',
                         'esperado': '_t0 = i * 4',
                         'tipo': 'str'},
                        {'caso': '1D: A[_t0]',
                         'codigo': 'char l[8][64] = {{0}};\n      int t = 0;\n      emitir_acceso(l, 8, "A", "i", 4, &t);',
                         'var': 'l[1]',
                         'esperado': '_t1 = A[_t0]',
                         'tipo': 'str'},
                        {'caso': '2D: i * 3',
                         'codigo': 'char l[16][64] = {{0}};\n      int t = 0;\n      emitir_acceso_2d(l, 16, "M", "i", "j", 3, 4, &t);',
                         'var': 'l[0]',
                         'esperado': '_t0 = i * 3',
                         'tipo': 'str'},
                        {'caso': '2D: offset por ancho',
                         'codigo': 'char l[16][64] = {{0}};\n      int t = 0;\n      emitir_acceso_2d(l, 16, "M", "i", "j", 3, 4, &t);',
                         'var': 'l[2]',
                         'esperado': '_t2 = _t1 * 4',
                         'tipo': 'str'},
                        {'caso': '2D: M[_t2]',
                         'codigo': 'char l[16][64] = {{0}};\n      int t = 0;\n      emitir_acceso_2d(l, 16, "M", "i", "j", 3, 4, &t);',
                         'var': 'l[3]',
                         'esperado': '_t3 = M[_t2]',
                         'tipo': 'str'},
                        {'caso': 'base NULL (sin acceso)',
                         'codigo': 'char l[8][64] = {{0}};\n      int t = 0;\n      int k = emitir_acceso(l, 8, NULL, "i", 4, &t);',
                         'var': 'k',
                         'esperado': 0,
                         'tipo': 'int'}],
              'criterios': ['El offset siempre incluye la multiplicación por el ancho del elemento.',
                            'En 2D el índice lineal es i * filas + j, en ese orden.',
                            'Cada acceso consume temporales nuevos y una base NULL no emite instrucciones.']}},
 28: {'tema': 'Optimización Local: Plegado de Constantes (Constant Folding)',
      'unidad': 'Unidad 3: Código Intermedio y Optimización',
      'teoria_principal': {'titulo': 'Reducción Estática y Propagación de Constantes',
                           'lead': 'El optimizador simplifica expresiones constantes en tiempo de compilación para ahorrar instrucciones '
                                   'de CPU.',
                           'tarjetas': [('01. Plegado de Constantes (Constant Folding)',
                                         "Si los dos argumentos de un cuádruplo son literales ('_t0 = 3 + 5'), se evalúa en compilación "
                                         "reemplazándolo por '_t0 = 8'.",
                                         'Reduce el número total de instrucciones que llegarán al ensamblador.'),
                                        ('02. Propagación de Constantes (Constant Propagation)',
                                         "Si una variable tiene asignado un valor constante ('x = 10'), sus usos posteriores se reemplazan "
                                         'por el valor literal.',
                                         'Habilita nuevos plegados de constantes en instrucciones dependientes.'),
                                        ('03. Identidades Algebraicas',
                                         "Simplificación de operaciones redundantes: 'x + 0 -> x', 'x * 1 -> x', 'x * 0 -> 0', 'x * 2 -> x "
                                         "+ x'.",
                                         'Sustituye operaciones costosas (multiplicaciones) por operaciones más rápidas o las elimina.')]},
      'arquitectura_memoria': {'titulo': 'Algoritmo de Paso Local sobre Cuádruplos',
                               'descripcion': 'Transformación iterativa de la lista de instrucciones:',
                               'tarjetas': [('Pase de Análisis de Constantes',
                                             'Recorre la lista de cuádruplos; si detecta constantes, calcula el resultado y modifica el '
                                             'cuádruplo a una asignación directa.',
                                             'Se repite en bucle hasta alcanzar un punto fijo donde no haya más simplificaciones '
                                             'posibles.'),
                                            ('Preservación de Semántica',
                                             'El optimizador debe respetar estrictamente el tamaño de los enteros para no alterar '
                                             'desbordamientos legítimos.',
                                             'Garantiza que el código optimizado produzca el mismo resultado que el original.')]},
      'casos_borde': {'titulo': 'Puntos Críticos en Plegado',
                      'items': ["Intentar plegar una división entre cero ('_t0 = 10 / 0') provocando la caída del propio compilador.",
                                'Propagar constantes a través de etiquetas de salto donde la variable podría haber sido modificada por '
                                'otra ruta.',
                                'Divergencia de precisión en operaciones de punto flotante entre host y target.']},
      'contexto': {'pregunta': '¿Para qué calcular en tiempo de ejecución algo que ya se sabe al compilar?',
                   'objetivo': 'Reducir instrucciones TAC aplicando plegado de constantes e identidades algebraicas, sin cambiar el '
                               'resultado del programa.',
                   'por_que': 'Cada operación que el compilador resuelve hoy es una operación que el procesador no ejecutará mañana. El '
                              'plegado también simplifica el código que ven los pases posteriores, pero debe ser conservador: una división '
                              'entre cero o un operando desconocido no se tocan.',
                   'conceptos': [('Plegado de constantes',
                                  'Calcular en compilación una operación cuyos dos operandos ya son literales.',
                                  'Como resolver 2 + 2 en tu cabeza antes de escribir la receta, en lugar de esperar a tener los '
                                  'ingredientes en la mano.'),
                                 ('Propagación de constantes',
                                  'Sustituir una variable por el valor constante que se le asignó, para habilitar más plegados.',
                                  'Como cambiar el nombre de una persona por su apodo en una lista: el significado no cambia y la lista '
                                  'queda más corta.'),
                                 ('Identidad algebraica',
                                  'Regla que elimina una operación redundante, como sumar cero o multiplicar por uno.',
                                  "Como quitar de una receta el paso 'agrega nada': no aporta y solo hace ruido."),
                                 ('Punto fijo',
                                  'Repetir el pase de optimización hasta que ninguna instrucción cambie.',
                                  'Como sacar brillo a un vidrio: repites la pasada hasta que ya no aparece nueva suciedad.')],
                   'resultado': 'Una función en C que pliega constantes, aplica identidades y deja intactas las operaciones que no puede '
                                'resolver.'},
      'lab': {'reto': 'Plegado de constantes e identidades',
              'entregable': 'tu función plegar() en artesano_sesion28_c.c, el harness en verde y la bitácora en '
                            'auditorias/auditoria_sesion28.md',
              'explicacion': 'Recibes el nombre del resultado, el operador y los dos operandos de una instrucción TAC. Debes escribir en '
                             'dst la versión más simple que conserve el significado: un literal calculado, una identidad resuelta o la '
                             'instrucción original.',
              'reglas': ['Solo pliega cuando ambos operandos son enteros completos; nada de prefijos ni texto sobrante.',
                         'x + 0 y x * 1 se reducen a x; x * 0 se reduce a 0.',
                         'Si el divisor es cero, no pliegues: deja la instrucción original y no provoques una excepción.'],
              'api': {'header': 'api_sesion28.h',
                      'decls': ['void plegar(char *dst, int cap, const char *res, const char *op, const char *a, const char *b);']},
              'stub': 'void plegar(char *dst, int cap, const char *res, const char *op, const char *a, const char *b) {\n'
                      '          (void)dst; (void)cap; (void)res; (void)op; (void)a; (void)b; /* TODO: plegar constantes e identidades */\n'
                      '      }',
              'casos': [{'caso': '3 + 5',
                         'codigo': 'char b[64] = "";\n      plegar(b, 64, "_t0", "+", "3", "5");',
                         'var': 'b',
                         'esperado': '_t0 = 8',
                         'tipo': 'str'},
                        {'caso': '2 * 3',
                         'codigo': 'char b[64] = "";\n      plegar(b, 64, "_t0", "*", "2", "3");',
                         'var': 'b',
                         'esperado': '_t0 = 6',
                         'tipo': 'str'},
                        {'caso': '7 - 10',
                         'codigo': 'char b[64] = "";\n      plegar(b, 64, "_t0", "-", "7", "10");',
                         'var': 'b',
                         'esperado': '_t0 = -3',
                         'tipo': 'str'},
                        {'caso': 'x + 0',
                         'codigo': 'char b[64] = "";\n      plegar(b, 64, "_t0", "+", "x", "0");',
                         'var': 'b',
                         'esperado': '_t0 = x',
                         'tipo': 'str'},
                        {'caso': 'x + y (sin plegar)',
                         'codigo': 'char b[64] = "";\n      plegar(b, 64, "_t0", "+", "x", "y");',
                         'var': 'b',
                         'esperado': '_t0 = x + y',
                         'tipo': 'str'},
                        {'caso': '10 / 0 (no plegar)',
                         'codigo': 'char b[64] = "";\n      plegar(b, 64, "_t0", "/", "10", "0");',
                         'var': 'b',
                         'esperado': '_t0 = 10 / 0',
                         'tipo': 'str'}],
              'criterios': ['Dos literales enteros se sustituyen por un solo literal con el resultado calculado.',
                            'Las identidades x + 0, x * 1 y x * 0 se resuelven sin emitir la operación.',
                            'Una división entre cero se conserva intacta y no aborta el programa.']}},
 29: {'tema': 'Optimización: Eliminación de Código Muerto (Dead Code Elimination)',
      'unidad': 'Unidad 3: Código Intermedio y Optimización',
      'teoria_principal': {'titulo': 'Detección de Instrucciones Inalcanzables y Variables Huérfanas',
                           'lead': 'Elimina instrucciones que calculan valores nunca leídos o que residen en bloques inalcanzables.',
                           'tarjetas': [('01. Instrucciones Inalcanzables (Unreachable Code)',
                                         "Código colocado inmediatamente después de un 'GOTO' o 'RETURN' sin una etiqueta intermedia.",
                                         'Se eliminan de forma segura ya que el flujo de ejecución nunca puede alcanzarlas.'),
                                        ('02. Variables Muertas (Dead Variables)',
                                         'Asignaciones a temporales o variables locales que nunca vuelven a leerse antes de ser '
                                         'sobrescritas o salir de ámbito.',
                                         'Reduce la presión sobre los registros de CPU en el backend.'),
                                        ('03. Poda de Ramas Condicionales Muertas',
                                         "En 'if (0) { ... }' o 'if (1) { ... }', el optimizador elimina la rama que nunca se ejecutará y "
                                         'el salto condicional.',
                                         'Convierte bifurcaciones complejas en código secuencial directo.')]},
      'arquitectura_memoria': {'titulo': 'Análisis de Alcance y Grafo de Flujo (Reachability)',
                               'descripcion': 'Algoritmo de marcado y barrido sobre el CFG:',
                               'tarjetas': [('Grafo de Bloques Básicos',
                                             'Se construye un grafo dirigido donde cada nodo es un bloque básico y las aristas son saltos.',
                                             'Un recorrido BFS/DFS desde el bloque inicial marca todos los bloques alcanzables.'),
                                            ('Barrido de Instrucciones Huérfanas',
                                             'Cualquier bloque no marcado como alcanzable se desvincula y se libera de la memoria de '
                                             'cuádruplos.',
                                             'Reduce significativamente el tamaño del binario final.')]},
      'casos_borde': {'titulo': 'Antipatrones en Eliminación de Código',
                      'items': ['Eliminar una instrucción con efectos secundarios (como llamadas a funciones de I/O) creyendo erróneamente '
                                'que es código muerto.',
                                'Borrar etiquetas que son destinos de saltos indirectos o tablas de saltos (switch).',
                                'Romper punteros de la lista de cuádruplos al desvincular un nodo eliminado.']},
      'contexto': {'pregunta': '¿Cómo distingue un compilador el código que nunca se ejecutará del que sí importa?',
                   'objetivo': 'Detectar instrucciones inalcanzables después de un GOTO o un RETURN y compactar la lista de cuádruplos '
                               'conservando las etiquetas.',
                   'por_que': 'El generador de código puede producir instrucciones después de un salto que nunca se alcanzan. Dejarlas no '
                              'cambia el resultado, pero infla el binario y confunde al asignador de registros. La regla es simple: tras '
                              'un salto incondicional, todo es inalcanzable hasta la siguiente etiqueta.',
                   'conceptos': [('Código inalcanzable',
                                  'Instrucciones que el flujo de control no puede ejecutar porque un salto o un retorno las deja atrás.',
                                  'Como una puerta tapiada al final del pasillo: sigue dibujada en el plano, pero nadie puede pasar por '
                                  'ella.'),
                                 ('Etiqueta destino',
                                  'Marca que puede recibir el control desde otra parte y, por lo tanto, reinicia la zona alcanzable.',
                                  'Como una estación de transbordo: aunque el tren anterior terminó, aquí puede llegar otro.'),
                                 ('Barrido',
                                  'Recorrer la lista y conservar solo las instrucciones que el flujo puede alcanzar.',
                                  'Como limpiar una fila de sillas: te llevas solo las que nadie va a usar y dejas las ocupadas.'),
                                 ('Punto de retorno',
                                  'Instrucción RETURN que corta el flujo actual y hace inalcanzable lo que sigue hasta una etiqueta.',
                                  'Como el final de una carta: después de la firma, lo que escribas ya no forma parte del mensaje.')],
                   'resultado': 'Una función en C que elimina instrucciones inalcanzables y devuelve el nuevo tamaño de la lista.'},
      'lab': {'reto': 'Eliminación de código inalcanzable',
              'entregable': 'tu función eliminar_muerto() en artesano_sesion29_c.c, el harness en verde y la bitácora en '
                            'auditorias/auditoria_sesion29.md',
              'explicacion': 'Recibes un arreglo con n instrucciones TAC y debes compactarlo en el mismo arreglo. Conserva todo hasta un '
                             'GOTO o RETURN y descarta lo que sigue hasta la próxima etiqueta; devuelve cuántas instrucciones quedaron.',
              'reglas': ['Una etiqueta termina en dos puntos y siempre es alcanzable: corta la zona muerta.',
                         'El GOTO y el RETURN se conservan; solo se descarta lo que viene después.',
                         'Compacta en el mismo arreglo y no cambies el orden de las instrucciones que sobreviven.'],
              'api': {'header': 'api_sesion29.h', 'decls': ['int eliminar_muerto(char lineas[][64], int n);']},
              'stub': 'int eliminar_muerto(char lineas[][64], int n) {\n'
                      '          (void)lineas; (void)n; /* TODO: compacta y descarta lo inalcanzable */\n'
                      '          return n;\n'
                      '      }',
              'casos': [{'caso': 'tras GOTO: nuevo tamano',
                         'codigo': 'char l[8][64] = {"_t0 = 1", "GOTO L1", "_t1 = 2", "L1:", "_t2 = 3"};\n'
                                   '      int m = eliminar_muerto(l, 5);',
                         'var': 'm',
                         'esperado': 4,
                         'tipo': 'int'},
                        {'caso': 'tras GOTO: etiqueta viva',
                         'codigo': 'char l[8][64] = {"_t0 = 1", "GOTO L1", "_t1 = 2", "L1:", "_t2 = 3"};\n      eliminar_muerto(l, 5);',
                         'var': 'l[2]',
                         'esperado': 'L1:',
                         'tipo': 'str'},
                        {'caso': 'tras RETURN: nuevo tamano',
                         'codigo': 'char l[8][64] = {"_t0 = 1", "RETURN", "_t1 = 2", "L5:", "_t2 = 3"};\n'
                                   '      int m = eliminar_muerto(l, 5);',
                         'var': 'm',
                         'esperado': 4,
                         'tipo': 'int'},
                        {'caso': 'tras RETURN: etiqueta viva',
                         'codigo': 'char l[8][64] = {"_t0 = 1", "RETURN", "_t1 = 2", "L5:", "_t2 = 3"};\n      eliminar_muerto(l, 5);',
                         'var': 'l[2]',
                         'esperado': 'L5:',
                         'tipo': 'str'},
                        {'caso': 'sin codigo muerto',
                         'codigo': 'char l[8][64] = {"_t0 = 1", "_t1 = 2", "_t2 = _t0 + _t1"};\n      int m = eliminar_muerto(l, 3);',
                         'var': 'm',
                         'esperado': 3,
                         'tipo': 'int'},
                        {'caso': 'lista vacia',
                         'codigo': 'char l[4][64] = {{0}};\n      int m = eliminar_muerto(l, 0);',
                         'var': 'm',
                         'esperado': 0,
                         'tipo': 'int'}],
              'criterios': ['Toda instrucción posterior a un GOTO o RETURN se descarta hasta la próxima etiqueta.',
                            'Las etiquetas y las instrucciones alcanzables conservan su orden original.',
                            'Una lista vacía devuelve 0 sin leer memoria fuera del arreglo.']}},
 30: {'tema': 'Hito 3: Generador de TAC y Optimizador End-to-End',
      'unidad': 'Unidad 3: Código Intermedio y Optimización',
      'teoria_principal': {'titulo': 'Integración del Generador de Código Intermedio y Optimizaciones',
                           'lead': 'Culminación de la Unidad 3. El compilador traduce un programa fuente completo a código TAC lineal y '
                                   'aplica optimizaciones locales.',
                           'tarjetas': [('01. Pipeline Intermedio Completo',
                                         "Flujo: 'AST Decorado -> Emisión de Cuádruplos -> Plegado de Constantes -> Eliminación de Código "
                                         "Muerto -> TAC Optimizado'.",
                                         'Produce una lista de instrucciones atómicas lista para la generación de ensamblador.'),
                                        ('02. Emisión Textual de TAC',
                                         "Capacidad de volcar la lista de cuádruplos a un archivo '.tac' legible para inspección y "
                                         'depuración.',
                                         'Permite verificar visual y algorítmicamente la corrección de las optimizaciones aplicadas.'),
                                        ('03. Entrega de Hito 3 (Git Tag)',
                                         "Etiquetado formal de versión en GitHub: 'git tag v0.3-hito3'.",
                                         'Representa el 25% del Proyecto Integrador Semestral.')]},
      'arquitectura_memoria': {'titulo': 'Auditoría de Integridad del Código Intermedio',
                               'descripcion': 'Verificación estricta de la suite de cuádruplos:',
                               'tarjetas': [('Verificación de Unicidad de Etiquetas',
                                             'Comprobación de que no existan etiquetas duplicadas ni saltos a destinos indefinidos.',
                                             'Garantiza que el generador de código x86-64 no produzca errores de ensamblado.'),
                                            ('Batería de Pruebas de Estrés de Optimización',
                                             'Prueba con programas de alta complejidad: ciclos anidados con arreglos, expresiones '
                                             'aritméticas extensas y múltiples funciones.',
                                             'Comprueba que el código optimizado mantenga equivalencia semántica estricta.')]},
      'casos_borde': {'titulo': 'Criterios de Rechazo del Hito 3',
                      'items': ['Generar cuádruplos sintácticamente inválidos o con argumentos superpuestos.',
                                'Corrupción de la lógica del programa tras aplicar el pase de Constant Folding.',
                                'Fugas de memoria al desvincular cuádruplos durante la optimización de código muerto.']},
      'contexto': {'pregunta': '¿Qué tan pequeño y correcto puede quedar el programa intermedio antes de convertirlo en ensamblador?',
                   'objetivo': 'Integrar la traducción de un AST a TAC con el plegado de constantes, devolviendo el lugar donde queda el '
                               'resultado y las instrucciones que sí hacen falta.',
                   'por_que': 'En un compilador real, generar y optimizar no son pasos separados: el emisor ya puede evitar instrucciones '
                              'para subexpresiones constantes. Este cierre de la unidad comprueba que ambas piezas conservan la semántica '
                              'y que el resultado final coincide con el árbol original.',
                   'conceptos': [('Pipeline intermedio',
                                  'Secuencia AST decorado, emisión de TAC, plegado, código muerto y TAC listo para el backend.',
                                  'Como una línea de ensamblaje: cada estación recibe la pieza de la anterior y la entrega más terminada, '
                                  'sin empezar de cero.'),
                                 ('Plegado en el AST',
                                  'Resolver una subexpresión constante durante el recorrido, antes de emitir instrucciones para ella.',
                                  'Como no pedir ingredientes que ya tienes en el refrigerador: evitas la compra y el paso de '
                                  'preparación.'),
                                 ('Resultado constante',
                                  'Valor numérico que sustituye a todo un subárbol porque no depende de ninguna variable.',
                                  'Como el total ya calculado en una factura: no necesitas volver a sumar los renglones.'),
                                 ('Equivalencia semántica',
                                  'Garantía de que el programa optimizado produce exactamente el mismo resultado que el original.',
                                  'Como cambiar el orden de los pasos de una receta sin cambiar el platillo final.')],
                   'resultado': 'Una función en C que traduce un AST a TAC optimizado, pliega constantes y reporta el lugar del '
                                'resultado.'},
      'lab': {'reto': 'AST a TAC optimizado de punta a punta',
              'entregable': 'tu función generar_tac_opt() en artesano_sesion30_c.c, el harness en verde y la bitácora en '
                            'auditorias/auditoria_sesion30.md',
              'explicacion': 'Recibes un árbol con hojas numéricas, variables y operadores binarios. Debes emitir solo las instrucciones '
                             'necesarias: si un subárbol es constante, se calcula en compilación y no genera línea. Además, escribe en '
                             'resultado el literal o el temporal que contiene el valor final.',
              'reglas': ['Un subárbol con dos hojas numéricas se pliega a un literal y no emite instrucciones.',
                         'Las identidades x + 0, x * 1 y x * 0 se resuelven sin generar una operación.',
                         'No pliegues una división entre cero: deja que la instrucción llegue al backend.'],
              'api': {'header': 'api_sesion30.h',
                      'tipos': ['typedef struct Nodo {',
                                '    char tipo;',
                                '    char op;',
                                '    char valor[16];',
                                '    struct Nodo *izq;',
                                '    struct Nodo *der;',
                                '} Nodo;'],
                      'decls': ['int generar_tac_opt(const Nodo *raiz, char lineas[][64], int max, char *resultado, int cap);']},
              'stub': 'int generar_tac_opt(const Nodo *raiz, char lineas[][64], int max, char *resultado, int cap) {\n'
                      '          (void)raiz; (void)lineas; (void)max; (void)resultado; (void)cap; /* TODO: traducir y plegar */\n'
                      '          return 0;\n'
                      '      }',
              'casos': [{'caso': 'x + 2 * 3 (linea)',
                         'codigo': 'Nodo x = {.tipo=\'V\', .valor="x"};\n'
                                   '      Nodo n2 = {.tipo=\'N\', .valor="2"};\n'
                                   '      Nodo n3 = {.tipo=\'N\', .valor="3"};\n'
                                   "      Nodo m = {.tipo='B', .op='*', .izq=&n2, .der=&n3};\n"
                                   "      Nodo s = {.tipo='B', .op='+', .izq=&x, .der=&m};\n"
                                   '      char l[8][64] = {{0}};\n'
                                   '      char r[16] = "";\n'
                                   '      generar_tac_opt(&s, l, 8, r, 16);',
                         'var': 'l[0]',
                         'esperado': '_t0 = x + 6',
                         'tipo': 'str'},
                        {'caso': 'x + 2 * 3 (resultado)',
                         'codigo': 'Nodo x = {.tipo=\'V\', .valor="x"};\n'
                                   '      Nodo n2 = {.tipo=\'N\', .valor="2"};\n'
                                   '      Nodo n3 = {.tipo=\'N\', .valor="3"};\n'
                                   "      Nodo m = {.tipo='B', .op='*', .izq=&n2, .der=&n3};\n"
                                   "      Nodo s = {.tipo='B', .op='+', .izq=&x, .der=&m};\n"
                                   '      char l[8][64] = {{0}};\n'
                                   '      char r[16] = "";\n'
                                   '      generar_tac_opt(&s, l, 8, r, 16);',
                         'var': 'r',
                         'esperado': '_t0',
                         'tipo': 'str'},
                        {'caso': 'x * y + 2 * 3',
                         'codigo': 'Nodo x = {.tipo=\'V\', .valor="x"};\n'
                                   '      Nodo y = {.tipo=\'V\', .valor="y"};\n'
                                   '      Nodo n2 = {.tipo=\'N\', .valor="2"};\n'
                                   '      Nodo n3 = {.tipo=\'N\', .valor="3"};\n'
                                   "      Nodo p = {.tipo='B', .op='*', .izq=&x, .der=&y};\n"
                                   "      Nodo m = {.tipo='B', .op='*', .izq=&n2, .der=&n3};\n"
                                   "      Nodo s = {.tipo='B', .op='+', .izq=&p, .der=&m};\n"
                                   '      char l[8][64] = {{0}};\n'
                                   '      char r[16] = "";\n'
                                   '      generar_tac_opt(&s, l, 8, r, 16);',
                         'var': 'l[1]',
                         'esperado': '_t1 = _t0 + 6',
                         'tipo': 'str'},
                        {'caso': 'todo constante: sin lineas',
                         'codigo': 'Nodo n2 = {.tipo=\'N\', .valor="2"};\n'
                                   '      Nodo n3 = {.tipo=\'N\', .valor="3"};\n'
                                   '      Nodo n4 = {.tipo=\'N\', .valor="4"};\n'
                                   '      Nodo n5 = {.tipo=\'N\', .valor="5"};\n'
                                   "      Nodo s1 = {.tipo='B', .op='+', .izq=&n2, .der=&n3};\n"
                                   "      Nodo s2 = {.tipo='B', .op='+', .izq=&n4, .der=&n5};\n"
                                   "      Nodo m = {.tipo='B', .op='*', .izq=&s1, .der=&s2};\n"
                                   '      char l[8][64] = {{0}};\n'
                                   '      char r[16] = "";\n'
                                   '      int n = generar_tac_opt(&m, l, 8, r, 16);',
                         'var': 'n',
                         'esperado': 0,
                         'tipo': 'int'},
                        {'caso': 'todo constante: resultado',
                         'codigo': 'Nodo n2 = {.tipo=\'N\', .valor="2"};\n'
                                   '      Nodo n3 = {.tipo=\'N\', .valor="3"};\n'
                                   '      Nodo n4 = {.tipo=\'N\', .valor="4"};\n'
                                   '      Nodo n5 = {.tipo=\'N\', .valor="5"};\n'
                                   "      Nodo s1 = {.tipo='B', .op='+', .izq=&n2, .der=&n3};\n"
                                   "      Nodo s2 = {.tipo='B', .op='+', .izq=&n4, .der=&n5};\n"
                                   "      Nodo m = {.tipo='B', .op='*', .izq=&s1, .der=&s2};\n"
                                   '      char l[8][64] = {{0}};\n'
                                   '      char r[16] = "";\n'
                                   '      generar_tac_opt(&m, l, 8, r, 16);',
                         'var': 'r',
                         'esperado': '45',
                         'tipo': 'str'},
                        {'caso': 'x + 0 (identidad)',
                         'codigo': 'Nodo x = {.tipo=\'V\', .valor="x"};\n'
                                   '      Nodo z = {.tipo=\'N\', .valor="0"};\n'
                                   "      Nodo s = {.tipo='B', .op='+', .izq=&x, .der=&z};\n"
                                   '      char l[4][64] = {{0}};\n'
                                   '      char r[16] = "";\n'
                                   '      generar_tac_opt(&s, l, 4, r, 16);',
                         'var': 'r',
                         'esperado': 'x',
                         'tipo': 'str'}],
              'criterios': ['Un subárbol constante se sustituye por su valor y no genera instrucciones.',
                            'El lugar del resultado coincide con el último temporal emitido o con el literal plegado.',
                            'El TAC optimizado conserva exactamente el valor que produciría el árbol original.']}}}
