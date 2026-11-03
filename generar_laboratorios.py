#!/usr/bin/env python3
"""
Genera las 40 libretas de laboratorio a partir del contenido único del curso.

Uso:
    python3 generar_laboratorios.py
    python3 generar_laboratorios.py --sesion 07
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from contenido_teorico_bloque1 import TEORIA_BLOQUE_1
from contenido_teorico_bloque2 import TEORIA_BLOQUE_2
from contenido_teorico_bloque3 import TEORIA_BLOQUE_3
from contenido_teorico_bloque4 import TEORIA_BLOQUE_4
from render_laboratorios import render

TOTAL = 40

SESIONES = {
    **TEORIA_BLOQUE_1,
    **TEORIA_BLOQUE_2,
    **TEORIA_BLOQUE_3,
    **TEORIA_BLOQUE_4,
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sesion", type=int, help="generar solo una sesión (1-40)")
    args = parser.parse_args()

    faltan = [n for n in range(1, TOTAL + 1) if n not in SESIONES]
    if faltan:
        sys.exit(f"❌ Faltan sesiones en el contenido: {faltan}")

    numeros = [args.sesion] if args.sesion else sorted(SESIONES)
    for n in numeros:
        if n not in SESIONES:
            sys.exit(f"❌ No existe la sesión {n}")
        nb = render(n, SESIONES[n], TOTAL)
        carpeta = f"laboratorios/sesion{n:02d}"
        os.makedirs(carpeta, exist_ok=True)
        ruta = f"{carpeta}/sesion{n:02d}_laboratorio.ipynb"
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(nb, f, ensure_ascii=False, indent=1)
            f.write("\n")
        print(f"  -> {ruta} ({len(nb['cells'])} celdas)")

    print(f"✅ {len(numeros)} libreta(s) generada(s).")


if __name__ == "__main__":
    main()
