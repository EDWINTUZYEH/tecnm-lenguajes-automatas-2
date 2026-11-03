# contenido_teorico_bloque2.py
# Base de conocimiento conceptual: Unidad 2 (Sesiones 11 a 20)
# Materia: Lenguajes y Autómatas II (SCD-1016)
# Docente Titular: MCC. Iván Márquez Larios (ijmarquezl)

TEORIA_BLOQUE_2 = {
    11: {
        "tema": "Arquitectura de la Tabla de Símbolos",
        "unidad": "Unidad 2: Tabla de Símbolos y Ámbitos",
        "teoria_principal": {
            "titulo": "Estructuras de Búsqueda y Resolución O(1)",
            "lead": "La tabla de símbolos es el diccionario central del compilador. Asocia identificadores textuales con sus metadatos semánticos durante todo el análisis.",
            "tarjetas": [
                ("01. Tablas Hash con Encadenamiento", "Un arreglo de punteros a listas enlazadas (*buckets*). Una función hash mapea el identificador a un índice.", "Permite inserción y búsqueda en tiempo promedio O(1), resolviendo colisiones por encadenamiento."),
                ("02. Función Hash (djb2 / Murmur)", "Algoritmos de dispersión deterministas que distribuyen uniformemente las cadenas en la tabla.", "Una mala función de hash degrada el rendimiento del compilador de O(1) a O(n)."),
                ("03. Carga Útil del Símbolo", "Almacena el nombre (lexema), categoría (variable, función, tipo), tipo de dato y dirección relativa.", "Sirve como puente de comunicación directo entre el frontend y el backend.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Modelado de Buckets y Nodos de Símbolo",
            "descripcion": "Gestión de memoria dinámica para entradas y colisiones:",
            "tarjetas": [
                ("Estructura SymbolEntry", "Contiene `char *nombre`, `Type *tipo`, `int offset`, `int linea` y un puntero `struct SymbolEntry *sig`.", "Se reserva dinámicamente en Heap cada vez que se procesa una declaración nueva."),
                ("Factor de Carga (Load Factor)", "Relación entre número de símbolos y tamaño de la tabla. Si supera 0.75, requiere rehasheo dinámico.", "Evita listas de colisión excesivamente largas que ralentizan la compilación.")
            ]
        },
        "casos_borde": {
            "titulo": "Antipatrones en Tablas de Símbolos",
            "items": [
                "Colisiones no resueltas: Sobrescribir una entrada existente al ocurrir una colisión de hash en lugar de encadenar.",
                "Comparación errónea de identificadores: Comparar punteros de memoria (`ptr1 == ptr2`) en lugar del contenido con `strcmp()`.",
                "Punteros colgantes tras rehasheo de tabla."
            ]
        },
        "contexto": {
            "pregunta": "¿Dónde guarda el compilador el nombre de cada variable mientras lee el programa?",
            "objetivo": "Entender por qué la tabla de símbolos usa una función de dispersión y cadenas de colisión, e implementar una tabla que inserte nombres sin perder información cuando dos claves caen en la misma cubeta.",
            "por_que": "Cada vez que el analizador encuentra un identificador debe responder rápido a dos preguntas: ¿ya existe? y ¿qué tipo tiene? Una tabla hash con encadenamiento resuelve ambas en tiempo casi constante, y esa velocidad es la que permite compilar archivos con miles de símbolos sin que el tiempo crezca de forma cuadrática. Si la tabla pierde entradas por una colisión mal manejada, el resto del compilador trabaja con información falsa.",
            "conceptos": [
                ("Cubeta", "Ranura de la tabla donde se guarda el primer símbolo de una lista.", "Como los casilleros de una recepción: la fórmula dice en qué casillero buscar, y si ya hay alguien se forma una lista en el mismo lugar."),
                ("Colisión", "Situación en la que dos nombres distintos producen el mismo índice de la tabla.", "Como dos personas con apellidos distintos a las que la regla alfabética manda al mismo cajón del archivador."),
                ("Encadenamiento", "Técnica que resuelve una colisión guardando los símbolos en una lista dentro de la misma cubeta.", "Como colgar varias llaves del mismo gancho: cada llave conserva su etiqueta y se recorren una por una."),
                ("Función hash", "Fórmula determinista que convierte un nombre en un número de posición.", "Como la regla que asigna mesa según la inicial del apellido: siempre la misma regla da siempre el mismo resultado.")
            ],
            "resultado": "Una tabla hash en C que inserta símbolos, rechaza nombres repetidos y conserva las colisiones en cadenas enlazadas, junto con un harness en verde que lo demuestra."
        },
        "lab": {
            "reto": "Tabla hash con encadenamiento",
            "entregable": "tus funciones hash_djb2() e insertar_simbolo() en artesano_sesion11_c.c, la salida del harness y la bitácora en auditorias/auditoria_sesion11.md",
            "explicacion": "Recibes un arreglo de cubetas vacías y una secuencia de nombres: calcula la posición con djb2, crea un nodo por símbolo nuevo y recorre la cadena cuando dos nombres coinciden en la misma cubeta. insertar_simbolo() devuelve 1 si insertó, 0 si el nombre ya existía y -1 ante argumentos inválidos; el harness comprueba cuántos nodos hay y qué offset conserva cada uno.",
            "reglas": [
                "Ningún nombre se duplica: si ya existe en cualquier cubeta, insertar devuelve 0 y no crea nodo.",
                "Una colisión se encadena; jamás se sobrescribe una entrada existente.",
                "Con tabla NULL, nombre NULL o cero cubetas, insertar devuelve -1."
            ],
            "api": {
                "header": "api_sesion11.h",
                "decls": [
                    "unsigned int hash_djb2(const char *clave);",
                    "int insertar_simbolo(Simbolo *tabla[], unsigned int cubetas, const char *nombre, int tipo, int offset);"
                ],
                "tipos": [
                    "typedef struct Simbolo {",
                    "    char nombre[16];",
                    "    int tipo;",
                    "    int offset;",
                    "    struct Simbolo *sig;",
                    "} Simbolo;"
                ]
            },
            "stub": "unsigned int hash_djb2(const char *clave) {\n    (void)clave; /* TODO: empieza en 5381 y multiplica por 33 en cada byte */\n    return 0;\n}\n\nint insertar_simbolo(Simbolo *tabla[], unsigned int cubetas, const char *nombre, int tipo, int offset) {\n    (void)tabla; (void)cubetas; (void)nombre; (void)tipo; (void)offset; /* TODO */\n    return -1;\n}",
            "casos": [
                {"caso": "hash_djb2(\"\")", "codigo": "unsigned int r = hash_djb2(\"\");", "var": "r", "esperado": 5381, "tipo": "int"},
                {"caso": "hash_djb2(\"abc\")", "codigo": "unsigned int r = hash_djb2(\"abc\");", "var": "r", "esperado": 193485963, "tipo": "int"},
                {"caso": "insertar x dos veces", "codigo": "Simbolo *t[8] = {0};\ninsertar_simbolo(t, 8, \"x\", 1, 0);\nint r = insertar_simbolo(t, 8, \"x\", 2, 8);", "var": "r", "esperado": 0, "tipo": "int"},
                {"caso": "dos claves, una cubeta", "codigo": "Simbolo *t[1] = {0};\ninsertar_simbolo(t, 1, \"alpha\", 1, 0);\ninsertar_simbolo(t, 1, \"beta\", 2, 4);\nint r = 0;\nfor (Simbolo *p = t[0]; p != NULL; p = p->sig) r++;", "var": "r", "esperado": 2, "tipo": "int"},
                {"caso": "offset de beta en cadena", "codigo": "Simbolo *t[1] = {0};\ninsertar_simbolo(t, 1, \"alpha\", 1, 0);\ninsertar_simbolo(t, 1, \"beta\", 2, 4);\nint r = -1;\nfor (Simbolo *p = t[0]; p != NULL; p = p->sig) {\n    if (strcmp(p->nombre, \"beta\") == 0) r = p->offset;\n}", "var": "r", "esperado": 4, "tipo": "int"},
                {"caso": "insertar en tabla NULL", "codigo": "int r = insertar_simbolo(NULL, 8, \"x\", 1, 0);", "var": "r", "esperado": -1, "tipo": "int"}
            ],
            "criterios": [
                "hash_djb2() reproduce la fórmula djb2 para claves vacías, cortas y repetidas.",
                "Dos nombres con el mismo índice quedan en la misma cadena y ninguno se pierde.",
                "El harness reporta 6/6 en verde y el esqueleto inicial falla antes de implementar."
            ]
        }
    },
    12: {
        "tema": "Atributos de Símbolos y Cálculo de Memoria",
        "unidad": "Unidad 2: Tabla de Símbolos y Ámbitos",
        "teoria_principal": {
            "titulo": "Metadatos Semánticos, Ancho de Tipos y Desplazamientos",
            "lead": "Cada variable declarada debe tener una ubicación relativa calculada en el registro de activación o segmento de datos.",
            "tarjetas": [
                ("01. Ancho de Tipos (Type Width)", "Tamaño en bytes requerido por el tipo de dato: `char: 1`, `short: 2`, `int/float: 4`, `double/ptr: 8`.", "Determina cuánto espacio debe reservar el compilador para cada variable."),
                ("02. Cálculo de Offset (Desplazamiento)", "Distancia en bytes desde la dirección base del marco de pila (`RBP - offset`).", "Las variables locales se acumulan consecutivamente: `offset_actual += ancho_variable`."),
                ("03. Alineación de Memoria (Data Alignment)", "Las CPUs acceden a datos de forma eficiente cuando las direcciones son múltiplos de su tamaño natural (2, 4 u 8 bytes).", "Requiere insertar bytes de relleno (*padding*) entre variables adyacentes.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Alineación y Padding en el Stack Frame",
            "descripcion": "Disposición en el registro de activación de la función:",
            "tarjetas": [
                ("Alineación por Palabras", "Una variable `int` (4 bytes) declarada después de un `char` (1 byte) requiere 3 bytes de padding intermedio.", "Fórmula de alineación: `offset = (offset + align - 1) & ~(align - 1)`."),
                ("Alineación del Stack a 16 Bytes", "La especificación ABI x86-64 System V exige que el Stack Pointer (RSP) esté alineado a 16 bytes antes de un `call`.", "Previene fallos de protección general en instrucciones vectoriales SSE.")
            ]
        },
        "casos_borde": {
            "titulo": "Puntos de Falla en Asignación de Memoria",
            "items": [
                "Offsets superpuestos por omitir el tamaño real del tipo de dato previo.",
                "Ignorar el padding de alineación provocando lecturas no alineadas y caídas de rendimiento en CPU.",
                "Desbordamiento de entero en el cálculo del tamaño total de estructuras grandes."
            ]
        },
        "contexto": {
            "pregunta": "¿Cuántos bytes ocupa cada variable y por qué el compilador no puede sumar tamaños sin más?",
            "objetivo": "Calcular el ancho de cada tipo y el desplazamiento que le corresponde a la siguiente variable dentro del marco de pila, respetando la alineación natural de la arquitectura.",
            "por_que": "El backend necesita una dirección concreta para cada variable, y esa dirección no es una suma directa: la CPU lee más rápido cuando un dato de 4 bytes empieza en un múltiplo de 4. El analizador semántico resuelve los offsets en tiempo de compilación, así que un error de alineación se convierte en código que funciona a medias o que falla solo en ciertas máquinas. Esta sesión produce el cálculo que después usarán todos los accesos a memoria del programa.",
            "conceptos": [
                ("Ancho de tipo", "Número de bytes que ocupa un valor de ese tipo cuando se guarda en memoria.", "Como el tamaño de la caja que pides en una mudanza: un libro va en caja chica y un televisor en caja grande."),
                ("Alineación", "Regla que exige que el inicio de un dato sea múltiplo de su tamaño.", "Como los postes de una barda: si quieres atravesar una tabla, los soportes deben caer en posiciones exactas y no a medio metro."),
                ("Desplazamiento", "Distancia en bytes desde el inicio del marco de pila hasta la variable.", "Como el número de asiento de un avión: la fila y la letra te dicen exactamente dónde sentarte sin contar desde la puerta."),
                ("Relleno", "Bytes vacíos que se dejan entre dos variables para respetar la alineación.", "Como el espacio libre que dejas entre platos en una caja para que no se rompan: no guarda nada, pero permite que todo quepa bien.")
            ],
            "resultado": "Un calculador que llena el registro de un símbolo con su offset alineado y devuelve el cursor para el siguiente, con pruebas de char, short, int y double."
        },
        "lab": {
            "reto": "Registro de símbolo y offsets alineados",
            "entregable": "tus funciones ancho_de_tipo() y asignar_offset() en artesano_sesion12_c.c, la salida del harness y la bitácora en auditorias/auditoria_sesion12.md",
            "explicacion": "Recibes un registro de símbolo con su nombre y su tipo, más el cursor donde terminó la variable anterior; asignar_offset() redondea el cursor, escribe el offset en el registro y devuelve dónde empieza el siguiente. ancho_de_tipo() devuelve el tamaño en bytes o -1 si el tipo no existe.",
            "reglas": [
                "Los tipos válidos son char, short, int, float, double y puntero; cualquier otro devuelve -1.",
                "El cursor nunca retrocede y el offset guardado siempre es múltiplo del ancho del tipo.",
                "Un registro NULL, un cursor negativo o un tipo desconocido se rechazan con -1."
            ],
            "api": {
                "header": "api_sesion12.h",
                "decls": [
                    "int ancho_de_tipo(const char *tipo);",
                    "int asignar_offset(Simbolo *simbolo, int cursor);"
                ],
                "tipos": [
                    "typedef struct Simbolo {",
                    "    const char *nombre;",
                    "    const char *tipo;",
                    "    int offset;",
                    "} Simbolo;"
                ]
            },
            "stub": "int ancho_de_tipo(const char *tipo) {\n    (void)tipo; /* TODO: char=1, short=2, int=4, double=8 */\n    return -1;\n}\n\nint asignar_offset(Simbolo *simbolo, int cursor) {\n    (void)simbolo; (void)cursor; /* TODO: alinea el cursor y guarda el offset */\n    return -1;\n}",
            "casos": [
                {"caso": "ancho_de_tipo(\"int\")", "codigo": "int r = ancho_de_tipo(\"int\");", "var": "r", "esperado": 4, "tipo": "int"},
                {"caso": "ancho_de_tipo(\"double\")", "codigo": "int r = ancho_de_tipo(\"double\");", "var": "r", "esperado": 8, "tipo": "int"},
                {"caso": "int en cursor 0", "codigo": "Simbolo s = {\"x\", \"int\", -1};\nint r = asignar_offset(&s, 0);", "var": "r", "esperado": 4, "tipo": "int"},
                {"caso": "char e int: offset de b", "codigo": "Simbolo a = {\"a\", \"char\", -1};\nSimbolo b = {\"b\", \"int\", -1};\nint cursor = asignar_offset(&a, 0);\nasignar_offset(&b, cursor);\nint r = b.offset;", "var": "r", "esperado": 4, "tipo": "int"},
                {"caso": "double desde cursor 4", "codigo": "Simbolo d = {\"d\", \"double\", -1};\nasignar_offset(&d, 4);\nint r = d.offset;", "var": "r", "esperado": 8, "tipo": "int"},
                {"caso": "registro NULL", "codigo": "int r = asignar_offset(NULL, 0);", "var": "r", "esperado": -1, "tipo": "int"}
            ],
            "criterios": [
                "ancho_de_tipo() respeta la tabla char=1, short=2, int=4, float=4, double=8, puntero=8.",
                "asignar_offset() guarda en el registro el offset ya alineado y devuelve el cursor del siguiente.",
                "El registro NULL devuelve -1 y no escribe memoria inválida."
            ]
        }
    },
    13: {
        "tema": "Manejo de Ámbitos (Scope Global vs Local)",
        "unidad": "Unidad 2: Tabla de Símbolos y Ámbitos",
        "teoria_principal": {
            "titulo": "Visibilidad de Identificadores y Ámbitos Anidados",
            "lead": "El alcance léxico determina en qué regiones del código fuente un identificador es accesible.",
            "tarjetas": [
                ("01. Ámbito Léxico Estático", "La visibilidad se resuelve en tiempo de compilación según la estructura de bloques del código.", "Un bloque hijo puede leer identificadores de bloques padre, pero no al revés."),
                ("02. Ocultamiento de Variables (Shadowing)", "Una variable local puede declarar el mismo nombre que una variable de un ámbito exterior.", "La búsqueda de símbolos debe priorizar la declaración más interna y cercana."),
                ("03. Pila de Tablas de Símbolos", "Cada ámbito nuevo (`{ ... }`) crea su propia tabla de símbolos enlazada a la tabla de su ámbito padre.", "Forma un árbol de ámbitos con la tabla global en la raíz.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Estructura Enlazada de Scopes (Scope Stack)",
            "descripcion": "Cadena estática de resolución de identificadores:",
            "tarjetas": [
                ("Puntero Padre (Enlace Estático)", "Cada `Scope` contiene su propia tabla hash y un puntero `struct Scope *padre`.", "La búsqueda (`lookup`) revisa el scope actual; si no lo halla, sube recursivamente por `padre`."),
                ("Ciclo de Vida de Scope", "Al entrar a `{`, se ejecuta `push_scope()`; al salir en `}`, se ejecuta `pop_scope()`.", "Garantiza que las variables locales dejen de ser visibles al terminar su bloque.")
            ]
        },
        "casos_borde": {
            "titulo": "Antipatrones en Gestión de Ámbitos",
            "items": [
                "Búsqueda invertida: Buscar en ámbitos hijos en lugar de subir hacia el ámbito global.",
                "Destruir la tabla local en `pop_scope()` si las fases posteriores de backend aún requieren consultar offsets de variables locales.",
                "Confundir shadowing con redeclaración ilegal en el mismo ámbito."
            ]
        },
        "contexto": {
            "pregunta": "¿Cómo sabe el compilador cuál variable \"x\" estás usando si hay varias con ese nombre?",
            "objetivo": "Construir una pila de ámbitos enlazados y buscar un identificador desde el bloque actual hacia la raíz, respetando el ocultamiento.",
            "por_que": "Un programa real tiene nombres repetidos en funciones y bloques distintos, y cada uno puede tener tipo y offset diferentes. Si la búsqueda no prioriza el ámbito más cercano, el compilador asigna la variable equivocada y el binario hace algo que el programador nunca escribió. La búsqueda jerárquica es la operación que conecta la sintaxis de llaves con la semántica de visibilidad.",
            "conceptos": [
                ("Ámbito", "Región del programa donde un nombre declarado es visible.", "Como el reglamento de un edificio: cada piso tiene sus reglas y las de arriba siguen aplicando hasta que una regla local diga otra cosa."),
                ("Ocultamiento", "Declarar un nombre en un ámbito interno tapa la versión del ámbito externo sin borrarla.", "Como poner una calcomanía nueva sobre una etiqueta vieja: la de abajo sigue ahí, pero ya no se ve ni se usa."),
                ("Pila de ámbitos", "Cadena de bloques donde cada uno apunta al que lo contiene.", "Como una muñeca rusa: al abrir el bloque actual encuentras el siguiente y así hasta el más grande."),
                ("Búsqueda jerárquica", "Recorrido que empieza en el ámbito actual y sube hasta el global hasta encontrar el nombre.", "Como buscar una herramienta: primero en tu cajón, luego en el taller y al final en el almacén.")
            ],
            "resultado": "Una pila de ámbitos enlazada que declara nombres y los busca desde el bloque actual hasta la raíz, con el harness en verde."
        },
        "lab": {
            "reto": "Pila de ámbitos y búsqueda jerárquica",
            "entregable": "tus funciones declarar() y buscar() en artesano_sesion13_c.c, la salida del harness y la bitácora en auditorias/auditoria_sesion13.md",
            "explicacion": "Recibes ámbitos enlazados ya inicializados y una lista de nombres; declarar() los guarda solo en el ámbito actual y buscar() devuelve el nombre del ámbito donde se encontró, empezando por el actual. Si el nombre no existe devuelve NULL.",
            "reglas": [
                "declarar() no consulta los ámbitos padre: el mismo nombre puede existir una vez en cada nivel.",
                "declarar() devuelve 1 si insertó, 0 si el nombre ya estaba en ese ámbito y -1 si el ámbito está lleno o recibe NULL o un nombre vacío.",
                "buscar() devuelve el nombre del ámbito más cercano, no el símbolo encontrado."
            ],
            "api": {
                "header": "api_sesion13.h",
                "decls": [
                    "int declarar(Ambito *ambito, const char *nombre);",
                    "const char *buscar(const Ambito *ambito, const char *nombre);"
                ],
                "tipos": [
                    "#define AMBITO_MAX 8",
                    "typedef struct Ambito {",
                    "    const char *nombre;",
                    "    const char *nombres[AMBITO_MAX];",
                    "    int total;",
                    "    struct Ambito *padre;",
                    "} Ambito;"
                ]
            },
            "stub": "int declarar(Ambito *ambito, const char *nombre) {\n    (void)ambito; (void)nombre; /* TODO: guarda el nombre si no esta en este ambito */\n    return -1;\n}\n\nconst char *buscar(const Ambito *ambito, const char *nombre) {\n    (void)ambito; (void)nombre; /* TODO: sube por padre hasta encontrar el nombre */\n    return NULL;\n}",
            "casos": [
                {"caso": "declarar(&g, \"x\")", "codigo": "Ambito g;\nmemset(&g, 0, sizeof g);\ng.nombre = \"global\";\nint r = declarar(&g, \"x\");", "var": "r", "esperado": 1, "tipo": "int"},
                {"caso": "buscar en el mismo ambito", "codigo": "Ambito g;\nmemset(&g, 0, sizeof g);\ng.nombre = \"global\";\ndeclarar(&g, \"x\");\nconst char *r = buscar(&g, \"x\");", "var": "r", "esperado": "global", "tipo": "str"},
                {"caso": "buscar subiendo al padre", "codigo": "Ambito g;\nmemset(&g, 0, sizeof g);\ng.nombre = \"global\";\ndeclarar(&g, \"x\");\nAmbito l;\nmemset(&l, 0, sizeof l);\nl.nombre = \"bloque\";\nl.padre = &g;\nconst char *r = buscar(&l, \"x\");", "var": "r", "esperado": "global", "tipo": "str"},
                {"caso": "shadowing en el hijo", "codigo": "Ambito g;\nmemset(&g, 0, sizeof g);\ng.nombre = \"global\";\ndeclarar(&g, \"x\");\nAmbito l;\nmemset(&l, 0, sizeof l);\nl.nombre = \"bloque\";\nl.padre = &g;\ndeclarar(&l, \"x\");\nconst char *r = buscar(&l, \"x\");", "var": "r", "esperado": "bloque", "tipo": "str"},
                {"caso": "tres niveles hasta la raiz", "codigo": "Ambito raiz;\nmemset(&raiz, 0, sizeof raiz);\nraiz.nombre = \"raiz\";\nAmbito medio;\nmemset(&medio, 0, sizeof medio);\nmedio.nombre = \"medio\";\nmedio.padre = &raiz;\nAmbito hoja;\nmemset(&hoja, 0, sizeof hoja);\nhoja.nombre = \"hoja\";\nhoja.padre = &medio;\ndeclarar(&raiz, \"x\");\nconst char *r = buscar(&hoja, \"x\");", "var": "r", "esperado": "raiz", "tipo": "str"},
                {"caso": "nombre no declarado", "codigo": "Ambito g;\nmemset(&g, 0, sizeof g);\ng.nombre = \"global\";\nconst char *p = buscar(&g, \"z\");\nconst char *r = p ? p : \"(nulo)\";", "var": "r", "esperado": "(nulo)", "tipo": "str"}
            ],
            "criterios": [
                "Cada nombre queda registrado solo en el ámbito donde se declara.",
                "buscar() devuelve el ámbito más interno que declara el nombre y sube hasta la raíz cuando hace falta.",
                "Un nombre inexistente devuelve NULL sin modificar los ámbitos."
            ]
        }
    },
    14: {
        "tema": "Declaración vs Uso de Variables",
        "unidad": "Unidad 2: Tabla de Símbolos y Ámbitos",
        "teoria_principal": {
            "titulo": "Invariante de Definición Previa y Control de Redeclaración",
            "lead": "Todo identificador utilizado en una expresión debe haber sido declarado previamente en un ámbito accesible.",
            "tarjetas": [
                ("01. Invariante: Use-Before-Declaration", "El compilador rechaza cualquier lectura o escritura de un símbolo inexistente en la jerarquía de scopes.", "Emite un error fatal: `error: 'x' no ha sido declarada en este ámbito`."),
                ("02. Detección de Redeclaración Ilegal", "Declarar dos variables con el mismo nombre en el *mismo* ámbito exacto es un error semántico.", "La inserción debe verificar primero si el símbolo ya existe exclusivamente en el scope actual."),
                ("03. Estado de Inicialización", "Rastreo de variables utilizadas antes de haber recibido un valor inicial.", "Permite emitir advertencias (*warnings*) de lectura de memoria no inicializada.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Diferenciación entre Inserción y Búsqueda",
            "descripcion": "Dos operaciones fundamentales con semántica distinta:",
            "tarjetas": [
                ("Insertar Símbolo (Scope Actual)", "`insertar(nombre, tipo)` solo consulta el scope actual. Si ya existe, falla con error de redeclaración.", "Si no existe, reserva memoria y lo agrega a la tabla local."),
                ("Resolver Símbolo (Búsqueda Jerárquica)", "`buscar(nombre)` itera desde el scope actual hasta el global.", "Retorna el puntero al `SymbolEntry` más cercano o `NULL` si la variable no existe.")
            ]
        },
        "casos_borde": {
            "titulo": "Puntos de Falla en Declaraciones",
            "items": [
                "Permitir que una variable se declare dos veces en la misma función con tipos contradictorios.",
                "Omitir el error cuando una variable se usa dentro de su propia declaración inicial (`int x = x + 1;`).",
                "Falsos positivos de no-declaración al buscar variables globales desde funciones profundas."
            ]
        },
        "contexto": {
            "pregunta": "¿Cómo detecta el compilador que usaste una variable que nunca declaraste?",
            "objetivo": "Implementar las dos operaciones que sostienen la regla de declaración previa: insertar en el ámbito actual y resolver un nombre declarado, distinguiendo uso válido, uso no declarado y redeclaración.",
            "por_que": "La tabla de símbolos solo sirve si distingue entre \"este nombre ya vive aquí\" y \"este nombre existe en algún lado\". Un compilador que acepta variables fantasma produce código que enlaza contra basura; uno que confunde redeclaración con ocultamiento rechaza programas correctos. Separar inserción y búsqueda es lo que convierte la tabla en un verificador semántico real.",
            "conceptos": [
                ("Declaración", "Aviso que registra un nombre nuevo con su tipo en el ámbito actual.", "Como inscribir a alguien en la lista de asistencia: a partir de ahí existe para el grupo."),
                ("Uso", "Referencia a un nombre que ya debía estar registrado.", "Como usar la credencial de un compañero: si no está en la lista, no puedes pasar."),
                ("Redeclaración", "Segundo registro del mismo nombre en el mismo ámbito.", "Como darle dos veces la misma habitación a una persona: la segunda vez hay que rechazarla."),
                ("Regla de declaración previa", "Todo nombre se registra antes de poder leerse o asignarse.", "Como abrir la llave del agua antes de llenar el vaso: si la llave no existe, no sale nada.")
            ],
            "resultado": "Una tabla de símbolos mínima que acepta declaraciones nuevas, rechaza repetidos y responde si un nombre puede usarse."
        },
        "lab": {
            "reto": "Declaración previa y redeclaración",
            "entregable": "tus funciones declarar() y usar() en artesano_sesion14_c.c, la salida del harness y la bitácora en auditorias/auditoria_sesion14.md",
            "explicacion": "Recibes una tabla vacía y una secuencia de operaciones; declarar() añade un nombre solo si no existe en ese mismo ámbito y usar() responde si ya fue declarado. La diferencia entre \"no existe\" y \"existe al lado\" es lo que mide el harness.",
            "reglas": [
                "declarar() devuelve 1 si insertó, 0 si el nombre ya estaba y -1 si recibe NULL o un nombre vacío.",
                "usar() devuelve 1 solo si el nombre ya fue declarado; en cualquier otro caso devuelve 0.",
                "La comparación es exacta: \"x\" y \"xy\" son nombres distintos."
            ],
            "api": {
                "header": "api_sesion14.h",
                "decls": [
                    "int declarar(Tabla *tabla, const char *nombre);",
                    "int usar(const Tabla *tabla, const char *nombre);"
                ],
                "tipos": [
                    "#define TABLA_MAX 16",
                    "typedef struct Tabla {",
                    "    const char *nombres[TABLA_MAX];",
                    "    int total;",
                    "} Tabla;"
                ]
            },
            "stub": "int declarar(Tabla *tabla, const char *nombre) {\n    (void)tabla; (void)nombre; /* TODO: rechaza el nombre si ya esta en esta tabla */\n    return -1;\n}\n\nint usar(const Tabla *tabla, const char *nombre) {\n    (void)tabla; (void)nombre; /* TODO: responde si el nombre ya fue declarado */\n    return 0;\n}",
            "casos": [
                {"caso": "usar sin declarar", "codigo": "Tabla t;\nmemset(&t, 0, sizeof t);\nint r = usar(&t, \"x\");", "var": "r", "esperado": 0, "tipo": "int"},
                {"caso": "usar despues de declarar", "codigo": "Tabla t;\nmemset(&t, 0, sizeof t);\ndeclarar(&t, \"x\");\nint r = usar(&t, \"x\");", "var": "r", "esperado": 1, "tipo": "int"},
                {"caso": "redeclarar el mismo nombre", "codigo": "Tabla t;\nmemset(&t, 0, sizeof t);\ndeclarar(&t, \"x\");\nint r = declarar(&t, \"x\");", "var": "r", "esperado": 0, "tipo": "int"},
                {"caso": "total tras redeclarar", "codigo": "Tabla t;\nmemset(&t, 0, sizeof t);\ndeclarar(&t, \"x\");\ndeclarar(&t, \"x\");\nint r = t.total;", "var": "r", "esperado": 1, "tipo": "int"},
                {"caso": "prefijo no es el mismo nombre", "codigo": "Tabla t;\nmemset(&t, 0, sizeof t);\ndeclarar(&t, \"x\");\nint r = usar(&t, \"xy\");", "var": "r", "esperado": 0, "tipo": "int"},
                {"caso": "declarar nombre vacio", "codigo": "Tabla t;\nmemset(&t, 0, sizeof t);\nint r = declarar(&t, \"\");", "var": "r", "esperado": -1, "tipo": "int"}
            ],
            "criterios": [
                "usar() distingue un nombre declarado de uno inexistente sin depender de comparaciones parciales.",
                "declarar() rechaza el duplicado y deja el total de símbolos intacto.",
                "El caso de nombre vacío devuelve -1 sin insertar nada."
            ]
        }
    },
    15: {
        "tema": "Bloques Anidados y Ciclo de Vida de Identificadores",
        "unidad": "Unidad 2: Tabla de Símbolos y Ámbitos",
        "teoria_principal": {
            "titulo": "Gestión Temporal de Bloques y Reutilización de Pila",
            "lead": "Los bloques `{ ... }` crean contextos temporales. Variables en bloques paralelos pueden compartir el mismo espacio de pila.",
            "tarjetas": [
                ("01. Bloques Paralelos", "Dos bloques `{ int a; }` y `{ int b; }` dentro de la misma función nunca están activos al mismo tiempo.", "Un compilador optimizador puede asignar a `a` y a `b` el mismo offset de memoria en el Stack."),
                ("02. Profundidad de Ámbito (Scope Depth)", "Un contador entero que se incrementa en cada nivel de anidamiento.", "Permite determinar rápidamente el nivel de acceso y el ciclo de vida de cada variable."),
                ("03. Preservación para Backend", "Aunque un scope se cierre, la información de sus símbolos debe conservarse en un árbol de scopes para el generador de código.", "Solo se desapila el puntero de búsqueda activa, no se destruyen los metadatos.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Árbol Completo de Scopes (Scope Tree)",
            "descripcion": "Estructura persistente para todo el análisis:",
            "tarjetas": [
                ("Estructura de Árbol", "El scope raíz apunta a sus hijos mediante una lista de sub-scopes: `Scope *primer_hijo, *sig_hermano`.", "Permite al backend recorrer todas las variables de todos los bloques al dimensionar el stack frame."),
                ("Puntero Scope Actual (Cursor)", "Una variable global `Scope *scope_actual` que sube y baja por el árbol de scopes durante el parsing.", "Garantiza contexto correcto en cada nodo procesado.")
            ]
        },
        "casos_borde": {
            "titulo": "Antipatrones en Bloques Anidados",
            "items": [
                "Acceder a variables locales de un bloque `{ ... }` después de haber cerrado la llave `}`.",
                "Fuga de memoria por no enlazar los scopes hijos al árbol general antes de hacer pop del cursor.",
                "Calcular mal el tamaño total de la función al sumar bloques paralelos en lugar de superponerlos."
            ]
        },
        "contexto": {
            "pregunta": "¿Qué pasa con las variables de un bloque cuando el programa cierra la llave y sale de él?",
            "objetivo": "Implementar push y pop de ámbitos enlazados, comprobando que al cerrar un bloque el cursor vuelve al padre y las variables del bloque dejan de ser visibles.",
            "por_que": "Los bloques no son decoración: delimitan el tiempo de vida de los nombres. Si el compilador no retrocede el cursor al encontrar la llave de cierre, sigue viendo variables que ya no existen y acepta código inválido. Al mismo tiempo, los datos del bloque hay que conservarlos para el backend, así que pop no puede limitarse a borrar la memoria: debe devolver el control al ámbito padre.",
            "conceptos": [
                ("Entrar a un bloque", "Crear un ámbito nuevo cuyo padre es el bloque activo.", "Como abrir una puerta hacia un cuarto interior: sigues dentro de la casa, pero ahora manda la luz de ese cuarto."),
                ("Salir de un bloque", "Cerrar el ámbito actual y volver al padre.", "Como salir del cuarto interior y cerrar la puerta: lo que estaba adentro deja de estar a la vista."),
                ("Ciclo de vida", "Periodo durante el cual una variable existe y puede usarse.", "Como la vigencia de un pase de estacionamiento: sirve mientras estés dentro y deja de servir al salir."),
                ("Cursor de ámbito", "Puntero que indica cuál es el bloque activo en cada momento.", "Como el cursor de un documento: marca el lugar donde estás trabajando ahora mismo.")
            ],
            "resultado": "Dos operaciones push y pop que construyen y deshacen la cadena de ámbitos sin perder el padre."
        },
        "lab": {
            "reto": "Push y pop de ámbitos",
            "entregable": "tus funciones push_ambito() y pop_ambito() en artesano_sesion15_c.c, la salida del harness y la bitácora en auditorias/auditoria_sesion15.md",
            "explicacion": "Recibes el ámbito activo y un nombre; push_ambito() reserva un ámbito nuevo enlazado al actual y pop_ambito() libera el actual y devuelve el padre. El harness revisa nombres, profundidad y que pop sobre la raíz no destruya el programa.",
            "reglas": [
                "push_ambito() devuelve NULL si el ámbito actual o el nombre son NULL.",
                "pop_ambito() devuelve NULL sobre la raíz y no libera memoria que no le pertenece.",
                "Cada push se empareja con un pop: no se dejan ámbitos colgando en la cadena."
            ],
            "api": {
                "header": "api_sesion15.h",
                "decls": [
                    "Ambito *push_ambito(Ambito *actual, const char *nombre);",
                    "Ambito *pop_ambito(Ambito *actual);"
                ],
                "tipos": [
                    "typedef struct Ambito {",
                    "    const char *nombre;",
                    "    struct Ambito *padre;",
                    "} Ambito;"
                ]
            },
            "stub": "Ambito *push_ambito(Ambito *actual, const char *nombre) {\n    (void)actual; (void)nombre; /* TODO: reserva un ambito y enlazalo al padre */\n    return NULL;\n}\n\nAmbito *pop_ambito(Ambito *actual) {\n    (void)actual; /* TODO: libera el actual y devuelve el padre */\n    return NULL;\n}",
            "casos": [
                {"caso": "nombre del ambito nuevo", "codigo": "Ambito raiz = {\"global\", NULL};\nAmbito *a = push_ambito(&raiz, \"if\");\nconst char *r = a ? a->nombre : \"(nulo)\";\npop_ambito(a);", "var": "r", "esperado": "if", "tipo": "str"},
                {"caso": "profundidad con dos push", "codigo": "Ambito raiz = {\"global\", NULL};\nAmbito *a = push_ambito(&raiz, \"if\");\nAmbito *b = push_ambito(a, \"while\");\nint r = 0;\nfor (Ambito *p = b; p != NULL; p = p->padre) r++;\npop_ambito(b);\npop_ambito(a);", "var": "r", "esperado": 3, "tipo": "int"},
                {"caso": "pop devuelve el padre", "codigo": "Ambito raiz = {\"global\", NULL};\nAmbito *a = push_ambito(&raiz, \"if\");\nint r = (pop_ambito(a) == &raiz);", "var": "r", "esperado": 1, "tipo": "int"},
                {"caso": "pop sobre la raiz", "codigo": "Ambito raiz = {\"global\", NULL};\nint r = (pop_ambito(&raiz) == NULL);", "var": "r", "esperado": 1, "tipo": "int"},
                {"caso": "push con padre NULL", "codigo": "int r = (push_ambito(NULL, \"x\") == NULL);", "var": "r", "esperado": 1, "tipo": "int"},
                {"caso": "profundidad tras pop", "codigo": "Ambito raiz = {\"global\", NULL};\nAmbito *a = push_ambito(&raiz, \"if\");\nAmbito *b = push_ambito(a, \"while\");\nAmbito *c = pop_ambito(b);\nint r = 0;\nfor (Ambito *p = c; p != NULL; p = p->padre) r++;\npop_ambito(c);", "var": "r", "esperado": 2, "tipo": "int"}
            ],
            "criterios": [
                "push_ambito() enlaza el nuevo ámbito con el padre y conserva el nombre recibido.",
                "pop_ambito() devuelve exactamente el padre y libera solo el ámbito que recibe.",
                "La profundidad de la cadena sube con cada push y baja con cada pop."
            ]
        }
    },
    16: {
        "tema": "Firmas de Función y Parámetros Formales",
        "unidad": "Unidad 2: Tabla de Símbolos y Ámbitos",
        "teoria_principal": {
            "titulo": "Contrato de Invocación, Aridad y Tipado de Argumentos",
            "lead": "Las funciones son símbolos especiales que transportan una lista ordenada de tipos de entrada y un tipo de retorno.",
            "tarjetas": [
                ("01. Aridad (Número de Parámetros)", "La cantidad exacta de argumentos que la función espera recibir en la llamada.", "Llamar a una función con menos o más argumentos de los definidos es un error semántico."),
                ("02. Parámetros Formales como Variables Locales", "Cada parámetro formal se inserta en la tabla de símbolos del cuerpo de la función como una variable local predefinida.", "Tienen offsets específicos asignados según la convención de llamadas de la arquitectura."),
                ("03. Prototipos vs Definición", "Declaración adelantada (*forward declaration*) de la firma antes de la implementación del cuerpo.", "Permite llamadas recursivas y dependencias mutuas entre funciones.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Modelado de Firmas de Función en C",
            "descripcion": "Estructura enlazada de tipos de parámetros:",
            "tarjetas": [
                ("Estructura FunctionSignature", "Contiene `Type *tipo_retorno`, `int num_params` y una lista de `ParamEntry *params`.", "Cada `ParamEntry` tiene el nombre del parámetro y su tipo formal verificado."),
                ("Mapeo a Registros de Argumentos", "En x86-64 System V, los primeros 6 parámetros se pasan en registros: RDI, RSI, RDX, RCX, R8, R9.", "Los parámetros 7 en adelante se apilan en memoria antes del `call`.")
            ]
        },
        "casos_borde": {
            "titulo": "Errores Semánticos en Funciones",
            "items": [
                "Discrepancia de aridad: Invocar una función `suma(int a, int b)` pasando un solo argumento.",
                "Incompatibilidad de tipos en argumentos: Pasar un puntero donde se requiere un entero.",
                "Redefinir una función con una firma incompatible con su prototipo previo."
            ]
        },
        "contexto": {
            "pregunta": "¿Cómo comprueba el compilador que llamaste a una función con los argumentos correctos?",
            "objetivo": "Registrar firmas con nombre y aridad, y verificar cada llamada contra ese registro devolviendo el diagnóstico adecuado.",
            "por_que": "Una llamada con menos argumentos de los declarados produce un desajuste silencioso en la pila que en C se convierte en comportamiento indefinido. El analizador semántico no ejecuta la función: compara la lista de argumentos con el prototipo guardado y detiene el programa antes de generar código. Esta verificación depende de que la firma se haya registrado correctamente en la tabla de símbolos.",
            "conceptos": [
                ("Firma", "Nombre de la función más la cantidad y el tipo de sus parámetros.", "Como la ficha técnica de un electrodoméstico: dice cuántas entradas necesita y de qué tipo antes de encenderlo."),
                ("Aridad", "Número exacto de argumentos que una función espera.", "Como los asientos de un coche: si viajan más o menos de los que hay, algo se rompe."),
                ("Prototipo", "Declaración adelantada de la firma antes del cuerpo.", "Como el menú de un restaurante: te dice qué hay antes de que entres a la cocina."),
                ("Argumento", "Valor concreto que se pasa en una llamada.", "Como los ingredientes que entregas en la ventanilla: deben ser los que pide la receta.")
            ],
            "resultado": "Un verificador de firmas que distingue llamada válida, aridad incorrecta y función inexistente."
        },
        "lab": {
            "reto": "Registro de prototipos y aridad",
            "entregable": "tu función verificar_llamada() en artesano_sesion16_c.c, la salida del harness y la bitácora en auditorias/auditoria_sesion16.md",
            "explicacion": "Recibes un catálogo de firmas ya registradas y una llamada descrita por nombre y número de argumentos; busca el nombre y compara la aridad. La función devuelve 1 si la llamada es válida, 0 si la aridad no coincide y -1 si el nombre no existe.",
            "reglas": [
                "La búsqueda del nombre es exacta y recorre el catálogo completo.",
                "Una función registrada con cero parámetros solo acepta cero argumentos.",
                "Un catálogo NULL, un nombre NULL o una aridad negativa devuelven -1."
            ],
            "api": {
                "header": "api_sesion16.h",
                "decls": [
                    "int verificar_llamada(const Funcion *catalogo, int total, const char *nombre, int nargs);"
                ],
                "tipos": [
                    "typedef struct Funcion {",
                    "    const char *nombre;",
                    "    int aridad;",
                    "} Funcion;"
                ]
            },
            "stub": "int verificar_llamada(const Funcion *catalogo, int total, const char *nombre, int nargs) {\n    (void)catalogo; (void)total; (void)nombre; (void)nargs; /* TODO: busca la firma y compara la aridad */\n    return -1;\n}",
            "casos": [
                {"caso": "suma con 3 argumentos", "codigo": "Funcion c[] = {{\"suma\", 3}};\nint r = verificar_llamada(c, 1, \"suma\", 3);", "var": "r", "esperado": 1, "tipo": "int"},
                {"caso": "suma con 2 argumentos", "codigo": "Funcion c[] = {{\"suma\", 3}};\nint r = verificar_llamada(c, 1, \"suma\", 2);", "var": "r", "esperado": 0, "tipo": "int"},
                {"caso": "suma con 4 argumentos", "codigo": "Funcion c[] = {{\"suma\", 3}};\nint r = verificar_llamada(c, 1, \"suma\", 4);", "var": "r", "esperado": 0, "tipo": "int"},
                {"caso": "funcion no registrada", "codigo": "Funcion c[] = {{\"suma\", 3}};\nint r = verificar_llamada(c, 1, \"resta\", 2);", "var": "r", "esperado": -1, "tipo": "int"},
                {"caso": "main sin argumentos", "codigo": "Funcion c[] = {{\"main\", 0}};\nint r = verificar_llamada(c, 1, \"main\", 0);", "var": "r", "esperado": 1, "tipo": "int"},
                {"caso": "nombre NULL", "codigo": "Funcion c[] = {{\"suma\", 3}};\nint r = verificar_llamada(c, 1, NULL, 3);", "var": "r", "esperado": -1, "tipo": "int"}
            ],
            "criterios": [
                "La aridad declarada se compara con la aridad de la llamada, no con el número de firmas del catálogo.",
                "Una función con cero parámetros se acepta únicamente con cero argumentos.",
                "Un nombre inexistente devuelve -1 sin confundirse con una aridad incorrecta."
            ]
        }
    },
    17: {
        "tema": "Comprobación Semántica de Retornos y Rutas de Control",
        "unidad": "Unidad 2: Tabla de Símbolos y Ámbitos",
        "teoria_principal": {
            "titulo": "Validación de Sentencias Return y Análisis de Flujo",
            "lead": "Toda función no-void debe garantizar un retorno de valor válido en todas las posibles rutas de ejecución.",
            "tarjetas": [
                ("01. Coincidencia de Tipo de Retorno", "El tipo de la expresión evaluada en `return expr;` debe coincidir o ser convertible al tipo de la función.", "Un `return` con valor dentro de una función `void` es un error semántico."),
                ("02. Análisis de Retorno en Ramas Condicionales", "Si una función tiene `if-else`, ambas ramas deben retornar un valor; omitir el `else` deja una ruta abierta.", "El compilador debe alertar: `control reaches end of non-void function`."),
                ("03. Sentencias Inalcanzables tras Return", "Cualquier código escrito inmediatamente después de un `return` incondicional en el mismo bloque es código muerto.", "El analizador semántico debe emitir advertencias de código inalcanzable.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Ubicación del Valor de Retorno en Hardware",
            "descripcion": "Convención ABI para valores devueltos:",
            "tarjetas": [
                ("Registro RAX / XMM0", "Los enteros y punteros devueltos se cargan en el registro `RAX` (64-bit) o `EAX` (32-bit).", "Los valores de punto flotante (`float`, `double`) se devuelven en el registro vectorial `XMM0`."),
                ("Estructuras Grandes (> 16 bytes)", "Se devuelven mediante un puntero oculto pasado como primer argumento implícito en `RDI`.", "El llamador reserva el espacio en su pila y la función escribe directamente en él.")
            ]
        },
        "casos_borde": {
            "titulo": "Puntos Críticos en Sentencias Return",
            "items": [
                "Retornar la dirección de una variable local de pila (`return &local;`), generando punteros colgantes en el llamador.",
                "Rutas de ejecución abiertas en sentencias `switch` sin cláusula `default` retornable.",
                "Retornar valores vacíos `return;` en funciones con tipo de retorno definido como `int`."
            ]
        },
        "contexto": {
            "pregunta": "¿Cómo sabe el compilador que una función siempre devuelve un valor, incluso cuando toma un camino con if?",
            "objetivo": "Verificar el tipo de cada return y que todas las rutas de una función no-void terminen en un retorno, devolviendo un diagnóstico único.",
            "por_que": "Una función que promete un entero y termina sin devolverlo deja en el registro de retorno un valor impredecible que el llamador usará como si fuera válido. El compilador detecta esa ruta abierta antes de emitir código y también rechaza devolver valores en funciones void. Sin esta comprobación, el análisis semántico deja pasar errores que solo aparecen en producción.",
            "conceptos": [
                ("Ruta de ejecución", "Camino posible desde el inicio de una función hasta su salida.", "Como las rutas de un mapa: llegar al destino por cualquier camino cuenta, pero no puedes quedarte a medio camino."),
                ("Tipo de retorno", "Tipo de valor que la función promete entregar a quien la llama.", "Como la etiqueta de un paquete: dice qué contiene y quien lo recibe confía en esa etiqueta."),
                ("Conversión implícita", "Cambio de tipo que el compilador acepta sin que lo pidas, cuando no pierde información.", "Como verter un vaso pequeño en uno grande: cabe sin derramarse; al revés, se pierde agua."),
                ("Código inalcanzable", "Instrucciones que nunca se ejecutan porque un return ya salió del bloque.", "Como un anuncio después de la salida de la autopista: está escrito, pero nadie pasa por ahí.")
            ],
            "resultado": "Un diagnóstico de retornos que distingue tipo incompatible, ruta sin retorno y función correcta."
        },
        "lab": {
            "reto": "Validación de retornos y rutas",
            "entregable": "tu función diagnosticar_retorno() en artesano_sesion17_c.c, la salida del harness y la bitácora en auditorias/auditoria_sesion17.md",
            "explicacion": "Recibes el tipo que promete la función, el tipo de la expresión devuelta y el conteo de rutas totales y rutas que sí retornan. Debes emitir 0 si todo está bien, 1 si el tipo es incompatible y 2 si queda una ruta sin retorno.",
            "reglas": [
                "La conversión solo se acepta cuando el tipo destino es igual o más ancho que el origen.",
                "Devolver un valor en una función void es siempre un error de tipo.",
                "Una firma NULL o un conteo de rutas incoherente (cero rutas o más retornos que rutas) devuelve -1."
            ],
            "api": {
                "header": "api_sesion17.h",
                "decls": [
                    "int diagnosticar_retorno(const char *tipo_funcion, const char *tipo_expresion, int rutas_totales, int rutas_con_return);"
                ]
            },
            "stub": "int diagnosticar_retorno(const char *tipo_funcion, const char *tipo_expresion, int rutas_totales, int rutas_con_return) {\n    (void)tipo_funcion; (void)tipo_expresion; (void)rutas_totales; (void)rutas_con_return; /* TODO */\n    return -1;\n}",
            "casos": [
                {"caso": "int con int y dos rutas", "codigo": "int r = diagnosticar_retorno(\"int\", \"int\", 2, 2);", "var": "r", "esperado": 0, "tipo": "int"},
                {"caso": "void devuelve valor", "codigo": "int r = diagnosticar_retorno(\"void\", \"int\", 1, 1);", "var": "r", "esperado": 1, "tipo": "int"},
                {"caso": "ruta sin retorno", "codigo": "int r = diagnosticar_retorno(\"int\", \"int\", 2, 1);", "var": "r", "esperado": 2, "tipo": "int"},
                {"caso": "double acepta int", "codigo": "int r = diagnosticar_retorno(\"double\", \"int\", 1, 1);", "var": "r", "esperado": 0, "tipo": "int"},
                {"caso": "int no acepta double", "codigo": "int r = diagnosticar_retorno(\"int\", \"double\", 1, 1);", "var": "r", "esperado": 1, "tipo": "int"},
                {"caso": "cero rutas de ejecucion", "codigo": "int r = diagnosticar_retorno(\"int\", \"int\", 0, 0);", "var": "r", "esperado": -1, "tipo": "int"}
            ],
            "criterios": [
                "El tipo se compara antes que las rutas: un return incompatible nunca se reporta como ruta faltante.",
                "Una función void solo es válida cuando la expresión devuelta también es void.",
                "El conteo de rutas detecta exactamente el caso de un if sin else que deja un camino abierto."
            ]
        }
    },
    18: {
        "tema": "Arreglos y Verificación de Límites Estáticos",
        "unidad": "Unidad 2: Tabla de Símbolos y Ámbitos",
        "teoria_principal": {
            "titulo": "Dimensionamiento de Memoria Contigua e Indexación",
            "lead": "Un arreglo es una secuencia homogénea y contigua de elementos en memoria indexada por desplazamientos escalares.",
            "tarjetas": [
                ("01. Cálculo del Tamaño Total", "El tamaño en bytes de un arreglo unidimensional es: $\\text{Bytes} = N \\times \\text{sizeof}(T)$.", "El compilador reserva este bloque continuo en el Stack o segmento de datos."),
                ("02. Indexación y Tipado de Índices", "La expresión dentro de `A[i]` debe evaluarse obligatoriamente a un tipo entero (`int`, `size_t`).", "El compilador rechaza índices de tipo flotante o punteros."),
                ("03. Verificación de Límites Estáticos", "Si el índice es una constante conocida en compilación (`A[15]` en un arreglo de 10 elementos), emitir error estático.", "Previene accesos fuera de límites (*out-of-bounds*) en tiempo de compilación.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Fórmula de Direccionamiento de Arreglos",
            "descripcion": "Cálculo de la dirección efectiva en tiempo de ejecución:",
            "tarjetas": [
                ("Fórmula 1D", "$\\text{Dir}(A[i]) = \\text{Base}(A) + (i \\times \\text{ancho})$.", "En ensamblador x86-64 se traduce directamente al modo de direccionamiento escalado: `[RBP + RAX*4 - offset]`."),
                ("Fórmula 2D (Row-Major Order)", "$\\text{Dir}(A[i][j]) = \\text{Base}(A) + (i \\times \\text{Columnas} + j) \\times \\text{ancho}$.", "C almacena las matrices por filas consecutivas en memoria lineal.")
            ]
        },
        "casos_borde": {
            "titulo": "Fallas Críticas en Arreglos",
            "items": [
                "Dimensiones no enteras o negativas en la declaración (`int arr[-5];`).",
                "Arreglos de tamaño cero `int arr[0];` en estándares estrictos ANSI C.",
                "Confundir la indexación `arr[i]` con la desreferenciación de punteros no inicializados."
            ]
        },
        "contexto": {
            "pregunta": "¿Cómo calcula el compilador cuánta memoria reservar para un arreglo y hasta dónde puede leer?",
            "objetivo": "Calcular el tamaño total de un arreglo a partir de su tipo y su número de elementos, y validar índices contra esos límites.",
            "por_que": "El arreglo es la primera estructura de memoria contigua que el compilador debe dimensionar y la fuente clásica de accesos fuera de rango. Calcular mal el tamaño reserva de menos y corrompe variables vecinas; validar mal el índice acepta el elemento número N, que ya está fuera del bloque. El análisis semántico hace estas dos cuentas antes de que exista una sola instrucción.",
            "conceptos": [
                ("Arreglo", "Secuencia de elementos del mismo tipo guardados uno tras otro.", "Como una fila de casilleros idénticos: todos del mismo tamaño y pegados, uno al lado del otro."),
                ("Tamaño total", "Bytes que ocupa el arreglo completo: elementos por ancho del tipo.", "Como calcular cuántas cajas necesitas multiplicando el número de artículos por el tamaño de cada caja."),
                ("Índice", "Posición del elemento que quieres leer, contada desde cero.", "Como el número de piso de un edificio: si tiene diez pisos numerados desde cero, el piso diez ya no existe."),
                ("Fuera de rango", "Índice menor que cero o mayor o igual al número de elementos.", "Como buscar el asiento 41 en un avión de 40 filas: el boleto parece válido, pero no hay tal asiento.")
            ],
            "resultado": "Dos funciones que dimensionan arreglos y rechazan índices fuera de rango, con pruebas en verde."
        },
        "lab": {
            "reto": "Tamaño de arreglo y límites",
            "entregable": "tus funciones bytes_arreglo() e indice_en_rango() en artesano_sesion18_c.c, la salida del harness y la bitácora en auditorias/auditoria_sesion18.md",
            "explicacion": "Recibes el nombre de un tipo y el número de elementos; bytes_arreglo() devuelve el total de bytes e indice_en_rango() devuelve 1 si el índice puede leerse o 0 si no. El harness prueba tipos de distinto ancho y los bordes exactos del rango.",
            "reglas": [
                "Tipos válidos: char, short, int, float, double y puntero; otro nombre devuelve -1.",
                "Un número negativo de elementos es inválido y devuelve -1; cero elementos pesa cero bytes.",
                "El índice válido más alto es elementos - 1, nunca elementos."
            ],
            "api": {
                "header": "api_sesion18.h",
                "decls": [
                    "long bytes_arreglo(const char *tipo, int elementos);",
                    "int indice_en_rango(int indice, int elementos);"
                ]
            },
            "stub": "long bytes_arreglo(const char *tipo, int elementos) {\n    (void)tipo; (void)elementos; /* TODO: elementos por ancho del tipo */\n    return -1;\n}\n\nint indice_en_rango(int indice, int elementos) {\n    (void)indice; (void)elementos; /* TODO: 0 <= indice < elementos */\n    return 0;\n}",
            "casos": [
                {"caso": "int[10]", "codigo": "long r = bytes_arreglo(\"int\", 10);", "var": "r", "esperado": 40, "tipo": "int"},
                {"caso": "double[3]", "codigo": "long r = bytes_arreglo(\"double\", 3);", "var": "r", "esperado": 24, "tipo": "int"},
                {"caso": "int[-4]", "codigo": "long r = bytes_arreglo(\"int\", -4);", "var": "r", "esperado": -1, "tipo": "int"},
                {"caso": "indice 0 de 5", "codigo": "int r = indice_en_rango(0, 5);", "var": "r", "esperado": 1, "tipo": "int"},
                {"caso": "indice 5 de 5", "codigo": "int r = indice_en_rango(5, 5);", "var": "r", "esperado": 0, "tipo": "int"},
                {"caso": "indice negativo", "codigo": "int r = indice_en_rango(-1, 5);", "var": "r", "esperado": 0, "tipo": "int"}
            ],
            "criterios": [
                "bytes_arreglo() multiplica elementos por el ancho correcto y rechaza dimensiones negativas.",
                "indice_en_rango() acepta el primer elemento y rechaza el índice igual al número de elementos.",
                "Los índices negativos se rechazan sin desbordar la comparación."
            ]
        }
    },
    19: {
        "tema": "Estructuras (struct) y Offsets de Miembros",
        "unidad": "Unidad 2: Tabla de Símbolos y Ámbitos",
        "teoria_principal": {
            "titulo": "Tipos Compuestos Heterogéneos y Sub-Tablas de Símbolos",
            "lead": "Las estructuras agrupan campos de distintos tipos. Cada `struct` posee su propia tabla de símbolos interna para sus miembros.",
            "tarjetas": [
                ("01. Tabla de Miembros (Member Table)", "Cada definición de estructura contiene una sub-tabla de símbolos con el nombre y offset de cada campo.", "Al evaluar `p.edad`, el compilador consulta la tabla de miembros del tipo de `p`."),
                ("02. Operador de Acceso a Miembro (`.` y `->`)", "El operador `.` accede sobre variables directas; el operador `->` desreferencia primero un puntero a estructura.", "Requiere validar que el operando izquierdo sea efectivamente de tipo `struct`."),
                ("03. Tamaño y Padding Total de Estructura", "El tamaño total de una estructura debe ser múltiplo de la alineación de su miembro más grande.", "Garantiza que en arreglos de estructuras todos los elementos queden correctamente alineados.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Alineación y Disposición de Campos en Memoria",
            "descripcion": "Cálculo paso a paso de offsets y padding interno:",
            "tarjetas": [
                ("Ejemplo de Disposición", "`struct { char a; int b; short c; };` -> `a` en offset 0, 3 bytes padding, `b` en offset 4, `c` en offset 8, 2 bytes padding final. Total: 12 bytes.", "El orden de declaración afecta directamente la memoria consumida."),
                ("Dirección Efectiva del Miembro", "$\\text{Dir}(p.campo) = \\text{Base}(p) + \\text{Offset}(campo)$.", "El compilador emite instrucciones con desplazamiento constante.")
            ]
        },
        "casos_borde": {
            "titulo": "Antipatrones en Estructuras",
            "items": [
                "Acceso a campos inexistentes (`p.telefono` cuando el campo no fue definido en el struct).",
                "Uso del operador `.` sobre un puntero en lugar de `->` o viceversa.",
                "Estructuras autorreferenciadas sin puntero (`struct Nodo { struct Nodo sig; };`) que generan tipos de tamaño infinito."
            ]
        },
        "contexto": {
            "pregunta": "¿Dónde queda cada campo de una estructura dentro de su bloque de memoria?",
            "objetivo": "Calcular los offsets de los miembros de una estructura aplicando alineación y padding, y obtener el tamaño total del tipo.",
            "por_que": "Un struct no se guarda campo tras campo sin más: entre un char y un int hay huecos que la CPU exige para leer alineado. El compilador calcula esos offsets una sola vez y los guarda en la tabla de miembros; el backend los usa como desplazamientos constantes. Si calcularas el offset sumando tamaños, el acceso al segundo campo leería bytes del relleno y el programa trabajaría con basura.",
            "conceptos": [
                ("Estructura", "Tipo compuesto que agrupa campos de distinto tipo en un solo bloque.", "Como una ficha de registro con casillas de distintos tamaños: nombre, edad y dirección viven en la misma hoja."),
                ("Miembro", "Cada campo declarado dentro de una estructura.", "Como cada casilla de la ficha: tiene su nombre y su lugar fijo."),
                ("Offset de miembro", "Distancia en bytes desde el inicio de la estructura hasta ese campo.", "Como la dirección de una casa dentro de una colonia: el número que dice cuántas calles avanzar desde la entrada."),
                ("Padding", "Bytes vacíos insertados para que el siguiente campo quede alineado.", "Como el relleno de burbujas en una caja: no es parte del producto, pero evita que se golpee.")
            ],
            "resultado": "Un calculador de offsets y tamaños de struct que respeta alineación y padding, verificado con cuatro disposiciones distintas."
        },
        "lab": {
            "reto": "Offsets de miembros y tamaño de struct",
            "entregable": "tus funciones offset_campo() y tamano_struct() en artesano_sesion19_c.c, la salida del harness y la bitácora en auditorias/auditoria_sesion19.md",
            "explicacion": "Recibes una lista ordenada de campos con su tipo; offset_campo() devuelve la posición del campo pedido y tamano_struct() el total con padding final. El harness compara contra la disposición real de la arquitectura.",
            "reglas": [
                "Cada campo se alinea a su propio ancho antes de asignarle offset.",
                "El tamaño total se redondea al múltiplo del campo más grande.",
                "Un campo inexistente, una lista NULL o un tipo desconocido devuelven -1."
            ],
            "api": {
                "header": "api_sesion19.h",
                "decls": [
                    "int offset_campo(const Campo *campos, int total, const char *nombre);",
                    "int tamano_struct(const Campo *campos, int total);"
                ],
                "tipos": [
                    "typedef struct Campo {",
                    "    const char *nombre;",
                    "    const char *tipo;",
                    "} Campo;"
                ]
            },
            "stub": "int offset_campo(const Campo *campos, int total, const char *nombre) {\n    (void)campos; (void)total; (void)nombre; /* TODO: recorre y alinea cada campo */\n    return -1;\n}\n\nint tamano_struct(const Campo *campos, int total) {\n    (void)campos; (void)total; /* TODO: suma con padding y redondea al final */\n    return -1;\n}",
            "casos": [
                {"caso": "struct char e int: b", "codigo": "Campo a[] = {{\"a\", \"char\"}, {\"b\", \"int\"}};\nint r = offset_campo(a, 2, \"b\");", "var": "r", "esperado": 4, "tipo": "int"},
                {"caso": "struct de tres campos: c", "codigo": "Campo b[] = {{\"a\", \"char\"}, {\"b\", \"int\"}, {\"c\", \"short\"}};\nint r = offset_campo(b, 3, \"c\");", "var": "r", "esperado": 8, "tipo": "int"},
                {"caso": "tamano total con padding", "codigo": "Campo b[] = {{\"a\", \"char\"}, {\"b\", \"int\"}, {\"c\", \"short\"}};\nint r = tamano_struct(b, 3);", "var": "r", "esperado": 12, "tipo": "int"},
                {"caso": "double seguido de char", "codigo": "Campo d[] = {{\"a\", \"double\"}, {\"b\", \"char\"}};\nint r = tamano_struct(d, 2);", "var": "r", "esperado": 16, "tipo": "int"},
                {"caso": "miembro inexistente", "codigo": "Campo b[] = {{\"a\", \"char\"}, {\"b\", \"int\"}, {\"c\", \"short\"}};\nint r = offset_campo(b, 3, \"z\");", "var": "r", "esperado": -1, "tipo": "int"},
                {"caso": "struct sin campos", "codigo": "Campo b[] = {{\"a\", \"char\"}};\nint r = tamano_struct(b, 0);", "var": "r", "esperado": 0, "tipo": "int"}
            ],
            "criterios": [
                "Cada offset coincide con la posición real del campo después de aplicar el relleno.",
                "El tamaño total incluye el padding final hasta el múltiplo de la alineación mayor.",
                "Un miembro inexistente devuelve -1 y una estructura sin campos devuelve 0."
            ]
        }
    },
    20: {
        "tema": "Hito 2: Analizador Semántico Completo y Scopes",
        "unidad": "Unidad 2: Tabla de Símbolos y Ámbitos",
        "teoria_principal": {
            "titulo": "Integración del Frontend Semántico Completo",
            "lead": "Culminación de la Unidad 2. El compilador ahora valida completamente tipos, ámbitos, funciones, arreglos y estructuras sin generar código erróneo.",
            "tarjetas": [
                ("01. Validación Semántica Integral", "Todo el código fuente se verifica contra la tabla de símbolos y las reglas de tipo antes de avanzar al código intermedio.", "Cualquier programa inválido es rechazado con mensajes de error precisos."),
                ("02. AST Decorado y Completo", "Cada nodo del AST contiene su tipo verificado, y cada identificador apunta directamente a su `SymbolEntry` con offset resuelto.", "El backend ya no necesita resolver nombres; solo consume desplazamientos y tamaños."),
                ("03. Entrega de Hito 2 (Git Tag)", "Etiquetado formal de versión en GitHub: `git tag v0.2-hito2`.", "Representa el 25% del Proyecto Integrador Semestral.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Auditoría de Integridad y Tabla de Símbolos",
            "descripcion": "Verificación del árbol de scopes y cálculo de memoria total:",
            "tarjetas": [
                ("Consistencia de Offsets", "Verificación de que ninguna variable local ni campo de estructura tenga offsets superpuestos en memoria.", "Garantiza que la generación de código x86-64 no corrompa variables adyacentes."),
                ("Batería de Pruebas de Estrés Semántico", "Programas de prueba con funciones mutuamente recursivas, shadowing profundo y estructuras complejas.", "Comprueba la robustez del compilador ante código hostil o ambiguo.")
            ]
        },
        "casos_borde": {
            "titulo": "Criterios de Rechazo del Hito 2",
            "items": [
                "Aceptar variables no declaradas o redeclaraciones en el mismo ámbito sin emitir error.",
                "Fallo de segmentación en la búsqueda de identificadores con shadowing profundo.",
                "Cálculo incorrecto de offsets en estructuras con padding de alineación."
            ]
        },
        "contexto": {
            "pregunta": "¿Puede el compilador responder de una sola pasada quién es cada nombre en un programa con bloques y funciones?",
            "objetivo": "Integrar la tabla de símbolos con el árbol de ámbitos para resolver nombres con shadowing y contar los símbolos visibles desde un punto del programa.",
            "por_que": "Hasta ahora cada pieza funciona sola; el Hito 2 exige que trabajen juntas. Resolver un nombre con shadowing profundo combina búsqueda jerárquica, ciclo de vida de bloque y deduplicación de símbolos, y es exactamente lo que el backend consultará para asignar offsets. Si esta integración falla, el compilador acepta programas donde dos variables distintas comparten el mismo nombre y el mismo espacio de memoria.",
            "conceptos": [
                ("Integración", "Hacer que dos estructuras del compilador intercambien información sin romper sus contratos.", "Como conectar dos tuberías: cada una funciona sola, pero la unión debe quedar sin fugas."),
                ("Símbolo visible", "Nombre que puede usarse en un punto del programa porque algún ámbito de la cadena lo declara.", "Como las herramientas que alcanzas desde tu banco de trabajo: las que están en cajones cerrados, no."),
                ("Shadowing profundo", "Nombre redeclarado en varios niveles anidados, donde gana el más interno.", "Como tres capas de pintura: la que ves es la última, aunque las anteriores sigan debajo."),
                ("Deduplicación", "Contar un nombre una sola vez aunque aparezca en varios ámbitos.", "Como contar invitados y no invitaciones: si la misma persona recibió varias, sigue siendo una.")
            ],
            "resultado": "Un resolvedor de nombres con profundidad y un contador de símbolos visibles que respeta shadowing, con el harness del Hito 2 en verde."
        },
        "lab": {
            "reto": "Resolución de nombres y visibilidad",
            "entregable": "tus funciones profundidad_de() y contar_visibles() en artesano_sesion20_c.c, la salida del harness y la bitácora en auditorias/auditoria_sesion20.md",
            "explicacion": "Recibes una cadena de ámbitos con sus símbolos; profundidad_de() dice a cuántos niveles está el nombre (0 es el ámbito actual) y contar_visibles() cuenta los nombres distintos que se ven desde el bloque actual. El harness arma cadenas de tres niveles con nombres repetidos.",
            "reglas": [
                "profundidad_de() devuelve -1 si el nombre no existe y -2 si algún argumento es NULL.",
                "contar_visibles() cuenta cada nombre una sola vez, aunque esté en varios ámbitos.",
                "El ámbito más interno siempre gana: el shadowing no se promedia ni se suma."
            ],
            "api": {
                "header": "api_sesion20.h",
                "decls": [
                    "int profundidad_de(const Ambito *actual, const char *nombre);",
                    "int contar_visibles(const Ambito *actual);"
                ],
                "tipos": [
                    "#define AMBITO_MAX 8",
                    "typedef struct Ambito {",
                    "    const char *nombre;",
                    "    const char *simbolos[AMBITO_MAX];",
                    "    int total;",
                    "    struct Ambito *padre;",
                    "} Ambito;"
                ]
            },
            "stub": "int profundidad_de(const Ambito *actual, const char *nombre) {\n    (void)actual; (void)nombre; /* TODO: busca el nombre subiendo por padre */\n    return -1;\n}\n\nint contar_visibles(const Ambito *actual) {\n    (void)actual; /* TODO: cuenta nombres distintos en toda la cadena */\n    return -1;\n}",
            "casos": [
                {"caso": "nombre en el ambito actual", "codigo": "Ambito g;\nmemset(&g, 0, sizeof g);\ng.nombre = \"global\";\ng.simbolos[g.total++] = \"x\";\nAmbito l;\nmemset(&l, 0, sizeof l);\nl.nombre = \"bloque\";\nl.padre = &g;\nl.simbolos[l.total++] = \"y\";\nint r = profundidad_de(&l, \"y\");", "var": "r", "esperado": 0, "tipo": "int"},
                {"caso": "nombre dos niveles arriba", "codigo": "Ambito raiz;\nmemset(&raiz, 0, sizeof raiz);\nraiz.nombre = \"raiz\";\nraiz.simbolos[raiz.total++] = \"x\";\nAmbito medio;\nmemset(&medio, 0, sizeof medio);\nmedio.nombre = \"medio\";\nmedio.padre = &raiz;\nAmbito hoja;\nmemset(&hoja, 0, sizeof hoja);\nhoja.nombre = \"hoja\";\nhoja.padre = &medio;\nint r = profundidad_de(&hoja, \"x\");", "var": "r", "esperado": 2, "tipo": "int"},
                {"caso": "shadowing gana el interno", "codigo": "Ambito g;\nmemset(&g, 0, sizeof g);\ng.nombre = \"global\";\ng.simbolos[g.total++] = \"x\";\nAmbito l;\nmemset(&l, 0, sizeof l);\nl.nombre = \"bloque\";\nl.padre = &g;\nl.simbolos[l.total++] = \"x\";\nint r = profundidad_de(&l, \"x\");", "var": "r", "esperado": 0, "tipo": "int"},
                {"caso": "nombre no visible", "codigo": "Ambito g;\nmemset(&g, 0, sizeof g);\ng.nombre = \"global\";\ng.simbolos[g.total++] = \"x\";\nAmbito l;\nmemset(&l, 0, sizeof l);\nl.nombre = \"bloque\";\nl.padre = &g;\nint r = profundidad_de(&l, \"z\");", "var": "r", "esperado": -1, "tipo": "int"},
                {"caso": "visibles sin repetir", "codigo": "Ambito g;\nmemset(&g, 0, sizeof g);\ng.nombre = \"global\";\ng.simbolos[g.total++] = \"x\";\ng.simbolos[g.total++] = \"y\";\nAmbito l;\nmemset(&l, 0, sizeof l);\nl.nombre = \"bloque\";\nl.padre = &g;\nl.simbolos[l.total++] = \"y\";\nl.simbolos[l.total++] = \"z\";\nint r = contar_visibles(&l);", "var": "r", "esperado": 3, "tipo": "int"},
                {"caso": "ambito NULL", "codigo": "int r = profundidad_de(NULL, \"x\");", "var": "r", "esperado": -2, "tipo": "int"}
            ],
            "criterios": [
                "profundidad_de() recorre la cadena completa y devuelve el nivel del ámbito más cercano que declara el nombre.",
                "contar_visibles() elimina duplicados incluso cuando el mismo nombre aparece en dos niveles.",
                "Los argumentos NULL se reportan con -2 sin desreferenciar memoria inválida."
            ]
        }
    }
}