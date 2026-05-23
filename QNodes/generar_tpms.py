#!/usr/bin/env python3
"""Genera TPMs faltantes N20A, N22A, N25A. Ejecutar con: uv run python generar_tpms.py"""

import sys
from src.models.base.application import aplicacion
from src.controllers.manager import Manager

PENDIENTES = [(20, "A"), (22, "A"), (25, "A")]

def main():
    for n_nodos, pagina in PENDIENTES:
        fname = f"N{n_nodos}{pagina}.csv"
        tpm_path = f"src/.samples/{fname}"
        import os
        if os.path.exists(tpm_path):
            print(f"  OK {fname} ya existe, saltando")
            continue

        print(f"Generando {fname} ({n_nodos} nodos)...")
        estado_inicial = "1" + "0" * (n_nodos - 1)
        aplicacion.set_pagina_red_muestra(pagina)
        gestor = Manager(estado_inicial)
        filename = gestor.generar_red(n_nodos)
        if filename:
            print(f"  OK Generado: {filename}")
        else:
            print(f"  Fallo generacion de {fname}")

if __name__ == "__main__":
    main()
