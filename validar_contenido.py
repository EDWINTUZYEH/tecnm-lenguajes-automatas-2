#!/usr/bin/env python3
"""
Valida el contenido de las 40 sesiones y comprueba que cada harness es real.

Para cada sesión:

  1. Revisa que el esquema de `contexto` y `lab` esté completo.
  2. Genera la cabecera, el harness y el esqueleto del estudiante.
  3. Compila el harness contra la implementación de referencia que esté en
     `.referencias/sesionNN_c.c` (esa carpeta NO se publica: contiene las
     soluciones).
  4. Ejecuta el harness y exige salida idéntica a la documentada en la libreta.
  5. Compila el harness contra el esqueleto (debe compilar) y lo ejecuta
     (debe fallar: no hay verde gratis).

Uso:
    python3 validar_contenido.py                 # todo
    python3 validar_contenido.py --bloque 1      # solo sesiones 01-10
    python3 validar_contenido.py --sesion 1 -v   # una sesión, con detalle
    python3 validar_contenido.py --sin-compilar  # solo esquema
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile

from contenido_teorico_bloque1 import TEORIA_BLOQUE_1
from contenido_teorico_bloque2 import TEORIA_BLOQUE_2
from contenido_teorico_bloque3 import TEORIA_BLOQUE_3
from contenido_teorico_bloque4 import TEORIA_BLOQUE_4
from lab_utils import (
    api_filename,
    api_header_source,
    expected_output,
    harness_filename,
    harness_source,
    student_filename,
    student_stub_source,
)

SESIONES = {
    **TEORIA_BLOQUE_1,
    **TEORIA_BLOQUE_2,
    **TEORIA_BLOQUE_3,
    **TEORIA_BLOQUE_4,
}

REFERENCIAS = ".referencias"


class ErrorValidacion(Exception):
    pass


def _esquema(num: int, data: dict) -> None:
    ctx = data.get("contexto")
    lab = data.get("lab")
    if not isinstance(ctx, dict):
        raise ErrorValidacion("falta 'contexto'")
    if not isinstance(lab, dict):
        raise ErrorValidacion("falta 'lab'")

    for clave in ("pregunta", "objetivo", "por_que", "resultado"):
        if not isinstance(ctx.get(clave), str) or len(ctx[clave]) < 20:
            raise ErrorValidacion(f"contexto['{clave}'] ausente o demasiado corto")
    if not ctx["pregunta"].strip().startswith("¿"):
        raise ErrorValidacion("contexto['pregunta'] debe ser una pregunta (empezar con ¿)")

    conceptos = ctx.get("conceptos")
    if not isinstance(conceptos, list) or not (3 <= len(conceptos) <= 4):
        raise ErrorValidacion("contexto['conceptos'] debe tener 3 o 4 entradas")
    for c in conceptos:
        if not (isinstance(c, tuple) and len(c) == 3 and all(isinstance(x, str) and x for x in c)):
            raise ErrorValidacion(f"concepto mal formado: {c!r}")
        termino, definicion, analogia = c
        if len(termino) < 3:
            raise ErrorValidacion(f"término demasiado corto: {termino!r}")
        if len(definicion) < 20 or len(analogia) < 20:
            raise ErrorValidacion(f"definición o analogía demasiado corta: {c!r}")

    for clave in ("reto", "entregable", "explicacion", "stub"):
        if not isinstance(lab.get(clave), str) or len(lab[clave]) < 10:
            raise ErrorValidacion(f"lab['{clave}'] ausente o demasiado corto")

    api = lab.get("api")
    if not isinstance(api, dict):
        raise ErrorValidacion("falta lab['api']")
    if api.get("header") != api_filename(num):
        raise ErrorValidacion(f"lab['api']['header'] debe ser {api_filename(num)}")
    if not api.get("decls") or not all(isinstance(d, str) for d in api["decls"]):
        raise ErrorValidacion("lab['api']['decls'] debe ser una lista de firmas")
    for tipo in api.get("tipos", []):
        if "\n" in tipo:
            raise ErrorValidacion("los tipos de la cabecera deben ser una línea cada uno")

    casos = lab.get("casos")
    if not isinstance(casos, list) or len(casos) < 3:
        raise ErrorValidacion("lab['casos'] debe tener al menos 3 casos")
    for i, caso in enumerate(casos, start=1):
        for clave in ("caso", "codigo", "var", "esperado"):
            if clave not in caso:
                raise ErrorValidacion(f"caso {i}: falta '{clave}'")
        if caso.get("tipo", "str") not in ("str", "int"):
            raise ErrorValidacion(f"caso {i}: tipo inválido")
        if not caso["caso"].isascii() or not str(caso["esperado"]).isascii():
            raise ErrorValidacion(f"caso {i}: 'caso' y 'esperado' deben ser ASCII")

    if len(lab.get("criterios", [])) < 3:
        raise ErrorValidacion("lab['criterios'] debe tener al menos 3 criterios")


def _compilar(directorio: str, *fuentes: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["gcc", "-std=c11", "-Wall", "-Wextra", "-Werror", "-o", "programa", *fuentes],
        cwd=directorio,
        capture_output=True,
        text=True,
    )


def _compilar_y_ejecutar(num: int, data: dict, verbose: bool) -> str:
    lab = data["lab"]
    referencia = os.path.join(REFERENCIAS, f"sesion{num:02d}_c.c")
    if not os.path.exists(referencia):
        raise ErrorValidacion(
            f"falta la referencia {referencia} (no se publica, pero se necesita para validar)"
        )

    with tempfile.TemporaryDirectory() as tmp:
        with open(os.path.join(tmp, api_filename(num)), "w", encoding="utf-8") as f:
            f.write(api_header_source(num, lab))
        with open(os.path.join(tmp, harness_filename(num)), "w", encoding="utf-8") as f:
            f.write(harness_source(num, lab))

        # 1. El harness contra la referencia: debe compilar, pasar y coincidir.
        subprocess.run(
            ["cp", referencia, os.path.join(tmp, f"referencia_sesion{num:02d}.c")],
            check=True,
        )
        compilacion = _compilar(
            tmp, harness_filename(num), f"referencia_sesion{num:02d}.c"
        )
        if compilacion.returncode != 0:
            raise ErrorValidacion(
                "la referencia no compila contra el harness:\n" + compilacion.stderr
            )
        ejecucion = subprocess.run(["./programa"], cwd=tmp, capture_output=True, text=True)
        if ejecucion.returncode != 0:
            raise ErrorValidacion(
                "la referencia no pasa el harness:\n" + ejecucion.stdout + ejecucion.stderr
            )
        esperado = expected_output(num, lab)
        if ejecucion.stdout != esperado:
            raise ErrorValidacion(
                "la salida real no coincide con la documentada.\n"
                "--- real ---\n" + ejecucion.stdout + "\n--- documentada ---\n" + esperado
            )

        # 2. El harness contra el esqueleto: debe compilar y fallar.
        with open(os.path.join(tmp, student_filename(num)), "w", encoding="utf-8") as f:
            f.write(student_stub_source(num, lab))
        compilacion_stub = _compilar(tmp, harness_filename(num), student_filename(num))
        if compilacion_stub.returncode != 0:
            raise ErrorValidacion(
                "el esqueleto del estudiante no compila con -Werror:\n"
                + compilacion_stub.stderr
            )
        ejecucion_stub = subprocess.run(
            ["./programa"], cwd=tmp, capture_output=True, text=True
        )
        if ejecucion_stub.returncode == 0:
            raise ErrorValidacion(
                "el esqueleto pasa el harness sin implementar: no hay verde gratis"
            )

        if verbose:
            print(ejecucion.stdout)

    return "ok"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bloque", type=int, choices=[1, 2, 3, 4])
    parser.add_argument("--sesion", type=int)
    parser.add_argument("--sin-compilar", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    numeros = sorted(SESIONES)
    if args.bloque:
        numeros = [n for n in numeros if (n - 1) // 10 == args.bloque - 1]
    if args.sesion:
        numeros = [args.sesion]

    errores = 0
    for n in numeros:
        try:
            _esquema(n, SESIONES[n])
            estado = "esquema ok"
            if not args.sin_compilar:
                estado = _compilar_y_ejecutar(n, SESIONES[n], args.verbose)
            print(f"  ✅ Sesión {n:02d} — {SESIONES[n]['tema']}: {estado}")
        except ErrorValidacion as exc:
            errores += 1
            print(f"  ❌ Sesión {n:02d} — {exc}")
        except KeyError as exc:
            errores += 1
            print(f"  ❌ Sesión {n:02d} — falta la clave {exc}")

    print()
    if errores:
        sys.exit(f"❌ {errores} sesión(es) con problemas.")
    print(f"✅ {len(numeros)} sesión(es) verificadas.")


if __name__ == "__main__":
    main()
