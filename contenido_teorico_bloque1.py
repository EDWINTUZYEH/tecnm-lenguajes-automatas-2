# contenido_teorico_bloque1.py
# Base de conocimiento conceptual: Unidad 1: Análisis Semántico y AST (Sesiones 01 a 10)
# Materia: Lenguajes y Autómatas II (SCD-1016)
# Docente Titular: MCC. Iván Márquez Larios (ijmarquezl)

TEORIA_BLOQUE_1 = {1: {'tema': 'Encuadre, Diagnóstico de Punteros y Metodología IA',
     'unidad': 'Unidad 1: Análisis Semántico y AST',
     'teoria_principal': {'titulo': 'El Código Fuente como Flujo Continuo de Memoria',
                          'lead': 'Todo compilador trata al programa de entrada como una secuencia contigua de bytes. Manipular punteros '
                                  'es la base del escaneo léxico y semántico.',
                          'tarjetas': [('01. Segmentación de Memoria',
                                        'El código fuente reside en el Heap o Data Segment; los punteros del escáner avanzan sobre '
                                        'direcciones virtuales lineales.',
                                        'Un error de puntero (desplazamiento fuera del buffer) genera un fallo de segmentación (SIGSEGV).'),
                                       ('02. Aritmética de Punteros',
                                        'Avanzar `ptr++` incrementa la dirección en `sizeof(*ptr)` bytes. En `char*`, el salto es de 1 '
                                        'byte exacto.',
                                        'Permite calcular distancias entre lexemas y offsets sin copias auxiliares en memoria.'),
                                       ('03. Invariante de Terminación',
                                        'Toda cadena en C finaliza en el byte nulo `\\0` (0x00). Si se sobreescribe, el compilador leerá '
                                        'memoria no asignada.',
                                        'El cálculo de longitud `strlen()` recorre hasta encontrar `\\0`, con complejidad O(n).')]},
     'arquitectura_memoria': {'titulo': 'Inversión In-Place: Stack vs Heap',
                              'descripcion': 'Modelado del intercambio de punteros en los extremos del buffer:',
                              'tarjetas': [('Punteros Contrapuestos',
                                            'Un puntero `inicio` en `str` y un puntero `fin` en `str + len - 1` convergen al centro en '
                                            'O(n/2) pasos.',
                                            'Requiere verificar que `inicio < fin` en cada iteración.'),
                                           ('Memoria Auxiliar O(1)',
                                            'El intercambio usa un solo byte temporal en el registro/pila sin invocar `malloc()` ni '
                                            'duplicar el buffer.',
                                            'Garantiza eficiencia máxima en entornos restringidos de compilación.')]},
     'casos_borde': {'titulo': 'Antipatrones y Casos Límite a Proteger',
                     'items': ['Puntero `NULL`: Intentar desreferenciar `*str` cuando `str == NULL` causa terminación abrupta.',
                               'Buffer de solo lectura: Intentar mutar un literal `char *s = "HOLA";` causa violación de segmento en el '
                               'segmento `.rodata`.',
                               'Cadenas vacías `""`: `fin` apuntaría a `str - 1`, una dirección ilegal previa al inicio del buffer.']},
     'contexto': {'pregunta': '¿Por qué un compilador necesita mirar la memoria del programa que analiza?',
                  'objetivo': 'Entender cómo vive el código fuente en memoria y recorrerlo con punteros sin salirse del buffer, '
                              'implementando una inversión in-place y auditándola con pruebas automáticas.',
                  'por_que': 'Todo lo que sigue en el curso (tokens, árbol sintáctico, tabla de símbolos) se construye recorriendo memoria '
                             'con punteros. Si un puntero se sale del buffer no hay mensaje de error: el programa se cae. Por eso '
                             'empezamos aquí, antes de compilar nada.',
                  'conceptos': [('Buffer',
                                 'Un tramo de memoria contiguo que guarda el texto de entrada; cada carácter ocupa la dirección siguiente.',
                                 'Como los vagones de un tren: uno pegado al otro, y el puntero es el boleto que dice en qué vagón estás.'),
                                ('Puntero',
                                 'Una variable que guarda una dirección de memoria en lugar de un valor.',
                                 'Como el número de página de un libro: el puntero dice dónde buscar; lo que hay escrito es otra cosa.'),
                                ('Inversión in-place',
                                 'Dar vuelta al contenido del buffer sin reservar un segundo buffer.',
                                 'Como voltear una fila de sillas sin moverlas a otro cuarto: dos personas en los extremos se intercambian '
                                 'hasta encontrarse.'),
                                ('Harness de pruebas',
                                 'Un programa que ejecuta casos de prueba y reporta cuáles pasan y cuáles no.',
                                 'Como un examen de manejo con ruta fija: no importa tu estilo, hay que pasar cada caseta.')],
                  'resultado': 'Una función en C que invierte cualquier cadena en su mismo espacio de memoria y un harness en verde que lo '
                               'demuestra con seis casos.'},
     'lab': {'reto': 'Inversión de buffer in-place',
             'entregable': 'tu función invertir() en artesano_sesion01_c.c, el harness en verde y la bitácora en '
                           'auditorias/auditoria_sesion01.md',
             'explicacion': 'Recibes una cadena mutable y debes darle vuelta sin reservar memoria nueva. Al terminar, la misma dirección '
                            'de memoria contiene los caracteres al revés.',
             'reglas': ['Sin malloc ni arreglos auxiliares: solo dos índices y un char temporal.',
                        'La cadena se modifica en su lugar; no devuelvas una copia.',
                        'invertir(NULL) debe terminar sin caerse.'],
             'api': {'header': 'api_sesion01.h', 'decls': ['void invertir(char *s);']},
             'stub': 'void invertir(char *s) {\n    (void)s; /* TODO: un indice al inicio, otro al final, y un char temporal */\n}',
             'casos': [{'caso': 'invertir("HOLA")',
                        'codigo': 'char a[] = "HOLA";\ninvertir(a);',
                        'var': 'a',
                        'esperado': 'ALOH',
                        'tipo': 'str'},
                       {'caso': 'invertir("abc")',
                        'codigo': 'char b[] = "abc";\ninvertir(b);',
                        'var': 'b',
                        'esperado': 'cba',
                        'tipo': 'str'},
                       {'caso': 'invertir("")', 'codigo': 'char c[] = "";\ninvertir(c);', 'var': 'c', 'esperado': '', 'tipo': 'str'},
                       {'caso': 'invertir("AB")', 'codigo': 'char d[] = "AB";\ninvertir(d);', 'var': 'd', 'esperado': 'BA', 'tipo': 'str'},
                       {'caso': 'invertir("a")', 'codigo': 'char e[] = "a";\ninvertir(e);', 'var': 'e', 'esperado': 'a', 'tipo': 'str'},
                       {'caso': 'invertir(NULL)',
                        'codigo': 'invertir(NULL);',
                        'var': '"sin crash"',
                        'esperado': 'sin crash',
                        'tipo': 'str'}],
             'criterios': ['El buffer original queda invertido: no hay copia ni malloc.',
                           'Los seis casos del harness salen OK con código de salida 0.',
                           'invertir(NULL) y la cadena vacía no provocan fallo de segmentación.']}},
 2: {'tema': 'Gestión en GitHub Web y Nodos Dinámicos en Heap',
     'unidad': 'Unidad 1: Análisis Semántico y AST',
     'teoria_principal': {'titulo': 'Estructuras Dinámicas para Tokens y Símbolos',
                          'lead': 'El compilador no conoce a priori el tamaño del programa. Cada token o nodo debe instanciarse '
                                  'dinámicamente en el Heap.',
                          'tarjetas': [('01. Asignación Dinámica',
                                        '`malloc(sizeof(Token))` reserva memoria contigua en el Heap y devuelve un puntero genérico '
                                        '`void*`.',
                                        'El sistema operativo marca el bloque como ocupado en la tabla de páginas.'),
                                       ('02. Tiempo de Vida (Lifetime)',
                                        'A diferencia del Stack (que se limpia al salir de la función), la memoria en Heap persiste hasta '
                                        'invocar `free()`.',
                                        'Olvidar liberar memoria genera *Memory Leaks* que saturan la compilación de programas extensos.'),
                                       ('03. Enlazamiento Simple',
                                        'Cada nodo contiene su carga útil (lexema, tipo) y un puntero autoreferenciado `struct Token '
                                        '*siguiente`.',
                                        'Permite construir flujos de tokens de longitud arbitraria O(n).')]},
     'arquitectura_memoria': {'titulo': 'El Ciclo de Liberación Segura',
                              'descripcion': 'Prevención del fallo crítico *Use-After-Free*:',
                              'tarjetas': [('Puntero Auxiliar Temporal',
                                            'Antes de ejecutar `free(actual)`, es indispensable respaldar `actual->siguiente` en una '
                                            'variable temporal.',
                                            'Acceder a `actual->siguiente` después de liberar `actual` es comportamiento indefinido (UB).'),
                                           ('Modelo RAII en Rust',
                                            '`Box<Token>` transfiere la propiedad; cuando el nodo sale de ámbito, Rust invoca `drop()` '
                                            'automáticamente.',
                                            'Elimina por completo fugas de memoria y punteros colgantes en tiempo de compilación.')]},
     'casos_borde': {'titulo': 'Antipatrones en la Gestión de Nodos',
                     'items': ['Desbordamiento en copia de lexema: Usar `strcpy` en lugar de `strncpy` provocando buffer overflow.',
                               'Fallo de asignación: No verificar si `malloc` retornó `NULL` por agotamiento de memoria del sistema.',
                               'Liberación de lista vacía: No proteger la función de liberación cuando la cabeza de la lista es `NULL`.']},
     'contexto': {'pregunta': '¿Cómo guarda un compilador una cantidad de datos que no conoce de antemano?',
                  'objetivo': 'Construir una lista enlazada de tokens en el heap, reservando y liberando memoria nodo por nodo sin fugas '
                              'ni accesos a memoria liberada.',
                  'por_que': 'El compilador no sabe cuántos tokens tendrá el programa hasta que lo lee: no puede usar un arreglo fijo. '
                             'Crea un nodo por token y los encadena. Si olvida liberarlos, el proceso crece hasta agotar la memoria; si '
                             'libera y sigue usando, el programa se corrompe.',
                  'conceptos': [('Heap',
                                 'La zona de memoria donde el programa pide espacio en tiempo de ejecución y decide cuándo devolverlo.',
                                 'Como una bodega que rentas por caja: nadie la limpia por ti cuando te vas.'),
                                ('Nodo enlazado',
                                 'Una estructura con dos partes: el dato que guarda y la dirección del siguiente nodo.',
                                 'Como una cadena de pistas: cada tarjeta trae una pista y la ubicación de la siguiente.'),
                                ('Fuga de memoria',
                                 'Reservar memoria y perder la única dirección que permitía liberarla.',
                                 'Como dejar cajas en la bodega sin el recibo: ya no puedes recogerlas, pero siguen ocupando lugar.'),
                                ('Use-after-free',
                                 'Seguir usando un nodo después de liberarlo: el contenido ya no es tuyo y puede cambiar sin aviso.',
                                 'Como usar el boleto de un vuelo que ya despegó: ese asiento ya es de otra persona.')],
                  'resultado': 'Una lista enlazada de tokens que crece token por token, se cuenta, se recorre y se libera sin fugas.'},
     'lab': {'reto': 'Lista enlazada de tokens en heap',
             'entregable': 'tu lista enlazada en artesano_sesion02_c.c, el harness en verde y la bitácora de la sesión',
             'explicacion': 'Recibes la cabeza de una lista y un lexema, y devuelves la lista con el token agregado al final. El harness '
                            'comprueba el orden, el final de la cadena y que liberar no reviente.',
             'reglas': ['Cada nodo se reserva con malloc; el campo siguiente del último vale NULL.',
                        'agregar_token devuelve la cabeza: si la lista estaba vacía, la nueva cabeza es el nodo creado.',
                        'liberar_lista(NULL) no debe caerse.'],
             'api': {'header': 'api_sesion02.h',
                     'tipos': ['typedef struct NodoToken {', '    char lexema[16];', '    struct NodoToken *siguiente;', '} NodoToken;'],
                     'decls': ['NodoToken *agregar_token(NodoToken *cabeza, const char *lexema);',
                               'int contar_tokens(NodoToken *cabeza);',
                               'void liberar_lista(NodoToken *cabeza);']},
             'stub': 'NodoToken *agregar_token(NodoToken *cabeza, const char *lexema) {\n'
                     '    (void)lexema; /* TODO: reserva el nodo, copia el lexema y enlazalo al final */\n'
                     '    return cabeza;\n'
                     '}\n'
                     '\n'
                     'int contar_tokens(NodoToken *cabeza) {\n'
                     '    (void)cabeza; /* TODO: recorre la lista contando nodos */\n'
                     '    return 0;\n'
                     '}\n'
                     '\n'
                     'void liberar_lista(NodoToken *cabeza) {\n'
                     '    (void)cabeza; /* TODO: libera sin perder el puntero al siguiente */\n'
                     '}',
             'casos': [{'caso': 'agregar_token(NULL,"if")',
                        'codigo': 'NodoToken *c = agregar_token(NULL, "if");',
                        'var': '(c != NULL ? c->lexema : "(NULL)")',
                        'esperado': 'if',
                        'tipo': 'str'},
                       {'caso': 'contar_tokens(3 tokens)',
                        'codigo': 'NodoToken *c = NULL;\n'
                                  'c = agregar_token(c, "if");\n'
                                  'c = agregar_token(c, "x");\n'
                                  'c = agregar_token(c, ";");',
                        'var': 'contar_tokens(c)',
                        'esperado': 3,
                        'tipo': 'int'},
                       {'caso': 'orden: segundo token',
                        'codigo': 'NodoToken *c = NULL;\nc = agregar_token(c, "uno");\nc = agregar_token(c, "dos");',
                        'var': '(c && c->siguiente ? c->siguiente->lexema : "(NULL)")',
                        'esperado': 'dos',
                        'tipo': 'str'},
                       {'caso': 'ultimo->siguiente == NULL',
                        'codigo': 'NodoToken *c = NULL;\nc = agregar_token(c, "a");\nc = agregar_token(c, "b");',
                        'var': '(c && c->siguiente ? (c->siguiente->siguiente == NULL) : 0)',
                        'esperado': 1,
                        'tipo': 'int'},
                       {'caso': 'contar_tokens(NULL)', 'codigo': '', 'var': 'contar_tokens(NULL)', 'esperado': 0, 'tipo': 'int'},
                       {'caso': 'liberar_lista(NULL)',
                        'codigo': 'NodoToken *c = NULL;\nc = agregar_token(c, "a");\nliberar_lista(c);\nliberar_lista(NULL);',
                        'var': '"sin crash"',
                        'esperado': 'sin crash',
                        'tipo': 'str'}],
             'criterios': ['Cada token ocupa un nodo reservado con malloc y encadenado con siguiente.',
                           'agregar_token devuelve la lista completa aunque la cabeza cambie.',
                           'contar_tokens(NULL) devuelve 0 y liberar_lista(NULL) no se cae.']}},
 3: {'tema': 'Google Colab, Mágicos y Flujo de Entrega',
     'unidad': 'Unidad 1: Análisis Semántico y AST',
     'teoria_principal': {'titulo': 'Automatización de Compiladores en Entornos Linux',
                          'lead': 'Un compilador se ejecuta como una herramienta de línea de comandos (CLI) sujeta a convenciones POSIX y '
                                  'códigos de retorno.',
                          'tarjetas': [('01. Comandos Mágicos %%writefile',
                                        'Colab permite volcar el contenido de una celda directamente al sistema de archivos virtual de '
                                        'Linux.',
                                        'Permite crear módulos `.c`, `.rs` y scripts de prueba limpios y reproducibles.'),
                                       ('02. Códigos de Salida ABI (Exit Codes)',
                                        'El valor retornado por `main()` (`return 0;` vs `return 1;`) indica al sistema si la compilación '
                                        'fue exitosa.',
                                        'Un compilador que falla debe retornar un código distinto de cero para detener el pipeline de '
                                        'construcción.'),
                                       ('03. Banderas Estrictas de GCC',
                                        'Compilar con `-Wall -Wextra -Werror` convierte cualquier advertencia de tipos o punteros en un '
                                        'error fatal.',
                                        'Evita que errores sutiles de compilación pasen desapercibidos a fases posteriores.')]},
     'arquitectura_memoria': {'titulo': 'Llamadas al Sistema y Flujos Estándar',
                              'descripcion': 'Separación de flujos para diagnósticos limpios:',
                              'tarjetas': [('stdout vs stderr',
                                            'El código generado se emite a `stdout` (1); los mensajes de error semántico deben enviarse a '
                                            '`stderr` (2).',
                                            'Permite redirigir el código objeto generado sin contaminarlo con logs de depuración.'),
                                           ('Tuberías (Pipes POSIX)',
                                            'La salida de un pase del compilador alimenta la entrada del siguiente: `scanner | parser | '
                                            'codegen`.',
                                            'Reduce el acceso a disco intermedio manteniendo los datos en memoria compartida.')]},
     'casos_borde': {'titulo': 'Puntos de Falla en el Pipeline',
                     'items': ['Escribir logs de depuración en `stdout` rompiendo la generación del archivo ensamblador.',
                               'Ignorar advertencias de conversión de tipos enteros con signo a no signo.',
                               'No limpiar archivos binarios previos generando pruebas falsas positivas con binarios obsoletos.']},
     'contexto': {'pregunta': '¿Cómo sabe una máquina de compilación si un paso terminó bien o falló?',
                  'objetivo': 'Escribir y leer archivos desde C y devolver códigos de salida POSIX, para que un pipeline de compilación '
                              'pueda encadenar pasos y detenerse ante un error.',
                  'por_que': 'Un compilador es una herramienta de línea de comandos: recibe un archivo, escribe otro y devuelve un número. '
                             'Ese número (0 = éxito, distinto de 0 = error) es lo que permite que make, GitHub Actions o un script '
                             'encadenen pasos. Sin él, nadie sabe si el paso anterior funcionó.',
                  'conceptos': [('Código de salida',
                                 'El número que un programa devuelve al sistema operativo al terminar; 0 significa éxito.',
                                 'Como el semáforo al final de un trámite: verde (0) o te regresan a ventanilla.'),
                                ('stdout y stderr',
                                 'Dos canales de salida: uno para el resultado y otro para los mensajes de error.',
                                 'Como la banda de equipaje y la oficina de reclamos: no mezcles tu maleta con las quejas.'),
                                ('Archivo como recurso',
                                 'Abrir, leer o escribir y cerrar: el archivo se pide prestado y hay que devolverlo.',
                                 'Como un libro de biblioteca: si no lo devuelves, nadie más puede usarlo.'),
                                ('Bandera -Werror',
                                 'Convertir cualquier advertencia del compilador en un error que detiene la compilación.',
                                 'Como el detector de humo que corta la energía: molesto, pero evita el incendio.')],
                  'resultado': 'Tres funciones en C que escriben y leen archivos y que reportan el código de salida real de un comando '
                               'externo.'},
     'lab': {'reto': 'Archivos: escribir y contar líneas',
             'entregable': 'tus funciones en artesano_sesion03_c.c, el harness en verde y la bitácora de la sesión',
             'explicacion': 'Tu programa escribe un archivo de texto y luego cuenta sus líneas. El harness prueba los tres casos que '
                            'rompen a casi todos: archivo sin salto final, archivo vacío y ruta inexistente.',
             'reglas': ['Usa fopen/fgetc o fgets y cierra siempre el archivo.',
                        'Un archivo inexistente se reporta con -1, no con un aborto.',
                        'Una última línea sin salto de línea también cuenta.'],
             'api': {'header': 'api_sesion03.h',
                     'decls': ['int escribir_texto(const char *ruta, const char *texto);', 'int contar_lineas(const char *ruta);']},
             'stub': 'int escribir_texto(const char *ruta, const char *texto) {\n'
                     '    (void)ruta; (void)texto; /* TODO: abre, escribe, cierra */\n'
                     '    return -1;\n'
                     '}\n'
                     '\n'
                     'int contar_lineas(const char *ruta) {\n'
                     '    (void)ruta; /* TODO: cuenta saltos de linea y no olvides la ultima */\n'
                     '    return -1;\n'
                     '}',
             'casos': [{'caso': 'escribir_texto(...)==0',
                        'codigo': 'int r = escribir_texto("datos.txt", "uno\\ndos\\ntres\\n");',
                        'var': 'r',
                        'esperado': 0,
                        'tipo': 'int'},
                       {'caso': 'contar_lineas(3 lineas)',
                        'codigo': 'escribir_texto("datos.txt", "uno\\ndos\\ntres\\n");',
                        'var': 'contar_lineas("datos.txt")',
                        'esperado': 3,
                        'tipo': 'int'},
                       {'caso': 'contar_lineas(sin salto final)',
                        'codigo': 'escribir_texto("datos2.txt", "a\\nb");',
                        'var': 'contar_lineas("datos2.txt")',
                        'esperado': 2,
                        'tipo': 'int'},
                       {'caso': 'contar_lineas(archivo vacio)',
                        'codigo': 'escribir_texto("vacio.txt", "");',
                        'var': 'contar_lineas("vacio.txt")',
                        'esperado': 0,
                        'tipo': 'int'},
                       {'caso': 'contar_lineas(inexistente)',
                        'codigo': '',
                        'var': 'contar_lineas("no_existe.txt")',
                        'esperado': -1,
                        'tipo': 'int'},
                       {'caso': 'escribir_texto(ruta invalida)',
                        'codigo': '',
                        'var': 'escribir_texto("/no/existe/x.txt", "a")',
                        'esperado': -1,
                        'tipo': 'int'}],
             'criterios': ['Los archivos se cierran en todos los caminos y un error se reporta con -1.',
                           'contar_lineas distingue un archivo vacío, uno con salto final y uno sin él.',
                           'escribir_texto falla con -1 si la ruta no se puede abrir.']}},
 4: {'tema': 'Anatomía de un Árbol Sintáctico Abstracto (AST)',
     'unidad': 'Unidad 1: Análisis Semántico y AST',
     'teoria_principal': {'titulo': 'De Árbol de Derivación Concreta (CST) a AST',
                          'lead': 'El CST contiene ruido sintáctico (paréntesis, palabras reservadas). El AST preserva únicamente la '
                                  'esencia semántica y la jerarquía de las operaciones.',
                          'tarjetas': [('01. Nodos Hoja vs Nodos Internos',
                                        'Las hojas almacenan operandos (literales numéricos, variables). Los nodos internos representan '
                                        'operadores y sentencias.',
                                        'En `3 + 5 * 2`, las hojas son `3`, `5`, `2`; los nodos internos son `+` y `*`.'),
                                       ('02. Tipos de Nodo Discriminados',
                                        'Un AST requiere un discriminante (`enum NodeType`) para interpretar correctamente la unión de '
                                        'datos de cada nodo.',
                                        'Permite representar de forma homogénea expresiones binarias, asignaciones y llamadas a función.'),
                                       ('03. Estructura Recursiva',
                                        'Cada nodo rama contiene punteros a sus hijos izquierdo y derecho (`struct ASTNode *izq, *der`).',
                                        'Refleja la naturaleza recursiva de las gramáticas libres de contexto.')]},
     'arquitectura_memoria': {'titulo': 'Modelado de Nodos AST en Heap',
                              'descripcion': 'Uniones discriminadas en C vs Enums con datos en Rust:',
                              'tarjetas': [('Uniones Etiquetadas (C)',
                                            'Una estructura con `tipo_nodo` y un `union` que comparte espacio para `valor_int`, '
                                            '`nombre_var` o punteros binarios.',
                                            'Ahorra memoria en Heap al dimensionar el nodo al tamaño de su miembro más grande.'),
                                           ('Tipos Algebraicos (Rust)',
                                            '`enum ASTNode { Num(i32), Var(String), BinOp(char, Box<ASTNode>, Box<ASTNode>) }`.',
                                            'El compilador verifica exhaustivamente los patrones mediante `match`, evitando punteros '
                                            'nulos.')]},
     'casos_borde': {'titulo': 'Antipatrones en la Construcción del AST',
                     'items': ['Árbol con ciclos: Un puntero hijo que apunte a un ancestro provocará recursión infinita en todos los '
                               'recorridos.',
                               'Desreferenciación de nodo nulo en operadores unarios (ej. negación `-x` con rama derecha `NULL`).',
                               'Fuga de memoria masiva al descartar ramas de árboles tras detectar un error semántico.']},
     'contexto': {'pregunta': '¿Cómo se guarda una expresión matemática para recorrerla sin perder su estructura?',
                  'objetivo': 'Modelar expresiones como nodos enlazados (número u operación binaria) y evaluarlas recorriendo el árbol.',
                  'por_que': 'El texto 3+5*2 es solo una fila de caracteres; su significado está en la jerarquía. El AST convierte esa '
                             'fila en una estructura donde la multiplicación cuelga de la suma, y esa jerarquía es la que después genera '
                             'código.',
                  'conceptos': [('Árbol',
                                 'Estructura donde cada elemento tiene hijos; en una expresión, cada operación cuelga de la operación que '
                                 'la contiene.',
                                 'Como un organigrama: el gerente (la operación principal) tiene subordinados (las subexpresiones).'),
                                ('Nodo hoja',
                                 'El nodo que no tiene hijos: un número o una variable.',
                                 'Como el extremo de una rama: ahí se acaba el árbol.'),
                                ('Nodo interno',
                                 'El nodo que tiene hijos: una operación que combina los resultados de sus ramas.',
                                 'Como una receta que dice qué hacer con dos ingredientes ya preparados.'),
                                ('Unión discriminada',
                                 'Un mismo tipo de nodo que guarda datos distintos según su etiqueta (número u operación).',
                                 'Como un sobre que dice factura o carta: el sobre es igual, lo que llevas dentro cambia.')],
                  'resultado': 'Un AST mínimo en C con el que puedes construir 3+5*2 y obtener 13 al evaluarlo.'},
     'lab': {'reto': 'Nodo binario de AST',
             'entregable': 'tu AST en artesano_sesion04_c.c, el harness en verde y la bitácora de la sesión',
             'explicacion': 'Construyes nodos numéricos y binarios, los enlazas y el harness recorre el árbol para comprobar su forma y su '
                            'valor. Solo se evalúan +, - y *.',
             'reglas': ['TipoNodo distingue número de operación; no uses campos mágicos.',
                        'Cada nodo se reserva en el heap.',
                        'evaluar(NULL) devuelve -1 y no debe caerse.'],
             'api': {'header': 'api_sesion04.h',
                     'tipos': ['typedef enum { NODO_NUM, NODO_BINOP } TipoNodo;',
                               'typedef struct ASTNode {',
                               '    TipoNodo tipo;',
                               '    int valor;',
                               '    char op;',
                               '    struct ASTNode *izq;',
                               '    struct ASTNode *der;',
                               '} ASTNode;'],
                     'decls': ['ASTNode *crear_numero(int v);',
                               'ASTNode *crear_binario(char op, ASTNode *izq, ASTNode *der);',
                               'int evaluar(ASTNode *n);']},
             'stub': 'ASTNode *crear_numero(int v) {\n'
                     '    (void)v; /* TODO: reserva y llena un nodo NUM */\n'
                     '    return NULL;\n'
                     '}\n'
                     '\n'
                     'ASTNode *crear_binario(char op, ASTNode *izq, ASTNode *der) {\n'
                     '    (void)op; (void)izq; (void)der; /* TODO: reserva y enlaza los hijos */\n'
                     '    return NULL;\n'
                     '}\n'
                     '\n'
                     'int evaluar(ASTNode *n) {\n'
                     '    (void)n; /* TODO: caso base (hoja) y caso recursivo con + - * */\n'
                     '    return -1;\n'
                     '}',
             'casos': [{'caso': 'evaluar(nodo 42)',
                        'codigo': 'ASTNode *n = crear_numero(42);',
                        'var': 'evaluar(n)',
                        'esperado': 42,
                        'tipo': 'int'},
                       {'caso': 'evaluar(3+5*2)',
                        'codigo': "ASTNode *n = crear_binario('+', crear_numero(3), crear_binario('*', crear_numero(5), crear_numero(2)));",
                        'var': 'evaluar(n)',
                        'esperado': 13,
                        'tipo': 'int'},
                       {'caso': 'hijo izquierdo de (* 5 2)',
                        'codigo': "ASTNode *n = crear_binario('*', crear_numero(5), crear_numero(2));",
                        'var': '(n && n->izq ? n->izq->valor : -1)',
                        'esperado': 5,
                        'tipo': 'int'},
                       {'caso': 'operador guardado',
                        'codigo': "ASTNode *n = crear_binario('*', crear_numero(5), crear_numero(2));\n"
                                  'char b[2];\n'
                                  "b[0] = n ? n->op : '?';\n"
                                  "b[1] = '\\0';",
                        'var': 'b',
                        'esperado': '*',
                        'tipo': 'str'},
                       {'caso': 'evaluar(NULL)', 'codigo': '', 'var': 'evaluar(NULL)', 'esperado': -1, 'tipo': 'int'},
                       {'caso': 'evaluar(10-4)',
                        'codigo': "ASTNode *n = crear_binario('-', crear_numero(10), crear_numero(4));",
                        'var': 'evaluar(n)',
                        'esperado': 6,
                        'tipo': 'int'}],
             'criterios': ['crear_binario respeta el orden izquierdo/derecho de los hijos.',
                           'evaluar aplica el operador después de evaluar ambos hijos.',
                           'evaluar(NULL) devuelve -1 sin provocar fallo de segmentación.']}},
 5: {'tema': 'Recorridos del AST y Notación Polaca Inversa',
     'unidad': 'Unidad 1: Análisis Semántico y AST',
     'teoria_principal': {'titulo': 'Patrones de Recorrido y Orden Topológico',
                          'lead': 'Para procesar un AST, debemos visitar sus nodos en un orden determinista según la tarea requerida.',
                          'tarjetas': [('01. Preorden (Raíz, Izq, Der)',
                                        'Útil para emitir declaraciones, copiar árboles o procesar estructuras de control como `if/while`.',
                                        'Visita el nodo padre antes que a cualquiera de sus operandos.'),
                                       ('02. Inorden (Izq, Raíz, Der)',
                                        'Permite reconstruir la expresión matemática en infijo original con su orden matemático.',
                                        'Solo es aplicable a operadores binarios simétricos.'),
                                       ('03. Postorden (Izq, Der, Raíz)',
                                        'El patrón fundamental de evaluación: evalúa primero los operandos hijos y luego aplica el '
                                        'operador padre.',
                                        'Genera directamente la Notación Polaca Inversa (RPN), base de las máquinas de pila.')]},
     'arquitectura_memoria': {'titulo': 'Consumo de Stack en Recorridos Recursivos',
                              'descripcion': 'Gestión del marco de pila durante la evaluación profunda:',
                              'tarjetas': [('Profundidad de Árbol h',
                                            'Cada nivel del árbol añade un marco de función al Stack del sistema operativo. Complejidad '
                                            'espacial O(h).',
                                            'Árboles degenerados lineales muy profundos (>10,000 nodos) provocan desbordamiento del '
                                            'Stack.'),
                                           ('Evaluación con Pila Explícita',
                                            'En RPN, cada hoja se apila (`push`); cada operador desapila dos valores (`pop`), calcula y '
                                            'apila el resultado.',
                                            'Permite evaluar expresiones complejas sin llamadas recursivas adicionales.')]},
     'casos_borde': {'titulo': 'Puntos de Falla en Recorridos',
                     'items': ['Inversión de operandos en operadores no conmutativos: Restar `der - izq` en lugar de `izq - der`.',
                               'No validar punteros `NULL` antes de invocar la llamada recursiva izquierda o derecha.',
                               'Modificación del árbol durante el recorrido sin actualizar los punteros padre.']},
     'contexto': {'pregunta': '¿En qué orden hay que visitar un árbol para poder calcularlo?',
                  'objetivo': 'Recorrer un AST en postorden y producir la notación polaca inversa (RPN), el formato que usa una máquina de '
                              'pila para evaluar.',
                  'por_que': 'Un árbol se puede leer de varias formas y cada una sirve para algo: preorden para declarar, inorden para '
                             'reconstruir la expresión escrita, postorden para calcular. El postorden entrega los operandos antes que el '
                             'operador, justo lo que necesita una pila.',
                  'conceptos': [('Recorrido',
                                 'Una regla fija para visitar todos los nodos de un árbol sin saltarte ninguno.',
                                 'Como el orden de revisar los cuartos de una casa: siempre el mismo, para no dejar ninguno sin revisar.'),
                                ('Postorden',
                                 'Primero el hijo izquierdo, luego el derecho y al final el nodo actual.',
                                 'Como pagar la cuenta: primero se consumen los platillos y al final llega la cuenta.'),
                                ('RPN',
                                 'Escribir la operación después de sus operandos: 3 5 + en vez de 3 + 5.',
                                 'Como una calculadora de pila: escribes los números y luego la operación.'),
                                ('Pila',
                                 'Estructura donde lo último que entra es lo primero que sale.',
                                 'Como una pila de platos: el que pusiste al final es el que tomas primero.')],
                  'resultado': 'Una función que convierte cualquier AST en su RPN y la escribe en un buffer, sin imprimir directamente.'},
     'lab': {'reto': 'Recorrido postorden y RPN',
             'entregable': 'tu función postorden en artesano_sesion05_c.c, el harness en verde y la bitácora',
             'explicacion': 'Dado un árbol, escribes su recorrido postorden separado por espacios en el buffer que te dan; el harness '
                            'compara el texto exacto.',
             'reglas': ['No imprimas con printf dentro de la función: escribe en el buffer.',
                        'Respeta la capacidad: nunca escribas más de cap-1 caracteres más el terminador.',
                        'Un árbol nulo debe producir cadena vacía.'],
             'api': {'header': 'api_sesion05.h',
                     'tipos': ['typedef enum { NODO_NUM, NODO_BINOP } TipoNodo;',
                               'typedef struct ASTNode {',
                               '    TipoNodo tipo;',
                               '    int valor;',
                               '    char op;',
                               '    struct ASTNode *izq;',
                               '    struct ASTNode *der;',
                               '} ASTNode;'],
                     'decls': ['void postorden(ASTNode *n, char *buf, int cap);']},
             'stub': 'void postorden(ASTNode *n, char *buf, int cap) {\n'
                     '    (void)n; (void)cap; /* TODO: recorre izq, der, raiz y escribe separado por espacios */\n'
                     "    if (buf != NULL && cap > 0) buf[0] = '\\0';\n"
                     '}',
             'casos': [{'caso': 'hoja 42',
                        'codigo': 'ASTNode a = {NODO_NUM, 42, 0, NULL, NULL};\nchar b[64];\npostorden(&a, b, 64);',
                        'var': 'b',
                        'esperado': '42',
                        'tipo': 'str'},
                       {'caso': '3+(5*2)',
                        'codigo': 'ASTNode a = {NODO_NUM, 3, 0, NULL, NULL};\n'
                                  'ASTNode b = {NODO_NUM, 5, 0, NULL, NULL};\n'
                                  'ASTNode c = {NODO_NUM, 2, 0, NULL, NULL};\n'
                                  "ASTNode m = {NODO_BINOP, 0, '*', &b, &c};\n"
                                  "ASTNode s = {NODO_BINOP, 0, '+', &a, &m};\n"
                                  'char buf[64];\n'
                                  'postorden(&s, buf, 64);',
                        'var': 'buf',
                        'esperado': '3 5 2 * +',
                        'tipo': 'str'},
                       {'caso': 'arbol NULL', 'codigo': 'char b[16];\npostorden(NULL, b, 16);', 'var': 'b', 'esperado': '', 'tipo': 'str'},
                       {'caso': '(1+2)*(3+4)',
                        'codigo': 'ASTNode a = {NODO_NUM, 1, 0, NULL, NULL};\n'
                                  'ASTNode b = {NODO_NUM, 2, 0, NULL, NULL};\n'
                                  'ASTNode c = {NODO_NUM, 3, 0, NULL, NULL};\n'
                                  'ASTNode d = {NODO_NUM, 4, 0, NULL, NULL};\n'
                                  "ASTNode s1 = {NODO_BINOP, 0, '+', &a, &b};\n"
                                  "ASTNode s2 = {NODO_BINOP, 0, '+', &c, &d};\n"
                                  "ASTNode m = {NODO_BINOP, 0, '*', &s1, &s2};\n"
                                  'char buf[64];\n'
                                  'postorden(&m, buf, 64);',
                        'var': 'buf',
                        'esperado': '1 2 + 3 4 + *',
                        'tipo': 'str'},
                       {'caso': '8-3',
                        'codigo': 'ASTNode a = {NODO_NUM, 8, 0, NULL, NULL};\n'
                                  'ASTNode b = {NODO_NUM, 3, 0, NULL, NULL};\n'
                                  "ASTNode r = {NODO_BINOP, 0, '-', &a, &b};\n"
                                  'char buf[32];\n'
                                  'postorden(&r, buf, 32);',
                        'var': 'buf',
                        'esperado': '8 3 -',
                        'tipo': 'str'}],
             'criterios': ['El recorrido respeta el orden izquierdo, derecho, raíz.',
                           'Los tokens quedan separados por un solo espacio y sin espacio final.',
                           "Un árbol nulo produce cadena vacía y el buffer siempre termina en '\\0'."]}},
 6: {'tema': 'Sistema de Tipos Primitivos y Verificación Semántica',
     'unidad': 'Unidad 1: Análisis Semántico y AST',
     'teoria_principal': {'titulo': 'El Rol del Analizador Semántico',
                          'lead': 'La sintaxis valida que la estructura sea legal; la semántica valida que las operaciones tengan sentido '
                                  'lógico y de tipos.',
                          'tarjetas': [('01. Tipado Estático vs Dinámico',
                                        'En compiladores estáticos, cada variable y expresión tiene un tipo determinado en tiempo de '
                                        'compilación.',
                                        'Previene errores de ejecución antes de generar una sola instrucción binaria.'),
                                       ('02. Tabla de Compatibilidad',
                                        'Una matriz booleana que define qué tipos pueden operar entre sí (ej. `int + int -> int`, `int + '
                                        'float -> float`).',
                                        'Determina si una operación es legal, requiere conversión o es un error semántico.'),
                                       ('03. Equivalencia de Tipos',
                                        'Equivalencia nominal (mismo nombre de tipo) vs estructural (misma disposición de bytes interna).',
                                        'C utiliza equivalencia nominal para `struct` y estructural para tipos básicos vía `typedef`.')]},
     'arquitectura_memoria': {'titulo': 'Atributos Sintetizados de Tipo en el AST',
                              'descripcion': 'Decoración del árbol con información de tipo durante el postorden:',
                              'tarjetas': [('Propagación Ascendente',
                                            'El tipo de un nodo operador se sintetiza a partir de los tipos ya validados de sus dos ramas '
                                            'hijas.',
                                            'Si `izq->tipo == INT` y `der->tipo == INT`, el nodo actual sintetiza `tipo = INT`.'),
                                           ('Tipo ERROR_TYPE',
                                            'Tipo centinela especial asignado a nodos inválidos para evitar que un solo error dispare una '
                                            'cascada de falsas alertas.',
                                            'El analizador semántico reporta el primer error y propaga el centinela.')]},
     'casos_borde': {'titulo': 'Errores Semánticos Típicos',
                     'items': ['Asignación de tipos incompatibles: Asignar un puntero a una variable entera sin casteo explícito.',
                               'Operadores incompatibles: Intentar aplicar operaciones aritméticas a estructuras o cadenas.',
                               'Cascada infinita de errores por no usar un tipo centinela al detectar el primer fallo.']},
     'contexto': {'pregunta': '¿Cómo decide el compilador si una operación entre dos tipos tiene sentido?',
                  'objetivo': 'Aplicar una tabla de compatibilidad de tipos y explicar por qué asignar un tipo más ancho a uno más angosto '
                              'exige una conversión explícita.',
                  'por_que': 'La sintaxis acepta x = y con cualquier cosa; la semántica decide si esos tipos pueden convivir. Esa decisión '
                             'evita que el programa genere instrucciones imposibles, como sumar una estructura con un número.',
                  'conceptos': [('Tipo',
                                 'La etiqueta que dice qué clase de valor es algo y qué operaciones admite.',
                                 'Como el género en una biblioteca: no es el libro, pero dice dónde va y cómo se usa.'),
                                ('Compatibilidad',
                                 'Regla que dice si un valor de un tipo puede usarse donde se espera otro.',
                                 'Como un adaptador de enchufe: si no encaja, o usas adaptador o no hay corriente.'),
                                ('Ensanchamiento y estrechamiento',
                                 'Pasar a un tipo que guarda más información (seguro) o menos (con pérdida).',
                                 'Como vaciar una cubeta en un vaso: cabe, pero algo se derrama.'),
                                ('Tipo centinela',
                                 'Un tipo especial que marca un nodo inválido para no encadenar falsos errores.',
                                 'Como una ficha roja en un inventario: dice este no cuenta y evita seguir contando mal.')],
                  'resultado': 'Una tabla de compatibilidad en C que acepta asignaciones seguras, rechaza las que pierden datos y nombra '
                               'cada tipo.'},
     'lab': {'reto': 'Tabla de compatibilidad de tipos',
             'entregable': 'tu tabla en artesano_sesion06_c.c, el harness en verde y la bitácora',
             'explicacion': 'Implementas compatible(destino, origen) y nombre_tipo(t); el harness prueba asignaciones legales e ilegales y '
                            'el nombre de cada tipo.',
             'reglas': ['La jerarquía es CHAR < INT < FLOAT.',
                        'Asignar a un tipo más angosto se rechaza: requiere cast explícito.',
                        'TIPO_ERROR nunca es compatible con nada.'],
             'api': {'header': 'api_sesion06.h',
                     'tipos': ['typedef enum { TIPO_ERROR = 0, TIPO_CHAR = 1, TIPO_INT = 2, TIPO_FLOAT = 3 } Tipo;'],
                     'decls': ['int compatible(Tipo destino, Tipo origen);', 'const char *nombre_tipo(Tipo t);']},
             'stub': 'int compatible(Tipo destino, Tipo origen) {\n'
                     '    (void)destino; (void)origen; /* TODO: compara la jerarquia */\n'
                     '    return 0;\n'
                     '}\n'
                     '\n'
                     'const char *nombre_tipo(Tipo t) {\n'
                     '    (void)t; /* TODO: devuelve el nombre legible */\n'
                     '    return "desconocido";\n'
                     '}',
             'casos': [{'caso': 'compatible(INT,INT)', 'codigo': '', 'var': 'compatible(TIPO_INT, TIPO_INT)', 'esperado': 1, 'tipo': 'int'},
                       {'caso': 'compatible(FLOAT,INT)',
                        'codigo': '',
                        'var': 'compatible(TIPO_FLOAT, TIPO_INT)',
                        'esperado': 1,
                        'tipo': 'int'},
                       {'caso': 'compatible(INT,FLOAT)',
                        'codigo': '',
                        'var': 'compatible(TIPO_INT, TIPO_FLOAT)',
                        'esperado': 0,
                        'tipo': 'int'},
                       {'caso': 'compatible(INT,ERROR)',
                        'codigo': '',
                        'var': 'compatible(TIPO_INT, TIPO_ERROR)',
                        'esperado': 0,
                        'tipo': 'int'},
                       {'caso': 'nombre_tipo(INT)', 'codigo': '', 'var': 'nombre_tipo(TIPO_INT)', 'esperado': 'int', 'tipo': 'str'},
                       {'caso': 'nombre_tipo(ERROR)', 'codigo': '', 'var': 'nombre_tipo(TIPO_ERROR)', 'esperado': 'error', 'tipo': 'str'}],
             'criterios': ['La compatibilidad solo acepta destinos de igual o mayor rango.',
                           'TIPO_ERROR se rechaza siempre y se nombra como error.',
                           'Los seis casos del harness salen OK con código de salida 0.']}},
 7: {'tema': 'Evaluación de Expresiones Aritméticas y Casos Límite',
     'unidad': 'Unidad 1: Análisis Semántico y AST',
     'teoria_principal': {'titulo': 'Intérprete AST y Evaluación Constante',
                          'lead': 'El analizador semántico debe ser capaz de evaluar expresiones constantes en tiempo de compilación para '
                                  'optimizar el código.',
                          'tarjetas': [('01. Evaluación Recursiva',
                                        'Función `evaluar(ASTNode *nodo)` que resuelve recursivamente subárboles constantes.',
                                        'Si ambos hijos son constantes numéricas, el nodo puede colapsarse a una sola hoja.'),
                                       ('02. Desbordamiento Aritmético (Overflow)',
                                        'Operaciones que exceden los límites del tipo (ej. `INT_MAX + 1` en enteros de 32 bits).',
                                        'El compilador debe advertir o manejar el desbordamiento según la especificación del lenguaje.'),
                                       ('03. División entre Cero',
                                        'Detectar operaciones `x / 0` o `x % 0` estáticamente durante el análisis del programa.',
                                        'Debe reportarse como error semántico fatal antes de intentar la evaluación en el host.')]},
     'arquitectura_memoria': {'titulo': 'Manejo Seguro de Excepciones Aritméticas',
                              'descripcion': 'Validación preventiva en el host de compilación:',
                              'tarjetas': [('Verificación de Divisor Nulo',
                                            'Antes de ejecutar la operación `/` o `%`, evaluar si la rama derecha se resuelve a valor '
                                            'cero.',
                                            'Evita que el propio compilador sufra una interrupción `SIGFPE` (Floating Point Exception).'),
                                           ('Tipos Seguros con Signo',
                                            'Manejo del caso borde de enteros mínimos: `-INT_MIN` causa overflow en arquitecturas de '
                                            'complemento a 2.',
                                            'Requiere promociones temporales a tipos de 64 bits durante la evaluación estática.')]},
     'casos_borde': {'titulo': 'Antipatrones en Evaluación Estática',
                     'items': ['Interrupción del compilador por división entre cero en expresiones constantes.',
                               'Divergencia de precisión de flotantes entre la máquina host (donde compila) y target (donde corre).',
                               'Mutación de variables globales durante la evaluación de expresiones que deberían ser puras.']},
     'contexto': {'pregunta': '¿Quién evalúa las expresiones constantes: el programa o el compilador?',
                  'objetivo': 'Evaluar expresiones de forma recursiva y detectar estáticamente la división entre cero antes de que el '
                              'compilador se caiga.',
                  'por_que': 'El compilador puede calcular 2*3*4 una sola vez y emitir 24 en lugar de tres instrucciones. Pero si esa '
                             'evaluación divide entre cero, el compilador muere con SIGFPE. Detectar el caso antes de operar es parte del '
                             'trabajo.',
                  'conceptos': [('Evaluación recursiva',
                                 'Calcular un nodo pidiendo primero el valor de sus hijos.',
                                 'Como calcular el total de una cuenta: primero cada renglón y luego la suma.'),
                                ('Expresión constante',
                                 'Una operación cuyos operandos ya se conocen en tiempo de compilación.',
                                 'Como un problema de aritmética en el examen: no necesitas ejecutar el programa para saber la respuesta.'),
                                ('División entre cero',
                                 'Operación sin resultado definido que, en el compilador, lo aborta con una señal del sistema.',
                                 'Como dividir una pizza entre cero personas: la pregunta no tiene sentido y el mesero se queda parado.'),
                                ('Propagación de error',
                                 'Cuando un nodo falla, sus padres no se evalúan: se marca el error y se sigue.',
                                 'Como una línea de producción: si una pieza sale mal, no se ensambla el producto; se marca y sigue la '
                                 'siguiente.')],
                  'resultado': 'Un evaluador de árboles que devuelve el valor, marca el error exacto y no se cae ante una división entre '
                               'cero.'},
     'lab': {'reto': 'Evaluador recursivo con detección de errores',
             'entregable': 'tu evaluador en artesano_sesion07_c.c, el harness en verde y la bitácora',
             'explicacion': 'Implementas evaluar(nodo, &error), que calcula el árbol y marca error=1 si hay división entre cero y error=2 '
                            'si el nodo es inválido.',
             'reglas': ['Nunca ejecutes la división antes de comprobar el divisor.',
                        'evaluar(NULL, &e) no debe caerse.',
                        'El error se propaga hacia arriba sin recalcular los padres.'],
             'api': {'header': 'api_sesion07.h',
                     'tipos': ['typedef enum { NODO_NUM, NODO_BINOP } TipoNodo;',
                               'typedef struct ASTNode {',
                               '    TipoNodo tipo;',
                               '    int valor;',
                               '    char op;',
                               '    struct ASTNode *izq;',
                               '    struct ASTNode *der;',
                               '} ASTNode;'],
                     'decls': ['int evaluar(ASTNode *n, int *error);']},
             'stub': 'int evaluar(ASTNode *n, int *error) {\n'
                     '    (void)n; (void)error; /* TODO: hoja, operador e informar el error */\n'
                     '    return 0;\n'
                     '}',
             'casos': [{'caso': '(2+3)*4',
                        'codigo': 'ASTNode a={NODO_NUM,2,0,NULL,NULL}, b={NODO_NUM,3,0,NULL,NULL}, c={NODO_NUM,4,0,NULL,NULL};\n'
                                  "ASTNode s={NODO_BINOP,0,'+',&a,&b}, m={NODO_BINOP,0,'*',&s,&c};\n"
                                  'int e=0;\n'
                                  'int r=evaluar(&m,&e);\n'
                                  '(void)e;',
                        'var': 'r',
                        'esperado': 20,
                        'tipo': 'int'},
                       {'caso': '7/0 -> error 1',
                        'codigo': 'ASTNode a={NODO_NUM,7,0,NULL,NULL}, b={NODO_NUM,0,0,NULL,NULL};\n'
                                  "ASTNode d={NODO_BINOP,0,'/',&a,&b};\n"
                                  'int e=0;\n'
                                  'int r=evaluar(&d,&e);\n'
                                  '(void)r;',
                        'var': 'e',
                        'esperado': 1,
                        'tipo': 'int'},
                       {'caso': '7%0 -> error 1',
                        'codigo': 'ASTNode a={NODO_NUM,7,0,NULL,NULL}, b={NODO_NUM,0,0,NULL,NULL};\n'
                                  "ASTNode d={NODO_BINOP,0,'%',&a,&b};\n"
                                  'int e=0;\n'
                                  'int r=evaluar(&d,&e);\n'
                                  '(void)r;',
                        'var': 'e',
                        'esperado': 1,
                        'tipo': 'int'},
                       {'caso': 'arbol NULL -> error 2',
                        'codigo': 'int e=0;\nint r=evaluar(NULL,&e);\n(void)r;',
                        'var': 'e',
                        'esperado': 2,
                        'tipo': 'int'},
                       {'caso': '10-2-3',
                        'codigo': 'ASTNode a={NODO_NUM,10,0,NULL,NULL}, b={NODO_NUM,2,0,NULL,NULL}, c={NODO_NUM,3,0,NULL,NULL};\n'
                                  "ASTNode s={NODO_BINOP,0,'-',&a,&b}, r2={NODO_BINOP,0,'-',&s,&c};\n"
                                  'int e=0;\n'
                                  'int r=evaluar(&r2,&e);\n'
                                  '(void)e;',
                        'var': 'r',
                        'esperado': 5,
                        'tipo': 'int'},
                       {'caso': '(8/2)+1',
                        'codigo': 'ASTNode a={NODO_NUM,8,0,NULL,NULL}, b={NODO_NUM,2,0,NULL,NULL}, c={NODO_NUM,1,0,NULL,NULL};\n'
                                  "ASTNode d={NODO_BINOP,0,'/',&a,&b}, s={NODO_BINOP,0,'+',&d,&c};\n"
                                  'int e=0;\n'
                                  'int r=evaluar(&s,&e);\n'
                                  '(void)e;',
                        'var': 'r',
                        'esperado': 5,
                        'tipo': 'int'}],
             'criterios': ['La división y el módulo comprueban el divisor antes de operar.',
                           'evaluar(NULL,&e) devuelve error=2 sin caerse.',
                           'Un error en un hijo impide evaluar el padre.']}},
 8: {'tema': 'Inferencia y Promoción de Tipos',
     'unidad': 'Unidad 1: Análisis Semántico y AST',
     'teoria_principal': {'titulo': 'Coerción Implícita y Ensanchamiento de Tipos',
                          'lead': 'Cuando los tipos de los operandos difieren pero son compatibles, el compilador debe insertar '
                                  'conversiones implícitas (*Casting*).',
                          'tarjetas': [('01. Jerarquía de Promoción',
                                        'Regla general: `char -> short -> int -> long -> float -> double`.',
                                        'Los tipos de menor rango se promocionan automáticamente al tipo de mayor rango sin pérdida de '
                                        'datos.'),
                                       ('02. Conversión con Pérdida (Narrowing)',
                                        'Convertir un tipo grande a uno menor (ej. `double -> int` o `int -> char`).',
                                        'El compilador debe emitir advertencias de posible pérdida de precisión o truncamiento.'),
                                       ('03. Nodos de Conversión en el AST',
                                        'La promoción no es mágica: el compilador inserta un nodo explícito `CAST_TO_FLOAT` en el AST.',
                                        'Garantiza que las etapas posteriores de generación de código emitan las instrucciones de '
                                        'conversión correctas.')]},
     'arquitectura_memoria': {'titulo': 'Representación Binaria y Alineación',
                              'descripcion': 'Transformación de registros enteros a flotantes:',
                              'tarjetas': [('Extensión de Signo vs Cero',
                                            'Promocionar un entero con signo (`int8 -> int32`) requiere extender el bit de signo '
                                            '(`movsbl`).',
                                            'Promocionar tipos sin signo requiere extensión con ceros (`movzbl`).'),
                                           ('Registros FPU / SSE',
                                            'Los enteros residen en registros de propósito general (RAX); los flotantes requieren '
                                            'registros vectoriales (XMM0).',
                                            'La conversión implica mover datos entre bancos de registros de CPU diferentes.')]},
     'casos_borde': {'titulo': 'Fallas Críticas de Promoción',
                     'items': ['Promoción de tipos no signados a signados provocando cambios de valores positivos a negativos.',
                               'Comparaciones ambiguas `unsigned int < int` donde el entero negativo se promociona a un valor positivo '
                               'gigante.',
                               'Olvidar insertar el nodo de casteo en el AST generando código ensamblador con tipos mezclados '
                               'incompatibles.']},
     'contexto': {'pregunta': '¿Qué tipo tiene el resultado de mezclar un entero con un flotante?',
                  'objetivo': 'Aplicar la jerarquía de promoción para decidir el tipo de una operación y distinguir cuándo una conversión '
                              'pierde información.',
                  'por_que': 'C no prohíbe mezclar tipos: los promociona en silencio. Ese silencio esconde pérdidas de datos. El '
                             'compilador debe insertar un nodo de conversión explícito en el AST para que el backend emita la instrucción '
                             'correcta.',
                  'conceptos': [('Promoción',
                                 'Convertir automáticamente al tipo más ancho para poder operar.',
                                 'Como pagar en pesos un precio en dólares: alguien hace el cambio antes de cobrar.'),
                                ('Pérdida (narrowing)',
                                 'Convertir a un tipo más angosto; puede truncar o cambiar el valor.',
                                 'Como guardar una foto en miniatura: se ve, pero ya no tiene el detalle.'),
                                ('Nodo de conversión',
                                 'Un nodo extra que el compilador mete en el AST para no olvidar la conversión.',
                                 'Como una nota adhesiva en el expediente: recuerda que hay un trámite antes de continuar.'),
                                ('Extensión de signo',
                                 'Al agrandar un entero con signo hay que copiar el bit de signo, no rellenar con ceros.',
                                 'Como copiar un número negativo a un formulario más largo: el signo también se copia, no solo los '
                                 'dígitos.')],
                  'resultado': 'Una función que decide el tipo común de dos operandos y otra que avisa si una conversión pierde datos.'},
     'lab': {'reto': 'Reglas de promoción y pérdida',
             'entregable': 'tus reglas en artesano_sesion08_c.c, el harness en verde y la bitácora',
             'explicacion': 'Implementas promover(a,b) y hay_perdida(destino,origen); el harness mezcla tipos y comprueba la jerarquía.',
             'reglas': ['Jerarquía: CHAR < INT < FLOAT.',
                        'promover devuelve el tipo más ancho; si uno es ERROR, devuelve ERROR.',
                        'hay_perdida es 1 cuando el destino es más angosto que el origen.'],
             'api': {'header': 'api_sesion08.h',
                     'tipos': ['typedef enum { TIPO_ERROR = 0, TIPO_CHAR = 1, TIPO_INT = 2, TIPO_FLOAT = 3 } Tipo;'],
                     'decls': ['Tipo promover(Tipo a, Tipo b);',
                               'int hay_perdida(Tipo destino, Tipo origen);',
                               'const char *nombre_tipo(Tipo t);']},
             'stub': 'Tipo promover(Tipo a, Tipo b) {\n'
                     '    (void)a; (void)b; /* TODO: devuelve el tipo mas ancho */\n'
                     '    return TIPO_ERROR;\n'
                     '}\n'
                     '\n'
                     'int hay_perdida(Tipo destino, Tipo origen) {\n'
                     '    (void)destino; (void)origen; /* TODO: compara los rangos */\n'
                     '    return 0;\n'
                     '}\n'
                     '\n'
                     'const char *nombre_tipo(Tipo t) {\n'
                     '    (void)t; /* TODO: nombre legible */\n'
                     '    return "desconocido";\n'
                     '}',
             'casos': [{'caso': 'promover(CHAR,INT)',
                        'codigo': '',
                        'var': 'nombre_tipo(promover(TIPO_CHAR, TIPO_INT))',
                        'esperado': 'int',
                        'tipo': 'str'},
                       {'caso': 'promover(INT,FLOAT)',
                        'codigo': '',
                        'var': 'nombre_tipo(promover(TIPO_INT, TIPO_FLOAT))',
                        'esperado': 'float',
                        'tipo': 'str'},
                       {'caso': 'promover(FLOAT,FLOAT)',
                        'codigo': '',
                        'var': 'nombre_tipo(promover(TIPO_FLOAT, TIPO_FLOAT))',
                        'esperado': 'float',
                        'tipo': 'str'},
                       {'caso': 'promover(ERROR,INT)',
                        'codigo': '',
                        'var': 'nombre_tipo(promover(TIPO_ERROR, TIPO_INT))',
                        'esperado': 'error',
                        'tipo': 'str'},
                       {'caso': 'hay_perdida(CHAR,INT)',
                        'codigo': '',
                        'var': 'hay_perdida(TIPO_CHAR, TIPO_INT)',
                        'esperado': 1,
                        'tipo': 'int'},
                       {'caso': 'hay_perdida(INT,CHAR)',
                        'codigo': '',
                        'var': 'hay_perdida(TIPO_INT, TIPO_CHAR)',
                        'esperado': 0,
                        'tipo': 'int'}],
             'criterios': ['promover devuelve siempre el tipo de mayor rango y nunca pierde el centinela ERROR.',
                           'hay_perdida solo es cierto cuando el destino es más angosto.',
                           'Los seis casos del harness salen OK con código de salida 0.']}},
 9: {'tema': 'Reporte Formal de Errores Semánticos y Diagnóstico',
     'unidad': 'Unidad 1: Análisis Semántico y AST',
     'teoria_principal': {'titulo': 'Ingeniería de Diagnósticos y Resiliencia del Parser',
                          'lead': 'Un buen compilador no aborta al primer error; reporta diagnósticos precisos y continúa el análisis para '
                                  'encontrar más fallos.',
                          'tarjetas': [('01. Metadatos de Localización',
                                        'Cada token y nodo AST debe almacenar su número de línea y columna en el archivo fuente.',
                                        'Permite emitir mensajes legibles con contexto visual exacto (`archivo.c:14:5: error: ...`).'),
                                       ('02. Recuperación Semántica',
                                        'Al detectar una incompatibilidad de tipos, el compilador registra el error, asigna un tipo '
                                        'centinela y continúa.',
                                        'Evita que un error tipográfico detenga la verificación del resto de las funciones.'),
                                       ('03. Niveles de Diagnóstico',
                                        'Clasificación formal en `INFO`, `WARNING`, `ERROR` y `FATAL`.',
                                        'Las advertencias no detienen la compilación a menos que se active la bandera `-Werror`.')]},
     'arquitectura_memoria': {'titulo': 'Estructura de la Lista de Diagnósticos',
                              'descripcion': 'Gestión de un pool de errores desacoplado del AST:',
                              'tarjetas': [('Estructura DiagnosticEntry',
                                            'Almacena código de error, mensaje formateado, coordenadas `(linea, columna)` y puntero al '
                                            'siguiente error.',
                                            'Se acumula en una lista enlazada dinámica en Heap durante todo el análisis semántico.'),
                                           ('Límite de Errores (Error Limit)',
                                            'Para evitar saturar la consola con miles de errores en cascada, el compilador aborta al '
                                            'llegar a 20 errores.',
                                            'Mantiene la salida legible para el desarrollador.')]},
     'casos_borde': {'titulo': 'Antipatrones en Manejo de Errores',
                     'items': ['Uso de `exit(1)` inmediato dentro de una función recursiva, impidiendo liberar la memoria del AST.',
                               'Mensajes de error crípticos sin coordenadas de línea ni nombres de identificadores.',
                               'Generar código binario corrupto a pesar de haber registrado errores semánticos fatales.']},
     'contexto': {'pregunta': '¿Qué debe decir un compilador cuando el programa está mal?',
                  'objetivo': 'Emitir diagnósticos con archivo, línea, columna y nivel, en el formato que las herramientas saben leer, y '
                              'seguir analizando después del primer error.',
                  'por_que': 'Un mensaje sin ubicación obliga a buscar a ciegas. El formato archivo:línea:columna: error: mensaje es el '
                             'que editores y CI entienden para llevarte al renglón exacto. Y abortar en el primer error esconde los demás.',
                  'conceptos': [('Diagnóstico',
                                 'El aviso que emite el compilador cuando algo no cumple las reglas, con su ubicación.',
                                 'Como el reporte de un inspector: dice qué está mal y en qué dirección exacta.'),
                                ('Coordenada de origen',
                                 'La línea y la columna donde empieza el problema en el archivo.',
                                 'Como el asiento en un estadio: fila y número, sin eso no encuentras a nadie.'),
                                ('Nivel',
                                 'La gravedad del aviso: info, aviso, error o fatal.',
                                 'Como el triage del hospital: no es lo mismo una gripa que una fractura.'),
                                ('Recuperación',
                                 'Seguir analizando tras un error para reportar varios en una sola pasada.',
                                 'Como el maestro que sigue calificando después de la primera respuesta mal: un error no invalida el '
                                 'examen entero.')],
                  'resultado': 'Un formateador de diagnósticos que produce mensajes idénticos al estilo de GCC y no desborda el buffer.'},
     'lab': {'reto': 'Diagnóstico con línea y columna',
             'entregable': 'tu formateador en artesano_sesion09_c.c, el harness en verde y la bitácora',
             'explicacion': 'Implementas reportar(...), que arma archivo:línea:columna: error: mensaje dentro del buffer que recibe.',
             'reglas': ['El formato es exacto: sin espacios extra ni punto final.',
                        'Nunca escribas más de cap-1 caracteres: el buffer es del llamador.',
                        "El resultado siempre termina en '\\0'."],
             'api': {'header': 'api_sesion09.h',
                     'decls': ['void reportar(const char *archivo, int linea, int columna, const char *mensaje, char *salida, int cap);']},
             'stub': 'void reportar(const char *archivo, int linea, int columna, const char *mensaje, char *salida, int cap) {\n'
                     '    (void)archivo; (void)linea; (void)columna; (void)mensaje; (void)cap;\n'
                     '    /* TODO: arma el diagnostico con snprintf y respeta cap */\n'
                     "    if (salida != NULL && cap > 0) salida[0] = '\\0';\n"
                     '}',
             'casos': [{'caso': 'main.c:14:5',
                        'codigo': 'char b[128];\nreportar("main.c", 14, 5, "tipo incompatible", b, 128);',
                        'var': 'b',
                        'esperado': 'main.c:14:5: error: tipo incompatible',
                        'tipo': 'str'},
                       {'caso': 'a.c:1:1',
                        'codigo': 'char b[64];\nreportar("a.c", 1, 1, "x", b, 64);',
                        'var': 'b',
                        'esperado': 'a.c:1:1: error: x',
                        'tipo': 'str'},
                       {'caso': 'linea 0',
                        'codigo': 'char b[64];\nreportar("x.c", 0, 0, "y", b, 64);',
                        'var': 'b',
                        'esperado': 'x.c:0:0: error: y',
                        'tipo': 'str'},
                       {'caso': 'cap=10 trunca',
                        'codigo': 'char b[10];\nreportar("main.c", 14, 5, "tipo incompatible", b, 10);',
                        'var': 'b',
                        'esperado': 'main.c:14',
                        'tipo': 'str'}],
             'criterios': ['El formato coincide carácter por carácter con el estilo de GCC.',
                           'El buffer nunca se desborda y siempre queda terminado.',
                           'Los cuatro casos del harness salen OK con código de salida 0.']}},
 10: {'tema': 'Hito 1: Mini-Evaluador de Expresiones y AST Completo',
      'unidad': 'Unidad 1: Análisis Semántico y AST',
      'teoria_principal': {'titulo': 'Integración del Frontend Semántico del Compilador',
                           'lead': 'Culminación de la Unidad 1. Conexión completa: Escaneo de tokens, construcción del AST, chequeo '
                                   'estático y reporte de tipos.',
                           'tarjetas': [('01. Pipeline del Frontend',
                                         'Flujo unificado: `Código Fuente -> Tokens -> AST -> Verificación Semántica -> Evaluación '
                                         'Estática`.',
                                         'Base estructural sobre la cual se construirán las siguientes unidades del compilador.'),
                                        ('02. Verificación de Invariantes',
                                         'El AST resultante debe ser acíclico, con tipos consistentes en todos sus nodos y sin fugas en '
                                         'Heap.',
                                         'Se audita automáticamente mediante la suite completa de pruebas unitarias.'),
                                        ('03. Entrega de Hito 1 (Git Tag)',
                                         'Etiquetado formal de versión en el repositorio del estudiante: `git tag v0.1-hito1`.',
                                         'Representa el 20% del Proyecto Integrador Semestral.')]},
      'arquitectura_memoria': {'titulo': 'Validación Integral de Memoria (Valgrind)',
                               'descripcion': 'Auditoría de integridad total del Frontend Semántico:',
                               'tarjetas': [('Cero Fugas (Zero Leaks)',
                                             'Toda la memoria reservada para tokens, nodos AST y tablas temporales debe liberarse '
                                             'limpiamente al terminar.',
                                             'Condición obligatoria para acreditar el hito de evaluación.'),
                                            ('Pruebas de Estrés',
                                             'Evaluación de árboles con más de 100 operadores anidados y combinaciones de tipos mixtos.',
                                             'Demuestra la solidez y estabilidad del código desarrollado.')]},
      'casos_borde': {'titulo': 'Criterios de Rechazo del Hito 1',
                      'items': ['Fallo de segmentación al evaluar expresiones con sintaxis incorrecta o punteros nulos.',
                                'Aceptar operaciones ilegales entre tipos incompatibles sin emitir error semántico.',
                                'Fugas de memoria detectables al destruir el árbol sintáctico.']},
      'contexto': {'pregunta': '¿Puede un programa leer una expresión escrita y devolver su valor sin que nadie la evalúe antes?',
                   'objetivo': 'Integrar lo aprendido en la unidad en un mini-evaluador que lee una expresión desde texto, respeta '
                               'precedencia y paréntesis, y reporta errores de sintaxis y división entre cero.',
                   'por_que': 'Hasta ahora el árbol lo construías tú a mano. El hito consiste en construirlo a partir del texto: eso es el '
                              'frontend de un compilador en miniatura. Si esto funciona, el resto del curso es cambiar el tamaño, no la '
                              'idea.',
                   'conceptos': [('Análisis descendente',
                                  'Leer el texto decidiendo por la estructura de la gramática, de lo general a lo particular.',
                                  'Como leer una receta: primero ves si es entrada, plato fuerte o postre, y luego los ingredientes.'),
                                 ('Precedencia',
                                  'El orden en que se agrupan las operaciones cuando no hay paréntesis.',
                                  'Como la fila del banco: primero quien tiene prioridad, aunque llegue después.'),
                                 ('Recursión mutua',
                                  'Dos funciones que se llaman entre sí para respetar los niveles de la gramática.',
                                  'Como dos porteros que se pasan la pelota según el nivel del visitante.'),
                                 ('Error de sintaxis',
                                  'El texto no encaja en ninguna regla de la gramática.',
                                  'Como una frase a la que le falta el verbo: se entiende la intención, pero no está bien formada.')],
                   'resultado': 'Un mini-evaluador que convierte 2+3*4 en 14, respeta paréntesis y distingue error de sintaxis de división '
                                'entre cero.'},
      'lab': {'reto': 'Mini-evaluador de expresiones (Hito 1)',
              'entregable': 'tu evaluador completo en artesano_sesion10_c.c, el harness en verde y la bitácora del hito',
              'explicacion': 'El analizador ya viene armado: solo completas primaria, termino y expr. Debes leer enteros, + - * /, '
                             'paréntesis y espacios. error=1 es división entre cero; error=2, sintaxis inválida.',
              'reglas': ['Sin variables ni menos unario: solo enteros y los operadores + - * /.',
                         'Respeta precedencia y paréntesis.',
                         'Completa las tres funciones marcadas; no cambies la firma de evaluar_expresion.'],
              'api': {'header': 'api_sesion10.h', 'decls': ['long evaluar_expresion(const char *fuente, int *error);']},
              'stub': '#include <ctype.h>\n'
                      '\n'
                      '/* El analizador ya viene armado: completa las tres funciones marcadas. */\n'
                      'typedef struct { const char *s; int error; } Parser;\n'
                      '\n'
                      'static void saltar(Parser *p) {\n'
                      "    while (*p->s == ' ') p->s++;\n"
                      '}\n'
                      '\n'
                      'long expr(Parser *p);\n'
                      '\n'
                      'long primaria(Parser *p) {\n'
                      "    /* TODO: si hay '(' resuelve expr y consume ')'; si hay digito leelo; si no, error 2 */\n"
                      '    (void)p;\n'
                      '    return 0;\n'
                      '}\n'
                      '\n'
                      'long termino(Parser *p) {\n'
                      "    /* TODO: empieza con primaria y repite mientras veas '*' o '/' */\n"
                      '    (void)p;\n'
                      '    return 0;\n'
                      '}\n'
                      '\n'
                      'long expr(Parser *p) {\n'
                      "    /* TODO: empieza con termino y repite mientras veas '+' o '-' */\n"
                      '    (void)p;\n'
                      '    return 0;\n'
                      '}\n'
                      '\n'
                      'long evaluar_expresion(const char *fuente, int *error) {\n'
                      '    static int sin_error;\n'
                      '    if (error == NULL) error = &sin_error;\n'
                      '    *error = 0;\n'
                      '    if (fuente == NULL) { *error = 2; return 0; }\n'
                      '    Parser p = { fuente, 0 };\n'
                      '    long v = expr(&p);\n'
                      '    saltar(&p);\n'
                      "    if (p.error == 0 && *p.s != '\\0') p.error = 2;\n"
                      '    *error = p.error;\n'
                      '    return p.error != 0 ? 0 : v;\n'
                      '}',
              'casos': [{'caso': '"2+3*4"',
                         'codigo': 'int e=0;\nlong r=evaluar_expresion("2+3*4",&e);\n(void)e;',
                         'var': 'r',
                         'esperado': 14,
                         'tipo': 'int'},
                        {'caso': '"(2+3)*4"',
                         'codigo': 'int e=0;\nlong r=evaluar_expresion("(2+3)*4",&e);\n(void)e;',
                         'var': 'r',
                         'esperado': 20,
                         'tipo': 'int'},
                        {'caso': '"10/0" -> error 1',
                         'codigo': 'int e=0;\nlong r=evaluar_expresion("10/0",&e);\n(void)r;',
                         'var': 'e',
                         'esperado': 1,
                         'tipo': 'int'},
                        {'caso': '"2+" -> error 2',
                         'codigo': 'int e=0;\nlong r=evaluar_expresion("2+",&e);\n(void)r;',
                         'var': 'e',
                         'esperado': 2,
                         'tipo': 'int'},
                        {'caso': '"  7 "',
                         'codigo': 'int e=0;\nlong r=evaluar_expresion("  7 ",&e);\n(void)e;',
                         'var': 'r',
                         'esperado': 7,
                         'tipo': 'int'},
                        {'caso': '"5-10"',
                         'codigo': 'int e=0;\nlong r=evaluar_expresion("5-10",&e);\n(void)e;',
                         'var': 'r',
                         'esperado': -5,
                         'tipo': 'int'}],
              'criterios': ['El analizador respeta precedencia: la multiplicación se resuelve antes que la suma.',
                            'Los paréntesis y los espacios no alteran el resultado.',
                            'La división entre cero y la sintaxis inválida se reportan con códigos distintos.']}}}
