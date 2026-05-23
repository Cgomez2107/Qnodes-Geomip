# 📚 Documentación Completa del Proyecto

## QNodes + GeoMIP: Bipartición Óptima de Información Integrada

**Última Actualización:** [Hoy]
**Estado:** Activo - Expandiendo a k-particiones
**Repositorio:** [Tu URL]

---

## 📖 Tabla de Contenidos

1. [Contexto Académico](#contexto-académico)
2. [Problema Central](#problema-central)
3. [Fundamentos Teóricos](#fundamentos-teóricos)
4. [Estructura del Repositorio](#estructura-del-repositorio)
5. [Arquitectura Actual](#arquitectura-actual)
6. [QNodes (Framework Base)](#qnodes-framework-base)
7. [GeoMIP (Extensión Geométrica)](#geomip-extensión-geométrica)
8. [Estado Actual del Código](#estado-actual-del-código)
9. [Convenciones y Estándares](#convenciones-y-estándares)
10. [Datos de Prueba](#datos-de-prueba)
11. [Próximos Pasos: k-Particiones](#próximos-pasos-k-particiones)

---

## 📖 Contexto Académico

### Asignatura

- **Nombre:** Análisis y Diseño de Algoritmos
- **Institución:** [Universidad del Cauca, Pasto, Colombia]
- **Período Lectivo:** 2025C
- **Tema Central:** Optimización de algoritmos para problemas NP-Hard combinatorios

### Motivación del Proyecto

El proyecto nace de una **pregunta fundamental en teoría de la información integrada (IIT)**:

> *"Dado un sistema de n variables binarias con dinámica temporal, ¿cuál es la forma de dividir el sistema en subsistemas independientes que minimice la pérdida de información sobre su comportamiento?"*

Esta pregunta es relevante para:

- Neurociencia: entender circuitos neurales como subsistemas independientes
- Física: descomposición de sistemas complejos
- Informática: análisis de topología de redes
- Biología: identificar "módulos" en redes biológicas

### Alcance Académico

El proyecto tiene 3 niveles de dificultad:

1. **Nivel 1 - Entender el problema:** Leer PDFs, implementar búsqueda exhaustiva (PyPhi)
2. **Nivel 2 - Mejorar con heurísticas:** Implementar QNodes (BruteForce mejorado)
3. **Nivel 3 - Innovar:** Proponer GeoMIP (estrategia geométrica) + k-particiones

**Vosotros estáis en Nivel 3.**

---

## 🎯 Problema Central

### Definición Formal

**Entrada:**

- Sistema binario: V = {X₁, X₂, ..., Xₙ} donde cada Xᵢ ∈ {0, 1}
- Matriz de Probabilidad de Transición (TPM): P(V_{t+1} | V_t)
  - Filas: 2ⁿ estados posibles en tiempo t
  - Columnas: 2ⁿ estados posibles en tiempo t+1
  - TPM[i][j]: probabilidad P(estado_j en t+1 | estado_i en t)
- Estado inicial conocido: por ej. "1000" (binario)

**Salida:**

- Bipartición óptima: {S₁, S₂} que divide el sistema
- Valor Φ (Phi): cantidad de información "perdida" al dividir
  - Φ = EMD( P(original), P(S₁) ⊗ P(S₂) )
  - Φ mínimo = mejor división

**Objetivo:**
Encontrar la bipartición que **minimiza Φ** (máxima independencia entre partes)

### Por Qué es Difícil

```
Número de posibles biparticiones = 2^(u+v-1) - 1

Ejemplos:
  u+v = 4   → 7 biparticiones
  u+v = 8   → 127 biparticiones
  u+v = 16  → 32,767 biparticiones
  u+v = 32  → ~2.1 billones de biparticiones (inviable)
```

**Conclusión:** Fuerza bruta es inviable para n > 20. Necesitamos heurísticas inteligentes.

---

## 🧠 Fundamentos Teóricos

### 1. Teoría de la Información Integrada (IIT)

**Axiomas principales:**

- Un sistema tiene "información integrada" si sus subsistemas no son independientes
- La "pérdida de información" al dividir = medida de integración
- Objetivo: encontrar mínima información pérdida (máxima independencia)

**Fórmula central:**

```
Φ({S₁, S₂}) = EMD( P(sistema_original), P(S₁) ⊗ P(S₂) )
```

### 2. Operaciones Sobre TPM

#### Condicionar

Fijar variables externas según estado inicial.

```
Si V = {A, B, C, D} y estado_ini = "1000" (D=0)
  Condicionamos en D=0
  → Eliminamos filas donde D ≠ 0
  → Matriz reducida de 16×16 a 8×16
```

#### Marginalizar Filas (en tiempo t)

Eliminar variables en el presente. Los estados duplicados se **promedian**.

```
Si queremos solo {A, B} en t, eliminamos C en t
  → Estados (A=0,B=0,C=0) y (A=0,B=0,C=1) se fusionan
  → Se promedian sus filas
  → Resultado: 4 filas (2^2)
```

**CRÍTICO:** Esta operación **promedia**, no suma.

#### Marginalizar Columnas (en tiempo t+1)

Eliminar variables en el futuro. Se **suman** las columnas.

```
Si queremos solo {A} en t+1, eliminamos B, C en t+1
  → Sumamos columnas donde A=0 con diferentes B,C
  → Resultado: matriz 2^n × 2 (formato "estado-nodo")
```

**CRÍTICO:** Esta operación **suma**, no promedia.

#### Producto Tensorial

Combinar dos subsistemas marginales.

```
Si M₁ es 8×2 (A futuro) y M₂ es 8×2 (B futuro)
  M₁ ⊗ M₂ es 8×4 (A y B futuros combinados)
  
  (M₁ ⊗ M₂)[i, j1*2 + j2] = M₁[i, j1] × M₂[i, j2]

NO es el producto de Kronecker.
Mantiene filas, multiplica columnas.
ES CONMUTATIVO.
```

### 3. Earth Mover's Distance (EMD)

**Definición:** Mínimo trabajo para transformar distribución u en distribución v.

```
EMD(u, v) = min(transporte) donde costo = suma(cantidad × distancia)

Con distancia Hamming:
  costo(estado_i, estado_j) = dH(i,j) = (i XOR j).bit_count()
  
Ejemplo:
  dH(000, 011) = 2 (difieren en 2 bits)
  dH(101, 111) = 1 (difieren en 1 bit)
```

**Interpretación:** EMD mide cuánto se "mueve" probabilidad entre estados.

### 4. Distancia de Hamming

```
Definición:
  dH(x, y) = número de posiciones donde x_i ≠ y_i
  
Cálculo:
  dH(x, y) = (x XOR y).bit_count()
  
Ejemplos (n=3):
  dH(000, 000) = 0  (idénticos)
  dH(000, 001) = 1  (1 bit diferente)
  dH(000, 110) = 2  (2 bits diferentes)
  dH(000, 111) = 3  (3 bits diferentes — opuestos)

Representación geométrica:
  En un hipercubo n-dimensional, dH = número de aristas a recorrer
```

### 5. Representación Geométrica (Hipercubo)

```
Los 2ⁿ estados se mapean a los 2ⁿ vértices de un hipercubo n-dimensional.

n=1:    0 — 1           (1-cubo: línea)
n=2:    00 — 10         (2-cubo: cuadrado)
        |    |
        01 — 11
      
n=3:    000 — 100       (3-cubo: cubo)
        / |  / |
       010 — 110
       |010|  |
       001 — 101
       /   |  /
      011 — 111

Propiedad clave:
  Dos estados son ADYACENTES (conectados por arista)
  ↔ dH = 1 (difieren en exactamente 1 bit)
```

---

## 📁 Estructura del Repositorio

```
repositorio/
│
├── QNodes/                          # Framework base (búsqueda exhaustiva mejorada)
│   ├── src/
│   │   ├── models/
│   │   │   ├── base/
│   │   │   │   ├── sia.py          # Clase base abstracta para estrategias
│   │   │   │   ├── system.py       # Representación del sistema (TPM + metadata)
│   │   │   │   ├── solution.py     # Resultado de estrategia (bipartición + Φ)
│   │   │   │   └── ncube.py        # Representación estado-nodo (columnas)
│   │   │   └── [más modelos...]
│   │   │
│   │   ├── controllers/
│   │   │   ├── strategies/         # Diferentes estrategias de bipartición
│   │   │   │   ├── __init__.py
│   │   │   │   ├── sia.py          # Clase base (duplicada con models/base/)
│   │   │   │   ├── bruteforce.py   # Búsqueda exhaustiva O(2^(2n-1))
│   │   │   │   ├── q_nodes.py      # Heurística QNodes mejorada
│   │   │   │   ├── phi.py          # Estrategia PhiMeasure
│   │   │   │   ├── recursive_refinement.py  # NUEVO: k-particiones
│   │   │   │   └── [más estrategias...]
│   │   │   │
│   │   │   └── system_manager.py   # Gestor central (interfaz con estrategias)
│   │   │
│   │   ├── utils/
│   │   │   ├── marginalization.py  # Funciones de marginalización
│   │   │   ├── emd.py              # Earth Mover's Distance con Hamming
│   │   │   ├── tensor_product.py   # Producto tensorial
│   │   │   └── [más utilidades...]
│   │   │
│   │   ├── services/
│   │   │   └── system_service.py   # Lógica de carga de sistemas
│   │   │
│   │   └── main.py                 # Punto de entrada (CLI o batch)
│   │
│   ├── tests/
│   │   ├── data/
│   │   │   ├── N2A.csv             # Redes de prueba (binarias)
│   │   │   ├── N3A.csv
│   │   │   ├── N3B.csv
│   │   │   ├── N3C.csv             # CASO DE REFERENCIA (3 nodos)
│   │   │   ├── N4A.csv
│   │   │   ├── N4B.csv
│   │   │   ├── N5A.csv
│   │   │   ├── N6A.csv
│   │   │   ├── N8A.csv
│   │   │   ├── N10A.csv
│   │   │   ├── N15A.csv
│   │   │   └── [más redes...]
│   │   │
│   │   ├── test_sia_interface.py
│   │   ├── test_bruteforce.py
│   │   ├── test_q_nodes.py
│   │   ├── test_marginalization.py
│   │   ├── test_emd.py
│   │   ├── test_recursive_refinement.py  # NUEVO
│   │   └── [más tests...]
│   │
│   ├── pyproject.toml              # Dependencias y configuración
│   ├── README.md                   # Instrucciones QNodes
│   ├── CHANGELOG.md
│   └── .gitignore
│
├── GeoMIP/                          # Extensión: Estrategia Geométrica
│   ├── Method1_GPU/                # Intento 1 con GPU
│   │   ├── src/
│   │   ├── tests/
│   │   └── README.md
│   │
│   ├── Method2_Dynamic_Programming_Reformulation/  # Método actual (DP)
│   │   ├── src/
│   │   │   ├── models/
│   │   │   │   ├── base/           # (duplicado con QNodes)
│   │   │   │   │   ├── sia.py
│   │   │   │   │   ├── system.py
│   │   │   │   │   ├── solution.py
│   │   │   │   │   └── ncube.py
│   │   │   │   └── [más...]
│   │   │   │
│   │   │   ├── controllers/
│   │   │   │   ├── strategies/
│   │   │   │   │   ├── geometric.py             # Estrategia actual (tabla T)
│   │   │   │   │   ├── recursive_refined_geometric.py  # NUEVO
│   │   │   │   │   └── [más...]
│   │   │   │   └── [más...]
│   │   │   │
│   │   │   ├── utils/
│   │   │   │   ├── hipercubo.py    # Cálculo tabla T y candidatas
│   │   │   │   ├── emd.py
│   │   │   │   └── [más...]
│   │   │   │
│   │   │   └── main.py
│   │   │
│   │   ├── tests/
│   │   │   ├── data/               # (mismos CSVs que QNodes)
│   │   │   ├── test_geometric.py
│   │   │   ├── test_tabla_T.py
│   │   │   ├── test_recursive_refined_geometric.py  # NUEVO
│   │   │   └── [más...]
│   │   │
│   │   ├── pyproject.toml
│   │   ├── README.md               # Documentación GeoMIP
│   │   └── .gitignore
│   │
│   └── docs/                        # Documentación teórica
│       ├── 1_Guía_Proyecto_ADAV1_2_0.pdf
│       └── 2_GeoMIP.pdf
│
├── tests/                           # NUEVO: tests de comparativa (ambos repos)
│   ├── test_comparativa_qnodes_vs_geomip.py
│   ├── test_validacion_pyphi.py
│   ├── benchmark_results.xlsx      # Tabla de resultados
│   └── CONTEXTO_PROYECTO.md        # Este documento
│
├── .github/
│   └── workflows/
│       ├── test.yml                # CI: correr tests
│       ├── lint.yml                # Linting (flake8, black)
│       └── benchmark.yml           # Comparativa automática
│
├── docs/                            # Documentación general
│   ├── README.md                    # Overview del proyecto
│   ├── ARQUITECTURA.md
│   ├── CONVENCIONES.md
│   ├── PLAN_ACCION_KPARTICIONES.md
│   └── CONTEXTO_PROYECTO.md        # ← ESTE ARCHIVO
│
└── .gitignore                       # Exclusiones de git

TOTAL: ~5000 líneas de código
       ~2000 líneas de tests
       ~50 funciones principales
```

---

## 🏗️ Arquitectura Actual

### Diagrama de Capas

```
                    ┌─────────────────────────────┐
                    │   CLI / Main.py             │
                    │   (Punto de entrada)        │
                    └────────────┬────────────────┘
                                 │
                    ┌────────────▼────────────────┐
                    │   SystemManager             │
                    │   (Gestor central)          │
                    │   - Carga CSV               │
                    │   - Llama estrategias       │
                    │   - Retorna Solution        │
                    └────────────┬────────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
    ┌────▼──────────┐   ┌────────▼─────────┐   ┌───────▼──────┐
    │  QNODES       │   │  GEOMIP          │   │  PyPhi       │
    │  Strategies   │   │  Geometric        │   │  Reference   │
    │  ────────     │   │  Strategy         │   │  ──────────  │
    │ • BruteForce  │   │  ────────────     │   │ • compute    │
    │ • QNodes      │   │ • Tabla T         │   │   _mip()     │
    │ • Recursive   │   │ • Candidatas      │   │              │
    │   Refinement  │   │ • Recursive       │   │  (validador) │
    └────┬──────────┘   │   Refined Geom    │   └──────────────┘
         │              └────┬──────────────┘
         │                   │
         └───────┬───────────┘
                 │
         ┌───────▼────────────┐
         │  CORE FUNCTIONS    │
         │  ──────────────    │
         │ • Marginalization  │
         │ • EMD + Hamming    │
         │ • Tensor Product   │
         │ • Decompose        │
         │ • Tabla T (Geom)   │
         └───────┬────────────┘
                 │
         ┌───────▼────────────┐
         │  DATA LAYER        │
         │  ──────────────    │
         │ • System (TPM)     │
         │ • Solution         │
         │ • NCube            │
         └────────────────────┘
```

### Flujo de Ejecución (QNodes)

```
1. main.py carga dataset (CSV)
   ↓
2. SystemManager crea objeto System
   System = {TPM: 8×8, estado_inicial: "000", n: 3, variables: [A,B,C]}
   ↓
3. SystemManager instancia estrategia (ej. BruteForce)
   ↓
4. BruteForce.aplicar_estrategia()
   a. Generar todas las biparticiones posibles (127 para n=3)
   b. Para cada bipartición:
      - Marginalizar TPM → P(S1), P(S2)
      - Producto tensorial: P(S1) ⊗ P(S2)
      - Calcular EMD vs TPM original
   c. Retornar bipartición con EMD mínimo
   ↓
5. Retorna Solution(biparticion={S1, S2}, phi=0.000, tiempo_ms=5)
   ↓
6. main.py muestra resultado y guarda en Excel
```

### Flujo de Ejecución (GeoMIP)

```
1-3. [Igual a QNodes]
   ↓
4. GeometricSIA.aplicar_estrategia()
   a. Descomponer TPM en tensores estado-nodo
      Tensor A: [0, 0, 0, 0, 1, 1, 1, 1]
      Tensor B: [0, 0, 1, 1, 0, 0, 1, 1]
      Tensor C: [0, 1, 0, 1, 0, 1, 0, 1]
   b. Construir tabla T de costos t(i,j) para cada par (i,j)
      Usa BFS bottom-up, O(n·2ⁿ)
   c. Identificar biparticiones candidatas
      Buscar patrones de complementariedad en T
   d. Evaluar top 3 candidatas
      Calcular EMD real para cada una
   e. Retornar mejor candidata
   ↓
5-6. [Igual a QNodes]

Ventaja: Tabla T acelera búsqueda de candidatas → 2-5× más rápido
```

---

## 🎯 QNodes (Framework Base)

### Propósito

Implementar búsqueda exhaustiva **mejorada** (no pura fuerza bruta).

### Componentes Clave

#### 1. System (Modelo de Datos)

```python
@dataclass
class System:
    """Representa un sistema binario con dinámica temporal"""
  
    tpm: np.ndarray              # Matriz 2^n × 2^n
    estado_inicial: str          # Ej. "1000" (binario)
    n: int                       # Número de nodos
    variables: List[str]         # Nombres: ["A", "B", "C", ...]
    velocidad: float = 0.1       # Parámetro de dinámica
```

#### 2. SIA (Clase Base Abstracta)

```python
class SIA(ABC):
    """Interfaz para todas las estrategias"""
  
    def __init__(self, gestor):
        self.gestor = gestor
        self.tpm = gestor.tpm
        self.n = gestor.n
  
    @abstractmethod
    def aplicar_estrategia(self) -> Solution:
        """Encontrar bipartición óptima"""
        pass
  
    @abstractmethod
    def aplicar_estrategia_kparticion(self, k: int) -> Solution:
        """NUEVO: Encontrar k-partición óptima"""
        pass
```

#### 3. Solution (Resultado)

```python
@dataclass
class Solution:
    """Resultado de aplicar una estrategia"""
  
    biparticion: Tuple[Set[int], Set[int]]  # ({A,B}, {C})
    particiones: List[Set[int]] = None      # NUEVO: para k-particiones
    phi: float = None                       # Valor de Φ
    tiempo_ms: float = None
    estrategia: str = None
    k: int = None                           # NUEVO: número de particiones
```

#### 4. Estrategias Existentes

**BruteForce (O(2^(2n-1)))**

- Enumera TODAS las biparticiones
- Evalúa Φ para cada una
- Retorna mínimo
- Inviable para n > 15

**QNodes (heurística)**

- Intenta reducir biparticiones a evaluar
- Usa heurísticas para "podar" el árbol de búsqueda
- Más rápido que BruteForce, menos exacto

**PhiMeasure**

- Calcula Φ para una bipartición dada
- Útil para validación

---

## 🌐 GeoMIP (Extensión Geométrica)

### Propósito

Usar **tabla T geométrica** para acelerar búsqueda de biparticiones óptimas.

### Innovación Principal

En lugar de:

```
Enumerar 2^(2n-1) biparticiones → evaluar cada una → O(exponencial)
```

GeoMIP hace:

```
Construir tabla T de costos t(i,j) → identificar candidatas → O(k·2^n)
```

### Componentes Clave

#### 1. Tabla T (Función de Costo)

**Definición:**

```
t_x(i, j) = γ · ( |X[i] - X[j]| + Σ_{k ∈ N(i,j)} t_x(k, j) )

donde:
  γ = 2^(-dH(i,j))                    factor exponencial
  X[i]                                valor del tensor en estado i
  |X[i] - X[j]|                       diferencia del tensor
  N(i,j)                              vecinos de i que acercan a j
  Σ t_x(k,j)                          suma recursiva de costos
```

**Interpretación:**

- Mide "energía causal" entre dos estados
- Considera no solo diferencia directa sino también caminos intermedios
- Exponencial decreciente con distancia Hamming

#### 2. Construcción de Tabla T

**Algoritmo BFS Bottom-Up:**

```
Para cada estado destino j:
  1. Agrupar todos los estados por dH(i,j)
  2. Calcular primero los de distancia 1
  3. Luego los de distancia 2 (usando cálculos de distancia 1)
  4. Así sucesivamente hasta distancia máxima
  
Complejidad: O(n·2^n) en lugar de O(2^(2n-1))
```

#### 3. Identificación de Candidatas

**Patrón de Búsqueda:**

- Buscar pares (i,j) donde el costo es 0 para muchas variables
- Indica complementariedad: cambios independientes
- Las biparticiones mejores tienden a tener patrones de "ceros complementarios"

**Resultado:**

- Top 3-5 biparticiones candidatas sin evaluar todas
- Evaluar solo los candidatos más prometedores

---

## 💾 Estado Actual del Código

### QNodes

#### Archivos Funcionales

- ✅ `models/base/sia.py` — Clase base (ORIGINAL)
- ✅ `controllers/strategies/bruteforce.py` — Búsqueda exhaustiva
- ✅ `controllers/strategies/q_nodes.py` — Heurística
- ✅ `utils/marginalization.py` — Marginalización
- ✅ `utils/emd.py` — EMD con Hamming
- ✅ `utils/tensor_product.py` — Producto tensorial
- ✅ Tests de cada componente

#### Archivos NUEVOS (a implementar)

- ❌ `controllers/strategies/recursive_refinement.py` — Estrategia k-particiones (TÚ)

#### Problemas Conocidos

- ⚠️ Código duplicado con GeoMIP (SIA, System, Solution)
- ⚠️ Inconsistencia ON/OFF (distribución_marginal retorna P(X=1) directamente)
- ⚠️ Entradas hardcodeadas en main.py (no parametrizable)

### GeoMIP (Method2)

#### Archivos Funcionales

- ✅ `models/base/sia.py` — Clase base (DUPLICADA)
- ✅ `controllers/strategies/geometric.py` — Estrategia tabla T
- ✅ `utils/hipercubo.py` — Tabla T y candidatas
- ✅ `utils/emd.py` — EMD
- ✅ Tests

#### Archivos NUEVOS (a implementar)

- ❌ `controllers/strategies/recursive_refined_geometric.py` — Estrategia k-particiones GEOMÉTRICA (Tu Compañero)

#### Problemas Conocidos

- ⚠️ distribucion_marginal retorna `1 - probabilidad` (inverso de QNodes)
- ⚠️ Código duplicado con QNodes
- ⚠️ Entradas hardcodeadas
- ⚠️ Construcción tabla T podría optimizarse

### Comparativa QNodes vs GeoMIP (Estado Actual)

| Aspecto           | QNodes     | GeoMIP                    |
| ----------------- | ---------- | ------------------------- |
| Estrategia base   | BruteForce | Tabla T                   |
| Velocidad (N=8)   | ~50ms      | ~20ms                     |
| Speedup           | Baseline   | 2.5×                     |
| Φ coincide       | ✅ Sí     | ⚠️ Inverso (bug ON/OFF) |
| k-particiones     | ❌ No      | ❌ No                     |
| Código duplicado | ⚠️ Sí   | ⚠️ Sí                  |

---

## 📐 Convenciones y Estándares

### 1. Indexación Binaria (CRÍTICO)

**Convención del Proyecto:** Little-Endian

```
Estado binario ABC → índice decimal
000 → 0*1 + 0*2 + 0*4 = 0
001 → 1*1 + 0*2 + 0*4 = 1
010 → 0*1 + 1*2 + 0*4 = 2
100 → 0*1 + 0*2 + 1*4 = 4

Inversamente:
índice 5 → 5 = 1*1 + 0*2 + 1*4 → 101 (binario)
```

**Verificación:**
Ver `tests/data/N3C.metadata.yaml` para confirmar indexación.

### 2. Convención ON/OFF (CRÍTICO - INCONSISTENCIA ACTUAL)

**QNodes (correcto):**

```python
distribucion_marginal(tpm, variables) → List[p_estado_0, p_estado_1, ...]
  donde p_estado_0 = P(X=0 | ...) 
  y p_estado_1 = P(X=1 | ...)
```

**GeoMIP (INVERSO - BUG):**

```python
distribucion_marginal(tpm, variables) → List[1-p, p, ...]
  Retorna el complemento de la probabilidad
```

**Impacto:** Φ se invierte (todo lo opuesto). Tests fallan.

**Solución Pendiente:** Unificar convención en Phase 1 de plan.

### 3. Marginalización (CRÍTICO)

```
Filas (en t):      Promedia (divide by count)
  filtramos estados → se clonan → promediamos filas duplicadas

Columnas (en t+1): Suma (no divide)
  agrupamos estados → sumamos columnas
```

**Validación:**

```python
# Después de marginalizar filas, cada fila sigue sumando 1
assert all(row.sum() == 1.0)

# Después de marginalizar columnas, cada fila sigue sumando 1
assert all(row.sum() == 1.0)
```

### 4. Producto Tensorial

```python
# M1: 8×2 (estado-nodo de A)
# M2: 8×2 (estado-nodo de B)
# Resultado: 8×4

result[i, j1*2 + j2] = M1[i, j1] * M2[i, j2]  # Multiplicación

# NO es:
result_kronecker = kron(M1, M2)  # Esto sería incorrecto
```

### 5. EMD con Distancia Hamming

```python
# Matriz de costos
costs[i, j] = (i ^ j).bit_count()  # XOR + contar bits

# Verificación: 
# dH(0, 5) = (0 ^ 5).bit_count() = (101 binario).bit_count() = 2
assert (0 ^ 5).bit_count() == 2

# EMD es sensible a esta matriz. Usar otra distancia → resultados incorrectos.
```

### 6. Formato de Datos

**TPM:**

- Tipo: `numpy.ndarray` dtype `float64`
- Shape: `(2^n, 2^n)`
- Cada fila suma 1.0 (distribución de probabilidad)

**Estado Inicial:**

- Tipo: `str` o `int`
- Rango: "000" a "111" para n=3, 0 a 7 para decimal
- Convención: Little-Endian (primer carácter = variable 0)

**Bipartición:**

- Tipo: `Tuple[Set[int], Set[int]]`
- Ejemplo: ({0, 1}, {2}) representa {{A, B}, {C}}

**Φ (Phi):**

- Tipo: `float`
- Rango: [0, ∞)
- 0 = partición perfecta (independencia total)
- Mayor = mayor integración (dependencia)

### 7. Logging y Debug

```python
import logging

logger = logging.getLogger(__name__)
logger.info(f"Estrategia iniciada con n={self.n}")
logger.debug(f"Bipartición evaluada: {biparticion}, Φ={phi:.6f}")
logger.warning("Marginalización degenerada")
logger.error("EMD no convergió")
```

---

## 🧪 Datos de Prueba

### Estructura

```
tests/data/
├── N3C.csv              # 3 nodos - CASO DE REFERENCIA
├── N3C.metadata.yaml    # Metadata conocida
├── N4A.csv
├── N4A.metadata.yaml
├── N5A.csv
└── ...
```

### N3C.csv (Caso de Referencia)

**Descripción:**

- 3 nodos binarios: A, B, C
- Estado inicial: "000" (todos OFF)
- TPM: 8×8 (todos los estados transitan determinísticamente)

**Valores Esperados:**

```yaml
nombre: N3C
nodos: 3
estado_inicial: "000"
estado_inicial_decimal: 0
tpm_shape: [8, 8]
tpm_indexacion: Little-Endian

# Bipartición óptima
esperado_phi_biparticion: 0.0
esperado_biparticion: [[0, 1], [2]]  # {{A, B}, {C}}

# Tensores (P(X=0 | estado))
tensor_A: [0, 0, 0, 0, 1, 1, 1, 1]
tensor_B: [0, 0, 1, 1, 0, 0, 1, 1]
tensor_C: [0, 1, 0, 1, 0, 1, 0, 1]

# Tabla T (valores esperados)
tabla_T_A:
  [000, 001]: 0.5
  [000, 101]: 0.375
  [000, 111]: 0.21875
```

**Validación:**

```python
def test_n3c_load():
    df = pd.read_csv("tests/data/N3C.csv")
    assert df.shape == (8, 8)
    assert all(df.sum(axis=1) == 1.0)

def test_n3c_bruteforce():
    # BruteForce debe encontrar Φ = 0.0
    sol = bruteforce.aplicar_estrategia()
    assert abs(sol.phi - 0.0) < 1e-6

def test_n3c_geomip():
    # GeoMIP debe encontrar Φ ≈ 0.0
    sol = geomip.aplicar_estrategia()
    assert abs(sol.phi - 0.0) < 0.01  # Tolerancia 1%
```

---

## 🚀 Próximos Pasos: k-Particiones

### Visión General

Expandir el proyecto de **biparticiones** (k=2) a **k-particiones** (k=2,3,4,...).

### Estrategia Elegida: Recursive Refinement

```
Algoritmo:
  1. Inicio: 1 partición (sistema completo)
  2. Loop: mientras #particiones < k:
     a. Para cada partición actual:
        - Dividir en 2 usando tabla T (GeoMIP) o BruteForce (QNodes)
        - Evaluar Φ total
     b. Si hay mejora: aplicar; si no: parar

Complejidad: O(k·2^n) — mucho mejor que O(2^(exponencial))
Resultado: Φ ≈ óptimo (95%+)
```

### Implementación Dual

**QNodes (TÚ):**

```python
class RecursiveRefinement(SIA):
    """Usa BruteForce para cada bipartición iterada"""
    def aplicar_estrategia_kparticion(self, k: int) -> Solution:
        pass
```

**GeoMIP (Tu Compañero):**

```python
class RecursiveRefinedGeometric(SIA):
    """Usa tabla T para acelerar cada bipartición iterada"""
    def aplicar_estrategia_kparticion(self, k: int) -> Solution:
        pass
```

### Timeline

- **Semana 1:** Extender interfaz SIA
- **Semana 2:** Implementar RecursiveRefinement (QNodes)
- **Semana 3:** Implementar RecursiveRefinedGeometric (GeoMIP)
- **Semana 4:** Validación, benchmarking, release v1.1-kpartitions

---

## 📚 Referencias Clave

### PDFs del Proyecto

1. **1_Guía_Proyecto_ADAV1_2_0.pdf**

   - Especificación del proyecto académico
   - Definiciones formales
   - Requisitos
2. **2_GeoMIP.pdf**

   - Teoría de representación geométrica
   - Tabla T (fórmula y algoritmo)
   - Caso de estudio N3C con valores esperados

### Código Existente

- `QNodes/src/controllers/strategies/bruteforce.py` — modelo de implementación
- `GeoMIP/Method2_Dynamic_Programming_Reformulation/src/utils/hipercubo.py` — tabla T referencia
- `tests/test_comparativa_qnodes_vs_geomip.py` — validación

### Librerías

- **numpy** — manejo de arrays/matrices
- **pandas** — lectura de CSV
- **pyemd** — Earth Mover's Distance
- **pyphi** — referencia de validación
- **pytest** — testing framework

---

## ✅ Resumen de Estado

### Lo Que Funciona ✅

- Carga de CSVs y creación de Systems
- BruteForce exhaustivo (O(2^(2n-1)))
- QNodes heurístico
- Marginalización (mayoría de casos)
- EMD con Hamming
- Producto tensorial
- Tabla T geométrica (GeoMIP)

### Lo Que NO Funciona ❌

- k-particiones (objetivo de este sprint)
- ON/OFF inconsistente entre QNodes y GeoMIP
- Código duplicado sin consolidación

### Lo Que Necesita Mejora ⚠️

- Parametrización de entrada (hardcodeado)
- Optimización tabla T (podría paralelizarse)
- Tests de integración completos
- Documentación de código (falta docstrings)

---

## 🎯 Conclusión

El proyecto QNodes + GeoMIP es una **implementación académica completa** de bipartición óptima con dos enfoques:

1. **QNodes:** Búsqueda exhaustiva mejorada
2. **GeoMIP:** Aceleración geométrica usando tabla T

Ahora, en el sprint de **k-particiones**, ambos equipos expandirán la solución para soportar divisiones en k > 2 partes.

**Éxito = ambas implementaciones funcionan, dan resultados similares, y GeoMIP es 2-5× más rápido.**

---

**Documento actualizado:** [Hoy]
**Responsables:** Dev 1 (QNodes) + Dev 2 (GeoMIP)
**Próxima revisión:** Final de Semana 4
