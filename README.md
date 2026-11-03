# Lenguajes y Autómatas II (SCD-1016)

Repositorio oficial del curso de **Lenguajes y Autómatas II** del Tecnológico Nacional de México / Instituto Tecnológico de Cancún.

**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)

---

## 🚀 Flujo de Trabajo en la Nube (100% en Navegador)
1. Realiza un **Fork** de este repositorio a tu cuenta personal de GitHub.
2. Abre la sesión correspondiente con el botón **Open in Colab**.
3. Sigue el ciclo **El Artesano** $\to$ **El Científico** $\to$ **El Auditor** hasta ver `TODO EN VERDE` en el *harness*.
4. Copia la plantilla de `plantillas/auditoria_sesionXX.md` a `auditorias/auditoria_sesionXX.md` en tu Fork, adjunta la salida del *harness* y realiza el commit.

---

## 🧭 Cómo está armada cada sesión

Cada presentación sigue el mismo recorrido de 8 láminas, para que siempre sepas dónde estás y a dónde vamos:

1. **Portada** — tema, pregunta guía y objetivo de la sesión.
2. **Conceptos básicos** — las ideas en lenguaje llano y con analogías, antes de los tecnicismos.
3. **¿Dónde estamos y a dónde vamos?** — mapa de las 4 unidades y los 4 hitos.
4. **Fundamentos teóricos**.
5. **Arquitectura de memoria**.
6. **Casos borde y antipatrones**.
7. **Lo que vas a construir hoy** — entregable, reglas, criterios y la salida literal del *harness*.
8. **Dinámica y entrega**.

Cada laboratorio declara, antes de pedir una sola línea de código:

* **Qué vas a construir** (operativo, sin repetir la teoría de la presentación).
* **El contrato exacto**: `api_sesionNN.h` con la firma que tu implementación debe respetar.
* **La tabla de casos** y **la salida literal** que el *harness* debe producir.
* **Los criterios de aceptación**.

El *harness* no aprueba por sí solo: compila tu archivo con `-Wall -Wextra -Werror`, ejecuta cada caso y termina con código 1 si algo falla. Mientras no implementes, la salida es roja.

---

## 🧰 ¿No te acuerdas de C?

La **[guía de C](docs/guia-c.md)** reúne los elementos del lenguaje que usan los laboratorios: punteros, `struct`, memoria dinámica, arreglos 2D, recursión, archivos y los errores de gcc más frecuentes. Incluye un mapa de qué repasar antes de cada una de las 40 sesiones y ejercicios de calentamiento.

---

## 🛠️ Regenerar el material (para el docente)

El contenido vive en los módulos `contenido_teorico_bloqueN.py`; las presentaciones y las libretas se generan desde ahí. No edites los HTML ni los `.ipynb` a mano: se sobrescriben.

```bash
python3 generar_presentaciones.py      # las 40 presentaciones
python3 generar_laboratorios.py        # las 40 libretas
python3 validar_contenido.py           # esquema + compilación de los 40 harness
```

`validar_contenido.py` compila cada *harness* contra su implementación de referencia (guardada en `.referencias/`, una carpeta local que `.gitignore` excluye del repositorio público), exige que la salida coincida con la documentada y comprueba que el esqueleto del estudiante falla. También puedes validar por bloques o por sesión:

```bash
python3 validar_contenido.py --bloque 2
python3 validar_contenido.py --sesion 7 -v
```

---

## 🏗️ Proyecto Integrador Semestral (30%)

**Lenguajito:** un compilador para un lenguaje mínimo de variables enteras, `if/else`, `while` y `print`. Equipos de 3 a 4 personas, un repositorio por equipo y cuatro hitos.

* **Hito 1 (Sesión 10):** léxico, sintaxis y AST de expresiones.
* **Hito 2 (Sesión 20):** sentencias, tabla de símbolos y ámbitos.
* **Hito 3 (Sesión 30):** TAC y optimizaciones.
* **Hito 4 (Sesión 40):** backend x86-64 y binario ELF.

Guía de trabajo, entregas y evaluación: **[guía del proyecto](proyecto_integrador/docs/guia-proyecto.md)**.
Reglas, rúbrica, calendario y definición de terminado: **[PROYECTO.md](PROYECTO.md)**.
El lenguaje y la interfaz de línea de comandos: **[gramática de Lenguajito](proyecto_integrador/docs/gramatica.md)**.
El arranque (Makefile, CLI y pruebas doradas): **[proyecto_integrador/](proyecto_integrador/)**.

---

## 📚 Índice General de las 40 Sesiones

| Sesión | Tema Principal | Presentación | Laboratorio |
| :--- | :--- | :---: | :---: |
| **Sesión 01** | Encuadre, Diagnóstico de Punteros y Metodología IA | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion01.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion01/sesion01_laboratorio.ipynb) |
| **Sesión 02** | Gestión en GitHub Web y Nodos Dinámicos | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion02.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion02/sesion02_laboratorio.ipynb) |
| **Sesión 03** | Google Colab, Mágicos y Flujo de Entrega | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion03.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion03/sesion03_laboratorio.ipynb) |
| **Sesión 04** | Anatomía de un Árbol Sintáctico (AST) | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion04.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion04/sesion04_laboratorio.ipynb) |
| **Sesión 05** | Recorridos del AST y Notación Polaca | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion05.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion05/sesion05_laboratorio.ipynb) |
| **Sesión 06** | Sistema de Tipos Primitivos | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion06.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion06/sesion06_laboratorio.ipynb) |
| **Sesión 07** | Evaluación de Expresiones Aritméticas | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion07.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion07/sesion07_laboratorio.ipynb) |
| **Sesión 08** | Inferencia y Promoción de Tipos | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion08.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion08/sesion08_laboratorio.ipynb) |
| **Sesión 09** | Reporte Formal de Errores Semánticos | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion09.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion09/sesion09_laboratorio.ipynb) |
| **Sesión 10** | Hito 1: Mini-Evaluador de Expresiones | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion10.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion10/sesion10_laboratorio.ipynb) |
| **Sesión 11** | Arquitectura de la Tabla de Símbolos | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion11.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion11/sesion11_laboratorio.ipynb) |
| **Sesión 12** | Atributos de Símbolos y Memoria | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion12.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion12/sesion12_laboratorio.ipynb) |
| **Sesión 13** | Manejo de Ámbitos (Scope Global/Local) | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion13.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion13/sesion13_laboratorio.ipynb) |
| **Sesión 14** | Declaración vs Uso de Variables | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion14.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion14/sesion14_laboratorio.ipynb) |
| **Sesión 15** | Bloques Anidados y Ciclo de Vida | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion15.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion15/sesion15_laboratorio.ipynb) |
| **Sesión 16** | Firmas de Función y Parámetros | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion16.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion16/sesion16_laboratorio.ipynb) |
| **Sesión 17** | Comprobación Semántica de Retornos | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion17.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion17/sesion17_laboratorio.ipynb) |
| **Sesión 18** | Arreglos y Verificación de Límites | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion18.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion18/sesion18_laboratorio.ipynb) |
| **Sesión 19** | Estructuras (struct) y Miembros | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion19.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion19/sesion19_laboratorio.ipynb) |
| **Sesión 20** | Hito 2: Analizador Semántico y Scopes | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion20.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion20/sesion20_laboratorio.ipynb) |
| **Sesión 21** | Fundamentos de Código de 3 Direcciones | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion21.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion21/sesion21_laboratorio.ipynb) |
| **Sesión 22** | Generación de TAC para Expresiones | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion22.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion22/sesion22_laboratorio.ipynb) |
| **Sesión 23** | Etiquetas y Saltos Incondicionales | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion23.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion23/sesion23_laboratorio.ipynb) |
| **Sesión 24** | Control de Flujo: Sentencia if-else | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion24.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion24/sesion24_laboratorio.ipynb) |
| **Sesión 25** | Control de Flujo: Bucles while y for | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion25.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion25/sesion25_laboratorio.ipynb) |
| **Sesión 26** | TAC para Llamadas a Funciones | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion26.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion26/sesion26_laboratorio.ipynb) |
| **Sesión 27** | Indexación de Arreglos en TAC | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion27.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion27/sesion27_laboratorio.ipynb) |
| **Sesión 28** | Optimización: Constant Folding | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion28.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion28/sesion28_laboratorio.ipynb) |
| **Sesión 29** | Optimización: Dead Code Elimination | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion29.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion29/sesion29_laboratorio.ipynb) |
| **Sesión 30** | Hito 3: Generador de TAC End-to-End | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion30.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion30/sesion30_laboratorio.ipynb) |
| **Sesión 31** | Introducción a Ensamblador x86-64 | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion31.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion31/sesion31_laboratorio.ipynb) |
| **Sesión 32** | Asignación Ingenua de Registros | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion32.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion32/sesion32_laboratorio.ipynb) |
| **Sesión 33** | Derramamiento a Memoria (Spilling) | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion33.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion33/sesion33_laboratorio.ipynb) |
| **Sesión 34** | Marco de Pila y Prólogo/Epílogo | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion34.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion34/sesion34_laboratorio.ipynb) |
| **Sesión 35** | Paso de Argumentos por Registro | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion35.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion35/sesion35_laboratorio.ipynb) |
| **Sesión 36** | Traducción de Comparaciones y Saltos | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion36.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion36/sesion36_laboratorio.ipynb) |
| **Sesión 37** | Integración de Pipeline del Compilador | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion37.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion37/sesion37_laboratorio.ipynb) |
| **Sesión 38** | Enlace y Creación de Binarios ELF | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion38.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion38/sesion38_laboratorio.ipynb) |
| **Sesión 39** | Auditoría de Rendimiento y Memoria | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion39.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion39/sesion39_laboratorio.ipynb) |
| **Sesión 40** | Hito 4: Demostración Final del Compilador | [Ver Diapositivas](https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2/presentaciones/sesion40.html) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-lenguajes-automatas-2/blob/main/laboratorios/sesion40/sesion40_laboratorio.ipynb) |

---

## 📋 Criterios de Evaluación
* **40% Laboratorios Diarios:** Cuadernos Colab y bitácoras en GitHub.
* **30% Proyecto Integrador:** Compilador modular funcional (4 hitos).
* **20% Evaluaciones Prácticas:** 4 hitos prácticos de unidad.
* **10% Participación Activa:** Sesiones síncronas en MS Teams.

---
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Tecnológico Nacional de México — Campus Cancún**