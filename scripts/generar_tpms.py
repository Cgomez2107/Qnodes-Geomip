#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera los archivos TPM faltantes: N20A.csv, N22A.csv, N25A.csv
en QNodes/src/.samples/ usando la semilla determinista del proyecto.

Uso: uv run python scripts/generar_tpms.py
"""

import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(
    io.BufferedWriter(sys.stdout.buffer), encoding="utf-8", errors="replace"
)

QNODES_DIR = Path(__file__).parent.parent / "QNodes"
sys.path.insert(0, str(QNODES_DIR))

from src.models.base.application import aplicacion
from src.controllers.manager import Manager


def generar_tpm(n_nodos: int, pagina: str) -> bool:
    estado_inicial = "1" + "0" * (n_nodos - 1)
    aplicacion.set_pagina_red_muestra(pagina)
    gestor = Manager(estado_inicial)
    filename = gestor.generar_red(n_nodos)
    if filename:
        print(f"  OK Generado: {filename}")
        return True
    print(f"  Fallo generacion de N{n_nodos}{pagina}.csv")
    return False


def main():
    print("=" * 60)
    print("  GENERAR TPMS FALTANTES")
    print("=" * 60)

    pendientes = [
        (20, "A", "N20A.csv"),
        (22, "A", "N22A.csv"),
        (25, "A", "N25A.csv"),
    ]

    samples_dir = QNODES_DIR / "src" / ".samples"
    for n_nodos, pagina, fname in pendientes:
        tpm_path = samples_dir / fname
        if tpm_path.exists():
            print(f"  OK {fname} ya existe, saltando")
            continue
        print(f"\nGenerando {fname} ({n_nodos} nodos)...")
        generar_tpm(n_nodos, pagina)

    print("\n--- Proceso completado ---")


if __name__ == "__main__":
    main()
