"""
Parser: Extrae Φ, Partición y Tiempo de la salida de QNodes
"""

import re


def parsear_salida_qnodes(salida_texto):
    """
    Parsea la salida de terminal de QNodes y extrae:
    - phi: Pérdida mínima (Φ)
    - particion: Mejor bipartición encontrada
    - tiempo: Segundos de ejecución
    
    Retorna dict con claves: phi, particion, tiempo
    """
    
    resultado = {
        "phi": None,
        "particion": None,
        "tiempo": None,
        "error": None
    }
    
    # Buscar Φ (Perdida mínima) - también buscar "Perdida minima" sin acentos
    match_phi = re.search(r'Perdida m[ií]nima.*?=\s*([\d.]+)', salida_texto, re.IGNORECASE)
    if match_phi:
        resultado["phi"] = float(match_phi.group(1))
    
    # Buscar Partición - intentar con caracteres especiales primero
    # Patrón: ⎛ PARTE1 ⎞⎛ PARTE2 ⎞
    match_partition = re.search(
        r'Mejor Bi-Partición:\s*⎛\s*(.*?)\s*⎞\s*⎛\s*(.*?)\s*⎞',
        salida_texto,
        re.DOTALL
    )
    
    if match_partition:
        parte1 = match_partition.group(1).strip()
        parte2 = match_partition.group(2).strip()
        # Limpiar saltos de línea
        parte1 = ' '.join(parte1.split())
        parte2 = ' '.join(parte2.split())
        resultado["particion"] = f"{parte1} | {parte2}"
    else:
        # Si no encuentra con caracteres especiales, buscar patrón alternativo
        # Buscar "Mejor Bi-Partición:" y las líneas siguientes
        match_alt = re.search(
            r'Mejor Bi-Partición:\s*\n\s*(.+?)\n\s*(.+?)\n',
            salida_texto
        )
        if match_alt:
            parte1 = match_alt.group(1).strip()
            parte2 = match_alt.group(2).strip()
            resultado["particion"] = f"{parte1} | {parte2}"
    
    # Buscar tiempo (Segundos)
    match_tiempo = re.search(r'Segundos: ([\d.]+)', salida_texto)
    if match_tiempo:
        resultado["tiempo"] = float(match_tiempo.group(1))
    
    # Verificar si hay error
    if resultado["phi"] is None:
        resultado["error"] = "No se pudo extraer phi de la salida"
    
    return resultado


# Tests
if __name__ == "__main__":
    salida_ejemplo = """
    Perdida mínima ( φ ) = 0.5000
    Mejor Bi-Partición:
    ⎛ A,B ⎞⎛  C  ⎞
    ⎝  c  ⎠⎝ a,b ⎠
    Tiempos de ejecución:
    Horas: 0.00 = Minutos: 0.0 = Segundos: 0.0170
    """
    
    resultado = parsear_salida_qnodes(salida_ejemplo)
    print("Resultado parseado:", resultado)
