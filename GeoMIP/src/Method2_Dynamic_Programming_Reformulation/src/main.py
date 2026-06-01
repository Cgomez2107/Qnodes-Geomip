"""
Prueba manual de GeometricSIA.
Cambia SOLO los valores de pagina, n_nodos, alcance y mecanismo.
Ejecutar con: .venv\Scripts\python src\main.py
"""

import sys
import io

sys.stdout = io.TextIOWrapper(
    io.BufferedWriter(sys.stdout.buffer), encoding="utf-8", errors="replace"
)

from pathlib import Path
# Asegurar que el directorio raiz del proyecto esta en sys.path
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import numpy as np
from src.models.base.application import aplicacion
from src.controllers.manager import Manager
from src.controllers.strategies.geometric import GeometricSIA

# ============================================================
# CONFIGURA AQUI:
# ============================================================
pagina = "A"  # "A", "B", etc.

n_nodos = 20
estado_inicial = "1" + "0" * (n_nodos - 1)
condiciones = "1" * n_nodos

# Usa la tabla del Excel:
alcance = "1" * n_nodos
mecanismo = "1" * n_nodos
# ============================================================

# Configurar pagina
aplicacion.pagina_sample_network = pagina
aplicacion.profiler_habilitado = False

# Cargar TPM
gestor = Manager(estado_inicial=estado_inicial)

# Buscar TPM
METHOD2_ROOT = Path(__file__).resolve().parents[1]
GEOMIP_ROOT = Path(__file__).resolve().parents[3]
sample_name = f"N{n_nodos}{pagina}.csv"
tpm_path = (
    GEOMIP_ROOT / "data" / "samples" / sample_name
)
if not tpm_path.exists():
    tpm_path = (
        METHOD2_ROOT / ".samples" / sample_name
    )
if not tpm_path.exists():
    tpm_path = (
        METHOD2_ROOT / "src" / ".samples" / sample_name
    )

print(f"TPM: {tpm_path}")
npy_path = tpm_path.with_suffix(".npy")
tpm = np.load(npy_path) if npy_path.exists() else np.genfromtxt(tpm_path, delimiter=",")
print(f"TPM shape: {tpm.shape}")

# Ejecutar GeometricSIA
analizador = GeometricSIA(gestor)
sol = analizador.aplicar_estrategia(condiciones, alcance, mecanismo, tpm)

print()
print("=" * 60)
print(sol)
print("=" * 60)
print()
print(f"Particion: {sol.particion}")
print(f"Perdida (phi): {sol.perdida}")
print(f"Tiempo (s): {sol.tiempo_ejecucion}")
