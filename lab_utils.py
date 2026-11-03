#!/usr/bin/env python3
"""
Utilidades compartidas de los laboratorios.

Aquí vive el contrato entre la presentación, la libreta y el harness:

  * `api_header_source`    -> el archivo `api_sesionNN.h` que define la firma.
  * `student_stub_source`  -> el esqueleto que el estudiante debe completar.
  * `ai_stub_source`       -> el archivo donde pegará el código de la IA.
  * `harness_source`       -> el examen automático que imprime OK/FALLA.
  * `expected_output`      -> la salida literal del harness cuando todo pasa.

La misma función `expected_output` alimenta la lámina "Lo que vas a construir
hoy" y la celda de la libreta, y `validar_contenido.py` comprueba que el
harness real produce exactamente ese texto.

Regla de oro: todo lo que el harness imprime es ASCII. Así el ancho de las
columnas (calculado en Python con caracteres) coincide con el de `printf`
(bytes) y la comparación es exacta.
"""

from __future__ import annotations

import unicodedata


# --------------------------------------------------------------------------
# Nombres de archivo por sesión
# --------------------------------------------------------------------------

def _n(num: int) -> str:
    return f"{num:02d}"


def api_filename(num: int) -> str:
    return f"api_sesion{_n(num)}.h"


def student_filename(num: int) -> str:
    return f"artesano_sesion{_n(num)}_c.c"


def ai_filename(num: int) -> str:
    return f"ia_sesion{_n(num)}_c.c"


def harness_filename(num: int) -> str:
    return f"harness_sesion{_n(num)}_c.c"


# --------------------------------------------------------------------------
# Escapado de cadenas C
# --------------------------------------------------------------------------

def c_str(text: str) -> str:
    """Literal de cadena C para usar como *argumento* (no como formato)."""
    out = []
    for ch in text:
        if ch == "\\":
            out.append("\\\\")
        elif ch == '"':
            out.append('\\"')
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\t":
            out.append("\\t")
        else:
            out.append(ch)
    return '"' + "".join(out) + '"'


def c_fmt(text: str) -> str:
    """Literal de cadena C para usar como *formato* de printf (escapa %)."""
    return c_str(text).replace("%", "%%")


# --------------------------------------------------------------------------
# Contrato
# --------------------------------------------------------------------------

def api_guard(num: int) -> str:
    return f"API_SESION{_n(num)}_H"


def api_header_source(num: int, lab: dict) -> str:
    api = lab["api"]
    lineas = [
        f"/* {api['header']} - contrato de la Sesion {_n(num)}",
        f" * {lab['reto']}",
        " *",
        " * Esta cabecera es el contrato: el harness y tu implementacion",
        " * deben incluirla. Si cambias una firma, el harness dejara de compilar.",
        " */",
        f"#ifndef {api_guard(num)}",
        f"#define {api_guard(num)}",
    ]
    if api.get("tipos"):
        lineas.append("")
        lineas.extend(api["tipos"])
    lineas.append("")
    lineas.extend(api["decls"])
    lineas.append("")
    lineas.append(f"#endif /* {api_guard(num)} */")
    return "\n".join(lineas) + "\n"


def student_stub_source(num: int, lab: dict) -> str:
    return (
        f"/* {student_filename(num)} - Fase 1: El Artesano (sin IA)\n"
        f" * {lab['reto']}.\n"
        f" *\n"
        f" * Implementa lo que declara {api_filename(num)}.\n"
        f" * El harness compila este archivo junto con el suyo: no escribas main().\n"
        " */\n"
        f'#include "{api_filename(num)}"\n'
        "#include <stdio.h>\n"
        "#include <string.h>\n"
        "\n"
        f"{lab['stub'].rstrip()}\n"
    )


def ai_stub_source(num: int) -> str:
    return (
        f"/* {ai_filename(num)} - Fase 2: El Cientifico\n"
        " *\n"
        " * Pega aqui el codigo que te devolvio la IA, con la MISMA firma\n"
        f" * que declara {api_filename(num)}. No puede traer main().\n"
        " */\n"
        f'#include "{api_filename(num)}"\n'
        "\n"
        "/* TODO: pega aqui la propuesta de la IA */\n"
    )


# --------------------------------------------------------------------------
# Harness
# --------------------------------------------------------------------------

def _col_caso(texto: str) -> str:
    """Formatea un caso igual que `printf("%-34s", texto)`."""
    return f"{texto:<34}"


def _col_valor(texto: str) -> str:
    """Formatea un valor igual que `printf("%-12s", texto)`."""
    return f"{texto:<12}"


def tabla_encabezado() -> str:
    return f"{'Caso':<34} esperado: {'':<12} obtenido: {'':<12} resultado"


def _ascii(texto: str) -> str:
    """Translitera acentos a ASCII (Inversión -> Inversion)."""
    return (
        unicodedata.normalize("NFKD", texto)
        .encode("ascii", "ignore")
        .decode("ascii")
    )


def caso_largo(caso: dict) -> bool:
    """True si el caso no cabe en la tabla compacta del harness."""
    return len(caso["caso"]) > 34 or len(str(caso["esperado"])) > 12


def harness_titulo(num: int, lab: dict) -> str:
    return f"=== AUDITORIA SESION {_n(num)} - {_ascii(lab['reto'])} ==="


def harness_source(num: int, lab: dict) -> str:
    casos = lab["casos"]
    tiene_str = any(
        c.get("tipo", "str") == "str" and not caso_largo(c) for c in casos
    )
    tiene_str_largo = any(
        c.get("tipo", "str") == "str" and caso_largo(c) for c in casos
    )
    tiene_int = any(c.get("tipo") == "int" for c in casos)

    partes = [
        f"/* {harness_filename(num)} - auditoria automatica de la Sesion {_n(num)}",
        " *",
        " * Compilacion:",
        f" *   gcc -std=c11 -Wall -Wextra -Werror {harness_filename(num)} "
        f"{student_filename(num)} -o test_artesano",
        " *",
        " * El harness NO aprueba nada por si solo: cada linea se calcula",
        " * ejecutando tu implementacion y comparandola contra el valor esperado.",
        " * Si algun caso falla, el programa termina con codigo de salida 1.",
        " */",
        "#include <stdio.h>",
        "#include <string.h>",
        f'#include "{api_filename(num)}"',
        "",
        "static int probadas = 0;",
        "static int fallidas = 0;",
        "",
    ]

    if tiene_str:
        partes += [
            "static void verificar_str(const char *caso, const char *esperado,",
            "                          const char *obtenido) {",
            "    int ok = (obtenido != NULL) && (strcmp(esperado, obtenido) == 0);",
            "    probadas++;",
            "    if (!ok) fallidas++;",
            '    printf("[%2d] %-34s esperado: %-12s obtenido: %-12s %s\\n",',
            '           probadas, caso, esperado, obtenido ? obtenido : "(NULL)",',
            '           ok ? "OK" : "FALLA");',
            "}",
            "",
        ]
    if tiene_str_largo:
        partes += [
            "static void verificar_str_largo(const char *caso, const char *esperado,",
            "                                const char *obtenido) {",
            "    int ok = (obtenido != NULL) && (strcmp(esperado, obtenido) == 0);",
            "    probadas++;",
            "    if (!ok) fallidas++;",
            '    printf("[%2d] %s\\n", probadas, caso);',
            '    printf("     esperado: %s\\n", esperado);',
            '    printf("     obtenido: %s\\n", obtenido ? obtenido : "(NULL)");',
            '    printf("     -> %s\\n", ok ? "OK" : "FALLA");',
            "}",
            "",
        ]
    if tiene_int:
        partes += [
            "static void verificar_int(const char *caso, long esperado, long obtenido) {",
            "    int ok = (esperado == obtenido);",
            "    probadas++;",
            "    if (!ok) fallidas++;",
            '    printf("[%2d] %-34s esperado: %-12ld obtenido: %-12ld %s\\n",',
            '           probadas, caso, esperado, obtenido, ok ? "OK" : "FALLA");',
            "}",
            "",
        ]

    partes += [
        "int main(void) {",
        f"    printf({c_fmt(harness_titulo(num, lab) + chr(10))});",
        f"    printf({c_fmt(tabla_encabezado() + chr(10))});",
        "",
    ]

    for caso in casos:
        tipo = caso.get("tipo", "str")
        codigo = " ".join(linea.strip() for linea in caso["codigo"].splitlines())
        if tipo == "int":
            partes.append(
                f"    {{ {codigo} verificar_int({c_str(caso['caso'])}, "
                f"(long)({caso['esperado']}), (long)({caso['var']})); }}"
            )
        elif caso_largo(caso):
            partes.append(
                f"    {{ {codigo} verificar_str_largo({c_str(caso['caso'])}, "
                f"{c_str(str(caso['esperado']))}, {caso['var']}); }}"
            )
        else:
            partes.append(
                f"    {{ {codigo} verificar_str({c_str(caso['caso'])}, "
                f"{c_str(str(caso['esperado']))}, {caso['var']}); }}"
            )

    partes += [
        "",
        '    printf("\\nRESULTADO: %d/%d pruebas superadas\\n",',
        "           probadas - fallidas, probadas);",
        "    if (fallidas != 0) {",
        '        printf("Aun hay %d caso(s) sin resolver. Revisa tu implementacion.\\n",',
        "               fallidas);",
        "        return 1;",
        "    }",
        f'    printf({c_fmt(f"TODO EN VERDE. Documenta tu auditoria en auditorias/auditoria_sesion{_n(num)}.md")} "\\n");',
        "    return 0;",
        "}",
    ]
    return "\n".join(partes) + "\n"


# --------------------------------------------------------------------------
# Salida esperada (todo en verde)
# --------------------------------------------------------------------------

def expected_output(num: int, lab: dict) -> str:
    """Texto exacto que imprime el harness cuando los casos pasan."""
    lineas = [harness_titulo(num, lab), tabla_encabezado()]
    total = len(lab["casos"])
    for i, caso in enumerate(lab["casos"], start=1):
        tipo = caso.get("tipo", "str")
        esperado = str(caso["esperado"])
        if tipo == "int":
            valor = f"{esperado:<12}"
        else:
            valor = _col_valor(esperado)
        if tipo == "str" and caso_largo(caso):
            lineas.extend([
                f"[{i:2d}] {caso['caso']}",
                f"     esperado: {esperado}",
                f"     obtenido: {esperado}",
                "     -> OK",
            ])
        else:
            lineas.append(
                f"[{i:2d}] {_col_caso(caso['caso'])} esperado: {valor} "
                f"obtenido: {valor} OK"
            )
    lineas.append("")
    lineas.append(f"RESULTADO: {total}/{total} pruebas superadas")
    lineas.append(
        f"TODO EN VERDE. Documenta tu auditoria en "
        f"auditorias/auditoria_sesion{_n(num)}.md"
    )
    return "\n".join(lineas) + "\n"


# --------------------------------------------------------------------------
# Tabla de casos para la libreta
# --------------------------------------------------------------------------

def casos_tabla_md(lab: dict) -> str:
    lineas = ["| # | Caso | Resultado esperado |", "| :-: | :--- | :--- |"]
    for i, caso in enumerate(lab["casos"], start=1):
        esperado = caso["esperado"]
        if caso.get("tipo", "str") == "int":
            esperado = str(esperado)
        else:
            esperado = f"`{esperado}`" if esperado != "" else "`(cadena vacía)`"
        lineas.append(f"| {i} | `{caso['caso']}` | {esperado} |")
    return "\n".join(lineas)
