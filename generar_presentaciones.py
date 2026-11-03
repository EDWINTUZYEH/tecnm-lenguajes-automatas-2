#!/usr/bin/env python3
"""
Genera las 40 presentaciones a partir del contenido único del curso.

Uso:
    python3 generar_presentaciones.py
    python3 generar_presentaciones.py --sesion 07
"""

from __future__ import annotations

import argparse
import os
import sys

from contenido_teorico_bloque1 import TEORIA_BLOQUE_1
from contenido_teorico_bloque2 import TEORIA_BLOQUE_2
from contenido_teorico_bloque3 import TEORIA_BLOQUE_3
from contenido_teorico_bloque4 import TEORIA_BLOQUE_4
from render_presentaciones import render

TOTAL = 40

SESIONES = {
    **TEORIA_BLOQUE_1,
    **TEORIA_BLOQUE_2,
    **TEORIA_BLOQUE_3,
    **TEORIA_BLOQUE_4,
}

UNIDADES = [
    {
        "nombre": "Unidad 1: Análisis Semántico y AST",
        "rango": "Sesiones 01–10",
        "hito": "Hito 1 · Sesión 10",
        "desde": 1,
        "hasta": 10,
    },
    {
        "nombre": "Unidad 2: Tabla de Símbolos y Ámbitos",
        "rango": "Sesiones 11–20",
        "hito": "Hito 2 · Sesión 20",
        "desde": 11,
        "hasta": 20,
    },
    {
        "nombre": "Unidad 3: Código Intermedio y Optimización",
        "rango": "Sesiones 21–30",
        "hito": "Hito 3 · Sesión 30",
        "desde": 21,
        "hasta": 30,
    },
    {
        "nombre": "Unidad 4: Código Objeto y Backend",
        "rango": "Sesiones 31–40",
        "hito": "Hito 4 · Sesión 40",
        "desde": 31,
        "hasta": 40,
    },
]


def validar_indice(numeros: list[int]) -> None:
    faltan = [n for n in range(1, TOTAL + 1) if n not in SESIONES]
    if faltan:
        sys.exit(f"❌ Faltan sesiones en el contenido: {faltan}")
    for n in numeros:
        for clave in ("tema", "unidad", "contexto", "lab"):
            if clave not in SESIONES[n]:
                sys.exit(f"❌ Sesión {n:02d}: falta la clave '{clave}'")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sesion", type=int, help="generar solo una sesión (1-40)")
    args = parser.parse_args()

    numeros = [args.sesion] if args.sesion else sorted(SESIONES)
    validar_indice(numeros)
    os.makedirs("presentaciones", exist_ok=True)

    for n in numeros:
        if n not in SESIONES:
            sys.exit(f"❌ No existe la sesión {n}")
        siguiente = SESIONES[n + 1]["tema"] if n < TOTAL else None
        html = render(n, SESIONES[n], UNIDADES, TOTAL, siguiente)
        ruta = f"presentaciones/sesion{n:02d}.html"
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  -> {ruta} ({len(html.splitlines())} líneas, 8 láminas)")

    print(f"✅ {len(numeros)} presentación(es) generada(s).")


if __name__ == "__main__":
    main()
