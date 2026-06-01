import heapq
from src.constants.error import ERROR_INCOMPATIBLE_SIZES
from src.models.core.system import System
from src.constants.base import NET_LABEL, STR_ZERO
from src.funcs.base import ABECEDARY
from src.middlewares.slogger import SafeLogger
from src.funcs.base import emd_efecto
from src.models.base.sia import SIA
from src.constants.base import (
    ACTUAL,
    EFECTO,
    TYPE_TAG,
)
from src.constants.models import (
    GEOMETRIC_ANALYSIS_TAG,
    GEOMETRIC_LABEL,
    GEOMETRIC_STRAREGY_TAG,
)
from src.controllers.manager import Manager
from src.funcs.format import fmt_biparte_q
from src.middlewares.profile import profiler_manager, profile
from src.models.core.solution import Solution
import numpy as np
import time
from typing import List, Dict, Tuple, Optional

from concurrent.futures import ThreadPoolExecutor
import itertools


class GeometricSIA(SIA):
    def __init__(self, gestor: Manager, beam_width: int = 1, timeout: Optional[float] = None):
        super().__init__(gestor)
        profiler_manager.start_session(
            f"{NET_LABEL}{len(gestor.estado_inicial)}{gestor.pagina}"
        )
        self.etiquetas = [tuple(s.lower() for s in ABECEDARY), ABECEDARY]
        self.logger = SafeLogger(GEOMETRIC_STRAREGY_TAG)
        self.tabla_transiciones: dict = {}
        self.vertices: set[tuple]
        self.tabla: dict[int, list[tuple[int, int]]] = {}
        self.memoria_particiones: dict[tuple[int, int], tuple[float, float]] = {}
        self.beam_width = beam_width
        self.timeout = timeout

    @profile(context={TYPE_TAG: GEOMETRIC_ANALYSIS_TAG})
    def aplicar_estrategia(
        self,
        condicion: str,
        alcance: str,
        mecanismo: str,
        tpm: np.ndarray,
        timeout: Optional[float] = None,
    ):
        self.sia_preparar_subsistema(condicion, alcance, mecanismo, tpm)

        futuro = tuple(
            (EFECTO, efecto) for efecto in self.sia_subsistema.indices_ncubos
        )
        presente = tuple(
            (ACTUAL, actual) for actual in self.sia_subsistema.dims_ncubos
        )

        self._flat_matrix = np.stack([
            ncubo.data.ravel() for ncubo in self.sia_subsistema.ncubos
        ])

        self.vertices = set(presente + futuro)
        dims = self.sia_subsistema.dims_ncubos
        self.estado_inicial = self.sia_subsistema.estado_inicial[dims]
        self.estado_final = 1 - self.estado_inicial
        self._pre_ini_idx = self._state_index(self.estado_inicial.tolist())
        self._initial_probs = self._flat_matrix[:, self._pre_ini_idx].copy()
        mip = self.find_mip(timeout=timeout or self.timeout)
        fmt_mip = fmt_biparte_q(list(mip), self.nodes_complement(mip))

        return Solution(
            estrategia=GEOMETRIC_LABEL,
            perdida=self.memoria_particiones[mip][0],
            distribucion_subsistema=self.sia_dists_marginales,
            distribucion_particion=self.memoria_particiones[mip][1],
            tiempo_total=time.time() - self.sia_tiempo_inicio,
            particion=fmt_mip,
        )

    def nodes_complement(self, nodes: list[tuple[int, int]]):
        return list(set(self.vertices) - set(nodes))

    def find_mip(self, timeout: Optional[float] = None):
        self.sia_logger.critic("empieza.")
        estado_inicial = self.estado_inicial
        estado_final = self.estado_final
        self.idx_ncubos = list(range(len(self.sia_subsistema.indices_ncubos)))
        init_list = estado_inicial.tolist()
        self.caminos: Dict[int, List[List[int]]] = {0: [init_list]}
        self.caminos_idx: Dict[int, List[int]] = {0: [self._pre_ini_idx]}
        self._init_state_tuple = tuple(init_list)
        n = len(estado_inicial)
        n_ncubos = len(self.sia_subsistema.indices_ncubos)
        init_key = (self._init_state_tuple, self._init_state_tuple)
        self.tabla_transiciones[init_key] = np.zeros(n_ncubos, dtype=np.float64)
        _t0 = time.time()
        _check_interval = max(1, n // 4)
        for nivel in range(1, n + 1):
            self.calcular_costos_nivel(estado_final, nivel)
            if timeout is not None and nivel % _check_interval == 0:
                if time.time() - _t0 > timeout:
                    self.sia_logger.critic(f"timeout {timeout}s en nivel {nivel}")
                    break
        candidatos = self.identificar_particiones_optimas()
        mejor_emd = float('inf')
        mejor_key = None
        for idx, (presentes, futuros) in enumerate(candidatos):
            if timeout is not None and idx % 5 == 0:
                if time.time() - _t0 > timeout:
                    self.sia_logger.critic(f"timeout {timeout}s evaluando candidato {idx}")
                    break
            presentes = self.sia_subsistema.dims_ncubos[presentes]
            futuros = self.sia_subsistema.indices_ncubos[futuros]
            dist = self.sia_subsistema.bipartir(futuros, presentes).distribucion_marginal()
            emd = emd_efecto(dist, self.sia_dists_marginales)
            key = [(0, nodo) for nodo in presentes]
            key.extend([(1, nodo) for nodo in futuros])
            self.memoria_particiones[tuple(key)] = (emd, dist)
            if emd < mejor_emd:
                mejor_emd = emd
                mejor_key = tuple(key)
            if emd <= 1e-10:
                self.mejor_mip = mejor_key
                return mejor_key
        self.mejor_mip = mejor_key
        return mejor_key

    def calcular_costos_nivel(self, estado_final: np.ndarray, nivel):
        n = len(estado_final)
        visitados: set[tuple] = set()
        self.caminos[nivel] = []
        self.caminos_idx[nivel] = []
        prev_caminos = self.caminos[nivel - 1]
        prev_indices = self.caminos_idx[nivel - 1]
        for idx_s, estado_anterior in enumerate(prev_caminos):
            idx_anterior = prev_indices[idx_s]
            for i in range(n):
                if estado_anterior[i] != estado_final[i]:
                    nuevo_estado = list(estado_anterior)
                    nuevo_estado[i] = int(estado_final[i])
                    nuevo_estado_tuple = tuple(nuevo_estado)
                    if nuevo_estado_tuple not in visitados:
                        nuevo_idx = idx_anterior ^ (1 << i)
                        self.caminos[nivel].append(nuevo_estado)
                        self.caminos_idx[nivel].append(nuevo_idx)
                        self.calcular_costo(self._init_state_tuple, nuevo_estado_tuple, nuevo_idx)
                        visitados.add(nuevo_estado_tuple)

    @staticmethod
    def _state_index(state: list) -> int:
        idx = 0
        for bit in reversed(state):
            idx = (idx << 1) | bit
        return idx

    def calcular_costo(self, estado_inicial: tuple, estado_final: tuple, estado_fin_int: int):
        distancia_hamming = self.hamming_ints(estado_inicial, estado_final)
        factor = 1.0 / (1 << distancia_hamming)

        diffs = np.abs(self._initial_probs - self._flat_matrix[:, estado_fin_int])
        diffs *= factor

        if distancia_hamming > 1:
            for i in range(len(estado_inicial)):
                if estado_inicial[i] != estado_final[i]:
                    inter = list(estado_final)
                    inter[i] = estado_inicial[i]
                    temp_key = estado_inicial, tuple(inter)
                    diffs += self.tabla_transiciones[temp_key]

        self.tabla_transiciones[(estado_inicial, estado_final)] = diffs

    def identificar_particiones_optimas(self):
        init_tuple = self._init_state_tuple
        final_tuple = tuple(self.estado_final.tolist())
        key = init_tuple, final_tuple
        costos: list = self.tabla_transiciones[key]
        candidatos = []
        n_vars = len(costos)
        for idx in range(n_vars):
            presentes = list(range(len(self.estado_final)))
            futuros = [i for i in range(n_vars) if i != idx]
            candidatos.append([presentes, futuros])
        es_par = len(self.caminos) % 2 == 0
        if es_par:
            mitad = len(self.caminos) // 2
        else:
            mitad = (len(self.caminos) // 2) + 1
        init_list = self.caminos[0][0]
        init_arr = np.array(init_list, dtype=np.int8)
        for nivel in range(1, mitad):
            candidatos_nivel = []
            for estado in self.caminos[nivel]:
                estado_arr = np.array(estado, dtype=np.int8)
                estado_tuple = tuple(estado)
                actual = self.tabla_transiciones.get((init_tuple, estado_tuple), None)
                comp_arr = 1 - estado_arr
                comp_tuple = tuple(comp_arr.tolist())
                complementario = self.tabla_transiciones.get((init_tuple, comp_tuple), None)
                mask = actual is not None and complementario is not None
                if not mask:
                    continue
                presentes = np.where(estado_arr == init_arr)[0].tolist()
                futuros_mask = actual <= complementario
                futuros = np.where(futuros_mask)[0].tolist()
                costo = np.where(futuros_mask, actual, complementario).sum()
                candidatos_nivel.append((costo, presentes, futuros))
            candidatos_nivel.sort(key=lambda x: x[0])
            for _, presentes, futuros in candidatos_nivel[:self.beam_width]:
                candidatos.append([presentes, futuros])
        return candidatos

    def hamming(self, a: List[int], b: List[int]) -> int:
        return sum(x != y for x, y in zip(a, b))

    @staticmethod
    def hamming_ints(a: tuple, b: tuple) -> int:
        return sum(x != y for x, y in zip(a, b))
