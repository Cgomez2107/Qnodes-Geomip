# Exploration Report - Proyecto Análisis y Diseño 20261

> **Arquitecto Senior SDD** - Fase: `/opsx:explore`
> **Fecha**: 2026-05-16
> **Tipo**: Brownfield Analysis (Código Existente)

---

## 1. Resumen Arquitectónico

### 1.1 Visión Macro del Proyecto

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                         ARQUITECTURA DEL SISTEMA - CAPAS                             │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│   ┌─────────────────────────────────────────────────────────────────────────────┐   │
│   │                        CAPA DE APLICACIÓN                                    │   │
│   │   ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────────┐    │   │
│   │   │   exec.py       │    │   exec.py       │    │   main.py           │    │   │
│   │   │   (QNodes)      │    │   (GeoMIP M1)   │    │   (GeoMIP M2)       │    │   │
│   │   └────────┬────────┘    └────────┬────────┘    └──────────┬──────────┘    │   │
│   └────────────┼──────────────────────┼───────────────────────┼──────────────┘   │
│                │                      │                       │                  │
│   ┌────────────┼──────────────────────┼───────────────────────┼──────────────┐    │
│   │            ▼                      ▼                       ▼              │    │
│   │   ═══════════════════════════════════════════════════════════════════════   │    │
│   │                        CAPA DE ESTRATEGIAS                                   │    │
│   │   ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌────────────────┐    │    │
│   │   │ BruteForce   │ │    Phi       │ │    Q-Nodes   │ │  Geometric     │    │    │
│   │   │ (Fuerza)     │ │  (PyPhi)     │ │  (Heurística)│ │  (GeoMIP)      │    │    │
│   │   └──────────────┘ └──────────────┘ └──────────────┘ └────────────────┘    │    │
│   └─────────────────────────────────────────────────────────────────────────────┘   │
│                                      │                                             │
│                                      ▼                                             │
│   ┌─────────────────────────────────────────────────────────────────────────────┐   │
│   │                        CAPA DE MODELOS                                       │    │
│   │   ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌───────────────────┐    │    │
│   │   │   System    │ │   NCube     │ │   SIA       │ │    Solution       │    │    │
│   │   │   (TPM)     │ │  (Estado)   │ │ (Análisis)  │ │    (Resultado)    │    │    │
│   │   └─────────────┘ └─────────────┘ └─────────────┘ └───────────────────┘    │    │
│   └─────────────────────────────────────────────────────────────────────────────┘   │
│                                      │                                             │
│                                      ▼                                             │
│   ┌─────────────────────────────────────────────────────────────────────────────┐   │
│   │                        CAPA DE DATOS                                         │    │
│   │   ┌──────────────────┐   ┌──────────────────┐   ┌────────────────────┐    │    │
│   │   │   CSV (TPMs)     │   │  Excel (Results) │   │   pyphi_cache      │    │    │
│   │   │   samples/       │   │  results/        │   │   (Computed)      │    │    │
│   │   └──────────────────┘   └──────────────────┘   └────────────────────┘    │    │
│   └─────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Identificación del Proyecto

| Atributo | Valor |
|----------|-------|
| **Nombre** | Proyecto Análisis y Diseño 20261 |
| **Tipo** | Framework de Análisis Algorítmico - IIT/MIP |
| **Paradigma** | Computación Científica + Optimización |
| **Lenguaje** | Python 3.11+ |
| **Naturaleza** | Brownfield (Código existente heredado) |

### 1.3 Propósito del Sistema

El sistema implementa un **framework para resolver el problema de Minimal Information Partition (MIP)** dentro del contexto de la **Integrated Information Theory (IIT)**:

- **Objetivo**: Calcular Φ (Phi) - la información integrada de un sistema
- **Problema central**: Encontrar la bipartición que minimiza la información integrada
- **Dominio**: Teoría de la información, sistemas complejos, neuroscience computacional

---

## 2. Grafo de Dependencias

### 2.1 Dependencias de Alto Nivel

```
                                    ┌─────────────────────┐
                                    │   Python 3.11+      │
                                    └──────────┬──────────┘
                                               │
           ┌──────────────────────────────────┼──────────────────────────────────┐
           │                                  │                                  │
           ▼                                  ▼                                  ▼
┌─────────────────────┐          ┌─────────────────────┐          ┌─────────────────────┐
│      QNodes         │          │      GeoMIP          │          │     OpenSpec        │
│   (Framework Core) │          │   (Algoritmos)       │          │   (Gestión)         │
└─────────┬───────────┘          └──────────┬────────────┘          └──────────┬────────────┘
          │                                  │                                  │
          ▼                                  ▼                                  ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                              DEPENDENCIAS COMPARTIDAS                                      │
├──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬────────────────┤
│    numpy     │    scipy     │   pandas     │  openpyxl    │ colorama     │ pyinstrument   │
│   1.26.4     │   1.17.0     │   2.3.3      │   3.1.3      │   0.4.5      │   5.1.2        │
│  Computación │   EMD        │    Excel     │   Output     │   Logging    │   Profiling    │
│    Numérica  │  Distancia  │    I/O       │   Writing    │   Colored    │   Performance  │
└──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴────────────────┘
                                           │
                                           ▼
                              ┌─────────────────────────┐
                              │       pyphi             │
                              │       1.2.0             │
                              │   (Referencia IIT)      │
                              │  ⚠️ Requiere C++ Build  │
                              └─────────────────────────┘
```

### 2.2 Dependencias por Componente

#### QNodes Dependencies
```
QNodes/
├── src/
│   ├── main.py
│   ├── exec.py
│   ├── constants/          → base.py, error.py, models.py
│   ├── models/            → SIA, System, NCube, Solution, Enums
│   ├── controllers/      → Manager (gestor de TPMs)
│   ├── funcs/            → force.py, format.py, iit.py
│   ├── middlewares/     → profile.py (pyinstrument), slogger.py
│   └── strategies/      → force.py, phi.py, q_nodes.py
│
├── Dependencies:
│   ├── numpy
│   ├── scipy
│   ├── pandas
│   ├── pyphi
│   ├── pyinstrument
│   ├── openpyxl
│   ├── colorama
│   └── pyttsx3
```

#### GeoMIP Dependencies
```
GeoMIP/src/
├── Method1_GPU_Accelerated/
│   └── src/ (similar structure)
│
└── Method2_Dynamic_Programming_Reformulation/
    ├── pyproject.toml
    ├── .venv/
    └── src/ (similar to QNodes)
        ├── strategies/geometric.py ← Algoritmo principal
        └── controllers/manager.py
```

### 2.3 Grafo de Dependencias Técnica (Simplificado)

```
                    ┌──────────────┐
                    │   sys/std    │
                    │  (Python)    │
                    └──────┬───────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
    ┌───────────┐    ┌───────────┐    ┌───────────┐
    │  numpy    │    │  scipy    │    │   pandas  │
    │ (numeric) │    │  (sci)    │    │ (tables)  │
    └─────┬─────┘    └─────┬─────┘    └─────┬─────┘
          │                │                │
          └────────┬───────┴───────┬────────┘
                   ▼              ▼
            ┌────────────┐ ┌────────────┐
            │  pyphi    │ │pyinstrument│
            │  (core)   │ │(profiling) │
            └───────────┘ └────────────┘
```

---

## 3. Análisis de Complejidad Algorítmica

### 3.1 BruteForce Strategy - Complejidad

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│                    COMPLEJIDAD BRUTEFORCE - ANÁLISIS COMPLETO                        │
├────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                    │
│   Para una red de N nodos, con m nodos de mecanismo y n nodos de alcance:          │
│                                                                                    │
│   ══════════════════════════════════════════════════════════════════════════════   │
│                                                                                    │
│   ETAPA 1: Generación de Sistemas Candidatos                                       │
│   ─────────────────────────────────────────────────────────────────────────────   │
│   C(N, k) = N! / (k!(N-k)!)  →  O(2^N)  [todos los subconjuntos]                  │
│                                                                                    │
│   ETAPA 2: Generación de Subsistemas por Candidato                                │
│   ─────────────────────────────────────────────────────────────────────────────   │
│   Para cada candidato de tamaño m:                                                │
│   └─> generar_subsistemas: O(2^m × 2^m) = O(4^m)                                  │
│                                                                                    │
│   ETAPA 3: Generación de Particiones (Biparticiones)                             │
│   ─────────────────────────────────────────────────────────────────────────────   │
│   P(m, n) = 2^(m+n-1) - 1  →  O(2^(m+n))                                          │
│                                                                                    │
│   ══════════════════════════════════════════════════════════════════════════════   │
│                                                                                    │
│   COMPLEJIDAD TOTAL:                                                              │
│                                                                                    │
│   T(N) = Σ_{k=1}^{N} [ C(N,k) × Σ_{m=1}^{k} ( 4^m × 2^(m+n) ) ]                  │
│                                                                                    │
│   Para N = 15 (caso empírico):                                                     │
│   ┌─────────────────────────────────────────────────────────────────────────┐      │
│   │  Nodos │  Estados  │  Candidatos   │  Particiones  │  Tiempo Est.       │      │
│   ├────────┼───────────┼───────────────┼───────────────┼────────────────────┤      │
│   │   4    │    16     │     15        │     127       │  ~ms               │      │
│   │   8    │   256     │    255        │   32,767      │  ~segundos         │      │
│   │  10    │  1,024    │   1,023       │  524,287      │  ~minutos          │      │
│   │  15    │  32,768   │   32,767      │  268M         │  ⚠️ HOURS          │      │
│   └─────────────────────────────────────────────────────────────────────────┘      │
│                                                                                    │
└────────────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 GeoMIP - Estrategia Geométrica

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│                    COMPLEJIDAD GEOMÉTRICA - GeoMIP                                 │
├────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                    │
│   El algoritmo geométrico reduce la complejidad mediante:                          │
│                                                                                    │
│   1. Camino de distancia Hamming: O(n) niveles                                     │
│   2. Por cada nivel: O(2^n) estados pero con memoización                          │
│   3. Cálculo de transiciones: O(n) por estado                                     │
│                                                                                    │
│   ══════════════════════════════════════════════════════════════════════════════   │
│                                                                                    │
│   T(n) = O(n × 2^n)  vs  BruteForce O(2^(m+n))                                     │
│                                                                                    │
│   COMPARATIVA:                                                                     │
│   ┌────────────┬─────────────────┬─────────────────┬───────────────┐               │
│   │   Nodos    │   BruteForce    │     GeoMIP     │  Speedup      │               │
│   ├────────────┼─────────────────┼─────────────────┼───────────────┤               │
│   │     4      │     O(127)      │     O(64)      │    ~2x        │               │
│   │     8      │    O(32K)       │    O(2K)       │    ~16x       │               │
│   │    15      │   O(268M)       │    O(500K)     │    ~500x      │               │
│   └────────────┴─────────────────┴─────────────────┴───────────────┘               │
│                                                                                    │
└────────────────────────────────────────────────────────────────────────────────────┘
```

### 3.3 Notación Asintótica - Resumen

| Algoritmo | Complejidad Temporal | Complejidad Espacial |
|-----------|---------------------|---------------------|
| **BruteForce** | O(2^(m+n)) | O(2^n) por estado |
| **GeoMIP** | O(n × 2^n) | O(n × 2^n) |
| **PyPhi** | O(2^(m+n)) | O(2^n) |
| **Q-Nodes** | Depende de heurística | O(2^n) |

---

## 4. Matriz de Riesgos

### 4.1 Riesgos Técnicos

| ID | Riesgo | Categoría | Probabilidad | Impacto | Severidad | Mitigación |
|----|--------|-----------|--------------|---------|-----------|------------|
| **R1** | PyPhi no compila en Windows (C++ Build Tools) | Entorno | Alta | Alto | 🔴 Crítica | Documentar instalación de MSVC |
| **R2** | Overflow de memoria para N > 12 (BruteForce) | Rendimiento | Alta | Alto | 🔴 Crítica | Limitar análisis a N≤10 |
| **R3** | Resultados inconsistentes entre estrategias | Validación | Media | Alto | 🟠 Alta | Comparar con PyPhi como gold standard |
| **R4** | EMD calculada incorrectamente | Algoritmo | Media | Alto | 🟠 Alta | Verificar con casos conocidos |
| **R5** | Cache de Pyphi corrupto | Datos | Baja | Medio | 🟡 Media | Limpiar `__pyphi_cache__` |
| **R6** | Diferencias numéricas (float32 vs float64) | Numérico | Media | Bajo | 🟡 Media | Estandarizar a float64 |

### 4.2 Riesgos de Proyecto

| ID | Riesgo | Probabilidad | Impacto | Severidad |
|----|--------|--------------|---------|-----------|
| **P1** | Complejidad algorítmica impide validación empírica | Media | Alto | 🟠 Alta |
| **P2** | Documentación desactualizada | Alta | Medio | 🟡 Media |
| **P3** | Falta de tests automatizados | Alta | Medio | 🟡 Media |

### 4.3 Constraints Identificados

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              CONSTRAINTS DEL PROYECTO                               │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│   [HARD CONSTRAINTS]                                                                │
│   ┌────────────────────────────────────────────────────────────────────────────┐    │
│   │ • Python 3.11+ como lenguaje obligatorio                                    │    │
│   │ • PyPhi 1.2.0 como referencia teórica (no reemplazable)                    │    │
│   │ • Windows como plataforma principal de desarrollo                          │    │
│   │ • Archivos CSV para TPMs (formato obligatorio)                            │    │
│   └────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                     │
│   [SOFT CONSTRAINTS]                                                                │
│   ┌────────────────────────────────────────────────────────────────────────────┐    │
│   │ • Preferir NumPy sobre Python puro para operaciones matriciales             │    │
│   │ • Mantener resultados en Excel para compatibilidad académica               │    │
│   │ • Usar colorama para logging visually distinguishable                       │    │
│   └────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                     │
│   [PERFORMANCE CONSTRAINTS]                                                         │
│   ┌────────────────────────────────────────────────────────────────────────────┐    │
│   │ • Análisis completo de red 4-nodos: < 1 segundo                            │    │
│   │ • Análisis completo de red 8-nodos: < 60 segundos                         │    │
│   │ • GeoMIP debe ser al menos 10x más rápido que BruteForce                   │    │
│   └────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Límites del Proyecto (Scope Boundaries)

### 5.1 What's IN Scope (Incluido)

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           DENTRO DEL ALCANCE (IN)                                   │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│   ✓ Implementación de estrategias MIP (BruteForce, Q, PyPhi, GeoMIP)               │
│   ✓ Cálculo de Φ (Phi) para redes de 3-15 nodos                                   │
│   ✓ Análisis de biparticiones y particiones                                       │
│   ✓ Generación de TPMs sintéticas                                                 │
│   ✓ Validación contra PyPhi (referencia teórica)                                  │
│   ✓ Comparativa de rendimiento entre estrategias                                  │
│   ✓ Visualización de resultados en Excel                                          │
│   ✓ Profiling de rendimiento (pyinstrument)                                       │
│   ✓ Logging estructurado                                                          │
│   ✓ Documentación del proyecto                                                    │
│                                                                                     │
│   [COMPONENTES INCLUIDOS]                                                           │
│   ┌─────────────────────────────────────────────────────────────────────────────┐    │
│   │ • QNodes: Framework principal                                               │    │
│   │ • GeoMIP Method 1: GPU Accelerated                                          │    │
│   │ • GeoMIP Method 2: Dynamic Programming Reformulation                       │    │
│   │ • Datos: TPMs de redes 3-15 nodos                                           │    │
│   │ • Resultados: Excel con comparativas                                         │    │
│   └─────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 What's OUT of Scope (Excluido)

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           FUERA DEL ALCANCE (OUT)                                   │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│   ✗ Implementación de otros algoritmos IIT (ECA, EMI, etc.)                       │
│   ✗ Interfaz gráfica de usuario (GUI)                                              │
│   ✗ API REST para servir el framework                                             │
│   ✗ Base de datos persistente (más allá de CSV/Excel)                            │
│   ✗ Integración con herramientas de visualization (D3.js, etc.)                  │
│   ✗ Análisis de redes mayores a 15 nodos (por limitaciones de rendimiento)         │
│   ✗ Implementación de MPI/Distributed computing                                   │
│   ✗ Soporte para otros lenguajes (R, Julia)                                        │
│   ✗ Despliegue en cloud (AWS, GCP, Azure)                                         │
│                                                                                     │
│   [EXPLICITAMENTE NO INCLUIDO]                                                      │
│   ┌─────────────────────────────────────────────────────────────────────────────┐    │
│   │ • Cliente web o aplicación móvil                                            │    │
│   │ • Integración con sistemas de archivos externos                             │    │
│   │ • Autenticación y autorización                                               │    │
│   │ • Tests unitarios formales (más allá de pruebas manuales)                   │    │
│   │ • CI/CD pipeline                                                              │    │
│   └─────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### 5.3 Scope Boundary Diagram

```
                    ┌──────────────────────────────────────────┐
                    │           FRONTERA DEL PROYECTO           │
                    │                                          │
    ┌───────────────┼──────────────────────────────────────────┼───────────────┐
    │               │                                          │               │
    │   DENTRO      │              PROYECTO                   │   DENTRO      │
    │               │                                          │               │
    │  ┌─────────┐  │  ┌────────────────────────────────────┐  │  ┌─────────┐  │
    │  │ QNodes  │  │  │         GeoMIP                     │  │  │  Data   │  │
    │  │ Framework│  │  │    (Method1 + Method2)             │  │  │ (TPMs)  │  │
    │  └─────────┘  │  └────────────────────────────────────┘  │  └─────────┘  │
    │               │                                          │               │
    │  ┌─────────┐  │  ┌────────────────────────────────────┐  │  ┌─────────┐  │
    │  │ PyPhi   │  │  │      Estrategias                    │  │  │Results  │  │
    │  │ (Ref)   │  │  │  (BF, Q, Geometric)                 │  │  │(Excel)  │  │
    │  └─────────┘  │  └────────────────────────────────────┘  │  └─────────┘  │
    │               │                                          │               │
    └───────────────┼──────────────────────────────────────────┼───────────────┘
                    │                                          │
                    │              FUERA                        │
                    │  ┌────────────────────────────────────┐  │
                    │  │ • GUI / Web App                    │  │
                    │  │ • API REST                         │  │
                    │  │ • Cloud Deployment                 │  │
                    │  │ • N > 15 nodes                     │  │
                    │  │ • Other IIT algorithms            │  │
                    │  └────────────────────────────────────┘  │
                    └──────────────────────────────────────────┘
```

---

## 6. Contexto Funcional

### 6.1 Objetivos Algorítmicos

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                         OBJETIVOS ALGORÍTMICOS DEL PROYECTO                          │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│   OBJ-1: RESOLUCIÓN DEL PROBLEMA MIP                                                │
│   ═══════════════════════════════════════════════════════════════════════════════   │
│   │ Objetivo: Encontrar la bipartición que minimiza la información integrada       │
│   │ Input: TPM (Transition Probability Matrix), estado inicial                    │
│   │ Output: Φ (Phi), partición óptima, distribución marginal                      │
│   │ Métrica: EMD (Earth Mover's Distance)                                          │
│   └────────────────────────────────────────────────────────────────────────────────   │
│                                                                                     │
│   OBJ-2: OPTIMIZACIÓN DE RENDIMIENTO                                               │
│   ═══════════════════════════════════════════════════════════════════════════════   │
│   │ Objetivo: Reducir complejidad temporal de O(2^(m+n)) a O(n × 2^n)              │
│   │ Enfoque: GeoMIP con estrategia geométrica-topológica                          │
│   │ Benchmark: GeoMIP debe ser al menos 10x más rápido que BruteForce             │
│   └────────────────────────────────────────────────────────────────────────────────   │
│                                                                                     │
│   OBJ-3: VALIDACIÓN CONTRA REFERENCIA                                             │
│   ═══════════════════════════════════════════════════════════════════════════════   │
│   │ Objetivo: Verificar que los resultados de GeoMIP coincidan con PyPhi          │
│   │ Criterio: |Φ_GeoMIP - Φ_PyPhi| < ε (tolerancia numérica)                     │
│   │ Metodología: Comparar con casos de prueba conocidos                            │
│   └────────────────────────────────────────────────────────────────────────────────   │
│                                                                                     │
│   OBJ-4: ESCALABILIDAD A REDES EMPÍRICAS                                            │
│   ═══════════════════════════════════════════════════════════════════════════════   │
│   │ Objetivo: Ejecutar análisis en redes de hasta 15 nodos                         │
│   │ Datos: Redes de Drosophila melanogaster (15 nodos)                             │
│   │ Constraint: Tiempo de ejecución < 1 hora para cualquier red                  │
│   └────────────────────────────────────────────────────────────────────────────────   │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### 6.2 Funcionalidades Clave

| ID | Funcionalidad | Descripción | Prioridad |
|----|---------------|-------------|-----------|
| **F1** | `aplicar_estrategia()` | Ejecutar análisis MIP con estrategia seleccionada | Crítica |
| **F2** | `analizar_completamente_una_red()` | Análisis exhaustivo de todos los subsistemas | Alta |
| **F3** | `cargar_red()` | Cargar TPM desde archivo CSV | Alta |
| **F4** | `generar_red()` | Generar TPM sintético | Media |
| **F5** | `bipartir()` | Crear bipartición de un sistema | Alta |
| **F6** | `distribucion_marginal()` | Calcular distribución marginal | Alta |
| **F7** | `emd_efecto()` | Calcular Earth Mover's Distance | Crítica |
| **F8** | Profiling | Medir rendimiento con pyinstrument | Media |

### 6.3 Diagrama de Flujo de Datos

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                        FLUJO DE DATOS - ANÁLISIS MIP                                 │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│                                                                                     │
│      ┌─────────┐      ┌─────────────┐      ┌──────────────┐      ┌─────────┐       │
│      │  TPM    │─────▶│   Manager   │─────▶│    SIA       │─────▶│ Solution│       │
│      │ (CSV)   │      │ (Loading)   │      │ (Analysis)   │      │ (Φ, π, t)│       │
│      └─────────┘      └─────────────┘      └──────────────┘      └─────────┘       │
│          │                                       │                    │              │
│          │                                       ▼                    │              │
│          │                              ┌─────────────────┐         │              │
│          │                              │   Subsystem     │         │              │
│          │                              │   Generation    │         │              │
│          │                              └────────┬────────┘         │              │
│          │                                       │                  │              │
│          │                                       ▼                  │              │
│          │                              ┌─────────────────┐         │              │
│          │                              │  Bipartition    │         │              │
│          │                              │  Generation     │─────────┘              │
│          │                              │  O(2^(m+n-1))   │                        │
│          │                              └────────┬────────┘                        │
│          │                                       │                                 │
│          │                                       ▼                                 │
│          │                              ┌─────────────────┐                        │
│          │                              │    EMD          │                        │
│          │                              │    Calculation  │                        │
│          │                              │  (scipy.OT)     │                        │
│          │                              └────────┬────────┘                        │
│          │                                       │                                 │
│          │                                       ▼                                 │
│          │                              ┌─────────────────┐                        │
│          │                              │   MIN(Φ)        │                        │
│          │                              │  Find MIP       │                        │
│          │                              └─────────────────┘                        │
│          │                                       │                                 │
│          ◄───────────────────────────────────────┘                                 │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Análisis de Punto de Anclaje (OpenSpec)

### 7.1 Módulos Estables (Anclaje)

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                         PUNTO DE ANCLAJE - MÓDULOS ESTABLES                         │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│   Los siguientes módulos han demostrado estabilidad y no requieren intervención:  │
│                                                                                     │
│   ✓ [ESTABLE] src/constants/base.py                                               │
│   │   └─ Solo definiciones de constantes, sin lógica compleja                    │
│   │                                                                                 │
│   ✓ [ESTABLE] src/models/core/solution.py                                         │
│   │   └─ Estructura de datos simple, validada en múltiples runs                   │
│   │                                                                                 │
│   ✓ [ESTABLE] src/funcs/format.py                                                 │
│   │   └─ Funciones de formateo sin efectos secundarios                             │
│   │                                                                                 │
│   ✓ [ESTABLE] data/samples/*.csv                                                  │
│   │   └─ Archivos de datos probados con múltiples estrategias                     │
│   │                                                                                 │
│   ✓ [ESTABLE] src/middlewares/slogger.py                                          │
│   │   └─ Logging maduro y estable                                                 │
│   │                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### 7.2 Módulos que Requieren Intervención

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                   MÓDULOS QUE REQUIEREN INTERVENCIÓN                                │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│   ⚠️ [INTERVENCIÓN] src/strategies/force.py                                         │
│   │   └─ Complejidad O(2^(m+n)) causing memory overflows for N>10                 │
│   │   └─ Necesita optimización o límite de uso                                    │
│   │                                                                                 │
│   ⚠️ [INTERVENCIÓN] src/funcs/force.py                                            │
│   │   └─ генератор particiones con posibles memory leaks                          │
│   │   └─ Necesita revisión de gestión de memoria                                   │
│   │                                                                                 │
│   ⚠️ [INTERVENCIÓN] GeoMIP/src/strategies/geometric.py                            │
│   │   └─ Algoritmo en desarrollo, no completamente validado                       │
│   │   └─ Necesita más casos de prueba                                             │
│   │                                                                                 │
│   ⚠️ [INTERVENCIÓN] src/controllers/manager.py                                    │
│   │   └─ Carga de datos tiene código duplicado en QNodes y GeoMIP                 │
│   │   └─ Refactorización necesaria para compartir código                          │
│   │                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 8. Resumen Ejecutivo

### 8.1 Hallazgos Clave

1. **Proyecto Brownfield** con código existente maduro en QNodes
2. **Dos implementaciones**: BruteForce (exhaustivo) vs GeoMIP (optimizado)
3. **Dependencia crítica**: PyPhi requiere C++ Build Tools en Windows
4. **Riesgo principal**: Complejidad exponencial limita análisis a N≤10 con BruteForce
5. **Validación**: Necesita más casos de prueba para GeoMIP

### 8.2 Recomendaciones

| Prioridad | Acción |
|-----------|--------|
| **Alta** | Documentar instalación de PyPhi en Windows |
| **Alta** | Implementar límites de N para BruteForce |
| **Media** | Unificar código entre QNodes y GeoMIP |
| **Media** | Añadir casos de prueba para GeoMIP |
| **Baja** | Considerar refactoring de Manager |

---

## 9. Próximos Pasos

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              ESTADO ACTUAL                                           │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│   [✓] Mapeo de Estructura          → Completado                                    │
│   [✓] Identificación de Dependencias → Completado                                   │
│   [✓] Detección de Riesgos          → Completado                                    │
│   [✓] Análisis de Punto de Anclaje → Completado                                    │
│                                                                                     │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                  SIGUIENTE FASE                                     │
│                                                                                     │
│   El usuario debe validar este análisis antes de proceder a /opsx:propose          │
│                                                                                     │
│   Para aprobar: "Los hallazgos son correctos, procede a la fase de propuesta"     │
│                                                                                     │
│   Para corregir: "Hay aspectos que deben revisarse: [especificar]"                  │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

*Exploration Report generado - Fase `/opsx:explore` completada*  
*awaiting_validation: true*