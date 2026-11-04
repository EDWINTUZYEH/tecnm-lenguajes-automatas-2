#!/usr/bin/env python3
"""Ejecuta las pruebas propias del equipo (tests/propias/).

Uso (desde proyecto_integrador/):
    python3 tests/propias/revisar.py
    make test-propias

Cada programa puede ser:
  - valido:   archivo.lj + archivo.out  -> se ejecuta con --run y se compara.
  - invalido: archivo.lj + archivo.err  -> --check debe salir con 1 y el
              diagnóstico esperado ("LINEA CODIGO") debe aparecer.
  - tac:      archivo.lj + archivo.tac  -> --tac debe coincidir exacto.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
BIN = RAIZ.parent.parent / "lenguajito"


def ejecutar(archivo: Path, modo: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [str(BIN), str(archivo), modo],
        capture_output=True,
        text=True,
    )


def main() -> int:
    if not BIN.exists():
        print(f"No existe {BIN}. Ejecuta `make` primero.")
        return 1

    errores: list[str] = []
    total = 0
    for prog in sorted(RAIZ.glob("*.lj")):
        total += 1
        archivo_tac = prog.with_suffix(".tac")
        if archivo_tac.exists():
            esperado = archivo_tac.read_text(encoding="utf-8")
            r = ejecutar(prog, "--tac")
            if r.returncode != 0:
                errores.append(f"{prog.name}: --tac terminó con {r.returncode}")
            elif r.stdout != esperado:
                errores.append(
                    f"{prog.name}: TAC distinto\n"
                    f"  esperado: {esperado!r}\n  obtenido: {r.stdout!r}"
                )
            continue

        archivo_err = prog.with_suffix(".err")
        if archivo_err.exists():
            linea, codigo = archivo_err.read_text(encoding="utf-8").split()
            r = ejecutar(prog, "--check")
            if r.returncode != 1 or not re.search(
                rf":{linea}:\d+: error {codigo}:", r.stdout
            ):
                errores.append(
                    f"{prog.name}: se esperaba {codigo} en la línea {linea}\n"
                    f"  obtenido: {r.stdout!r} (código {r.returncode})"
                )
            continue

        esperado = prog.with_suffix(".out").read_text(encoding="utf-8")
        r = ejecutar(prog, "--run")
        if r.returncode != 0:
            errores.append(f"{prog.name}: --run terminó con {r.returncode}")
        elif r.stdout != esperado:
            errores.append(
                f"{prog.name}: salida distinta\n"
                f"  esperado: {esperado!r}\n  obtenido: {r.stdout!r}"
            )

    for error in errores:
        print(f"ERROR: {error}")
    print(f"\nPruebas propias: {total - len(errores)}/{total} superadas")
    return 0 if not errores else 1


if __name__ == "__main__":
    sys.exit(main())
