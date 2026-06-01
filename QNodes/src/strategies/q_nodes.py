import time
from typing import Union
import numpy as np
from src.middlewares.slogger import SafeLogger
from src.funcs.iit import emd_efecto, ABECEDARY
from src.middlewares.profile import gestor_perfilado, profile
from src.funcs.format import fmt_biparticion_q
from src.models.base.sia import SIA

from src.models.core.solution import Solution
from src.constants.models import (
    QNODES_ANALYSIS_TAG,
    QNODES_LABEL,
    QNODES_STRAREGY_TAG,
)
from src.constants.base import (
    COLS_IDX,
    INT_ZERO,
    TYPE_TAG,
    NET_LABEL,
    INFTY_POS,
    LAST_IDX,
    EFFECT,
    ACTUAL,
)
from src.models.base.application import aplicacion


class QNodes(SIA):
    """
    Clase QNodes para el análisis de redes mediante el algoritmo Q.

    Esta clase implementa un gestor principal para el análisis de redes que utiliza
    el algoritmo Q para encontrar la partición óptima que minimiza la
    pérdida de información en el sistema. Hereda de la clase base SIA (Sistema de
    Información Activo) y proporciona funcionalidades para analizar la estructura
    y dinámica de la red.

    Args:
    ----
        config (Loader):
            Instancia de la clase Loader que contiene la configuración del sistema
            y los parámetros necesarios para el análisis.

    Attributes:
    ----------
        m (int):
            Número de elementos en el conjunto de purview (vista).

        n (int):
            Número de elementos en el conjunto de mecanismos.

        tiempos (tuple[np.ndarray, np.ndarray]):
            Tupla de dos arrays que representan los tiempos para los estados
            actual y efecto del sistema.

        etiquetas (list[tuple]):
            Lista de tuplas conteniendo las etiquetas para los nodos,
            con versiones en minúsculas y mayúsculas del abecedario.

        vertices (set[tuple]):
            Conjunto de vértices que representan los nodos de la red,
            donde cada vértice es una tupla (tiempo, índice).

        memoria (dict):
            Diccionario para almacenar resultados intermedios y finales
            del análisis (memoización).

        logger:
            Instancia del logger configurada para el análisis Q.

    Methods:
    -------
        run(condicion, purview, mechanism):
            Ejecuta el análisis principal de la red con las condiciones,
            purview y mecanismo especificados.

        algorithm(vertices):
            Implementa el algoritmo Q para encontrar la partición
            óptima del sistema.

        funcion_submodular(deltas, omegas):
            Calcula la función submodular para evaluar particiones candidatas.

        view_solution(mip):
            Visualiza la solución encontrada en términos de las particiones
            y sus valores asociados.

        nodes_complement(nodes):
            Obtiene el complemento de un conjunto de nodos respecto a todos
            los vértices del sistema.

    Notes:
    -----
    - La clase implementa una versión secuencial del algoritmo Q para encontrar la partición que minimiza la pérdida de información.
    - Utiliza memoización para evitar recálculos innecesarios durante el proceso.
    - El análisis se realiza considerando dos tiempos: actual (presente) y
      efecto (futuro).
    """

    def __init__(self, tpm: np.ndarray):
        super().__init__(tpm)
        gestor_perfilado.start_session(
            f"{NET_LABEL}{len(tpm[COLS_IDX])}{aplicacion.pagina_red_muestra}"
        )
        self.m: int
        self.n: int
        self.tiempos: tuple[np.ndarray, np.ndarray]
        self.etiquetas = [tuple(s.lower() for s in ABECEDARY), ABECEDARY]
        self.vertices: set[tuple]
        self.clave_submodular = [], []
        self.memoria_delta = {}
        self.memoria_grupo_candidato = {}

        self.indices_alcance: np.ndarray
        self.indices_mecanismo: np.ndarray

        self.logger = SafeLogger(QNODES_STRAREGY_TAG)
        self.restarts = 1  # random restarts >1 no mejoraron φ

    def aplicar_estrategia(
        self,
        estado_inicial: str,
        condicion: str,
        alcance: str,
        mecanismo: str,
    ):
        self.sia_preparar_subsistema(estado_inicial, condicion, alcance, mecanismo)

        # e.g. (1,0)=A (1,1)=B (1,2)=C #
        futuro = tuple(
            (EFFECT, idx_efecto) for idx_efecto in self.sia_subsistema.indices_ncubos
        )

        # e.g. (0,0)=a (0,2)=c (0,4)=e #
        presente = tuple(
            (ACTUAL, idx_actual) for idx_actual in self.sia_subsistema.dims_ncubos
        )

        self.m = self.sia_subsistema.indices_ncubos.size
        self.n = self.sia_subsistema.dims_ncubos.size

        self.indices_alcance = self.sia_subsistema.indices_ncubos
        self.indices_mecanismo = self.sia_subsistema.dims_ncubos

        self.tiempos = (
            np.zeros(self.n, dtype=np.int8),
            np.zeros(self.m, dtype=np.int8),
        )

        vertices = list(presente + futuro)
        self.vertices = set(presente + futuro)
        mip = self.algorithm(vertices)

        fmt_mip = fmt_biparticion_q(list(mip), self.nodes_complement(mip))
        perdida_mip, dist_marginal_mip = self.memoria_grupo_candidato[mip]

        return Solution(
            estrategia=QNODES_LABEL,
            perdida=perdida_mip,
            distribucion_subsistema=self.sia_dists_marginales,
            distribucion_particion=dist_marginal_mip,
            tiempo_total=time.time() - self.sia_tiempo_inicio,
            particion=fmt_mip,
        )

    @profile(context={TYPE_TAG: QNODES_ANALYSIS_TAG})
    def algorithm(self, vertices: list[tuple[int, int]]):
        """
        Implementa el algoritmo Q con Random Restarts para encontrar la partición óptima.

        Ejecuta self.restarts veces con diferentes órdenes de vértices, acumulando
        resultados en memoria (memoización cruzada entre restarts). Retorna la
        partición con menor φ encontrada en cualquier restart.

        El primer restart usa el orden original de vértices (backward compatible).
        Los restarts adicionales usan órdenes aleatorios para explorar diferentes
        trayectorias de búsqueda.

        Después de los restarts, aplica post-hoc refinement (1-opt local search)
        para escapar óptimos locales que el greedy no puede corregir.
        """
        best_key = None
        best_emd = float('inf')

        for restart in range(self.restarts):
            if restart == 0:
                v = list(vertices)
            else:
                rng = np.random.default_rng(restart * 137 + 42)
                v = list(vertices)
                rng.shuffle(v)

            key = self._algorithm_run(v)
            emd = self.memoria_grupo_candidato[key][0]
            if emd < best_emd:
                best_emd = emd
                best_key = key
                if best_emd == 0:
                    if self.restarts == 1:
                        refined = self._refinar_particion(best_key)
                        if refined != best_key:
                            emd_r, dist_r = self._evaluar_emd_particion(refined)
                            self.memoria_grupo_candidato[refined] = (emd_r, dist_r)
                        return refined
                    return best_key

        if best_key is not None:
            refined = self._refinar_particion(best_key)
            if refined != best_key:
                emd_r, dist_r = self._evaluar_emd_particion(refined)
                self.memoria_grupo_candidato[refined] = (emd_r, dist_r)
            return refined

        return best_key

    def _algorithm_run(self, vertices: list[tuple[int, int]]):
        """
        Ejecución interna del algoritmo Q con un orden fijo de vértices.
        Acumula resultados en self.memoria_grupo_candidato y self.memoria_delta.
        """
        indice_emd = INT_ZERO

        for i in range(len(vertices) - 1):
            omegas_ciclo = [vertices[0]]
            deltas_ciclo = vertices[1:]

            emd_particion_candidata = INFTY_POS
            dist_particion_candidata = None

            for j in range(len(deltas_ciclo) - 1):
                emd_local = 1e5
                indice_mip: int

                for k in range(len(deltas_ciclo)):
                    emd_union, emd_delta, dist_marginal_delta = self.funcion_submodular(
                        deltas_ciclo[k], omegas_ciclo
                    )

                    emd_iteracion = emd_union - emd_delta

                    if emd_iteracion < emd_local:
                        if emd_delta == INT_ZERO:
                            clave = (
                                tuple(deltas_ciclo[k])
                                if isinstance(deltas_ciclo[k], list)
                                else (deltas_ciclo[k],)
                            )
                            self.memoria_grupo_candidato[clave] = (
                                emd_delta,
                                dist_marginal_delta,
                            )
                            return clave

                        emd_local = emd_iteracion
                        indice_mip = k
                        emd_particion_candidata = emd_delta
                        dist_particion_candidata = dist_marginal_delta

                omegas_ciclo.append(deltas_ciclo[indice_mip])
                deltas_ciclo.pop(indice_mip)
            self.memoria_grupo_candidato[
                tuple(
                    deltas_ciclo[LAST_IDX]
                    if isinstance(deltas_ciclo[LAST_IDX], list)
                    else deltas_ciclo
                )
            ] = emd_particion_candidata, dist_particion_candidata

            par_candidato = (
                [omegas_ciclo[LAST_IDX]]
                if isinstance(omegas_ciclo[LAST_IDX], tuple)
                else omegas_ciclo[LAST_IDX]
            ) + (
                deltas_ciclo[LAST_IDX]
                if isinstance(deltas_ciclo[LAST_IDX], list)
                else deltas_ciclo
            )

            omegas_ciclo.pop()
            omegas_ciclo.append(par_candidato)

            vertices = omegas_ciclo

        return min(
            self.memoria_grupo_candidato,
            key=lambda k: self.memoria_grupo_candidato[k][indice_emd],
        )

    def _evaluar_emd_particion(self, clave: tuple) -> tuple[float, np.ndarray]:
        """
        Evalúa el φ (EMD-Effect) de una partición arbitraria.

        Dado un conjunto de vértices (clave) que representan un lado de la
        bipartición, extrae los índices de efecto (futuro) y actual (presente)
        y computa la EMD vía bipartir + distribucion_marginal.

        Returns:
            tuple[float, np.ndarray]: (emd, distribucion_marginal)
        """
        efectos = [idx for time, idx in clave if time == EFFECT]
        actuales = [idx for time, idx in clave if time == ACTUAL]

        if not efectos and not actuales:
            return float('inf'), None

        particion = self.sia_subsistema.bipartir(
            np.array(efectos, dtype=np.int8),
            np.array(actuales, dtype=np.int8),
        )
        dist = particion.distribucion_marginal()
        emd = emd_efecto(dist, self.sia_dists_marginales)
        return emd, dist

    def _refinar_particion(self, clave: tuple) -> tuple:
        """
        Post-hoc refinement (1-opt local search) sobre una partición.

        Intercambia cada vértice de un lado al otro uno por uno.
        Si el movimiento mejora φ, lo acepta y reinicia el ciclo.
        Repite hasta que ningún movimiento individual mejore φ
        (mínimo local en distancia de Hamming 1).

        Args:
            clave: tupla de vértices representando un lado de la bipartición.

        Returns:
            tuple: la mejor partición encontrada (posiblemente la misma).
        """
        if not clave or len(clave) <= 1:
            return clave

        vertices_particion = set(clave)
        vertices_complemento = self.vertices - vertices_particion

        if not vertices_complemento:
            return clave

        mejor_emd, _ = self._evaluar_emd_particion(clave)
        mejor_clave = clave

        while True:
            hubo_mejora = False

            for v in list(vertices_particion):
                if len(vertices_particion) <= 1:
                    break
                if len(vertices_complemento) + 1 > len(self.vertices) - 1:
                    break
                nueva_particion = vertices_particion - {v}
                emd, _ = self._evaluar_emd_particion(tuple(nueva_particion))
                if emd < mejor_emd:
                    mejor_emd = emd
                    mejor_clave = tuple(nueva_particion)
                    vertices_complemento = vertices_complemento | {v}
                    vertices_particion = nueva_particion
                    hubo_mejora = True
                    break

            if not hubo_mejora:
                for v in list(vertices_complemento):
                    if len(vertices_complemento) <= 1:
                        break
                    if len(vertices_particion) + 1 > len(self.vertices) - 1:
                        break
                    nueva_particion = vertices_particion | {v}
                    emd, _ = self._evaluar_emd_particion(tuple(nueva_particion))
                    if emd < mejor_emd:
                        mejor_emd = emd
                        mejor_clave = tuple(nueva_particion)
                        vertices_particion = nueva_particion
                        vertices_complemento = vertices_complemento - {v}
                        hubo_mejora = True
                        break

            if not hubo_mejora:
                break

        return mejor_clave

    def funcion_submodular(
        self, deltas: Union[tuple, list[tuple]], omegas: list[Union[tuple, list[tuple]]]
    ):
        """
        Evalúa el impacto de combinar el conjunto de nodos individual delta y su agrupación con el conjunto omega, calculando la diferencia entre EMD (Earth Mover's Distance) de las configuraciones, en conclusión los nodos delta evaluados individualmente y su combinación con el conjunto omega.

        El proceso se realiza en dos fases principales:

        1. Evaluación Individual:
           - Crea una copia del estado temporal del subsistema.
           - Activa los nodos delta en su tiempo correspondiente (presente/futuro).
           - Si el delta ya fue evaluado antes, recupera su EMD y distribución marginal de memoria
           - Si no, ha de:
             * Identificar dimensiones activas en presente y futuro.
             * Realiza bipartición del subsistema con esas dimensiones.
             * Calcular la distribución marginal y EMD respecto al subsistema.
             * Guarda resultados en memoria para seguro un uso futuro.

        2. Evaluación Combinada:
           - Sobre la misma copia temporal, activa también los nodos omega.
           - Calcula dimensiones activas totales (delta + omega).
           - Realiza bipartición del subsistema completo.
           - Obtiene EMD de la combinación.

        Args:
            deltas: Un nodo individual (tupla) o grupo de nodos (lista de tuplas)
                   donde cada tupla está identificada por su (tiempo, índice), sea el tiempo t_0 identificado como 0, t_1 como 1 y, el índice hace referencia a las variables/dimensiones habilitadas para operaciones de substracción/marginalización sobre el subsistema, tal que genere la partición.
            omegas: Lista de nodos ya agrupados, puede contener tuplas individuales
                   o listas de tuplas para grupos formados por los pares candidatos o más uniones entre sí (grupos candidatos).

        Returns:
            tuple: (
                EMD de la combinación omega y delta,
                EMD del delta individual,
                Distribución marginal del delta individual
            )
            Esto lo hice así para hacer almacenamiento externo de la emd individual y su distribución marginal en las particiones candidatas.
        """
        vector_delta_marginal = None
        self.clave_submodular = [], []

        # Delta #

        clave_delta_actual, clave_delta_efecto = self.definir_clave(deltas)
        clave_delta = tuple(clave_delta_actual), tuple(clave_delta_efecto)

        idxs_alcance_delta = self.clave_submodular[EFFECT]
        dims_mecanismo_delta = self.clave_submodular[ACTUAL]

        if clave_delta not in self.memoria_delta:
            particion_delta = self.sia_subsistema.bipartir(
                np.array(idxs_alcance_delta, dtype=np.int8),
                np.array(dims_mecanismo_delta, dtype=np.int8),
            )
            vector_delta_marginal = particion_delta.distribucion_marginal()
            emd_delta = emd_efecto(vector_delta_marginal, self.sia_dists_marginales)
            self.memoria_delta[clave_delta] = emd_delta, vector_delta_marginal

        else:
            emd_delta, vector_delta_marginal = self.memoria_delta[clave_delta]

        # Unión #

        for omega in omegas:
            self.definir_clave(omega)

        idxs_alcance_union = self.clave_submodular[EFFECT]
        dims_mecanismo_union = self.clave_submodular[ACTUAL]

        particion_union = self.sia_subsistema.bipartir(
            np.array(idxs_alcance_union, dtype=np.int8),
            np.array(dims_mecanismo_union, dtype=np.int8),
        )
        vector_union_marginal = particion_union.distribucion_marginal()
        emd_union = emd_efecto(vector_union_marginal, self.sia_dists_marginales)

        return emd_union, emd_delta, vector_delta_marginal

    def definir_clave(
        self,
        conjunto: Union[tuple[int, int], list[tuple[int, int]]],
    ):
        if isinstance(conjunto, tuple):
            tiempo, indice = conjunto
            self.clave_submodular[tiempo].append(indice)
        else:
            for tiempo, indice in conjunto:
                self.clave_submodular[tiempo].append(indice)
        self.clave_submodular[ACTUAL].sort()
        self.clave_submodular[EFFECT].sort()
        return self.clave_submodular

    def nodes_complement(self, nodes: list[tuple[int, int]]):
        return list(set(self.vertices) - set(nodes))
