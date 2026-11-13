#!/usr/bin/env python3
"""Ejecuta las pruebas propias del equipo (Hitos 1 y 2) de Lenguajito.

Uso (desde proyecto_integrador/):
    python3 tests/propias/revisar.py
    make test-propias

Convención de archivos, junto a cada `caso.lj`:

- `caso.tokens` : salida exacta esperada de `./lenguajito caso.lj --tokens`
- `caso.ast`    : salida exacta esperada de `./lenguajito caso.lj --ast`
- `caso.out`    : salida exacta esperada de `./lenguajito caso.lj --run`
- `caso.err`    : una línea `LINEA CODIGO` por diagnóstico esperado en
                  `./lenguajito caso.lj --check`; el programa debe salir
                  con código 1 y cada diagnóstico debe aparecer en stdout
- `caso.diag`   : lista exacta de diagnósticos `LINEA CODIGO` que debe
                  emitir `--check` (mismo orden); el programa sale con 1
- (nada)        : `--check` debe terminar con código 0 y sin diagnósticos
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
BIN = RAIZ.parent.parent / "lenguajito"
DIAGNOSTICO = re.compile(r":(\d+):\d+: error ([A-Z]\d+):")


def normalizar(texto: str) -> str:
    return texto.replace("\r\n", "\n").strip()


def ejecutar(archivo: Path, modo: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [str(BIN), str(archivo), modo],
        capture_output=True,
        text=True,
    )


def leer_diagnosticos(archivo: Path) -> list[tuple[int, str]]:
    diagnosticos: list[tuple[int, str]] = []
    for linea in archivo.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#"):
            continue
        numero, codigo = linea.split()
        diagnosticos.append((int(numero), codigo))
    return diagnosticos


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

        esperado_out = prog.with_suffix(".out")
        if esperado_out.exists():
            r = ejecutar(prog, "--run")
            esperado = normalizar(esperado_out.read_text(encoding="utf-8"))
            if r.returncode != 0:
                errores.append(f"{nombre}: --run terminó con {r.returncode}")
                fallo = True
            elif normalizar(r.stdout) != esperado:
                errores.append(
                    f"{nombre}: salida de --run distinta\n"
                    f"  esperado: {esperado!r}\n  obtenido: {normalizar(r.stdout)!r}"
                )
                fallo = True

        esperado_err = prog.with_suffix(".err")
        esperado_diag = prog.with_suffix(".diag")
        if esperado_err.exists() or esperado_diag.exists():
            r = ejecutar(prog, "--check")
            if esperado_err.exists():
                if r.returncode != 1:
                    errores.append(
                        f"{nombre}: --check debió salir con 1, salió con {r.returncode}"
                    )
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
                esperados = leer_diagnosticos(esperado_diag)
                obtenidos = [
                    (int(numero), codigo)
                    for numero, codigo in DIAGNOSTICO.findall(r.stdout)
                ]
                if r.returncode != 1:
                    errores.append(
                        f"{nombre}: --check debió salir con 1, salió con {r.returncode}"
                    )
                    fallo = True
                elif obtenidos != esperados:
                    errores.append(
                        f"{nombre}: diagnósticos distintos\n"
                        f"  esperado: {esperados}\n  obtenido: {obtenidos}"
                    )
                    fallo = True
        else:
            r = ejecutar(prog, "--check")
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
    print(f"\nPruebas propias: {total - fallos}/{total} superadas")
    return 0 if not errores else 1


if __name__ == "__main__":
    sys.exit(main())
