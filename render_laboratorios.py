#!/usr/bin/env python3
"""
Plantilla única de las libretas de laboratorio.

Cada libreta empieza declarando qué se va a construir, cuál es el contrato
exacto (cabecera + firma), qué casos evalúa el harness y cuál es la salida
literal que debe aparecer al final. Después vienen las tres fases de la
Tríada Metodológica, con el harness real en la Fase 3.

La teoría NO se repite aquí: vive en la presentación de la sesión.
"""

from __future__ import annotations



from lab_utils import (
    ai_filename,
    ai_stub_source,
    api_filename,
    api_header_source,
    casos_tabla_md,
    expected_output,
    harness_filename,
    harness_source,
    student_filename,
    student_stub_source,
)

REPO = "https://github.com/ijmarquezl/tecnm-lenguajes-automatas-2"
SITIO = "https://ijmarquezl.github.io/tecnm-lenguajes-automatas-2"


def _src(texto: str) -> list[str]:
    return texto.splitlines(keepends=True)


def _md(texto: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": _src(texto)}


def _code(texto: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": _src(texto),
    }


def _fence(texto: str, lenguaje: str = "text") -> str:
    return f"```{lenguaje}\n{texto.rstrip()}\n```"


def render(num: int, data: dict, total: int = 40) -> dict:
    n = f"{num:02d}"
    tema = data["tema"]
    ctx = data["contexto"]
    lab = data["lab"]
    api = lab["api"]
    firma = "\n".join(api["decls"])

    salida = expected_output(num, lab)
    tabla = casos_tabla_md(lab)
    reglas = "\n".join(f"- {r}" for r in lab.get("reglas", []))
    criterios = "\n".join(f"- [ ] {c}" for c in lab["criterios"])

    encabezado = f"""# Lenguajes y Autómatas II (SCD-1016)
## Sesión {n} · {tema}

**Docente:** MCC. Iván Márquez Larios (`ijmarquezl`) · **Repositorio maestro:** {REPO}

---

> **Pregunta guía:** {ctx["pregunta"]}
>
> **Objetivo de la sesión:** {ctx["objetivo"]}

**Entregable:** {lab["entregable"]}

**Tiempo:** 60 min · **Fases:** Artesano (manual) → Científico (IA con contrato) → Auditor (harness)

> ¿Dudas de C? Consulta la [guía de C]({REPO}/blob/main/docs/guia-c.md) antes de empezar.
"""

    que_construyo = f"""## 1. ¿Qué vas a construir?

{lab["explicacion"]}

Al final de la sesión tendrás: **{ctx["resultado"]}**

Los conceptos y el porqué de esta sesión están en la presentación
([sesión {n}]({SITIO}/presentaciones/sesion{n}.html)). Aquí solo está el trabajo: qué se
recibe, qué debe salir y cómo se comprueba.
"""

    contrato = f"""## 2. El contrato exacto

El archivo `{api["header"]}` declara la interfaz que el harness sabe probar.
Tu implementación **debe** respetar esas firmas; si las cambias, el harness no compila.

{_fence("#include \"" + api["header"] + "\"\n\n" + firma, "c")}

{reglas}

> El harness compila con `-Wall -Wextra -Werror`: una advertencia del compilador cuenta como error.
>
> El harness compila `{harness_filename(num)}` junto con `{student_filename(num)}`
> (o `{ai_filename(num)}`). Por eso tu archivo **no debe tener `main()`**: el `main()`
> es del harness.
"""

    calificacion = f"""## 3. Cómo se califica

### Casos que evalúa el harness

{tabla}

### Salida literal que debes obtener

{_fence(salida)}

Los números entre corchetes son el contador de casos. Mientras algo falle verás
`FALLA` en esa línea, el total será menor y el programa terminará con código de
salida 1.

### Criterios de aceptación

{criterios}
"""

    entorno = """## Paso 0 · Entorno
"""

    entorno_code = """import os

if os.system('which gcc > /dev/null 2>&1') != 0:
    print('⏳ Instalando compilador...')
    !apt-get update -qq && apt-get install -y -qq gcc > /dev/null 2>&1

print('✅ Entorno listo:')
!gcc --version | head -n 1
"""

    fase1 = f"""## Fase 1 · El Artesano (15 min, sin IA)

Escribe a mano la implementación en `{student_filename(num)}`. El archivo ya trae la
firma y un `TODO`: edita el contenido de la celda `%%writefile` que está abajo (o el
archivo en el panel **Archivos** de Colab) y vuelve a ejecutarla para guardar los
cambios. Hazlo sin consultar a la IA. Si te atoras, anota en tu bitácora exactamente
en qué te atoraste; eso también es evidencia.
"""

    fase2 = f"""## Fase 2 · El Científico (10 min)

Redacta el contrato **C-R-E-O** (Contexto, Rol, Especificación, Output) para pedirle
la misma función a la IA, y pega el resultado en la celda de `{ai_filename(num)}`. La
firma debe ser idéntica a la del contrato; si la IA la cambia, corrígela antes de
compilar.
"""

    fase3 = f"""## Fase 3 · El Auditor (10 min)

El harness de abajo **no aprueba nada por sí solo**: ejecuta tu función caso por caso,
la compara contra el valor esperado e imprime `OK` o `FALLA`. Léelo antes de ejecutarlo:
los casos te dicen qué se está midiendo.
"""

    resultado = f"""## Resultado esperado

Si tu implementación es correcta, la última línea del harness será:

{_fence("RESULTADO: " + str(len(lab["casos"])) + "/" + str(len(lab["casos"])) + " pruebas superadas")}

y la celda terminará sin error (código de salida 0). Compara tu salida completa
contra la de la sección 3: debe ser idéntica, línea por línea.
"""

    entrega = f"""## Entrega

1. Copia `plantillas/auditoria_sesion{n}.md` a `auditorias/auditoria_sesion{n}.md` en tu fork.
2. Adjunta la salida del harness (las {len(lab["casos"])} líneas con `OK`).
3. Explica en el reporte crítico qué caso borde omitió la IA y cómo lo detectaste.
4. Haz commit y sincroniza tu fork.

Este laboratorio alimenta el 40% de laboratorios y es la base del Hito correspondiente
del Proyecto Integrador.
"""

    celdas = [
        _md(encabezado),
        _md(que_construyo),
        _md(contrato),
        _md(calificacion),
        _md(entorno),
        _code(entorno_code),
        _md(fase1),
        _code(f"%%writefile {api_filename(num)}\n{api_header_source(num, lab)}"),
        _code(f"%%writefile {student_filename(num)}\n{student_stub_source(num, lab)}"),
        _md(fase2),
        _code(f"%%writefile {ai_filename(num)}\n{ai_stub_source(num)}"),
        _md(fase3),
        _code(f"%%writefile {harness_filename(num)}\n{harness_source(num, lab)}"),
        _code(
            f"!gcc -std=c11 -Wall -Wextra -Werror {harness_filename(num)} "
            f"{student_filename(num)} -o test_artesano && ./test_artesano"
        ),
        _code(
            f"!gcc -std=c11 -Wall -Wextra -Werror {harness_filename(num)} "
            f"{ai_filename(num)} -o test_ia && ./test_ia"
        ),
        _md(resultado),
        _md(entrega),
    ]

    return {
        "cells": celdas,
        "metadata": {
            "language_info": {"name": "python"},
            "kernelspec": {"display_name": "Python 3", "name": "python3"},
            "colab": {"provenance": []},
        },
        "nbformat": 4,
        "nbformat_minor": 2,
    }
