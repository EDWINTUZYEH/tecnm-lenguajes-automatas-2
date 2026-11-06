#!/usr/bin/env python3
"""Ejecuta las pruebas propias del Hito 1 de Lenguajito.

Uso (desde proyecto_integrador/):
    python3 tests/propias/revisar.py

Convención de archivos, junto a cada `caso.lj`:

- `caso.tokens` : salida exacta esperada de `./lenguajito caso.lj --tokens`
- `caso.ast`    : salida exacta esperada de `./lenguajito caso.lj --ast`
- `caso.err`    : una línea `LINEA CODIGO` por diagnóstico esperado en
                  `./lenguajito caso.lj --check`; el programa debe salir
                  con código 1 y cada diagnóstico debe aparecer en stdout
- (nada)        : `--check` debe terminar con código 0 y sin diagnósticos
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
BIN = RAIZ.parent.parent / "lenguajito"


def normalizar(texto: str) -> str:
    return texto.replace("\r\n", "\n").strip()


def ejecutar(archivo: Path, modo: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [str(BIN), str(archivo), modo],
        capture_output=True,
        text=True,
    )


def revisar(errores: list[str]) -> tuple[int, int]:
    casos = sorted(RAIZ.glob("*.lj"))
    fallos = 0
    for prog in casos:
        nombre = prog.name
        fallo = False

        esperado_tokens = prog.with_suffix(".tokens")
        if esperado_tokens.exists():
            r = ejecutar(prog, "--tokens")
            esperado = normalizar(esperado_tokens.read_text(encoding="utf-8"))
            if r.returncode != 0:
                errores.append(f"{nombre}: --tokens terminó con {r.returncode}")
                fallo = True
            elif normalizar(r.stdout) != esperado:
                errores.append(
                    f"{nombre}: tokens distintos\n"
                    f"  esperado: {esperado!r}\n  obtenido: {normalizar(r.stdout)!r}"
                )
                fallo = True

        esperado_ast = prog.with_suffix(".ast")
        if esperado_ast.exists():
            r = ejecutar(prog, "--ast")
            esperado = normalizar(esperado_ast.read_text(encoding="utf-8"))
            if r.returncode != 0:
                errores.append(f"{nombre}: --ast terminó con {r.returncode}")
                fallo = True
            elif normalizar(r.stdout) != esperado:
                errores.append(
                    f"{nombre}: AST distinto\n"
                    f"  esperado: {esperado}\n  obtenido: {normalizar(r.stdout)}"
                )
                fallo = True

        esperado_err = prog.with_suffix(".err")
        r = ejecutar(prog, "--check")
        if esperado_err.exists():
            if r.returncode != 1:
                errores.append(f"{nombre}: --check debió salir con 1, salió con {r.returncode}")
                fallo = True
            else:
                for linea in esperado_err.read_text(encoding="utf-8").splitlines():
                    linea = linea.strip()
                    if not linea:
                        continue
                    lin, codigo = linea.split()
                    if not re.search(rf":{lin}:\d+: error {codigo}:", r.stdout):
                        errores.append(
                            f"{nombre}: se esperaba un diagnóstico '{codigo}' en la línea {lin}\n"
                            f"  obtenido: {r.stdout!r}"
                        )
                        fallo = True
        else:
            if r.returncode != 0:
                errores.append(
                    f"{nombre}: --check debió salir con 0, salió con {r.returncode}\n"
                    f"  obtenido: {r.stdout!r}"
                )
                fallo = True

        if fallo:
            fallos += 1
    return len(casos), fallos


def main() -> int:
    if not BIN.exists():
        print(f"❌ No existe {BIN}. Ejecuta `make` primero.")
        return 1

    errores: list[str] = []
    total, fallos = revisar(errores)

    for error in errores:
        print(f"❌ {error}")
    print(f"\nHito 1 propias: {total - fallos}/{total} pruebas superadas")
    return 0 if not errores else 1


if __name__ == "__main__":
    sys.exit(main())
