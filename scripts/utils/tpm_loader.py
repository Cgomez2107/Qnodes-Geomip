"""
Cargador de TPMs con soporte para .npy (float32).
Busca primero .npy (mitad de RAM), fallback a CSV (float64).

Uso:
    from utils.tpm_loader import cargar_tpm
    tpm = cargar_tpm(ruta_csv)
"""

from pathlib import Path
import numpy as np


def cargar_tpm(path: Path, delimiter: str = ",") -> np.ndarray:
    """
    Carga una TPM desde archivo.
    Prefiere .npy (float32) sobre .csv (float64) si existe.

    Args:
        path: Ruta al archivo .csv
        delimiter: Delimitador del CSV (default: ",")

    Returns:
        np.ndarray: TPM como float32 si vino de .npy, o float64 si vino de .csv
    """
    npy_path = path.with_suffix(".npy")
    if npy_path.exists():
        return np.load(npy_path)

    return np.genfromtxt(path, delimiter=delimiter)
