from src.controllers.manager import Manager

from src.strategies.q_nodes import QNodes


def iniciar():
    """Punto de entrada"""

    estado_inicial = "1000000000000000000000000"
    condiciones = "1111111111111111111111111"
    alcance = "1111111111111111111111111"
    mecanismo = "1111111111111111111111110"

    gestor_redes = Manager(estado_inicial)
    mpt = gestor_redes.cargar_red()

    analizador = QNodes(mpt)

    resultado = analizador.aplicar_estrategia(
        estado_inicial,
        condiciones,
        alcance,
        mecanismo,
    )

    import sys
    import io
    from colorama import deinit
    deinit()

    try:
        sys.stdout = io.TextIOWrapper(io.BufferedWriter(sys.stdout.buffer), encoding='utf-8', errors='replace')
        print(resultado)
    except Exception as e:
        print(f"Perdida minima = {resultado.phi}")
        print(f"Partition = {resultado.partition}")
        print(f"Segundos: {resultado.tiempo_ejecucion}")
