# contenido_teorico_bloque4.py
# Base de conocimiento conceptual: Unidad 4: Código Objeto y Backend (Sesiones 31 a 40)
# Materia: Lenguajes y Autómatas II (SCD-1016)
# Docente Titular: MCC. Iván Márquez Larios (ijmarquezl)

TEORIA_BLOQUE_4 = {31: {'tema': 'Introducción a Ensamblador x86-64 y Arquitectura de CPU',
      'unidad': 'Unidad 4: Código Objeto y Backend',
      'teoria_principal': {'titulo': 'Mapeo de Código Intermedio a Instrucciones Máquina',
                           'lead': 'El backend traduce cuádruplos abstractos a instrucciones x86-64 reales que operan sobre registros y '
                                   'memoria.',
                           'tarjetas': [('01. Registros de Propósito General',
                                         '16 registros de 64 bits (RAX, RBX, RCX, RDX, RSI, RDI, RBP, RSP, R8-R15).',
                                         'Permiten realizar operaciones aritméticas a la velocidad del reloj del procesador sin tocar la '
                                         'RAM.'),
                                        ('02. Sintaxis GNU Assembler (AT&T vs Intel)',
                                         "AT&T: 'movl %eax, %ebx' (origen -> destino). Intel: 'mov ebx, eax' (destino <- origen).",
                                         "GCC utiliza por defecto la convención AT&T con prefijos '%' para registros y '$' para "
                                         'literales.'),
                                        ('03. Instrucciones Aritméticas Básicas',
                                         "Traducción de cuádruplos directos: 'addq', 'subq', 'imulq', 'idivq'.",
                                         "Operan destructivamente sobre el registro destino: 'addq %rbx, %rax' calcula RAX = RAX + RBX.")]},
      'arquitectura_memoria': {'titulo': 'Jerarquía de Registros y Sub-Registros',
                               'descripcion': 'Acceso a partes de 8, 16, 32 y 64 bits del mismo registro físico:',
                               'tarjetas': [('Subdivisiones (Ejemplo RAX)',
                                             'RAX (64 bits), EAX (32 bits), AX (16 bits), AL/AH (8 bits inferiores/superiores).',
                                             'Escribir en un registro de 32 bits (EAX) limpia a ceros automáticamente los 32 bits '
                                             'superiores de RAX.'),
                                            ('Modos de Direccionamiento',
                                             'Directo por registro (%rax), Inmediato ($42), y Desplazamiento de memoria (-8(%rbp)).',
                                             'Permite leer variables locales ubicadas en la pila con una sola instrucción.')]},
      'casos_borde': {'titulo': 'Antipatrones en Ensamblador',
                      'items': ["Mover memoria a memoria directamente ('movq -8(%rbp), -16(%rbp)'), operación ilegal en la arquitectura "
                                'x86-64.',
                                "Confundir sufijos de tamaño ('movb', 'movw', 'movl', 'movq') corrompiendo registros adyacentes.",
                                "No extender el signo en divisiones enteras ('cdq' / 'cqo') provocando interrupciones de punto flotante."]},
      'contexto': {'pregunta': '¿Cómo se convierte una operación abstracta como t3 = t1 + t2 en instrucciones que la CPU entiende?',
                   'objetivo': 'Traducir un cuádruplo TAC a la secuencia x86-64 que lo ejecuta y comprobar que el valor calculado coincide '
                               'con la operación original.',
                   'por_que': 'El backend existe para que el programa deje de ser texto y se vuelva instrucciones. Antes de emitir un '
                              'archivo .s completo hay que dominar la pieza mínima: cargar un operando, aplicar la operación y dejar el '
                              'resultado donde la siguiente instrucción lo encuentre. Si esa traducción está mal, todo el compilador '
                              'produce binarios que calculan otra cosa.',
                   'conceptos': [('Registro',
                                  'Una ranura de memoria dentro de la CPU, mucho más rápida que la RAM, que guarda un valor mientras se '
                                  'opera con él.',
                                  'Como la libreta pequeña que usas en una suma: no vas al archivo cada vez que necesitas un número.'),
                                 ('Sufijo de tamaño',
                                  'El final del mnemónico (movb, movw, movl, movq) indica cuántos bytes mueve la instrucción.',
                                  'Como las tallas de una caja: si pides la equivocada, el contenido no cabe o se sale.'),
                                 ('Sintaxis AT&T',
                                  'Convención de GNU donde el origen va primero y el destino después, con % para registros y $ para '
                                  'literales.',
                                  'Como una receta escrita de ingrediente a plato: primero lo que echas, luego dónde lo pones.'),
                                 ('Operación destructiva',
                                  'addq %rbx, %rax guarda el resultado en %rax y borra el valor anterior de ese registro.',
                                  'Como sumar en la misma hoja donde tenías el primer número: el borrador anterior ya no existe.')],
                   'resultado': 'Dos funciones en C: una que nombra la instrucción x86-64 de cada operador TAC y otra que ejecuta el '
                                'cuádruplo con la semántica de la CPU.'},
      'lab': {'reto': 'Mapeo de TAC a instrucciones mov/add/sub',
              'entregable': 'tu implementación de mnemonico() y ejecutar_tac() en artesano_sesion31_c.c, el harness en verde y la bitácora '
                            'en auditorias/auditoria_sesion31.md',
              'explicacion': 'Recibes un operador (+, -, *) o un cuádruplo con la forma tN = A op B, y devuelves el mnemónico AT&T '
                             'correspondiente o el valor que la CPU obtendría al ejecutarlo.',
              'reglas': ['Los operandos del cuádruplo son literales decimales con signo; no hay variables ni acceso a memoria.',
                         'Un operador desconocido se responde con nop, y un cuádruplo mal formado vale cero.',
                         'Nada de main(): el harness ya trae el suyo y compila con -Werror.'],
              'api': {'header': 'api_sesion31.h', 'decls': ['const char *mnemonico(char op);', 'long ejecutar_tac(const char *tac);']},
              'stub': 'const char *mnemonico(char op) {\n'
                      '    (void)op; /* TODO: + -> addq, - -> subq, * -> imulq, otro -> nop */\n'
                      '    return "nop";\n'
                      '}\n'
                      '\n'
                      'long ejecutar_tac(const char *tac) {\n'
                      '    (void)tac; /* TODO: leer tN = A op B y aplicar la operacion */\n'
                      '    return 0;\n'
                      '}',
              'casos': [{'caso': "mnemonico('+')",
                         'codigo': "const char *r = mnemonico('+');",
                         'var': 'r',
                         'esperado': 'addq',
                         'tipo': 'str'},
                        {'caso': "mnemonico('*')",
                         'codigo': "const char *r = mnemonico('*');",
                         'var': 'r',
                         'esperado': 'imulq',
                         'tipo': 'str'},
                        {'caso': "mnemonico('?')",
                         'codigo': "const char *r = mnemonico('?');",
                         'var': 'r',
                         'esperado': 'nop',
                         'tipo': 'str'},
                        {'caso': 'ejecutar_tac("t0 = 4 + 5")',
                         'codigo': 'long r = ejecutar_tac("t0 = 4 + 5");',
                         'var': 'r',
                         'esperado': 9,
                         'tipo': 'int'},
                        {'caso': 'ejecutar_tac("t1 = 10 - 25")',
                         'codigo': 'long r = ejecutar_tac("t1 = 10 - 25");',
                         'var': 'r',
                         'esperado': -15,
                         'tipo': 'int'},
                        {'caso': 'ejecutar_tac("t2 = 7 * 6")',
                         'codigo': 'long r = ejecutar_tac("t2 = 7 * 6");',
                         'var': 'r',
                         'esperado': 42,
                         'tipo': 'int'}],
              'criterios': ['mnemonico devuelve exactamente el mnemónico AT&T de cada operador, sin prefijos ni sufijos extra.',
                            'ejecutar_tac aplica la operación del cuádruplo y devuelve el mismo valor que produciría la CPU.',
                            'Los seis casos del harness salen OK y el programa termina con código de salida 0.']}},
 32: {'tema': 'Asignación Ingenua de Registros (Naive Allocation)',
      'unidad': 'Unidad 4: Código Objeto y Backend',
      'teoria_principal': {'titulo': 'Estrategia Cargar-Computar-Almacenar (Load-Op-Store)',
                           'lead': 'El asignador ingenuo mapea cada temporal a la memoria de pila y utiliza un conjunto mínimo de '
                                   'registros como intermediarios.',
                           'tarjetas': [('01. Patrón Load-Op-Store',
                                         "Para cada cuádruplo 't2 = t0 + t1': carga t0 en RAX, t1 en RBX, suma y almacena RAX en la "
                                         'dirección de t2.',
                                         'Estrategia robusta y sencilla de implementar que no requiere análisis de vida de variables.'),
                                        ('02. Registros de Trabajo Reservados',
                                         'Se reservan registros fijos (ej. RAX y RBX para aritmética, R10 y R11 para temporales).',
                                         'Evita conflictos de asignación manteniendo un pool constante para todas las operaciones.'),
                                        ('03. Desventaja de Rendimiento',
                                         'Genera un tráfico masivo de lecturas y escrituras en el Stack (RAM / Caché L1).',
                                         'Compensado por la simplicidad en la generación directa de código.')]},
      'arquitectura_memoria': {'titulo': 'Tabla de Desplazamientos del Stack Frame',
                               'descripcion': 'Mapeo estático de variables y temporales a offsets negativos:',
                               'tarjetas': [('Offset de Temporales',
                                             "Cada '_t0, _t1...' recibe una ranura fija de 8 bytes en la pila: '-8(%rbp), -16(%rbp)...'.",
                                             'Calculado consecutivamente durante la fase de análisis de cuádruplos.'),
                                            ('Alineación del Marco',
                                             "El tamaño total del marco de pila debe redondearse al múltiplo superior de 16 bytes: 'subq "
                                             "$32, %rsp'.",
                                             'Obligatorio según la convención ABI x86-64.')]},
      'casos_borde': {'titulo': 'Puntos de Falla en Asignación Ingenua',
                      'items': ['Superposición de offsets entre variables locales del usuario y temporales generados por el compilador.',
                                'Olvidar guardar el resultado del registro de vuelta a la memoria tras la operación.',
                                'Agotar el espacio de direccionamiento de 32 bits en funciones con miles de temporales.']},
      'contexto': {'pregunta': '¿Dónde vive cada temporal mientras el backend lo está usando?',
                   'objetivo': 'Asignar cada temporal a una ranura fija de la pila y elegir los registros de trabajo con los que el código '
                               'generado carga, opera y almacena.',
                   'por_que': 'El asignador ingenuo es el primer backend que funciona: da a cada temporal una dirección estable y usa un '
                              'puñado de registros conocidos para operar. Entender ese mapa es requisito para optimizar registros más '
                              'adelante y para depurar un archivo .s que calcula mal porque dos temporales compartieron la misma ranura.',
                   'conceptos': [('Temporal',
                                  'Un valor intermedio que el compilador inventa (t0, t1, ...) y que no existe en el programa fuente.',
                                  'Como el papel de borrador donde anotas un resultado parcial antes de pasarlo en limpio.'),
                                 ('Ranura de pila',
                                  'Un hueco de 8 bytes dentro del marco de la función, identificado por un desplazamiento negativo desde '
                                  '%rbp.',
                                  'Como el casillero numerado de una estación: cada temporal tiene el suyo y no se mezclan.'),
                                 ('Registro de trabajo',
                                  'Un registro reservado por el generador para realizar la operación del momento, sin importar qué '
                                  'variable representa.',
                                  'Como el martillo de un carpintero: no pertenece a ninguna pieza, sirve para todas.'),
                                 ('Patrón load-op-store',
                                  'Cargar un operando a un registro, aplicar la operación y guardar el resultado en su ranura.',
                                  'Como sacar una herramienta del cajón, usarla y devolverla antes de abrir el siguiente cajón.')],
                   'resultado': 'Un mapa de temporales a desplazamientos de pila y una tabla de registros de trabajo, implementados y '
                                'verificados caso por caso.'},
      'lab': {'reto': 'Asignador directo de temporales a registros',
              'entregable': 'tu implementación de slot_temporal() y registro_de_trabajo() en artesano_sesion32_c.c, el harness en verde y '
                            'la bitácora en auditorias/auditoria_sesion32.md',
              'explicacion': 'Recibes el nombre de un temporal (t0, t1, ...) o el índice de un registro de trabajo, y devuelves su '
                             'desplazamiento en el marco o el nombre AT&T del registro que le toca.',
              'reglas': ['Cada temporal tN ocupa 8 bytes: su desplazamiento es -8 * (N + 1).',
                         'Los registros de trabajo son %rax, %rbx, %r10 y %r11, en ese orden; del índice 4 en adelante no hay registro.',
                         'Un nombre que no sea t seguido de dígitos se considera inválido y vale cero.'],
              'api': {'header': 'api_sesion32.h',
                      'decls': ['int slot_temporal(const char *temporal);', 'const char *registro_de_trabajo(int indice);']},
              'stub': 'int slot_temporal(const char *temporal) {\n'
                      '    (void)temporal; /* TODO: t0 -> -8, t1 -> -16, ... */\n'
                      '    return 0;\n'
                      '}\n'
                      '\n'
                      'const char *registro_de_trabajo(int indice) {\n'
                      '    (void)indice; /* TODO: 0 -> %rax, 1 -> %rbx, ... */\n'
                      '    return "ninguno";\n'
                      '}',
              'casos': [{'caso': 'slot_temporal("t0")',
                         'codigo': 'int r = slot_temporal("t0");',
                         'var': 'r',
                         'esperado': -8,
                         'tipo': 'int'},
                        {'caso': 'slot_temporal("t7")',
                         'codigo': 'int r = slot_temporal("t7");',
                         'var': 'r',
                         'esperado': -64,
                         'tipo': 'int'},
                        {'caso': 'slot_temporal("x")', 'codigo': 'int r = slot_temporal("x");', 'var': 'r', 'esperado': 0, 'tipo': 'int'},
                        {'caso': 'registro_de_trabajo(0)',
                         'codigo': 'const char *r = registro_de_trabajo(0);',
                         'var': 'r',
                         'esperado': '%rax',
                         'tipo': 'str'},
                        {'caso': 'registro_de_trabajo(3)',
                         'codigo': 'const char *r = registro_de_trabajo(3);',
                         'var': 'r',
                         'esperado': '%r11',
                         'tipo': 'str'},
                        {'caso': 'registro_de_trabajo(4)',
                         'codigo': 'const char *r = registro_de_trabajo(4);',
                         'var': 'r',
                         'esperado': 'ninguno',
                         'tipo': 'str'}],
              'criterios': ['slot_temporal acierta el desplazamiento de cada temporal y rechaza nombres mal formados con cero.',
                            'registro_de_trabajo respeta el orden del pool y responde ninguno cuando el índice se sale.',
                            'Los seis casos del harness salen OK y el programa termina con código de salida 0.']}},
 33: {'tema': 'Derramamiento a Memoria (Register Spilling)',
      'unidad': 'Unidad 4: Código Objeto y Backend',
      'teoria_principal': {'titulo': 'Gestión de Presión de Registros y Desalojo',
                           'lead': 'Cuando el número de variables activas simultáneamente excede los registros físicos disponibles, se '
                                   "deben 'derramar' valores a la pila.",
                           'tarjetas': [('01. Presión de Registros (Register Pressure)',
                                         'Ocurre en expresiones con muchos operandos concurrentes donde todos los registros de CPU están '
                                         'ocupados.',
                                         'El compilador debe seleccionar qué registro desalojar a la pila para liberar espacio.'),
                                        ('02. Criterio de Selección (Heurística de Desalojo)',
                                         'Desalojar el temporal cuyo próximo uso esté más lejano en el tiempo.',
                                         'Minimiza la penalización de rendimiento de recargar datos desde el Stack.'),
                                        ('03. Instrucciones de Derrame (Spill Code)',
                                         "Emisión explícita de 'movq %reg, offset(%rbp)' al desalojar y 'movq offset(%rbp), %reg' al "
                                         'reutilizar.',
                                         'Introduce instrucciones adicionales de acceso a memoria para salvar la limitación física.')]},
      'arquitectura_memoria': {'titulo': 'Ranuras de Derrame en el Marco de Pila',
                               'descripcion': 'Zona reservada en el Stack para variables derramadas:',
                               'tarjetas': [('Spill Slots',
                                             'Espacio reservado al fondo del stack frame exclusivo para variables que no cupieron en '
                                             'registros.',
                                             'Se accede mediante direccionamiento indirecto indexado a RBP.'),
                                            ('Análisis de Vida (Liveness)',
                                             'Determina en qué punto una variable muere (no vuelve a leerse), permitiendo reciclar su '
                                             'registro inmediatamente.',
                                             'Reduce drásticamente la necesidad de hacer derrame a memoria.')]},
      'casos_borde': {'titulo': 'Fallas Críticas en Derramamiento',
                      'items': ['Desalojar un registro que contiene un puntero base activo corrompiendo el marco de pila.',
                                'Sobrescribir ranuras de derrame por no calcular correctamente el tamaño del área de spill.',
                                'Recargar un registro con el dato incorrecto tras múltiples saltos condicionales.']},
      'contexto': {'pregunta': '¿Qué hace el compilador cuando tiene más valores vivos que registros disponibles?',
                   'objetivo': 'Calcular cuántas ranuras de derrame necesita una función y elegir qué valor mandar a la pila cuando la '
                               'presión de registros aprieta.',
                   'por_que': 'Los registros de la CPU son un recurso escaso y el programa puede tener más valores activos de los que '
                              'caben. El derrame es la válvula de escape que mantiene correcto el programa aunque sea más lento; si se '
                              'calcula mal el área de derrame, dos valores se pisan y el binario produce resultados imposibles de '
                              'rastrear.',
                   'conceptos': [('Presión de registros',
                                  'La cantidad de valores que están vivos al mismo tiempo y que compiten por los registros físicos de la '
                                  'CPU.',
                                  'Como viajar en un coche de cinco plazas con siete personas: alguien tiene que esperar afuera.'),
                                 ('Derrame (spill)',
                                  'Copiar un valor de un registro a una ranura de pila para liberar ese registro para otro uso.',
                                  'Como bajar una maleta del portaequipajes para que quepa otra cosa y recogerla después.'),
                                 ('Próximo uso',
                                  'La distancia, medida en instrucciones, hasta la siguiente vez que un valor se va a leer.',
                                  'Como saber cuál ingrediente vas a necesitar al final de la receta: ese puede esperar en el '
                                  'refrigerador.'),
                                 ('Recarga (reload)',
                                  'Traer de vuelta el valor derramado desde la pila al registro cuando vuelve a hacer falta.',
                                  'Como recuperar la maleta del maletero justo antes de bajarte del coche.')],
                   'resultado': 'Dos funciones: una que dimensiona el área de derrame y otra que elige la víctima correcta según su '
                                'próximo uso.'},
      'lab': {'reto': 'Manejo de pila ante agotamiento de registros',
              'entregable': 'tu implementación de ranuras_derrame() y victima_desalojo() en artesano_sesion33_c.c, el harness en verde y '
                            'la bitácora en auditorias/auditoria_sesion33.md',
              'explicacion': 'Recibes cuántos valores están vivos y cuántos registros hay, o el arreglo de próximos usos de cada valor; '
                             'devuelves las ranuras necesarias o el índice del valor que debe irse a la pila.',
              'reglas': ['Si los valores vivos caben en los registros, no se reserva ninguna ranura.',
                         'La víctima del desalojo es el valor con el próximo uso más lejano; ante empate gana el índice menor.',
                         'Un arreglo vacío o NULL no tiene víctima: se responde con -1.'],
              'api': {'header': 'api_sesion33.h',
                      'decls': ['int ranuras_derrame(int vivas, int registros);', 'int victima_desalojo(const int *proximos, int n);']},
              'stub': 'int ranuras_derrame(int vivas, int registros) {\n'
                      '    (void)vivas;\n'
                      '    (void)registros; /* TODO: solo sobran los que no caben */\n'
                      '    return 0;\n'
                      '}\n'
                      '\n'
                      'int victima_desalojo(const int *proximos, int n) {\n'
                      '    (void)proximos;\n'
                      '    (void)n; /* TODO: el proximo uso mas lejano */\n'
                      '    return 0;\n'
                      '}',
              'casos': [{'caso': 'ranuras_derrame(12, 8)',
                         'codigo': 'int r = ranuras_derrame(12, 8);',
                         'var': 'r',
                         'esperado': 4,
                         'tipo': 'int'},
                        {'caso': 'ranuras_derrame(10, 8)',
                         'codigo': 'int r = ranuras_derrame(10, 8);',
                         'var': 'r',
                         'esperado': 2,
                         'tipo': 'int'},
                        {'caso': 'ranuras_derrame(3, 8)',
                         'codigo': 'int r = ranuras_derrame(3, 8);',
                         'var': 'r',
                         'esperado': 0,
                         'tipo': 'int'},
                        {'caso': 'victima_desalojo({1,9,4}, 3)',
                         'codigo': 'int v[] = {1, 9, 4};\nint r = victima_desalojo(v, 3);',
                         'var': 'r',
                         'esperado': 1,
                         'tipo': 'int'},
                        {'caso': 'victima_desalojo({2,2,2}, 3)',
                         'codigo': 'int v[] = {2, 2, 2};\nint r = victima_desalojo(v, 3);',
                         'var': 'r',
                         'esperado': 0,
                         'tipo': 'int'},
                        {'caso': 'victima_desalojo(NULL, 0)',
                         'codigo': 'int r = victima_desalojo(NULL, 0);',
                         'var': 'r',
                         'esperado': -1,
                         'tipo': 'int'}],
              'criterios': ['ranuras_derrame nunca reserva de más ni de menos: solo cuenta los valores que no caben.',
                            'victima_desalojo aplica la heurística del próximo uso más lejano y resuelve el empate por índice.',
                            'Los seis casos del harness salen OK y el programa termina con código de salida 0.']}},
 34: {'tema': 'Marco de Pila (Stack Frame) y Prólogo/Epílogo',
      'unidad': 'Unidad 4: Código Objeto y Backend',
      'teoria_principal': {'titulo': 'Convención ABI System V x86-64 y Control de Pila',
                           'lead': 'Cada función debe construir su marco de pila al iniciar (Prólogo) y destruirlo al finalizar (Epílogo).',
                           'tarjetas': [('01. Puntero de Base (RBP) y de Pila (RSP)',
                                         'RBP marca la base fija del marco actual; RSP marca el límite superior dinámico de la pila.',
                                         "Permite acceder a variables locales mediante offsets constantes negativos: '-offset(%rbp)'."),
                                        ('02. El Prólogo Estándar',
                                         "Secuencia obligatoria: 'pushq %rbp', 'movq %rsp, %rbp', 'subq $N, %rsp'.",
                                         'Salva el RBP del llamador, establece el nuevo marco y reserva N bytes para variables locales.'),
                                        ('03. El Epílogo Estándar',
                                         "Secuencia obligatoria: 'movq %rbp, %rsp', 'popq %rbp', 'ret'. (O equivalentemente: 'leave', "
                                         "'ret').",
                                         'Restaura la pila del llamador y devuelve el control mediante la dirección de retorno en el tope '
                                         'de la pila.')]},
      'arquitectura_memoria': {'titulo': 'Anatomía del Stack Frame en Memoria',
                               'descripcion': 'Disposición física de una llamada a función en la pila (crece hacia abajo):',
                               'tarjetas': [('Dirección Retorno y RBP Previo',
                                             "El 'call' empuja la dirección de retorno de 8 bytes; el prólogo empuja el RBP anterior.",
                                             "Garantiza que al hacer 'ret' el procesador sepa exactamente a qué instrucción regresar."),
                                            ('Alineación a 16 Bytes',
                                             "El valor 'N' en 'subq $N, %rsp' debe elegirse de modo que '(N + 8) % 16 == 0'.",
                                             "Evita excepciones del procesador en llamadas a bibliotecas externas como 'printf'.")]},
      'casos_borde': {'titulo': 'Antipatrones en Stack Frames',
                      'items': ['Desalineación de pila que causa fallos de segmentación dentro de funciones de la biblioteca estándar '
                                '(libc).',
                                "Olvidar salvar registros 'callee-saved' (RBX, R12-R15) si son modificados dentro de la función.",
                                'Corrupción de la dirección de retorno por desbordamiento de arreglos locales en el stack.']},
      'contexto': {'pregunta': '¿Cómo se construye y se destruye el espacio de trabajo de una función en la pila?',
                   'objetivo': 'Calcular el tamaño alineado del marco para que la pila quede lista para llamar a libc y reconocer la '
                               'secuencia con la que una función se despide.',
                   'por_que': 'Cada función del binario generado debe respetar la ABI System V: si %rsp no queda alineado a 16 bytes, una '
                              'llamada a printf puede fallar dentro del programa del usuario. El prólogo y el epílogo son la frontera '
                              'entre el mundo del llamador y el de la función; equivocarse ahí corrompe la dirección de retorno y el '
                              'proceso muere.',
                   'conceptos': [('Marco de pila',
                                  'El bloque de memoria que una función reserva en la pila para sus locales, sus parámetros salvados y su '
                                  'dirección de retorno.',
                                  'Como la mesa de trabajo que extiendes al empezar una tarea y recoges al terminarla.'),
                                 ('%rbp y %rsp',
                                  '%rbp apunta a la base fija del marco; %rsp apunta al borde móvil de la pila.',
                                  'Como el borde fijo y el borde ajustable de una regla extensible.'),
                                 ('Prólogo',
                                  'Las instrucciones con las que una función guarda el marco anterior y reserva el nuevo.',
                                  'Como clavar la mesa al piso antes de poner las herramientas encima.'),
                                 ('Epílogo',
                                  'Las instrucciones que restauran %rsp y %rbp y devuelven el control al llamador.',
                                  'Como doblar la mesa y devolver la silla a su sitio al terminar la jornada.')],
                   'resultado': 'Una función que calcula el tamaño de marco alineado a 16 bytes y otra que devuelve el epílogo compacto, '
                                'ambas auditadas.'},
      'lab': {'reto': 'Configuración de punteros RBP y RSP',
              'entregable': 'tu implementación de marco_alineado() y epilogo() en artesano_sesion34_c.c, el harness en verde y la bitácora '
                            'en auditorias/auditoria_sesion34.md',
              'explicacion': 'Recibes cuántos bytes de variables locales y cuántos registros callee-saved hay que preservar; devuelves la '
                             'N exacta de subq $N, %rsp. También devuelves la secuencia de salida de la función.',
              'reglas': ['El prólogo ya empujó %rbp y los k registros callee-saved antes de restar N a %rsp.',
                         'N debe ser el menor valor que cubra las locales y deje %rsp alineado a 16 bytes.',
                         'Un número negativo de locales o de registros se rechaza con -1.'],
              'api': {'header': 'api_sesion34.h',
                      'decls': ['int marco_alineado(int locales, int callee_saved);', 'const char *epilogo(void);']},
              'stub': 'int marco_alineado(int locales, int callee_saved) {\n'
                      '    (void)locales;\n'
                      '    (void)callee_saved; /* TODO: redondear segun la alineacion de la ABI */\n'
                      '    return 0;\n'
                      '}\n'
                      '\n'
                      'const char *epilogo(void) {\n'
                      '    /* TODO: la secuencia compacta de salida */\n'
                      '    return "nop";\n'
                      '}',
              'casos': [{'caso': 'marco_alineado(0, 0)',
                         'codigo': 'int r = marco_alineado(0, 0);',
                         'var': 'r',
                         'esperado': 0,
                         'tipo': 'int'},
                        {'caso': 'marco_alineado(8, 0)',
                         'codigo': 'int r = marco_alineado(8, 0);',
                         'var': 'r',
                         'esperado': 16,
                         'tipo': 'int'},
                        {'caso': 'marco_alineado(24, 0)',
                         'codigo': 'int r = marco_alineado(24, 0);',
                         'var': 'r',
                         'esperado': 32,
                         'tipo': 'int'},
                        {'caso': 'marco_alineado(8, 1)',
                         'codigo': 'int r = marco_alineado(8, 1);',
                         'var': 'r',
                         'esperado': 8,
                         'tipo': 'int'},
                        {'caso': 'marco_alineado(-1, 0)',
                         'codigo': 'int r = marco_alineado(-1, 0);',
                         'var': 'r',
                         'esperado': -1,
                         'tipo': 'int'},
                        {'caso': 'epilogo()', 'codigo': 'const char *r = epilogo();', 'var': 'r', 'esperado': 'leave; ret', 'tipo': 'str'}],
              'criterios': ['marco_alineado devuelve la N mínima que cubre las locales y deja %rsp en múltiplo de 16.',
                            'epilogo devuelve exactamente la secuencia compacta leave; ret, sin texto adicional.',
                            'Los seis casos del harness salen OK y el programa termina con código de salida 0.']}},
 35: {'tema': 'Paso de Parámetros por Registro y Convención ABI',
      'unidad': 'Unidad 4: Código Objeto y Backend',
      'teoria_principal': {'titulo': 'Convención de Paso de Argumentos en x86-64',
                           'lead': 'A diferencia de arquitecturas antiguas de 32 bits, x86-64 pasa los primeros argumentos en registros '
                                   'rápidos en lugar de memoria.',
                           'tarjetas': [('01. Los 6 Registros de Argumentos',
                                         'Orden estricto para enteros y punteros: 1: RDI, 2: RSI, 3: RDX, 4: RCX, 5: R8, 6: R9.',
                                         "El backend debe cargar los parámetros en estos registros antes de emitir la instrucción 'call'."),
                                        ('02. Parámetros Flotantes (XMM0 a XMM7)',
                                         "Los argumentos de tipo 'float' y 'double' se pasan en los primeros 8 registros vectoriales SSE.",
                                         'Desacoplados completamente de los registros de propósito general.'),
                                        ('03. Parámetros Excedentes (Stack Overflow)',
                                         "Los parámetros a partir del 7mo se empujan al Stack en orden inverso antes del 'call'.",
                                         'El llamador es responsable de limpiar estos parámetros de la pila tras el retorno.')]},
      'arquitectura_memoria': {'titulo': 'Almacenamiento de Parámetros Formales en el Callee',
                               'descripcion': 'Cómo la función receptora respalda sus argumentos:',
                               'tarjetas': [('Copia al Frame Local',
                                             "En el prólogo, la función mueve los registros de entrada a su propio stack: 'movq %rdi, "
                                             "-8(%rbp)'.",
                                             'Libera los registros RDI, RSI... para que puedan usarse en llamadas internas subsecuentes.'),
                                            ('Registros Caller-Saved vs Callee-Saved',
                                             "Caller-saved (RAX, RCX, RDX, RSI, RDI, R8-R11) pueden ser sobrescritos por cualquier 'call'.",
                                             'Callee-saved (RBX, RBP, R12-R15) deben preservarse obligatoriamente si se usan.')]},
      'casos_borde': {'titulo': 'Puntos de Falla en Paso de Argumentos',
                      'items': ['Inversión en el orden de asignación de registros (ej. poner arg1 en RSI y arg2 en RDI).',
                                'Sobrescribir RDI con el segundo parámetro antes de haber emitido el primero.',
                                'No colocar el número de registros flotantes usados en AL antes de llamar a funciones variádicas como '
                                "'printf'."]},
      'contexto': {'pregunta': '¿En qué registro viaja cada argumento cuando una función llama a otra?',
                   'objetivo': 'Asignar argumentos enteros y flotantes a los registros que impone System V y calcular cuántos terminan en '
                               'la pila.',
                   'por_que': 'El call no copia argumentos por arte de magia: el llamador debe dejar el primero en %rdi, el segundo en '
                              '%rsi y así sucesivamente, o el callee leerá basura. Este contrato es el mismo que usa printf; si el backend '
                              'lo rompe, el binario generado llama bien a la función pero con los valores cambiados.',
                   'conceptos': [('Registro de argumento',
                                  'El registro fijo donde el llamador coloca un parámetro antes de ejecutar call.',
                                  'Como el número de asiento asignado a cada invitado: si se sienta en otro, el mesero le sirve el plato '
                                  'equivocado.'),
                                 ('Argumento en pila',
                                  'Un parámetro que ya no cabe en registros y se empuja a la pila antes de la llamada.',
                                  'Como cuando la mesa se llena: los últimos invitados ponen su silla aparte.'),
                                 ('Registro vectorial',
                                  'Un registro SSE como %xmm0 reservado para float y double.',
                                  'Como un mostrador separado para líquidos: no compite con la caja de sólidos.'),
                                 ('Argumento variádico',
                                  'Una función como printf que no conoce de antemano cuántos argumentos recibirá.',
                                  'Como un buffet: el cocinero prepara los platos según lo que pidas en el mostrador.')],
                   'resultado': 'Una tabla de asignación de argumentos a registros y un contador de argumentos que se van a la pila, '
                                'verificados con enteros y flotantes.'},
      'lab': {'reto': 'Mapeo a registros RDI, RSI, RDX, RCX, R8, R9',
              'entregable': 'tu implementación de registro_argumento() y en_pila() en artesano_sesion35_c.c, el harness en verde y la '
                            'bitácora en auditorias/auditoria_sesion35.md',
              'explicacion': 'Recibes la posición de un argumento y si es entero o flotante; devuelves el registro AT&T que le toca o pila '
                             'si ya no hay. Además calculas cuántos argumentos de una firma terminan en la pila.',
              'reglas': ['Enteros y punteros usan %rdi, %rsi, %rdx, %rcx, %r8 y %r9, en ese orden.',
                         'float y double usan %xmm0 a %xmm7, en un contador independiente del anterior.',
                         'El séptimo entero o el noveno flotante ya no recibe registro: se responde pila.'],
              'api': {'header': 'api_sesion35.h',
                      'decls': ['const char *registro_argumento(int indice, char tipo);', 'int en_pila(int total, int flotantes);']},
              'stub': 'const char *registro_argumento(int indice, char tipo) {\n'
                      '    (void)indice;\n'
                      '    (void)tipo; /* TODO: primeros 6 enteros por registro, primeros 8 flotantes */\n'
                      '    return "ninguno";\n'
                      '}\n'
                      '\n'
                      'int en_pila(int total, int flotantes) {\n'
                      '    (void)total;\n'
                      '    (void)flotantes; /* TODO: contar los que exceden cada banco de registros */\n'
                      '    return 0;\n'
                      '}',
              'casos': [{'caso': "registro_argumento(0, 'e')",
                         'codigo': "const char *r = registro_argumento(0, 'e');",
                         'var': 'r',
                         'esperado': '%rdi',
                         'tipo': 'str'},
                        {'caso': "registro_argumento(5, 'e')",
                         'codigo': "const char *r = registro_argumento(5, 'e');",
                         'var': 'r',
                         'esperado': '%r9',
                         'tipo': 'str'},
                        {'caso': "registro_argumento(3, 'f')",
                         'codigo': "const char *r = registro_argumento(3, 'f');",
                         'var': 'r',
                         'esperado': '%xmm3',
                         'tipo': 'str'},
                        {'caso': "registro_argumento(6, 'e')",
                         'codigo': "const char *r = registro_argumento(6, 'e');",
                         'var': 'r',
                         'esperado': 'pila',
                         'tipo': 'str'},
                        {'caso': 'en_pila(8, 0)', 'codigo': 'int r = en_pila(8, 0);', 'var': 'r', 'esperado': 2, 'tipo': 'int'},
                        {'caso': 'en_pila(7, 3)', 'codigo': 'int r = en_pila(7, 3);', 'var': 'r', 'esperado': 0, 'tipo': 'int'}],
              'criterios': ['registro_argumento respeta el orden de los seis registros enteros y de los ocho vectoriales.',
                            'en_pila cuenta por separado los enteros y los flotantes que exceden su banco.',
                            'Los seis casos del harness salen OK y el programa termina con código de salida 0.']}},
 36: {'tema': 'Traducción de Comparaciones y Saltos a Ensamblador',
      'unidad': 'Unidad 4: Código Objeto y Backend',
      'teoria_principal': {'titulo': 'Instrucciones de Comparación (CMP) y Banderas de CPU',
                           'lead': 'Las operaciones booleanas y saltos condicionales se implementan mediante la evaluación del registro de '
                                   'banderas EFLAGS.',
                           'tarjetas': [('01. Instrucción CMP',
                                         "'cmpq %rbx, %rax' realiza internamente una resta sustractiva 'RAX - RBX' sin alterar los "
                                         'operandos.',
                                         'Modifica las banderas Zero Flag (ZF), Sign Flag (SF) y Overflow Flag (OF).'),
                                        ('02. Saltos Condicionales Directos',
                                         "'je' (Jump Equal / ZF=1), 'jne' (Jump Not Equal / ZF=0), 'jl' (Jump Less), 'jge' (Jump "
                                         'Greater/Equal).',
                                         "Traduce directamente los cuádruplos 'IFFALSE' y 'GOTO' a bifurcaciones nativas del hardware."),
                                        ('03. Instrucciones SETcc (Booleanos)',
                                         "'sete', 'setne', 'setl' escriben un byte (0 o 1) en un registro de 8 bits según las banderas.",
                                         'Permite convertir el resultado de una comparación directamente en un entero booleano en '
                                         'memoria.')]},
      'arquitectura_memoria': {'titulo': 'Mapeo de Estructuras If y Ciclos a Ensamblador',
                               'descripcion': 'Traducción de etiquetas y bifurcaciones:',
                               'tarjetas': [('Emisión de Etiquetas de Ensamblador',
                                             "Las etiquetas TAC ('L0', 'L1') se emiten como símbolos globales/locales seguidos de dos "
                                             "puntos: '.L0:'.",
                                             "El ensamblador de GNU ('as') resuelve las distancias relativas de salto de 32 bits."),
                                            ('Salto Incondicional JMP',
                                             "El cuádruplo 'GOTO L1' se traduce directamente a 'jmp .L1'.",
                                             'Fuerza al contador de programa (RIP) a cargar la nueva dirección de memoria.')]},
      'casos_borde': {'titulo': 'Fallas en Saltos Condicionales',
                      'items': ["Confundir saltos con signo ('jl', 'jg') con saltos sin signo ('jb', 'ja').",
                                'Invertir los operandos en CMP provocando que una condición menor (<) se comporte como mayor (>).',
                                "Omitir el prefijo de punto ('.L') en etiquetas provocando colisiones con funciones de la biblioteca "
                                'estándar.']},
      'contexto': {'pregunta': '¿Cómo se convierte un if o un while en un salto que la CPU sepa ejecutar?',
                   'objetivo': 'Elegir la instrucción de salto correcta para cada comparación, con y sin signo, y comprobar cuándo la '
                               'condición se cumple.',
                   'por_que': 'Las estructuras de control del lenguaje no existen en el hardware: existen cmp, banderas y saltos. Si el '
                              'backend usa jl donde tocaba jb, un while con índices sin signo se sale del arreglo; si invierte los '
                              'operandos de cmp, el programa niega todas sus condiciones. Esta sesión fija ese mapeo antes de emitir el '
                              'archivo .s completo.',
                   'conceptos': [('cmp',
                                  'Resta dos operandos sin guardar el resultado; solo actualiza las banderas de la CPU.',
                                  'Como pesar dos cajas con una balanza: no te quedas con la diferencia, solo con la respuesta de quién '
                                  'pesa más.'),
                                 ('Bandera ZF',
                                  'La bandera que se enciende cuando el resultado de cmp fue cero, es decir, cuando los operandos eran '
                                  'iguales.',
                                  'Como el timbre que suena cuando dos fichas coinciden exactamente.'),
                                 ('Salto condicional',
                                  'Una instrucción que mueve el contador de programa a otra etiqueta solo si se cumple una bandera.',
                                  'Como un guardia que solo te deja pasar si muestras la credencial correcta.'),
                                 ('Signo vs sin signo',
                                  'jl y jg interpretan los bits como números con signo; jb y ja los interpretan como sin signo.',
                                  'Como leer 100 en una balanza: no significa lo mismo si la escala admite negativos o no.')],
                   'resultado': 'Una función que traduce operadores a saltos condicionales y otra que evalúa la comparación con la misma '
                                'semántica que la CPU.'},
      'lab': {'reto': 'Instrucciones cmp, jmp y saltos condicionales',
              'entregable': 'tu implementación de salto_para() y evaluar_salto() en artesano_sesion36_c.c, el harness en verde y la '
                            'bitácora en auditorias/auditoria_sesion36.md',
              'explicacion': 'Recibes un operador relacional y una bandera de signo, o dos valores comparados con ese operador; devuelves '
                             'el salto AT&T correcto o el resultado de la comparación.',
              'reglas': ['Los operadores válidos son <, <=, >, >=, == y !=.',
                         'Con signo se usan jl, jle, jg y jge; sin signo, jb, jbe, ja y jae; igualdad y diferencia no cambian.',
                         'Un operador desconocido responde nop y una comparación desconocida evalúa a falso.'],
              'api': {'header': 'api_sesion36.h',
                      'decls': ['const char *salto_para(const char *operador, int con_signo);',
                                'int evaluar_salto(const char *operador, long a, long b);']},
              'stub': 'const char *salto_para(const char *operador, int con_signo) {\n'
                      '    (void)operador;\n'
                      '    (void)con_signo; /* TODO: mapear el operador al salto condicional */\n'
                      '    return "nop";\n'
                      '}\n'
                      '\n'
                      'int evaluar_salto(const char *operador, long a, long b) {\n'
                      '    (void)operador;\n'
                      '    (void)a;\n'
                      '    (void)b; /* TODO: comparar como lo haria cmp */\n'
                      '    return 0;\n'
                      '}',
              'casos': [{'caso': 'salto_para("<", 1)',
                         'codigo': 'const char *r = salto_para("<", 1);',
                         'var': 'r',
                         'esperado': 'jl',
                         'tipo': 'str'},
                        {'caso': 'salto_para("<", 0)',
                         'codigo': 'const char *r = salto_para("<", 0);',
                         'var': 'r',
                         'esperado': 'jb',
                         'tipo': 'str'},
                        {'caso': 'salto_para("==", 0)',
                         'codigo': 'const char *r = salto_para("==", 0);',
                         'var': 'r',
                         'esperado': 'je',
                         'tipo': 'str'},
                        {'caso': 'evaluar_salto("<", 3, 5)',
                         'codigo': 'int r = evaluar_salto("<", 3, 5);',
                         'var': 'r',
                         'esperado': 1,
                         'tipo': 'int'},
                        {'caso': 'evaluar_salto(">=", 5, 5)',
                         'codigo': 'int r = evaluar_salto(">=", 5, 5);',
                         'var': 'r',
                         'esperado': 1,
                         'tipo': 'int'},
                        {'caso': 'evaluar_salto("!=", 7, 7)',
                         'codigo': 'int r = evaluar_salto("!=", 7, 7);',
                         'var': 'r',
                         'esperado': 0,
                         'tipo': 'int'}],
              'criterios': ['salto_para distingue correctamente los operadores con signo de los que no lo tienen.',
                            'evaluar_salto devuelve 1 solo cuando la comparación es verdadera, igual que las banderas de cmp.',
                            'Los seis casos del harness salen OK y el programa termina con código de salida 0.']}},
 37: {'tema': 'Integración del Pipeline Completo del Compilador',
      'unidad': 'Unidad 4: Código Objeto y Backend',
      'teoria_principal': {'titulo': 'Conexión Integral: Del Código Fuente al Archivo Ensamblador',
                           'lead': 'Integración modular de todas las etapas: Scanner -> Parser -> AST -> Semántico -> TAC -> Optimizador '
                                   '-> Emisor ASM.',
                           'tarjetas': [('01. Arquitectura en Pases (Multi-Pass Compiler)',
                                         'Cada pase consume la estructura de datos del pase anterior y produce una representación más '
                                         'cercana al hardware.',
                                         'Garantiza modularidad estricta y aislamiento de fallos.'),
                                        ('02. El Emisor de Ensamblador (Code Generator)',
                                         "Recorre la lista de cuádruplos optimizados y emite instrucciones de texto en formato '.s'.",
                                         "Escribe la directiva de sección de texto ('.text'), exportación global ('.globl main') y los "
                                         'marcos de función.'),
                                        ('03. Sección de Datos (.data y .rodata)',
                                         'Emite literales de cadenas y constantes globales: \'.section .rodata\', \'.string "Resultado: '
                                         '%d\\n"\'.',
                                         "Permite enlazar cadenas de texto usadas por 'printf' o funciones del sistema.")]},
      'arquitectura_memoria': {'titulo': 'Estructura del Archivo Ensamblador Emitido (.s)',
                               'descripcion': 'Formato estándar para el ensamblador GNU:',
                               'tarjetas': [('Encabezado de Sección',
                                             "'.text', '.globl main', '.type main, @function'.",
                                             "Indica al linker que 'main' es el punto de entrada ejecutable del programa."),
                                            ('Directivas de Tamaño y Depuración',
                                             "'.size main, .-main'.",
                                             'Informa al sistema operativo el tamaño exacto del bloque de código binario generado.')]},
      'casos_borde': {'titulo': 'Antipatrones en la Integración del Pipeline',
                      'items': ['Emitir código ensamblador cuando el analizador semántico registró errores fatales previos.',
                                "Falta de exportación global ('.globl main') causando errores de símbolo indefinido al enlazar.",
                                'Colisión de nombres de variables globales con identificadores de bibliotecas C estándar.']},
      'contexto': {'pregunta': '¿Cómo se pasa de una expresión en el código fuente a un archivo .s que el ensamblador acepta?',
                   'objetivo': 'Emitir un archivo ensamblador mínimo pero completo: secciones, símbolo global, prólogo, cuerpo y epílogo, '
                               'respetando el contrato que espera as.',
                   'por_que': 'Hasta ahora cada pase funcionaba por separado. El valor de un compilador aparece cuando encadena todos y '
                              'produce un texto que gcc puede ensamblar sin intervención manual. Un .globl olvidado o una etiqueta mal '
                              'formada hacen que el enlace falle aunque el cálculo sea correcto.',
                   'conceptos': [('Directiva',
                                  'Una línea del archivo .s que empieza con punto y le da una orden al ensamblador, no a la CPU.',
                                  'Como las notas al margen de una receta: no son ingredientes, son instrucciones para el cocinero.'),
                                 ('.globl',
                                  'La directiva que exporta un símbolo para que el enlazador pueda verlo desde otros archivos.',
                                  'Como poner el nombre en la puerta de la oficina: sin él, nadie sabe que existes.'),
                                 ('Etiqueta',
                                  'Un nombre seguido de dos puntos que marca una dirección dentro del código para que un salto o call '
                                  'pueda referirse a ella.',
                                  'Como el número de una casa en una calle: sirve para que el cartero llegue sin conocer el plano.'),
                                 ('Sección .text',
                                  'La región del archivo donde viven las instrucciones ejecutables.',
                                  'Como el escenario de un teatro: allí ocurre la obra; el vestuario va en otra sección.')],
                   'resultado': 'Una función que emite un archivo .s mínimo válido y comprobable, con símbolo global, prólogo, cuerpo y '
                                'epílogo.'},
      'lab': {'reto': 'Conexión de Frontend, TAC y Backend',
              'entregable': 'tu implementación de emitir_funcion() en artesano_sesion37_c.c, el harness en verde y la bitácora en '
                            'auditorias/auditoria_sesion37.md',
              'explicacion': 'Recibes el nombre de una función y el valor entero que debe devolver; escribes en el buffer un ensamblador '
                             'x86-64 completo con sección, símbolo global, prólogo, el valor en %rax y epílogo.',
              'reglas': ['La salida empieza en .text y debe contener .globl <nombre>, <nombre>:, pushq %rbp, movq %rsp, %rbp, movq '
                         '$<retorno>, %rax, leave y ret.',
                         'Cada pieza va en su propia línea terminada en salto de línea.',
                         'Si falta espacio en el buffer o algún puntero es NULL, no se escribe nada y se devuelve -1.'],
              'api': {'header': 'api_sesion37.h', 'decls': ['int emitir_funcion(const char *nombre, int retorno, char *salida, int cap);']},
              'stub': 'int emitir_funcion(const char *nombre, int retorno, char *salida, int cap) {\n'
                      '    (void)nombre;\n'
                      '    (void)retorno;\n'
                      '    (void)salida;\n'
                      '    (void)cap; /* TODO: emitir .text, .globl, prologo, cuerpo y epilogo */\n'
                      '    return 0;\n'
                      '}',
              'casos': [{'caso': 'emitir_funcion("main", 7)',
                         'codigo': 'char b[512];\nint r = emitir_funcion("main", 7, b, sizeof b);',
                         'var': 'r',
                         'esperado': 0,
                         'tipo': 'int'},
                        {'caso': 'salida .globl main',
                         'codigo': 'char b[512] = "";\nemitir_funcion("main", 7, b, sizeof b);\nint r = strstr(b, ".globl main") != NULL;',
                         'var': 'r',
                         'esperado': 1,
                         'tipo': 'int'},
                        {'caso': 'salida pushq %rbp',
                         'codigo': 'char b[512] = "";\nemitir_funcion("main", 7, b, sizeof b);\nint r = strstr(b, "pushq %rbp") != NULL;',
                         'var': 'r',
                         'esperado': 1,
                         'tipo': 'int'},
                        {'caso': 'salida movq $7, %rax',
                         'codigo': 'char b[512] = "";\n'
                                   'emitir_funcion("main", 7, b, sizeof b);\n'
                                   'int r = strstr(b, "movq $7, %rax") != NULL;',
                         'var': 'r',
                         'esperado': 1,
                         'tipo': 'int'},
                        {'caso': 'emitir_funcion(NULL)',
                         'codigo': 'char b[512];\nint r = emitir_funcion(NULL, 7, b, sizeof b);',
                         'var': 'r',
                         'esperado': -1,
                         'tipo': 'int'},
                        {'caso': 'buffer de 16 bytes',
                         'codigo': 'char b[16];\nint r = emitir_funcion("main", 7, b, sizeof b);',
                         'var': 'r',
                         'esperado': -1,
                         'tipo': 'int'}],
              'criterios': ['El buffer contiene .text, .globl <nombre> y la etiqueta <nombre>: antes del prólogo.',
                            'El cuerpo carga el retorno en %rax y el epílogo usa leave y ret.',
                            'Los seis casos del harness salen OK y el programa termina con código de salida 0.']}},
 38: {'tema': 'Enlace (Linking) y Creación de Binarios Ejecutables ELF',
      'unidad': 'Unidad 4: Código Objeto y Backend',
      'teoria_principal': {'titulo': 'Ensamblado con AS y Enlace con GCC / LD',
                           'lead': "El archivo ensamblador '.s' se convierte en código máquina reubicable '.o' y finalmente en un "
                                   'ejecutable ELF.',
                           'tarjetas': [('01. El Ensamblador (as)',
                                         "Traduce las instrucciones mnemónicas ('movq', 'addq') a bytes de código máquina hexadecimales.",
                                         'Genera un archivo objeto en formato ELF (Executable and Linkable Format) con símbolos no '
                                         'resueltos.'),
                                        ('02. El Enlazador (Linker / ld)',
                                         "Resuelve direcciones de funciones externas ('printf', 'malloc', 'exit') y conecta el código de "
                                         'inicio de C (crt1.o).',
                                         'Produce el binario ejecutable final autónomo.'),
                                        ('03. Invocación desde GCC',
                                         "El comando 'gcc salida.s -o binario_final' coordina automáticamente el ensamblado y enlace.",
                                         "Incluye las rutas de búsqueda de bibliotecas estándar sin necesidad de llamar a 'ld' "
                                         'manualmente.')]},
      'arquitectura_memoria': {'titulo': 'Estructura del Binario ELF en Linux',
                               'descripcion': 'Segmentos de memoria cargados por el núcleo del sistema operativo:',
                               'tarjetas': [('Segmentos ELF',
                                             'Segmento de Texto (.text, solo lectura/ejecución), Datos (.data/.rodata, lectura/escritura) '
                                             'y Pila (Stack).',
                                             'El cargador de Linux (ELF Loader) mapea estos segmentos en el espacio de direcciones '
                                             'virtuales.'),
                                            ('Código de Salida ($?)',
                                             "El valor devuelto por 'main()' en RAX se pasa al sistema operativo como exit code del "
                                             'proceso.',
                                             "Verificable en consola mediante 'echo $?'.")]},
      'casos_borde': {'titulo': 'Puntos de Falla en el Enlace',
                      'items': ["Error 'undefined reference to main': no declarar el punto de entrada global.",
                                'Incompatibilidad de arquitectura: intentar compilar código de 32 bits en modo de 64 bits sin banderas '
                                'multilib.',
                                "Permisos de ejecución no asignados en el binario resultante ('chmod +x')."]},
      'contexto': {'pregunta': '¿Qué ocurre entre el archivo .s y el programa que finalmente corre en Linux?',
                   'objetivo': 'Seguir el recorrido as, .o, ld/gcc, ELF y comprobar dos resultados observables: símbolos sin resolver y el '
                               'código de salida que ve el shell.',
                   'por_que': 'Un compilador no termina cuando escribe ensamblador: termina cuando el binario se ejecuta. El enlazador '
                              'conecta tu call printf con la biblioteca real y tu main con crt1.o; si falta un símbolo, no hay binario. '
                              'Además, el $? que revisa el script de pruebas no es el return completo de main, sino su byte bajo, algo que '
                              'confunde a cualquiera que audita.',
                   'conceptos': [('Archivo objeto',
                                  'El .o que produce as: instrucciones máquina más una tabla de símbolos que aún puede tener referencias '
                                  'pendientes.',
                                  'Como una mudanza a medio hacer: las cajas están cerradas pero algunas llevan la etiqueta de dirección '
                                  'desconocida.'),
                                 ('Símbolo indefinido',
                                  'Un nombre que el .o usa pero no define, como printf o malloc, y que el enlazador debe resolver.',
                                  'Como una llamada a un proveedor que todavía no está en tu agenda: hay que buscarlo antes de usarlo.'),
                                 ('ELF',
                                  'El formato de archivo que Linux reconoce para ejecutables y objetos; declara secciones, símbolos y '
                                  'puntos de entrada.',
                                  'Como el pasaporte de un programa: sin él, el sistema no lo deja entrar.'),
                                 ('Código de salida',
                                  'El byte bajo del valor que main devuelve; el shell lo expone en $?.',
                                  'Como el resumen de una factura: ves el total redondeado, no el detalle completo de cada centavo.')],
                   'resultado': 'Dos funciones: una que predice el $? de un main y otra que cuenta los símbolos que el enlazador todavía '
                                'debe resolver.'},
      'lab': {'reto': 'Llamada a ensamblador as y enlazador gcc',
              'entregable': 'tu implementación de codigo_salida() y simbolos_sin_resolver() en artesano_sesion38_c.c, el harness en verde '
                            'y la bitácora en auditorias/auditoria_sesion38.md',
              'explicacion': 'Recibes un valor de retorno de main o una tabla de símbolos con marca :U o :T; devuelves el código de salida '
                             'que verá el shell o cuántos símbolos siguen indefinidos.',
              'reglas': ['El código de salida es retorno & 0xFF: los valores negativos y los mayores que 255 se recortan.',
                         'En la tabla, cada símbolo es un token separado por espacios y termina en :U (indefinido) o :T (definido).',
                         'Una tabla vacía no tiene símbolos indefinidos; un token que no termina en :U tampoco se cuenta.'],
              'api': {'header': 'api_sesion38.h',
                      'decls': ['int codigo_salida(int retorno_main);', 'int simbolos_sin_resolver(const char *tabla);']},
              'stub': 'int codigo_salida(int retorno_main) {\n'
                      '    (void)retorno_main; /* TODO: recortar al byte bajo del proceso */\n'
                      '    return 0;\n'
                      '}\n'
                      '\n'
                      'int simbolos_sin_resolver(const char *tabla) {\n'
                      '    (void)tabla; /* TODO: contar los tokens terminados en :U */\n'
                      '    return 0;\n'
                      '}',
              'casos': [{'caso': 'codigo_salida(42)', 'codigo': 'int r = codigo_salida(42);', 'var': 'r', 'esperado': 42, 'tipo': 'int'},
                        {'caso': 'codigo_salida(256)', 'codigo': 'int r = codigo_salida(256);', 'var': 'r', 'esperado': 0, 'tipo': 'int'},
                        {'caso': 'codigo_salida(-1)', 'codigo': 'int r = codigo_salida(-1);', 'var': 'r', 'esperado': 255, 'tipo': 'int'},
                        {'caso': 'simbolos_sin_resolver("printf:U malloc:U main:T")',
                         'codigo': 'int r = simbolos_sin_resolver("printf:U malloc:U main:T");',
                         'var': 'r',
                         'esperado': 2,
                         'tipo': 'int'},
                        {'caso': 'simbolos_sin_resolver("")',
                         'codigo': 'int r = simbolos_sin_resolver("");',
                         'var': 'r',
                         'esperado': 0,
                         'tipo': 'int'},
                        {'caso': 'simbolos_sin_resolver("main:T")',
                         'codigo': 'int r = simbolos_sin_resolver("main:T");',
                         'var': 'r',
                         'esperado': 0,
                         'tipo': 'int'}],
              'criterios': ['codigo_salida reproduce el recorte a 8 bits que hace el sistema operativo con el retorno de main.',
                            'simbolos_sin_resolver cuenta solo los tokens terminados en :U y tolera cadenas vacías.',
                            'Los seis casos del harness salen OK y el programa termina con código de salida 0.']}},
 39: {'tema': 'Auditoría de Rendimiento y Fugas de Memoria en el Compilador',
      'unidad': 'Unidad 4: Código Objeto y Backend',
      'teoria_principal': {'titulo': 'Perfilado de Rendimiento y Análisis Estático con Valgrind',
                           'lead': 'Un compilador de calidad industrial debe ser rápido, consumir memoria constante y no sufrir fugas en '
                                   'el Heap.',
                           'tarjetas': [('01. Auditoría con Valgrind (Memcheck)',
                                         'Herramienta de instrumentación dinámica que detecta lecturas de memoria no inicializada y memory '
                                         'leaks.',
                                         "Verifica que cada 'malloc' de tokens, nodos AST y cuádruplos tenga su correspondiente 'free'."),
                                        ('02. Perfilado de Tiempo de Compilación',
                                         'Medición de tiempo consumido en cada pase: frontend, optimización y backend.',
                                         'Garantiza que la complejidad global del compilador sea lineal O(n) respecto al tamaño del código '
                                         'fuente.'),
                                        ('03. Pruebas de Estrés Masivas',
                                         'Compilación de programas fuente extensos (>1,000 líneas de código con funciones anidadas).',
                                         'Comprueba que la memoria del compilador se mantenga acotada y estable.')]},
      'arquitectura_memoria': {'titulo': 'Patrón Arena Allocator para Compiladores Rápidos',
                               'descripcion': 'Técnica industrial de asignación en bloque:',
                               'tarjetas': [('Asignador de Arena',
                                             "En lugar de miles de 'malloc' individuales, se reserva un bloque grande continuo en Heap.",
                                             'Al terminar la compilación, se libera toda la arena de un solo golpe, eliminando fugas y '
                                             'acelerando la ejecución.'),
                                            ('Cero Fugas (Zero Leaks)',
                                             "El reporte de Valgrind debe certificar: 'All heap blocks were freed -- no leaks are "
                                             "possible'.",
                                             'Requisito indispensable para la acreditación técnica final.')]},
      'casos_borde': {'titulo': 'Antipatrones en Calidad del Compilador',
                      'items': ['Fugas acumulativas en la tabla de símbolos al compilar múltiples archivos en serie.',
                                'Punteros colgantes tras la liberación de cuádruplos optimizados.',
                                'Degradación cuadrática O(n^2) en el tiempo de búsqueda de símbolos en tablas de hash mal dimensionadas.']},
      'contexto': {'pregunta': '¿Cómo se demuestra que el compilador no se está comiendo la memoria ni volviéndose lento?',
                   'objetivo': 'Medir dos síntomas de calidad del backend: cuántos bloques de arena consume un lote de objetos y cuántas '
                               'reservas quedan sin liberar tras una compilación.',
                   'por_que': 'Un compilador que funciona en el programa de prueba pero filtra memoria se cae al compilar el siguiente '
                              'archivo. Valgrind y los contadores de arena convierten la impresión de que todo va bien en un número que se '
                              'puede exigir en la entrega. Sin esa medición no hay forma de saber si el Hito 4 es sólido o solo pasó una '
                              'vez.',
                   'conceptos': [('Fuga de memoria',
                                  'Una reserva de heap que ya no tiene puntero para liberarse y que el proceso no puede reutilizar.',
                                  'Como una maleta que dejas en la cinta del aeropuerto y nadie reclama: ocupa espacio para siempre.'),
                                 ('Arena',
                                  'Un bloque grande de memoria del que se reparten objetos pequeños sin llamar a malloc por cada uno.',
                                  'Como una hoja de papel que divides en cupones en lugar de pedir un papel nuevo por cupón.'),
                                 ('Cero fugas',
                                  'El estado en el que toda reserva hecha por el compilador fue liberada antes de terminar.',
                                  'Como dejar la cocina como la encontraste: sin platos sucios ni sobras fuera del refrigerador.'),
                                 ('Complejidad O(n)',
                                  'Tiempo de ejecución que crece proporcionalmente al tamaño del programa de entrada.',
                                  'Como recorrer una fila de personas una sola vez: el doble de gente cuesta el doble, no el cuádruple.')],
                   'resultado': 'Un medidor de bloques de arena y un contador de fugas a partir de una bitácora de reservas y '
                                'liberaciones.'},
      'lab': {'reto': 'Inspección de tiempos y fugas de memoria',
              'entregable': 'tu implementación de bloques_arena() y fugas_en_log() en artesano_sesion39_c.c, el harness en verde y la '
                            'bitácora en auditorias/auditoria_sesion39.md',
              'explicacion': 'Recibes un lote de objetos con su tamaño y el tamaño de bloque de la arena, o una bitácora de eventos m/f; '
                             'devuelves cuántos bloques hacen falta o cuántas reservas quedaron vivas.',
              'reglas': ['Cada bloque de arena se llena antes de pedir el siguiente; se reserva el bloque completo aunque sobre espacio.',
                         'La bitácora usa tokens separados por espacios: m reserva, f libera; cualquier otro token es inválido.',
                         'Si hay más liberaciones que reservas o un token inválido, la bitácora es inconsistente y se responde -1.'],
              'api': {'header': 'api_sesion39.h',
                      'decls': ['int bloques_arena(int objetos, int tamano, int bloque);', 'int fugas_en_log(const char *log);']},
              'stub': 'int bloques_arena(int objetos, int tamano, int bloque) {\n'
                      '    (void)objetos;\n'
                      '    (void)tamano;\n'
                      '    (void)bloque; /* TODO: cuantos bloques completos hacen falta */\n'
                      '    return 0;\n'
                      '}\n'
                      '\n'
                      'int fugas_en_log(const char *log) {\n'
                      '    (void)log; /* TODO: contar m menos f, rechazando lo inconsistente */\n'
                      '    return 0;\n'
                      '}',
              'casos': [{'caso': 'bloques_arena(1000, 32, 4096)',
                         'codigo': 'int r = bloques_arena(1000, 32, 4096);',
                         'var': 'r',
                         'esperado': 8,
                         'tipo': 'int'},
                        {'caso': 'bloques_arena(10, 32, 1024)',
                         'codigo': 'int r = bloques_arena(10, 32, 1024);',
                         'var': 'r',
                         'esperado': 1,
                         'tipo': 'int'},
                        {'caso': 'bloques_arena(0, 32, 4096)',
                         'codigo': 'int r = bloques_arena(0, 32, 4096);',
                         'var': 'r',
                         'esperado': 0,
                         'tipo': 'int'},
                        {'caso': 'fugas_en_log("m f")', 'codigo': 'int r = fugas_en_log("m f");', 'var': 'r', 'esperado': 0, 'tipo': 'int'},
                        {'caso': 'fugas_en_log("m m f")',
                         'codigo': 'int r = fugas_en_log("m m f");',
                         'var': 'r',
                         'esperado': 1,
                         'tipo': 'int'},
                        {'caso': 'fugas_en_log("f")', 'codigo': 'int r = fugas_en_log("f");', 'var': 'r', 'esperado': -1, 'tipo': 'int'}],
              'criterios': ['bloques_arena redondea hacia arriba y no reserva bloques cuando no hay objetos.',
                            'fugas_en_log distingue una bitácora equilibrada de una con reservas vivas o liberaciones de más.',
                            'Los seis casos del harness salen OK y el programa termina con código de salida 0.']}},
 40: {'tema': 'Hito 4: Demostración Final del Compilador End-to-End',
      'unidad': 'Unidad 4: Código Objeto y Backend',
      'teoria_principal': {'titulo': 'Evaluación Integradora y Demostración del Compilador',
                           'lead': 'Culminación del curso. Demostración práctica de un compilador modular completamente funcional que '
                                   'traduce código de alto nivel a binarios ELF ejecutables.',
                           'tarjetas': [('01. Suite de Pruebas de Acreditación',
                                         'Batería de 10 programas de prueba completos que evalúan todas las características del lenguaje.',
                                         'Abarca: expresiones aritméticas, variables globales/locales, control if/else, ciclos while, '
                                         'funciones recursivas y arreglos.'),
                                        ('02. Reporte Técnico de Arquitectura',
                                         "Documento en 'proyecto_integrador/docs/' que detalla las estructuras de datos, gramática, "
                                         'decisiones de diseño y análisis de complejidad.',
                                         'Constituye la evidencia formal de ingeniería del estudiante.'),
                                        ('03. Entrega Final y Release en GitHub',
                                         "Etiquetado formal de la versión definitiva en el repositorio: 'git tag v1.0-final'.",
                                         'Concluye el 30% del Proyecto Integrador y la acreditación final del curso.')]},
      'arquitectura_memoria': {'titulo': 'Verificación del Binario Resultante',
                               'descripcion': 'Criterio de éxito: el ejecutable generado produce los resultados correctos de forma nativa:',
                               'tarjetas': [('Ejecución Nativa',
                                             "'./compilador programa.c -o programa && ./programa'.",
                                             'El binario corre directamente en la CPU x86-64 sin intérpretes ni dependencias intermedias.'),
                                            ('Comprobación de Salida',
                                             'Los resultados emitidos por el programa generado coinciden exactamente con los oráculos de '
                                             'prueba.',
                                             'Certifica la corrección semántica de todo el pipeline del compilador.')]},
      'casos_borde': {'titulo': 'Criterios de Acreditación del Hito 4',
                      'items': ['El compilador debe compilar y ejecutar exitosamente los 10 programas de prueba sin errores de '
                                'segmentación.',
                                "El código fuente del compilador debe compilar limpiamente con '-Wall -Wextra' sin advertencias.",
                                'La bitácora de auditoría y la documentación de arquitectura deben estar completas en GitHub.']},
      'contexto': {'pregunta': '¿Puede el compilador que construiste llevar un programa del texto fuente hasta un resultado correcto sin '
                               'intervención manual?',
                   'objetivo': 'Cerrar el pipeline ejecutando un mini lenguaje de asignaciones y return de principio a fin, y demostrar '
                               'que las decisiones de las nueve sesiones anteriores encajan en un solo flujo.',
                   'por_que': 'El Hito 4 no se aprueba con piezas sueltas: se aprueba cuando una entrada arbitraria del lenguaje produce '
                              'la salida que el oráculo espera. Esta función concentra el recorrido completo (parseo, tabla de variables, '
                              'evaluación y retorno) en una sola llamada, que es exactamente lo que hace el binario final del compilador.',
                   'conceptos': [('Pipeline',
                                  'La cadena de pases donde la salida de uno es la entrada del siguiente, del fuente al resultado.',
                                  'Como una línea de montaje: cada estación recibe la pieza de la anterior y la entrega lista a la '
                                  'siguiente.'),
                                 ('Tabla de variables',
                                  'El mapa que asocia cada nombre del programa con su valor o su ubicación durante la ejecución.',
                                  'Como el directorio telefónico de la oficina: buscas por nombre y obtienes el número que necesitas.'),
                                 ('Sentencia return',
                                  'La instrucción que termina la ejecución de una función y entrega un valor al llamador.',
                                  'Como el cierre de una carta: lo que pones después ya no se lee.'),
                                 ('Oráculo de prueba',
                                  'El resultado que se considera correcto y contra el que se compara lo que produce el compilador.',
                                  'Como la respuesta al final del libro de ejercicios: sirve para saber si tu procedimiento llegó bien.')],
                   'resultado': 'Una función ejecutar_programa que interpreta asignaciones y return de un mini lenguaje, integrando todas '
                                'las fases del compilador en una sola llamada.'},
      'lab': {'reto': 'Compilador Modular Funcional Completo',
              'entregable': 'tu implementación de ejecutar_programa() en artesano_sesion40_c.c, el harness en verde y la bitácora en '
                            'auditorias/auditoria_sesion40.md',
              'explicacion': 'El ayudante de lectura (nombres, números, variables) ya viene resuelto: solo escribes ejecutar_programa, que '
                             'recorre las sentencias, guarda los valores y resuelve el return. Cada expresión usa a lo sumo un operador '
                             'entre dos átomos.',
              'reglas': ['Las variables no asignadas valen cero y conservan su valor hasta el final.',
                         'Solo se admiten +, - y *, aplicados una vez por expresión.',
                         'Si no hay return o el programa está vacío, el resultado es cero; NULL también devuelve cero.'],
              'api': {'header': 'api_sesion40.h',
                      'tipos': ['typedef struct { char nombre[16]; long valor; } Variable;'],
                      'decls': ['long ejecutar_programa(const char *fuente);']},
              'stub': '#include <ctype.h>\n'
                      '\n'
                      '/* Estos ayudantes ya estan resueltos: usalos tal cual. */\n'
                      'const char *saltar(const char *p) {\n'
                      "    while (*p == ' ' || *p == '\\t' || *p == '\\n' || *p == '\\r') p++;\n"
                      '    return p;\n'
                      '}\n'
                      '\n'
                      'int es_letra(char c) {\n'
                      "    return isalpha((unsigned char)c) || c == '_';\n"
                      '}\n'
                      '\n'
                      'int es_alnum(char c) {\n'
                      "    return isalnum((unsigned char)c) || c == '_';\n"
                      '}\n'
                      '\n'
                      'const char *leer_nombre(const char *p, char *destino, int cap) {\n'
                      '    int len = 0;\n'
                      '    while (es_alnum(*p)) {\n'
                      '        if (len < cap - 1) destino[len++] = *p;\n'
                      '        p++;\n'
                      '    }\n'
                      "    destino[len] = '\\0';\n"
                      '    return p;\n'
                      '}\n'
                      '\n'
                      'long buscar(const Variable *vars, int n, const char *nombre) {\n'
                      '    for (int i = 0; i < n; i++) {\n'
                      '        if (strcmp(vars[i].nombre, nombre) == 0) return vars[i].valor;\n'
                      '    }\n'
                      '    return 0;\n'
                      '}\n'
                      '\n'
                      'const char *leer_atomo(const char *p, const Variable *vars, int n, long *valor) {\n'
                      '    p = saltar(p);\n'
                      '    int signo = 1;\n'
                      "    if (*p == '+' || *p == '-') {\n"
                      "        if (*p == '-') signo = -1;\n"
                      '        p++;\n'
                      '        p = saltar(p);\n'
                      '    }\n'
                      "    if (*p >= '0' && *p <= '9') {\n"
                      '        long v = 0;\n'
                      "        while (*p >= '0' && *p <= '9') {\n"
                      "            v = v * 10 + (*p - '0');\n"
                      '            p++;\n'
                      '        }\n'
                      '        *valor = signo * v;\n'
                      '        return p;\n'
                      '    }\n'
                      '    if (es_letra(*p)) {\n'
                      '        char nombre[16];\n'
                      '        p = leer_nombre(p, nombre, 16);\n'
                      '        *valor = signo * buscar(vars, n, nombre);\n'
                      '        return p;\n'
                      '    }\n'
                      '    *valor = 0;\n'
                      '    return p;\n'
                      '}\n'
                      '\n'
                      'long evaluar(const char *p, const Variable *vars, int n, const char **fin) {\n'
                      '    long a = 0;\n'
                      '    long b = 0;\n'
                      '    p = leer_atomo(p, vars, n, &a);\n'
                      '    p = saltar(p);\n'
                      "    if (*p == '+' || *p == '-' || *p == '*') {\n"
                      '        char op = *p;\n'
                      '        p++;\n'
                      '        p = leer_atomo(p, vars, n, &b);\n'
                      "        if (op == '+') a += b;\n"
                      "        else if (op == '-') a -= b;\n"
                      '        else a *= b;\n'
                      '    }\n'
                      '    *fin = p;\n'
                      '    return a;\n'
                      '}\n'
                      '\n'
                      'long ejecutar_programa(const char *fuente) {\n'
                      '    /* TODO: recorre las sentencias separadas por \';\', atiende "return"\n'
                      '       y guarda x = expresion en la tabla de variables (maximo 16). */\n'
                      '    (void)fuente;\n'
                      '    return 0;\n'
                      '}\n',
              'casos': [{'caso': 'x = 5; return x + 3',
                         'codigo': 'long r = ejecutar_programa("x = 5; return x + 3");',
                         'var': 'r',
                         'esperado': 8,
                         'tipo': 'int'},
                        {'caso': 'x = 2; y = x * 3; return y - 1',
                         'codigo': 'long r = ejecutar_programa("x = 2; y = x * 3; return y - 1");',
                         'var': 'r',
                         'esperado': 5,
                         'tipo': 'int'},
                        {'caso': 'a = 4; b = a * a; return b',
                         'codigo': 'long r = ejecutar_programa("a = 4; b = a * a; return b");',
                         'var': 'r',
                         'esperado': 16,
                         'tipo': 'int'},
                        {'caso': 'return 7', 'codigo': 'long r = ejecutar_programa("return 7");', 'var': 'r', 'esperado': 7, 'tipo': 'int'},
                        {'caso': 'x = 0; return x',
                         'codigo': 'long r = ejecutar_programa("x = 0; return x");',
                         'var': 'r',
                         'esperado': 0,
                         'tipo': 'int'},
                        {'caso': 'return z',
                         'codigo': 'long r = ejecutar_programa("return z");',
                         'var': 'r',
                         'esperado': 0,
                         'tipo': 'int'}],
              'criterios': ['El recorrido respeta el orden de las asignaciones y resuelve variables ya definidas.',
                            'El return devuelve el valor de la expresión y termina el programa.',
                            'Las variables no asignadas valen cero y el caso NULL devuelve cero.']}}}
