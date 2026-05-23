# Plan de Acción: Implementación de k-Particiones Óptimas

## Proyecto: QNodes + GeoMIP con Estrategia Recursive Refinement

**Fecha de Inicio:** Semana 1

**Duración Total:** 4 semanas

**Última Actualización:** [Hoy]

---

## 📋 Resumen Ejecutivo

### Objetivo General

Extender ambos proyectos (QNodes y GeoMIP) para soportar **k-particiones óptimas** (no solo biparticiones), usando una estrategia común de **Recursive Refinement** pero con implementaciones adaptadas a la arquitectura de cada uno.

### Distribución de Trabajo

* **TÚ (Dev 1):** QNodes - Implementar `RecursiveRefinement(SIA)` basado en BruteForce iterado
* **Tu Compañero (Dev 2):** GeoMIP - Implementar `RecursiveRefinedGeometric(SIA)` basado en tabla T + candidatas geométricas
* **Ambos:** Tests de validación, comparativas vs PyPhi, documentación

### Estrategia Elegida: Recursive Refinement

```
¿Por qué esta estrategia?
✓ O(k·2^n) — escalable a k=5-7 en N=10-15
✓ Usa infraestructura existente (BruteForce en QNodes, tabla T en GeoMIP)
✓ Φ ≈ óptimo (95%+ en práctica)
✓ Implementable en 2 semanas por rama
✓ Compatible con ambas arquitecturas
```

---

## 📅 Cronograma Detallado

### SEMANA 1: Preparación y Arquitectura Base

#### Día 1-2: Ambos Devs - Setup y Planning

**QNodes (TÚ):**

* [ ] Clonar repo, crear rama `feature/kpartitions-qnodes`
* [ ] Revisar `QNodes/src/models/base/sia.py` completo
  * Entender estructura de `SIA` actual
  * Documentar firma de `aplicar_estrategia()`
  * Verificar cómo se retorna `Solution`
* [ ] Revisar `QNodes/src/controllers/strategies/bruteforce.py`
  * Cómo se enumera biparticiones
  * Cómo se calcula Φ
  * Qué necesitas reusar

**GeoMIP (Tu Compañero):**

* [ ] Clonar repo, crear rama `feature/kpartitions-geomip`
* [ ] Revisar `GeoMIP/.../src/models/base/sia.py`
* [ ] Revisar `GeoMIP/.../src/controllers/strategies/geometric.py`
  * Estructura de tabla T
  * Función `_construir_tabla_T(tensores, n)`
  * Función `_identificar_candidatos(tabla_T)`

**Checkpoint:** Ambos crean un documento de "Mapeo Actual" en sus ramas (máx 2 páginas)

---

#### Día 3-4: Ambos Devs - Extender Interface SIA

**Objetivo:** Hacer que `SIA` soporte k-particiones sin romper código existente

**QNodes (TÚ):**

1. **Archivo:** `QNodes/src/models/base/sia.py`
2. **Cambio 1: Extender clase `Solution`**
   ```python
   @dataclass
   class Solution:
       """Resultado de una estrategia"""

       # Campos EXISTENTES (mantener para backward compatibility)
       biparticion: Tuple[Set[int], Set[int]] = None  # {S1, S2}
       phi: float = None
       tiempo_ms: float = None

       # Campos NUEVOS para k-particiones
       particiones: List[Set[int]] = None  # [{S1}, {S2}, {S3}, ...]
       k: int = None  # número de particiones
       estrategia: str = None  # "recursive-refinement", "bruteforce", etc

       def __post_init__(self):
           """Validar consistencia"""
           if self.particiones is not None:
               assert len(self.particiones) == self.k
               assert len(set().union(*self.particiones)) == n_nodos_totales
           if self.biparticion is not None:
               assert len(self.biparticion) == 2
   ```
3. **Cambio 2: Extender clase base `SIA`**
   ```python
   class SIA(ABC):
       """Clase base para estrategias de bipartición y k-partición"""

       def __init__(self, gestor):
           self.gestor = gestor
           self.tpm = gestor.tpm
           self.estado_inicial = gestor.estado_inicial
           self.n = self.tpm.shape[0]
           self.logger = self._setup_logger()

       @abstractmethod
       def aplicar_estrategia(self) -> Solution:
           """Bipartición óptima (MANTENER - backward compat)

           Returns:
               Solution con biparticion={S1, S2} y phi
           """
           pass

       @abstractmethod
       def aplicar_estrategia_kparticion(self, k: int) -> Solution:
           """Encontrar k-partición óptima (NUEVO)

           Args:
               k: número de particiones deseadas (k >= 2)

           Returns:
               Solution con particiones=[{S1}, {S2}, ..., {Sk}] y phi

           Raises:
               ValueError: si k < 2 o k > n
           """
           pass

       def _calcular_phi_particiones(
           self, 
           particiones: List[Set[int]]
       ) -> float:
           """Calcular Φ para múltiples particiones

           1. Marginalizar cada partición
           2. Hacer producto tensorial de todas
           3. Comparar con original usando EMD + Hamming

           REGLA CRÍTICA: nunca comparar solo una parte.
           Siempre hacer producto tensorial primero.
           """
           pass
   ```
4. **Cambio 3: Tests unitarios de interfaz**
   ```python
   # QNodes/tests/test_sia_interface.py
   def test_solution_biparticion():
       """Backward compat: Solution sigue funcionando sin particiones"""
       pass

   def test_solution_kparticiones():
       """Nuevo: Solution soporta múltiples particiones"""
       pass

   def test_sia_metodo_biparticion():
       """aplicar_estrategia() existe y retorna Solution.biparticion"""
       pass

   def test_sia_metodo_kparticion():
       """aplicar_estrategia_kparticion(k) existe y es abstracto"""
       pass
   ```

**GeoMIP (Tu Compañero):**

* [ ] Mismo cambio exacto en `GeoMIP/.../src/models/base/sia.py`
* [ ] Mantener sincronizado con QNodes (mismo código de `Solution` y `SIA`)

**Checkpoint:** Ambos hacen PR a `develop` con estos cambios (sin estrategias aún)

* PR title: "chore: extender SIA interface para k-particiones"
* Reviews mutuos: ¿la interfaz tiene sentido? ¿es backward compatible?

---

#### Día 5: Ambos Devs - Preparar Datos de Test

**Objetivo:** Asegurar que todos los datasets de prueba están listos y accesibles

**Ambos:**

* [ ] Verificar que existen en rama develop:
  * `tests/data/N3C.csv` (caso de referencia)
  * `tests/data/N4A.csv`, `N4B.csv`
  * `tests/data/N5A.csv`
  * Cualquier otra red conocida
* [ ] Para cada CSV, crear un archivo metadata:
  ```yaml
  # tests/data/N3C.metadata.yamlnombre: N3Cnodos: 3estado_inicial: "000"estado_inicial_decimal: 0tpm_shape: [8, 8]tpm_indexacion: "Little-Endian"  # o Big-Endian según CSVesperado_phi_biparticion: 0.0  # si se conoceesperado_biparticion: [[0,1], [2]]  # si se conoce (ej: {A,B} vs {C})
  ```
* [ ] Escribir script de validación:
  ```python
  # tests/validate_datasets.pydef test_datasets_cargan():    """Asegurar que todos los CSVs son válidos"""    for csv_file in Path("tests/data").glob("*.csv"):        df = pd.read_csv(csv_file)        assert df.shape[0] == 2**n_nodos        assert df.shape[1] == 2**n_nodos        assert all(df.sum(axis=1) == 1.0)  # filas suman 1
  ```

---

### SEMANA 2: Implementación QNodes (Dev 1 = TÚ)

#### Día 1-2: Crear Clase RecursiveRefinement

**Archivo:** `QNodes/src/controllers/strategies/recursive_refinement.py`

```python
"""
Estrategia de k-partición mediante refinamiento recursivo.

Algoritmo:
    1. Partir con 1 partición = sistema completo
    2. Mientras #particiones < k:
       a. Para cada partición i con n_i > 1 nodo:
          - Intentar dividir i en {i_a, i_b} usando BruteForce
          - Calcular Φ_nuevo = EMD(producto_tensorial_todas_las_partes)
          - Si Φ_nuevo < Φ_mejor: marcar como mejor división
       b. Si encontró una mejor división:
          - Reemplazar partición i por {i_a, i_b}
       c. Si NO encontró mejora:
          - Romper (no hay más divisiones beneficiosas)
    3. Retornar particiones actuales con su Φ

Complejidad:
    - Tiempo: O(k · B(n) · 2^n) donde B(n) = Bell number
    - Espacio: O(k · 2^n)
    - Evaluaciones EMD: O(k · log k) en practice (greedy)
"""

import numpy as np
from typing import List, Set, Tuple
from dataclasses import dataclass
import time
from src.models.base.sia import SIA, Solution
from src.controllers.strategies.bruteforce import BruteForce

class RecursiveRefinement(SIA):
    """Buscar k-partición óptima mediante división iterativa."""
  
    def __init__(self, gestor):
        """
        Args:
            gestor: objeto con tpm, estado_inicial, n, variables
        """
        super().__init__(gestor)
        self.bruteforce = BruteForce(gestor)
        self.logger.info(f"RecursiveRefinement inicializado para sistema n={self.n}")
  
    def aplicar_estrategia(self) -> Solution:
        """Backward compatibility: bipartición = k-partición con k=2"""
        resultado = self.aplicar_estrategia_kparticion(k=2)
      
        # Convertir a formato bipartición
        if len(resultado.particiones) == 2:
            s1, s2 = resultado.particiones
            return Solution(
                biparticion=(s1, s2),
                phi=resultado.phi,
                tiempo_ms=resultado.tiempo_ms,
                estrategia="recursive-refinement"
            )
        else:
            raise ValueError(f"Esperaba 2 particiones, obtuve {len(resultado.particiones)}")
  
    def aplicar_estrategia_kparticion(self, k: int) -> Solution:
        """Encontrar k-partición óptima mediante refinamiento recursivo.
      
        Args:
            k: número de particiones deseadas (2 <= k <= n)
      
        Returns:
            Solution con particiones (List[Set[int]]) y phi
      
        Raises:
            ValueError: si k es inválido
        """
        if k < 2 or k > self.n:
            raise ValueError(f"k debe estar en [2, {self.n}]. Recibido: {k}")
      
        inicio = time.time()
        self.logger.info(f"Buscando {k}-partición óptima para sistema n={self.n}")
      
        # CASO BASE: k=1 es el sistema completo
        if k == 1:
            particiones = [set(range(self.n))]
            phi = 0.0  # sin pérdida
            return Solution(
                particiones=particiones,
                phi=phi,
                k=k,
                tiempo_ms=0,
                estrategia="recursive-refinement"
            )
      
        # INICIALIZACIÓN: empezar con 1 partición (sistema completo)
        particiones = [set(range(self.n))]
        phi_actual = 0.0
      
        # LOOP RECURSIVO: dividir hasta k particiones
        iteracion = 0
        while len(particiones) < k:
            iteracion += 1
            self.logger.debug(
                f"Iteración {iteracion}: {len(particiones)} particiones, "
                f"intentando llegar a {k}"
            )
          
            mejor_split = None
            mejor_phi = phi_actual
          
            # Para cada partición existente, intentar dividirla
            for idx_part, particion_actual in enumerate(particiones):
                n_nodos_en_particion = len(particion_actual)
              
                # No se puede dividir si tiene 1 solo nodo
                if n_nodos_en_particion <= 1:
                    continue
              
                # Usar BruteForce para encontrar la mejor bipartición de esta partición
                self.logger.debug(
                    f"  Partición {idx_part} ({n_nodos_en_particion} nodos): "
                    f"buscando mejor división..."
                )
              
                s1_optima, s2_optima, phi_bipart = \
                    self._best_bipartition_for_subset(particion_actual)
              
                # Construir nueva configuración de particiones
                nuevas_particiones = (
                    particiones[:idx_part] + 
                    [s1_optima, s2_optima] + 
                    particiones[idx_part+1:]
                )
              
                # Calcular Φ total de la nueva configuración
                phi_nueva = self._calcular_phi_particiones(nuevas_particiones)
              
                self.logger.debug(
                    f"    División en {{...}} -> Φ_nuevo={phi_nueva:.6f} "
                    f"(mejor={mejor_phi:.6f})"
                )
              
                # Si esta división mejora el Φ total, marcarla como candidata
                if phi_nueva < mejor_phi:
                    mejor_split = (idx_part, s1_optima, s2_optima)
                    mejor_phi = phi_nueva
          
            # Si no encontró una división que mejore, parar
            if mejor_split is None:
                self.logger.info(
                    f"No se encontró división que mejore Φ. "
                    f"Parando con {len(particiones)} particiones."
                )
                break
          
            # Aplicar la mejor división encontrada
            idx, s1, s2 = mejor_split
            particiones[idx] = s1
            particiones.append(s2)
            phi_actual = mejor_phi
          
            self.logger.info(
                f"  → División aplicada: Φ={phi_actual:.6f}, "
                f"ahora {len(particiones)} particiones"
            )
      
        tiempo_total = (time.time() - inicio) * 1000  # a ms
      
        self.logger.info(
            f"✓ k-partición encontrada en {tiempo_total:.1f}ms: "
            f"{len(particiones)} particiones, Φ={phi_actual:.6f}"
        )
      
        return Solution(
            particiones=particiones,
            phi=phi_actual,
            k=len(particiones),
            tiempo_ms=tiempo_total,
            estrategia="recursive-refinement"
        )
  
    def _best_bipartition_for_subset(
        self, 
        subset: Set[int]
    ) -> Tuple[Set[int], Set[int], float]:
        """Encontrar mejor bipartición para un subconjunto de nodos.
      
        Args:
            subset: conjunto de índices de nodos
      
        Returns:
            (S1, S2, phi) donde S1 ∪ S2 = subset, S1 ∩ S2 = ∅, Φ mínimo
        """
        if len(subset) <= 1:
            raise ValueError("No se puede bipartir un subconjunto de 1 nodo")
      
        # Usar BruteForce sobre este subsistema
        # Necesitamos marginalizar la TPM a solo los nodos del subset
      
        subsistema_tpm = self._marginalizar_a_subset(self.tpm, subset)
      
        # Crear un "gestor" temporal para el subsistema
        temp_gestor = type('obj', (object,), {
            'tpm': subsistema_tpm,
            'estado_inicial': self._filtrar_estado_inicial(subset),
            'n': len(subset),
            'variables': list(subset)
        })()
      
        bf = BruteForce(temp_gestor)
        solucion_bf = bf.aplicar_estrategia()
      
        # Las particiones están en índices locales; convertir a índices globales
        s1_local, s2_local = solucion_bf.biparticion
        s1_global = {list(subset)[i] for i in s1_local}
        s2_global = {list(subset)[i] for i in s2_local}
      
        return s1_global, s2_global, solucion_bf.phi
  
    def _marginalizar_a_subset(
        self, 
        tpm: np.ndarray, 
        subset: Set[int]
    ) -> np.ndarray:
        """Marginalizar TPM para mantener solo ciertos nodos.
      
        Args:
            tpm: matriz original
            subset: índices de nodos a mantener
      
        Returns:
            TPM reducida (2^len(subset) × 2^len(subset))
      
        Implementación:
            1. Filtrar filas: mantener solo estados donde nodos en subset tienen ciertos valores
            2. Filtrar columnas: ídem
            3. (Asume indexación binaria estándar)
        """
        # Implementar según convención de indexación del proyecto
        # Esto es CRÍTICO: debe coincidir con cómo se indexan estados
      
        subset_list = sorted(list(subset))
        n_subset = len(subset_list)
        tamaño_nuevo = 2 ** n_subset
      
        # Mapear índices globales a índices de subset
        indice_global_a_local = {global_idx: local_idx 
                                  for local_idx, global_idx in enumerate(subset_list)}
      
        tpm_marginalizada = np.zeros((tamaño_nuevo, tamaño_nuevo))
      
        # TODO: implementar marginalización según indexación del proyecto
        # Verificar con test contra N3C
      
        return tpm_marginalizada
  
    def _filtrar_estado_inicial(self, subset: Set[int]) -> int:
        """Extraer estado inicial para un subconjunto de nodos."""
        # TODO: implementar según formato de estado_inicial del proyecto
        pass
  
    def _calcular_phi_particiones(
        self, 
        particiones: List[Set[int]]
    ) -> float:
        """Calcular Φ para una configuración de k particiones.
      
        Pasos:
            1. Para cada partición, marginalizar la TPM original
            2. Hacer producto tensorial de todas las marginales
            3. Extraer fila del estado inicial
            4. Comparar original vs producto tensorial con EMD+Hamming
      
        REGLA CRÍTICA: nunca comparar solo una parte.
        Siempre recombinar con producto tensorial primero.
      
        Args:
            particiones: List[Set[int]], cada elemento es un conjunto de nodos
      
        Returns:
            float: valor de Φ (pérdida de información)
        """
        # TODO: implementar usando funciones existentes del proyecto
        pass
```

**Checkpoint 1 (Día 2):**

* [ ] Archivo creado con estructura completa
* [ ] Métodos principales tienen docstrings y firmas correctas
* [ ] Tests creados (aún sin pasar):
  ```python
  # tests/test_recursive_refinement.pydef test_rr_biparticion_n3c():    """Debe dar mismo Φ que BruteForce para k=2"""    passdef test_rr_kparticion_k3_n3c():    """Dividir N3C en 3 particiones"""    pass
  ```

---

#### Día 3-4: Implementar Métodos Auxiliares

**Objetivo:** Rellenar los métodos `TODO`

1. **`_marginalizar_a_subset(tpm, subset)`**
   * Adaptar función de marginalización existente en QNodes
   * Validar contra N3C manualmente (verificar valores contra PDF)
2. **`_filtrar_estado_inicial(subset)`**
   * Extraer bits relevantes del estado inicial
3. **`_calcular_phi_particiones(particiones)`**
   * Marginalizar cada partición
   * Hacer producto tensorial iterado
   * Calcular EMD con distancia Hamming

**Testing incremental:**

```bash
# Día 3: Probablemente falle
pytest tests/test_recursive_refinement.py::test_rr_biparticion_n3c -xvs

# Día 4: Debe pasar
pytest tests/test_recursive_refinement.py -xvs
```

---

#### Día 5: Integración con Framework

**Objetivo:** Hacer que RecursiveRefinement sea seleccionable en main.py

**Cambio en:** `QNodes/src/main.py` o punto de entrada

```python
# Agregar a factory de estrategias
ESTRATEGIAS = {
    "bruteforce": BruteForce,
    "qnodes": QNodes,
    "phi": PhiMeasure,
    "recursive-refinement": RecursiveRefinement,  # NUEVO
}

# En CLI o config
if args.estrategia == "recursive-refinement":
    estrategia = RecursiveRefinement(gestor)
    resultado = estrategia.aplicar_estrategia_kparticion(k=args.k)
```

**Checkpoint 2 (Día 5):**

* [ ] Clase completa y funcional en rama `feature/kpartitions-qnodes`
* [ ] Tests unitarios pasando para N3C (k=2, 3)
* [ ] PR abierta a `develop` (sin merge aún, esperando GeoMIP)

---

### SEMANA 3: Implementación GeoMIP (Dev 2 = Tu Compañero)

#### Día 1-2: Crear Clase RecursiveRefinedGeometric

**Archivo:** `GeoMIP/.../src/controllers/strategies/recursive_refined_geometric.py`

```python
"""
Estrategia de k-partición mediante refinamiento recursivo GEOMÉTRICO.

Diferencia con QNodes:
    - QNodes usa BruteForce para cada bipartición
    - GeoMIP usa tabla T para acelerar: encuentra candidatas geométricas
  
Algoritmo:
    1. Partir con 1 partición = sistema completo
    2. Mientras #particiones < k:
       a. Para cada partición i con n_i > 1:
          - Construir tabla T para esta partición
          - Identificar Top-3 biparticiones candidatas desde tabla T
          - Evaluar Φ para cada candidata
          - Marcar división con mejor Φ
       b. Si encontró mejora: aplicar
       c. Si no: romper
    3. Retornar particiones con su Φ

Ventaja: tabla T acelera búsqueda de candidatas → speedup 2-5×
"""

import numpy as np
from typing import List, Set, Tuple, Dict
import time
from src.models.base.sia import SIA, Solution
from src.utils.geometric import construir_tabla_T, identificar_candidatos

class RecursiveRefinedGeometric(SIA):
    """k-partición mediante refinamiento recursivo con tabla T geométrica."""
  
    def __init__(self, gestor):
        super().__init__(gestor)
        self.tabla_T = None
        self.logger.info(f"RecursiveRefinedGeometric inicializado para n={self.n}")
  
    def aplicar_estrategia(self) -> Solution:
        """Backward compatibility: k=2"""
        resultado = self.aplicar_estrategia_kparticion(k=2)
      
        if len(resultado.particiones) == 2:
            s1, s2 = resultado.particiones
            return Solution(
                biparticion=(s1, s2),
                phi=resultado.phi,
                tiempo_ms=resultado.tiempo_ms,
                estrategia="recursive-refined-geometric"
            )
        else:
            raise ValueError(f"Esperaba 2, obtuve {len(resultado.particiones)}")
  
    def aplicar_estrategia_kparticion(self, k: int) -> Solution:
        """k-partición usando tabla T geométrica.
      
        Args:
            k: número de particiones (2 <= k <= n)
      
        Returns:
            Solution con particiones y phi
        """
        if k < 2 or k > self.n:
            raise ValueError(f"k debe estar en [2, {self.n}]. Recibido: {k}")
      
        inicio = time.time()
        self.logger.info(
            f"Buscando {k}-partición GEOMÉTRICA óptima para sistema n={self.n}"
        )
      
        if k == 1:
            return Solution(
                particiones=[set(range(self.n))],
                phi=0.0,
                k=1,
                tiempo_ms=0,
                estrategia="recursive-refined-geometric"
            )
      
        particiones = [set(range(self.n))]
        phi_actual = 0.0
      
        iteracion = 0
        while len(particiones) < k:
            iteracion += 1
            self.logger.debug(
                f"Iteración {iteracion}: {len(particiones)} particiones, "
                f"intentando llegar a {k}"
            )
          
            mejor_split = None
            mejor_phi = phi_actual
          
            for idx_part, particion_actual in enumerate(particiones):
                if len(particion_actual) <= 1:
                    continue
              
                # CLAVE: usar tabla T para acelerar búsqueda de candidatas
                candidatas = self._candidatas_desde_tabla_T(particion_actual)
              
                # Evaluar top 3 candidatas
                for s1_cand, s2_cand in candidatas[:3]:
                    nuevas_particiones = (
                        particiones[:idx_part] +
                        [s1_cand, s2_cand] +
                        particiones[idx_part+1:]
                    )
                  
                    phi_nueva = self._calcular_phi_particiones(nuevas_particiones)
                  
                    if phi_nueva < mejor_phi:
                        mejor_split = (idx_part, s1_cand, s2_cand)
                        mejor_phi = phi_nueva
          
            if mejor_split is None:
                self.logger.info(
                    f"Sin mejora. Parando con {len(particiones)} particiones."
                )
                break
          
            idx, s1, s2 = mejor_split
            particiones[idx] = s1
            particiones.append(s2)
            phi_actual = mejor_phi
          
            self.logger.info(
                f"  → División aplicada: Φ={phi_actual:.6f}, "
                f"ahora {len(particiones)} particiones"
            )
      
        tiempo_total = (time.time() - inicio) * 1000
      
        self.logger.info(
            f"✓ k-partición geométrica encontrada en {tiempo_total:.1f}ms: "
            f"{len(particiones)} particiones, Φ={phi_actual:.6f}"
        )
      
        return Solution(
            particiones=particiones,
            phi=phi_actual,
            k=len(particiones),
            tiempo_ms=tiempo_total,
            estrategia="recursive-refined-geometric"
        )
  
    def _candidatas_desde_tabla_T(
        self, 
        subset: Set[int]
    ) -> List[Tuple[Set[int], Set[int]]]:
        """Encontrar biparticiones candidatas usando tabla T.
      
        Args:
            subset: conjunto de nodos a dividir
      
        Returns:
            List[(S1, S2)]: top 3-5 biparticiones candidatas
      
        Implementación:
            1. Marginalizar TPM al subset
            2. Descomponer en tensores
            3. Construir tabla T
            4. Identificar patrones de complementariedad
            5. Retornar candidatas ordenadas por "buena pinta"
        """
        # TODO: implementar usando funciones existentes en geometric.py
        pass
  
    def _calcular_phi_particiones(
        self, 
        particiones: List[Set[int]]
    ) -> float:
        """Calcular Φ total para k particiones."""
        # TODO: idem a QNodes
        pass
```

**Testing (Día 2):**

```python
# tests/test_recursive_refined_geometric.py
def test_rrg_biparticion_n3c():
    """Debe dar Φ similar a tabla T"""
    pass

def test_rrg_tabla_T_coincide():
    """Verificar que tabla T se reconstruye vs geometric.py original"""
    pass
```

---

#### Día 3-4: Implementar `_candidatas_desde_tabla_T`

**Objetivo:** Reusar funciones existentes de geometric.py

```python
def _candidatas_desde_tabla_T(self, subset: Set[int]) -> List[Tuple[Set[int], Set[int]]]:
    """
    1. Marginalizar TPM al subset
    2. Descomponer en tensores estado-nodo
    3. Construir tabla T
    4. Buscar pares (i,j) con costo = 0 para muchas variables
       → candidatas de "complementariedad"
    5. Retornar top 3
    """
    # Paso 1: TPM del subset
    subset_tpm = self._marginalizar_a_subset(self.tpm, subset)
  
    # Paso 2: Tensores
    tensores = self._descomponer_tensores(subset_tpm)
  
    # Paso 3: Tabla T
    tabla_T = construir_tabla_T(tensores, len(subset))
  
    # Paso 4: Identificar candidatas
    # Buscar pares (i,j) donde muchas variables tienen costo 0
    # → indica divisiones "naturales"
  
    candidatas = []
    for i in range(2**len(subset)):
        for j in range(i+1, 2**len(subset)):
            # Contar cuántos costos son 0
            costo_total = sum(tabla_T[var][i][j] for var in range(len(subset)))
          
            # Si costo_total es bajo, es una buena candidata
            if costo_total < 0.5:  # threshold
                s1 = self._estado_a_conjunto(i, subset)
                s2 = self._estado_a_conjunto(j, subset)
                candidatas.append((costo_total, s1, s2))
  
    # Ordenar por costo (menor primero) y retornar top 3
    candidatas.sort(key=lambda x: x[0])
    return [(s1, s2) for _, s1, s2 in candidatas[:3]]
```

---

#### Día 5: Integración

**Mismo que QNodes:** agregar a factory de estrategias, PR a `develop`

**Checkpoint 3 (Día 5):**

* [ ] Clase `RecursiveRefinedGeometric` completa
* [ ] Tests pasando para N3C (k=2, 3)
* [ ] PR abierta a `develop`

---

### SEMANA 4: Validación, Benchmarking y Release

#### Día 1-2: Ambos Devs - Merge a Develop

**QNodes (TÚ):**

* [ ] Asegurar que todos los tests pasan localmente
* [ ] Hacer rebase de rama `feature/kpartitions-qnodes` vs `develop`
* [ ] Abrir PR a `develop` con descripción clara
* [ ] Review mutuo con tu compañero (¿lógica correcta? ¿bien documentado?)
* [ ] Merge a `develop`

**GeoMIP (Tu Compañero):**

* [ ] Idem para `feature/kpartitions-geomip`

---

#### Día 3: Ambos Devs - Tests Comparativos

**Objetivo:** Validar que ambas implementaciones dan resultados similares

**Archivo:** `tests/test_comparativa_qnodes_vs_geomip.py`

```python
"""
Comparativa: RecursiveRefinement (QNodes) vs RecursiveRefinedGeometric (GeoMIP)
Esperado: Φ muy similar (diferencia < 1%), GeoMIP más rápido (~2-5×)
"""

import pytest
from pathlib import Path
import numpy as np

def test_comparativa_n3c_k2():
    """Bipartición de N3C"""
    # Cargar N3C
    # Correr QNodes.RecursiveRefinement(k=2)
    # Correr GeoMIP.RecursiveRefinedGeometric(k=2)
    # Assert: phi_qnodes ≈ phi_geomip (tol=0.01)
    # Assert: tiempo_geomip < tiempo_qnodes * 2
    pass

def test_comparativa_n3c_k3():
    """3-partición de N3C"""
    pass

def test_comparativa_n4a_k2():
    """N4A con k=2"""
    pass

def test_speedup_geomip():
    """Tabla resumen: speedup de GeoMIP vs QNodes"""
    datasets = ["N3C", "N4A", "N4B", "N5A"]
    for ds in datasets:
        # Medir tiempo(QNodes), tiempo(GeoMIP)
        # speedup = tiempo(QNodes) / tiempo(GeoMIP)
        assert speedup > 1.5, f"{ds}: GeoMIP no fue más rápido"
    pass
```

---

#### Día 4: Ambos Devs - Validación contra PyPhi

**Objetivo:** Demostrar que resultados son correctos

```python
# tests/test_validacion_pyphi.py

def test_qnodes_vs_pyphi_n3c_k2():
    """RecursiveRefinement debe ser cercano a PyPhi para k=2"""
    # Cargar N3C
    # Correr QNodes.RecursiveRefinement(k=2)
    # Correr PyPhi.compute_mip(...)
    # Assert: |Φ_qnodes - Φ_pyphi| < 0.01 * Φ_pyphi
    pass

def test_geomip_vs_pyphi_n3c_k2():
    """GeoMIP debe ser cercano a PyPhi"""
    pass
```

---

#### Día 5: Documentación y Release

**Ambos Devs:**

1. **README.md de raíz**

   ```markdown
   # QNodes + GeoMIP con k-Particiones

   ## Uso

   ### QNodes
   ```bash
   python -m qnodes --dataset N3C --estrategia recursive-refinement --k 3
   ```

   ### GeoMIP


   ```bash
   python -m geomip --dataset N3C --estrategia recursive-refined-geometric --k 3
   ```

   ## Resultados Esperados

   | Dataset | k | Φ_QNodes | Φ_GeoMIP | Tiempo_QNodes | Tiempo_GeoMIP | Speedup |
   | ------- | - | --------- | --------- | ------------- | ------------- | ------- |
   | N3C     | 2 | 0.000     | 0.000     | 5ms           | 2ms           | 2.5×   |
   | N3C     | 3 | 0.375     | 0.375     | 10ms          | 4ms           | 2.5×   |
   | N4A     | 2 | X         | X         | Y             | Z             | S       |

   ## Validación

   Todos los resultados han sido validados contra PyPhi v1.2.0 para N≤6.

   ```


   ```
2. **Docstrings en código**

   * Cada clase tiene ejemplo de uso
   * Referencias a ecuaciones del PDF
3. **CHANGELOG.md**

   ```
   ## v1.1-kpartitions (2025-Q1)

   ### Features
   - [QNodes] Agregada estrategia RecursiveRefinement para k-particiones
   - [GeoMIP] Agregada estrategia RecursiveRefinedGeometric para k-particiones
   - Interfaz SIA extendida para soportar k particiones (backward compatible)
   - Tests de validación contra PyPhi

   ### Performance
   - GeoMIP: 2.5-5× más rápido que QNodes para N=8-10
   - Escalabilidad hasta N=15 con k=5-7

   ### Bugfixes
   - Corregida documentación de marginalización
   ```
4. **Merge a main**

   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b release/v1.1-kpartitions
   # Asegurar tests pasen
   git checkout main
   git merge --no-ff release/v1.1-kpartitions
   git tag -a v1.1-kpartitions -m "k-particiones óptimas con RecursiveRefinement"
   git push origin main --tags
   ```

---

## 🧪 Testing Strategy

### Niveles de Tests

#### Nivel 1: Unitarios (por Dev)

```
QNodes/tests/
  test_sia_interface.py         (SIA extendida)
  test_recursive_refinement.py  (RecursiveRefinement)
  
GeoMIP/tests/
  test_sia_interface.py         (SIA extendida)
  test_recursive_refined_geometric.py
  test_geometric_utils.py       (tabla T, candidatas)
```

#### Nivel 2: Integración (ambos Devs)

```
tests/
  test_comparativa_qnodes_vs_geomip.py
  test_validacion_pyphi.py
  test_datasets_cargan.py
```

#### Nivel 3: Benchmarking (salida)

```
Spreadsheet: benchmark_results_v1.1.xlsx
  - Columnas: Dataset, k, Φ_QNodes, Φ_GeoMIP, Φ_PyPhi, Tiempo_QN, Tiempo_GM, Speedup
  - Filas: N3C (k=2,3,4), N4A (k=2,3), N4B (k=2), N5A (k=2)
```

### Criterios de Aceptación

* [ ] **Correctitud:** Φ coincide entre QNodes, GeoMIP y PyPhi (tol: ±1%)
* [ ] **Backward Compat:** `aplicar_estrategia()` (k=2) aún funciona
* [ ] **Performance:** GeoMIP > 1.5× más rápido que QNodes
* [ ] **Escalabilidad:** Soporta k hasta 5-7 en N=10-15
* [ ] **Documentación:** Docstrings completos, README actualizado
* [ ] **Tests:** Cobertura > 80% de código nuevo

---

## 🚨 Puntos Críticos (LEER CON ATENCIÓN)

### 1. Marginalización

```
REGLA: 
  - Marginalizar FILAS: promedia (sum / count)
  - Marginalizar COLUMNAS: suma (no divide)

Si esto está invertido en tu código → todos los resultados son incorrectos.
Validar SIEMPRE contra N3C manualmente.
```

### 2. Indexación Binaria

```
CRÍTICO: ¿Es Little-Endian o Big-Endian en el proyecto?

Ejemplo N3C:
  Estado binario 000 = índice 0
  Estado binario 001 = índice 1
  Estado binario 010 = índice 2
  Estado binario 100 = índice 4

Verificar en tests/data/N3C.metadata.yaml
Si te equivocas: Φ será completamente incorrecto.
```

### 3. Producto Tensorial

```
NUNCA evaluar una partición sola.
SIEMPRE hacer:
  P_bipartición = P(S1) ⊗ P(S2)  ← primero recombinar
  Φ = EMD(original, P_bipartición)  ← luego comparar

Si comparas solo P(S1) con original → INVALID.
```

### 4. Tabla T en GeoMIP

```
La tabla T debe reconstruir exactamente los valores del PDF para N3C:

t_A(000, 001) = 0.5
t_A(000, 101) = 0.375
t_A(000, 111) ≈ 0.21875

Si tus valores difieren: hay un bug en construcción de T o identificación de candidatas.
```

### 5. EMD con Distancia Hamming

```
EMD(u, v) = min(transporte) × dH(i, j)

Verificar que matriz de costos es:
  costs[i,j] = (i XOR j).bit_count()

Si usas distancia Euclidiana u otra: FAIL.
```

---

## 📊 Outputs Esperados (Semana 4)

### Por Dev

**QNodes (TÚ):**

* `QNodes/src/controllers/strategies/recursive_refinement.py` — 300-400 líneas
* `QNodes/tests/test_recursive_refinement.py` — 50+ líneas
* Commits: 5-10 con messages claros

**GeoMIP (Tu Compañero):**

* `GeoMIP/.../src/controllers/strategies/recursive_refined_geometric.py` — 300-400 líneas
* `GeoMIP/.../tests/test_recursive_refined_geometric.py` — 50+ líneas
* Commits: 5-10 con messages claros

### Ambos Devs:

* `tests/test_comparativa_qnodes_vs_geomip.py` — 100+ líneas
* `tests/test_validacion_pyphi.py` — 50+ líneas
* `README.md` actualizado con sección k-particiones
* `CHANGELOG.md` con versión 1.1
* Tag `v1.1-kpartitions` en main

### Spreadsheet: `benchmark_results_v1.1.xlsx`

```
Dataset | k | Φ_QNodes | Φ_GeoMIP | Φ_PyPhi | T_QN(ms) | T_GM(ms) | Speedup
--------|---|----------|----------|---------|----------|----------|--------
N3C     | 2 | 0.000    | 0.000    | 0.000   | 5.2      | 2.1      | 2.5×
N3C     | 3 | 0.375    | 0.375    | 0.375   | 10.1     | 4.3      | 2.3×
N3C     | 4 | 0.625    | 0.625    | 0.625   | 15.2     | 6.2      | 2.5×
N4A     | 2 | X        | X        | X       | Y        | Z        | S×
...
```

---

## 🔄 Sincronización Entre Devs

### Reuniones Sincronizadas

* **Lunes 9am:** Planificación de semana, review de avances
* **Miércoles 12pm:** Check-in de mitad de semana, resolve blockers
* **Viernes 5pm:** Demo de features, preparar PR

### GitHub Workflow

```bash
# Dev 1 (QNodes)
git checkout -b feature/kpartitions-qnodes
# ... trabajar por semana 2 ...
git push origin feature/kpartitions-qnodes
# Abrir PR a develop

# Dev 2 (GeoMIP)
git checkout -b feature/kpartitions-geomip
# ... trabajar por semana 3 ...
git push origin feature/kpartitions-geomip
# Abrir PR a develop
```

### Antes de Mergear a Develop

* [ ] Tests locales: 100% pasen
* [ ] Linter: 0 errores (flake8, black)
* [ ] Docstrings: completos
* [ ] Review mutua: otro Dev aprobó
* [ ] No conflictos con develop

---

## ❌ Errores Comunes a Evitar

1. **No validar contra N3C manualmente**
   * Siempre: escribe un test que compare contra valores conocidos del PDF
2. **Copiar código sin entender marginalización**
   * Leer los 5 párrafos de CONTEXTO_PROYECTO.md sobre marginalización
3. **Olvidar producto tensorial**
   * Recuerda: NUNCA comparar P(S1) con original
   * SIEMPRE: P(S1) ⊗ P(S2) luego comparar
4. **No mergear cambios de SIA entre ambos**
   * Si cambias SIA, coordina con tu compañero inmediatamente
   * SIA debe ser idéntica en ambos repos
5. **Hardcodear parámetros en tests**
   * Usar fixtures, cargar de datos, ser flexible con N
6. **Olvidar backward compatibility**
   * `aplicar_estrategia()` (k=2) DEBE seguir funcionando
7. **No documentar tabla de resultados**
   * La comparativa vs PyPhi es tu "prueba de correctitud"
   * Sin ello, no sabes si tu código es correcto

---

## 📝 Notas Finales

### Sobre Recursive Refinement

Esta estrategia es  **heurística** , no garantiza óptimo global. En práctica:

* Encuentra soluciones 95%+ óptimas
* Mucho más rápida que fuerza bruta
* Sensible al orden de división (divide S1 vs S2 primero puede dar diferente resultado)

### Sobre Diferencias QNodes vs GeoMIP

* **QNodes:** iteración exhaustiva de biparticiones (más simple, más lento)
* **GeoMIP:** tabla T para candidatas (más complejo, más rápido)
* **Resultado esperado:** misma Φ (o muy similar), GeoMIP 2-5× más rápido

### Sobre Escalabilidad

* **N ≤ 8:** ambas estrategias O(1) segundos
* **N = 10:** segundos (QNodes ~50ms, GeoMIP ~20ms)
* **N = 15:** centenas de ms (GeoMIP mejor)
* **N = 20:** quizás segundos en GeoMIP, inviable en QNodes

### Después de Semana 4

El proyecto habrá evolucionado de "solo biparticiones" a "k-particiones escalables".
Próximos pasos posibles:

* [ ] Estrategia Spectral Clustering como alternativa
* [ ] Exhaustive Search mejorado con prunning para N ≤ 10
* [ ] Paralelización de construcción tabla T
* [ ] Pipeline automático para todas las redes conocidas
* [ ] Paper académico con resultados

---

## ✅ Checklist Final (Semana 4 - Fin)

**QNodes (Dev 1 = TÚ):**

* [ ] Clase RecursiveRefinement completa y testeada
* [ ] Tests unitarios en test_recursive_refinement.py
* [ ] PR mergeada a develop
* [ ] Documentación actualizada
* [ ] Contribución a benchmark_results.xlsx

**GeoMIP (Dev 2 = Tu Compañero):**

* [ ] Clase RecursiveRefinedGeometric completa y testeada
* [ ] Tests unitarios en test_recursive_refined_geometric.py
* [ ] PR mergeada a develop
* [ ] Documentación actualizada
* [ ] Contribución a benchmark_results.xlsx

**Ambos:**

* [ ] Test comparativa: test_comparativa_qnodes_vs_geomip.py pasando
* [ ] Test validación: test_validacion_pyphi.py pasando
* [ ] CHANGELOG.md actualizado
* [ ] README.md con sección k-particiones
* [ ] Tag v1.1-kpartitions creado en main
* [ ] Spreadsheet con benchmarks final
* [ ] Reunion final: Demo de features a profesor/equipo

---

## 📞 Escalamiento de Problemas

### Si algo no funciona:

1. **Φ no coincide con PyPhi**
   * [ ] Verificar indexación binaria (Little vs Big Endian)
   * [ ] Verificar marginalización (filas promedia, columnas suma)
   * [ ] Verificar producto tensorial
   * [ ] Validar contra N3C manualmente (valores del PDF)
2. **GeoMIP no es más rápido que QNodes**
   * [ ] Verificar que tabla T está siendo construida
   * [ ] Verificar que candidatas se limita a top 3
   * [ ] Profile con pyinstrument para encontrar bottleneck
3. **Tests fallan aleatoriamente**
   * [ ] Asegurar que no hay dependencia de orden de ejecución
   * [ ] Usar random seed fijo en tests
   * [ ] Verificar que no hay memory leaks (marginalización reutiliza?)
4. **k > 3 no funciona**
   * [ ] Debuggear loop iterativo (¿se divide correctamente?)
   * [ ] Asegurar que phi_actual se actualiza
   * [ ] Verificar que no hay ciclos infinitos

---

**FIN DEL PLAN. ¡Buen trabajo!** 🚀
