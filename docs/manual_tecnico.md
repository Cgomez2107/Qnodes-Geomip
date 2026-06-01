# Manual Técnico — Proyecto K-QGMIP

**K-Particiones de Mínima Información con KQNodes y KGeoMIP**

Universidad de Caldas  
Facultad de Inteligencia Artificial e Ingenierías  
Análisis y Diseño de Algoritmos — 2026-1

---

## Tabla de Contenidos

1. [Introducción](#1-introducción)
2. [Marco Teórico](#2-marco-teórico)
   - 2.1 [K-Partición](#21-k-partición)
   - 2.2 [Partición de Mínima Información](#22-partición-de-mínima-información)
   - 2.3 [Pérdida de Información (φ)](#23-pérdida-de-información-φ)
   - 2.4 [Earth Mover's Distance (EMD)](#24-earth-movers-distance-emd)
   - 2.5 [Distribución Marginal](#25-distribución-marginal)
   - 2.6 [Submodularidad](#26-submodularidad)
3. [Arquitectura del Software](#3-arquitectura-del-software)
   - 3.1 [Estructura General del Proyecto](#31-estructura-general-del-proyecto)
   - 3.2 [Diagrama de Componentes](#32-diagrama-de-componentes)
   - 3.3 [Diagrama de Clases](#33-diagrama-de-clases)
   - 3.4 [Flujo de Ejecución](#34-flujo-de-ejecución)
4. [Algoritmos](#4-algoritmos)
   - 4.1 [Algoritmo General de K-Particiones](#41-algoritmo-general-de-k-particiones-recursivas)
   - 4.2 [KQNodes: Algoritmo Q con Optimización Submodular](#42-kqnodes-algoritmo-q-con-optimización-submodular)
   - 4.3 [KGeoMIP: GeometricSIA con Búsqueda Geométrica](#43-kgeomip-geometricsia-con-búsqueda-geométrica-dp)
   - 4.4 [Post-Optimización Local](#44-post-optimización-local)
   - 4.5 [Cálculo de φ_k](#45-cálculo-de-φ_k)
5. [Análisis de Complejidad](#5-análisis-de-complejidad)
   - 5.1 [Complejidad del Sistema Base](#51-complejidad-del-sistema-base)
   - 5.2 [Complejidad de KQNodes](#52-complejidad-de-kqnodes)
   - 5.3 [Complejidad de KGeoMIP](#53-complejidad-de-kgeomip)
   - 5.4 [Complejidad del Post-Optimizador](#54-complejidad-del-post-optimizador)
   - 5.5 [Complejidad Total por Estrategia](#55-complejidad-total-por-estrategia)
6. [Resultados Experimentales](#6-resultados-experimentales)
   - 6.1 [Configuración Experimental](#61-configuración-experimental)
   - 6.2 [Resultados por Sistema](#62-resultados-por-sistema)
   - 6.3 [Comparación KQNodes vs KGeoMIP](#63-comparación-kqnodes-vs-kgeomip)
   - 6.4 [Análisis de Tiempos de Ejecución](#64-análisis-de-tiempos-de-ejecución)
   - 6.5 [Anomalías y Casos Especiales](#65-anomalías-y-casos-especiales)
7. [Reflexión Crítica](#7-reflexión-crítica)
   - 7.1 [Limitaciones](#71-limitaciones)
   - 7.2 [Mejoras Potenciales](#72-mejoras-potenciales)
   - 7.3 [Lecciones Aprendidas](#73-lecciones-aprendidas)

---

## 1. Introducción

El proyecto K-QGMIP aborda el problema de encontrar **k-particiones de mínima información** en sistemas dinámicos discretos. Dado un sistema de N nodos con una Matriz de Probabilidades de Transición (TPM), se busca dividir sus nodos en k subconjuntos (particiones) de manera que la **pérdida de información** (φ) entre la dinámica del sistema completo y la dinámica del sistema particionado sea mínima.

Se implementan dos estrategias independientes:

- **KQNodes** (_K-Particiones QNodes_): Extensión del algoritmo QNodes original de bi-particiones, que utiliza **optimización submodular** con reinicios aleatorios para encontrar particiones que minimicen φ. La estrategia subyacente es QNodes (Q), un algoritmo voraz con refinamiento local 1-opt.

- **KGeoMIP** (_K-Particiones GeoMIP_): Extensión del algoritmo GeometricSIA original, que reformula el problema de partición como una **búsqueda geométrica sobre estados** utilizando programación dinámica con beam search. La estrategia subyacente es GeometricSIA.

Ambas estrategias operan de forma independiente sobre los mismos datos de entrada, permitiendo comparar sus resultados en términos de calidad de partición (φ) y tiempo de ejecución.

El problema tiene aplicaciones en el análisis de sistemas complejos, particularmente en el marco de la Teoría de la Información Integrada (IIT), donde encontrar la partición de mínima información es fundamental para determinar el nivel de integración de un sistema.

---

## 2. Marco Teórico

### 2.1 K-Partición

Una **k-partición** de un conjunto de N elementos es una colección de k subconjuntos no vacíos, disjuntos y cuya unión es el conjunto original. Formalmente:

Dado un conjunto de nodos _V_ = {v₁, v₂, ..., v_N}, una k-partición es una familia de subconjuntos {P₁, P₂, ..., P_k} tal que:

- Pᵢ ≠ ∅ para todo i ∈ {1, ..., k}
- Pᵢ ∩ Pⱼ = ∅ para todo i ≠ j
- ⋃ᵢ₌₁ᵏ Pᵢ = V

En el contexto del proyecto, cada Pᵢ representa un **subsistema** que agrupa un subconjunto de nodos del sistema original. La partición se construye recursivamente: se parte del conjunto completo de nodos y se aplican **(k-1) bi-particiones** sucesivas, donde cada bi-partición divide el subconjunto más grande en dos partes.

### 2.2 Partición de Mínima Información

Una **Partición de Mínima Información** (Minimum Information Partition, MIP) es aquella que minimiza la pérdida de información φ al dividir el sistema en subsistemas independientes. La idea fundamental es:

- El sistema completo tiene una dinámica conjunta descrita por su TPM.
- Al particionar el sistema, se "cortan" las interacciones entre subsistemas.
- Cada subsistema evoluciona independientemente según su propia dinámica marginal.
- La **pérdida de información** mide qué tanto se desvía la dinámica particionada de la dinámica original.

La MIP es la partición que causa la menor distorsión posible, es decir, aquella donde los subsistemas resultantes son "lo más independientes posible" pero "lo menos disruptivos posible" respecto al comportamiento original.

### 2.3 Pérdida de Información (φ)

La pérdida de información φ (phi) cuantifica qué tanto difiere el comportamiento del sistema particionado respecto al sistema original. Se define como:

φ = EMD( p_original(X), p_partición(X) )

Donde:
- **p_original(X)** es la distribución de probabilidad marginal del sistema completo sobre el estado de cada nodo.
- **p_partición(X)** es la distribución de probabilidad marginal del sistema particionado, donde cada subsistema se evalúa independientemente y luego se combinan sus distribuciones.

Un valor de **φ = 0** indica que la partición no causa pérdida de información: el sistema particionado se comporta exactamente igual que el sistema completo. Valores más altos indican mayor distorsión.

### 2.4 Earth Mover's Distance (EMD)

La **Earth Mover's Distance** (también conocida como distancia de Wasserstein o distancia de Kantorovich-Rubinstein) mide la distancia entre dos distribuciones de probabilidad. En este proyecto, bajo el supuesto de independencia condicional entre variables, la EMD se reduce a la **distancia L1** (Manhattan) entre los vectores de probabilidad marginal:

EMD(u, v) = Σᵢ |uᵢ - vᵢ|

Donde uᵢ y vᵢ son las probabilidades marginales del nodo i bajo las dos distribuciones comparadas. Cada elemento representa la probabilidad de que un nodo específico esté en un estado particular (ON = 1) dado el estado inicial del sistema.

**Interpretación intuitiva**: La EMD mide cuánta "masa de probabilidad" debe moverse para transformar una distribución en otra. En una dimensión y con distribuciones marginales condicionalmente independientes, el costo de transporte óptimo es simplemente la suma de las diferencias absolutas por variable.

### 2.5 Distribución Marginal

La **distribución marginal** de un nodo en un sistema es la probabilidad de que ese nodo esté en un estado específico, promediando sobre todos los posibles estados de los demás nodos. Formalmente, dado un sistema con TPM _T_ y un estado inicial _s₀_:

p(Xᵢ = 1 | s₀) = Σ_{s∈{0,1}^N} T(s | s₀) · δ(sᵢ = 1)

Bajo el modelo de red de cubos (n-cubes) utilizado en el proyecto, la distribución marginal se obtiene directamente de la TPM seleccionando la probabilidad correspondiente al estado inicial para cada nodo.

### 2.6 Submodularidad

Una función de conjunto _f_: 2^V → ℝ es **submodular** si para todo A ⊆ B ⊆ V y todo elemento v ∉ B:

f(A ∪ {v}) - f(A) ≥ f(B ∪ {v}) - f(B)

**Interpretación**: La submodularidad captura la propiedad de **rendimientos decrecientes**: añadir un elemento a un conjunto pequeño produce mayor ganancia que añadirlo a un conjunto grande.

En el contexto de QNodes, la función de pérdida de información al agrupar nodos en una partición resulta ser submodular. Esto permite utilizar algoritmos voraces con **garantías de aproximación** (factor (1 - 1/e) para maximización de funciones submodulares monótonas). Sin embargo, en el problema de minimización de φ, la submodularidad permite búsquedas locales eficientes con buenas soluciones en la práctica.

---

## 3. Arquitectura del Software

### 3.1 Estructura General del Proyecto

```
Proyecto_Analisis_2026_1/
├── QNodes/                          # Estrategia KQNodes
│   ├── src/
│   │   ├── strategies/
│   │   │   └── q_nodes.py           # Algoritmo QNodes (Q)
│   │   ├── models/
│   │   │   └── core/
│   │   │       ├── system.py        # Sistema, NCube
│   │   │       └── ...
│   │   └── funcs/
│   │       └── iit.py               # emd_efecto
│   ├── pyproject.toml
│   └── .samples/                    # TPMs (N3 a N25)
│
├── GeoMIP/                          # Estrategia KGeoMIP
│   ├── src/
│   │   ├── controllers/
│   │   │   └── strategies/
│   │   │       └── geometric.py     # GeometricSIA
│   │   ├── models/
│   │   │   └── core/
│   │   │       └── system.py        # System, NCube
│   │   └── funcs/
│   │       └── base.py              # emd_efecto
│   ├── pyproject.toml
│   └── data/samples/                # TPMs (N3 a N25)
│
├── scripts/                         # Código de experimentación
│   ├── k_partitions_qnodes.py       # Runner KQNodes
│   ├── k_partitions.py              # Runner KGeoMIP
│   ├── analisis_resultados.py       # Extracción y visualización
│   └── utils/
│       ├── converter.py             # excel_a_bits / bits_a_excel
│       ├── excel_handler.py         # Lectura/escritura Excel
│       └── tpm_loader.py            # Carga de TPMs
│
├── DatosPruebas2026_1 (1).xlsx      # Datos de prueba y resultados
├── reports/                         # Gráficas generadas
└── docs/                            # Documentación
```

### 3.2 Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────────────┐
│                      scripts/ (orquestación)                     │
│                                                                  │
│  ┌─────────────────────┐    ┌──────────────────────────────┐    │
│  │ k_partitions_qnodes │    │     k_partitions.py          │    │
│  │ (Runner KQNodes)    │    │   (Runner KGeoMIP)           │    │
│  └────────┬────────────┘    └────────────┬─────────────────┘    │
│           │                              │                       │
│  ┌────────▼────────────┐    ┌────────────▼─────────────────┐    │
│  │ utils/converter.py  │    │   utils/excel_handler.py     │    │
│  │                     │    │                              │    │
│  │ Excel ⇄ Bits        │    │   Lectura/Escritura .xlsx   │    │
│  └─────────────────────┘    └──────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
           │                              │
           ▼                              ▼
┌──────────────────────┐    ┌──────────────────────────────┐
│      QNodes/         │    │         GeoMIP/              │
│                      │    │                              │
│  ┌────────────────┐  │    │  ┌────────────────────────┐  │
│  │ QNodesStrategy │  │    │  │  GeometricSIA          │  │
│  │ (q_nodes.py)   │  │    │  │  (geometric.py)        │  │
│  │                │  │    │  │                        │  │
│  │ • restarts     │  │    │  │ • beam_width           │  │
│  │ • func.        │  │    │  │ • DP sobre estados     │  │
│  │   submodular   │  │    │  │ • timeout              │  │
│  └──────┬─────────┘  │    │  └───────────┬────────────┘  │
│         │            │    │              │               │
│  ┌──────▼─────────┐  │    │  ┌───────────▼────────────┐  │
│  │  System / NCube │  │    │  │  System / NCube       │  │
│  │  (models/core)  │  │    │  │  (models/core)        │  │
│  └─────────────────┘  │    │  └────────────────────────┘  │
│                       │    │                              │
│  ┌─────────────────┐  │    │  ┌────────────────────────┐  │
│  │  iit.py (EMD)   │  │    │  │  base.py (EMD)        │  │
│  └─────────────────┘  │    │  └────────────────────────┘  │
└───────────────────────┘    └──────────────────────────────┘
```

### 3.3 Diagrama de Clases

```
┌──────────────────────────────────────────────────────────────┐
│                     System                                    │
├──────────────────────────────────────────────────────────────┤
│ - tpm: np.ndarray                                            │
│ - estado_inicio: np.ndarray                                  │
│ - ncubos: tuple[NCube]                                       │
│ - memo: dict (QNodes)                                        │
├──────────────────────────────────────────────────────────────┤
│ + condicionar(indices) → System                              │
│ + substraer(alcance, mecanismo) → System                     │
│ + bipartir(alcance, mecanismo) → System                      │
│ + distribucion_marginal() → np.ndarray                       │
│ + indices_ncubos: np.ndarray                                 │
│ + dims_ncubos: np.ndarray                                    │
└──────────────────────────┬───────────────────────────────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
┌─────────────────────────┐  ┌─────────────────────────┐
│   NCube                 │  │   Solution               │
├─────────────────────────┤  ├─────────────────────────┤
│ - indices: list[int]    │  │ + estrategia: str        │
│ - dims: np.ndarray      │  │ + perdida: float         │
│ - data: np.ndarray      │  │ + particion: str         │
├─────────────────────────┤  │ + tiempo_total: float    │
│ + condicionar()         │  │ + distribuciones         │
│ + marginalizar()        │  └─────────────────────────┘
└─────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  <<abstract>> SIA (Sistema de Información Activo)            │
├──────────────────────────────────────────────────────────────┤
│ # pagina_sample_network: str                                 │
├──────────────────────────────────────────────────────────────┤
│ + aplicar_estrategia(estado, cond, alcance, mec) → Solution  │
│ # sia_preparar_subsistema() → System                         │
└──────────────────────┬───────────────────────────────────────┘
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
┌──────────────────────┐  ┌──────────────────────────────┐
│  QNodes (SIA)        │  │  GeometricSIA (SIA)          │
├──────────────────────┤  ├──────────────────────────────┤
│ + restarts: int      │  │ + beam_width: int            │
│ - memoria_delta      │  │ - tabla_transiciones         │
│ - memoria_grupo      │  │ - caminos / caminos_idx      │
├──────────────────────┤  ├──────────────────────────────┤
│ + aplicar_estrategia │  │ + aplicar_estrategia()       │
│ - funcion_submodular │  │ - find_mip()                 │
│ - refinar_particion  │  │ - identificar_particiones()  │
│ - evaluar_emd        │  │ - calcular_costo()           │
└──────────────────────┘  └──────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  Runner (k_partitions_qnodes.py / k_partitions.py)           │
├──────────────────────────────────────────────────────────────┤
│ + preparar_sistema() → (System, marginal)                    │
│ + resolver_k_particiones() → (subsystems, steps)             │
│   • Algoritmo recursivo: (k-1) bi-particiones                │
│ + post_optimizar() → subsystems                              │
│   • Intercambio local de nodos entre grupos                  │
│ + calcular_phi_k() → float                                   │
│   • EMD entre marginal original y marginal particionado      │
│ + procesar_hoja() → None                                     │
│   • Orquesta lectura, ejecución, escritura Excel             │
└──────────────────────────────────────────────────────────────┘
```

### 3.4 Flujo de Ejecución

El flujo general de ejecución para ambas estrategias es idéntico, diferenciándose solo en la función de bi-partición interna:

```
1. INICIO
   │
2. Cargar configuración (hoja, k_values, parámetros)
   │
3. Leer pruebas desde Excel (10 pruebas por hoja)
   │   Cada prueba tiene: alcance, mecanismo (notación ABCD...)
   │
4. Cargar TPM del sistema (desde archivo .csv o .npy)
   │
5. Para cada prueba:
   │
   5.1 Convertir alcance/mecanismo a bits (excel_a_bits)
   5.2 Preparar sistema base:
   │     System(tpm, estado_inicial)
   │       → condicionar(cond_dims)
   │       → substraer(alc_remove, mec_remove)
   │       → distribucion_marginal()  ← φ de referencia
   │
   5.3 Para cada valor de k (3, 4, 5):
   │
       5.3.1 resolver_k_particiones():
              subsistemas = [todos los nodos efectivos]
              Para i = 1 to k-1:
                ■ Elegir subsistema más grande
                ■ Extraer alcance/mecanismo del subgrupo
                ■ Aplicar estrategia de bi-partición:
                    • KQNodes → QNodesStrategy.aplicar_estrategia()
                    • KGeoMIP → GeometricSIA.aplicar_estrategia()
                ■ Parsear partición resultante (g1, g2)
                ■ Reemplazar subgrupo original por g1, g2
              Retornar: lista de k subsistemas

       5.3.2 post_optimizar(subsistemas):
              Para cada nodo en cada subsistema:
                Probar moverlo a otro subsistema
                Si φ mejora (disminuye), aceptar cambio
              Repetir hasta convergencia (solo N ≤ 15)

       5.3.3 calcular_phi_k(subsistemas):
              Para cada subsistema:
                ■ substraer(resto_nodos, dimensiones_resto)
                ■ distribucion_marginal()
              Combinar distribuciones → k_marginal
              φ = EMD(k_marginal, original_marginal)

   5.4 Acumular resultado en buffer
   │
6. Guardar todos los resultados en Excel (escritura única)
   │
7. FIN
```

---

## 4. Algoritmos

### 4.1 Algoritmo General de K-Particiones Recursivas

El algoritmo central para obtener una k-partición a partir de (k-1) bi-particiones es idéntico para ambas estrategias:

```
ALGORITMO resolver_k_particiones(TPM, estado_inicial, alcance, mecanismo, k, estrategia)
  ENTRADA:
    TPM: matriz de probabilidades de transición (2^N × N)
    estado_inicial: string binario del estado inicial
    alcance, mecanismo: strings binarios de selección de variables
    k: número de particiones deseado
    estrategia: función de bi-partición (QNodes o GeometricSIA)

  SALIDA:
    subsystems: lista de k listas de índices de nodos
    steps: historial de decisiones de partición

1.  cond_dims ← índices donde cond_orig = "0"
2.  all_alc ← índices donde alc_orig = "1"
3.  all_mec ← índices donde mec_orig = "1"
4.  effective_nodes ← sorted(all_alc - cond_dims)
5.  SI effective_nodes está vacío → RETORNAR [], []

6.  SI k > |effective_nodes| → k ← |effective_nodes|

7.  subsystems ← [effective_nodes]
8.  steps ← []

9.  PARA iteration ← 1 HASTA k-1:
10.     largest ← subsistema más grande en subsystems
11.     SI |largest| ≤ 1 → SALIR

12.     alc, mec ← alcance_mec_para_grupo(largest, alc_orig, mec_orig)
13.     sol ← estrategia(TPM, estado_inicial, cond_orig, alc, mec)

14.     g1, g2 ← parse_partition(sol.partición)
15.     SI g1 o g2 vacío → dividir largest por la mitad

16.     Reemplazar largest por g1 y g2 en subsystems
17.     steps ← steps ∪ {(largest, g1, g2, sol.pérdida)}

18.  RETORNAR subsystems, steps
```

**Fundamento del diseño recursivo**: La partición recursiva (dividir el subconjunto más grande en cada paso) es una heurística de construcción basada en el principio de "divide y vencerás". Al dividir siempre el grupo más grande, se busca balancear los tamaños de los subsistemas resultantes. Esta heurística no garantiza optimalidad global pero reduce drásticamente el espacio de búsqueda: de un número exponencial de k-particiones posibles a solo (k-1) bi-particiones.

### 4.2 KQNodes: Algoritmo Q con Optimización Submodular

**Origen**: El algoritmo Q fue desarrollado originalmente para bi-particiones (2-partición o MIP). KQNodes lo extiende aplicándolo recursivamente.

**Fundamento**: La función de pérdida de información al asignar nodos a uno u otro lado de una bipartición es **submodular**. Esto permite usar un algoritmo voraz con garantías teóricas de aproximación.

```
ALGORITMO QNodes.aplicar_estrategia(estado, cond, alc, mec)
  ENTRADA: strings de estado, condición, alcance, mecanismo
  SALIDA: Solution con la mejor bi-partición encontrada

1.  subsistema ← sia_preparar_subsistema(estado, cond, alc, mec)
      → System condicionado y substraído

2.  vertices ← [(0, i) para i en presente] ∪ [(1, j) para j en futuro]

3.  mejor_perdida ← ∞
4.  mejor_particion ← None
5.  mejor_distribucion ← None

6.  PARA restart ← 1 HASTA restarts:
7.      permutar_aleatoriamente(vertices)

8.      // Fase voraz: construir partición creciente
9.      omega ← vertices[0]
10.     delta ← vertices[1:]
11.     PARA v EN delta:
12.         // Evaluar ganancia submodular de mover v a omega
13.         ganancia ← funcion_submodular(delta, omega, v)
14.         SI ganancia mejora φ → mover v a omega

15.     // Fase de refinamiento 1-opt
16.     refinar_particion(omega, delta)

17.     perdida ← evaluar_emd_particion(omega, delta)
18.     SI perdida < mejor_perdida:
19.         mejor_perdida ← perdida
20.         mejor_particion ← (omega, delta)

21.  RETORNAR Solution(mejor_particion, mejor_perdida, ...)
```

**Función submodular** (`funcion_submodular`): Evalúa el cambio en φ al mover un nodo del conjunto delta al conjunto omega. Aprovecha la propiedad de que la EMD puede descomponerse por variable bajo independencia condicional:

```
funcion_submodular(delta, omega, v):
  // EMD actual = Σ|p_delta - p_original| + Σ|p_omega - p_original|
  // EMD propuesta = mover v de delta a omega
  // Solo cambian términos que involucran a v
  // → evaluar marginal(omega ∪ {v}) y marginal(delta \ {v})
  → RETORNAR cambio en EMD
```

**Refinamiento 1-opt** (`refinar_particion`): Después de la fase voraz, se prueba mover cada vértice individualmente al otro lado de la partición. Si el movimiento reduce φ, se acepta. Se repite hasta que ningún movimiento unilateral mejore la solución. Esto convierte el resultado voraz en un **mínimo local** bajo movimientos 1-opt.

### 4.3 KGeoMIP: GeometricSIA con Búsqueda Geométrica DP

**Origen**: GeometricSIA reformula el problema de partición como la búsqueda del camino de costo mínimo entre el estado inicial y el estado final (bit-flip), en un espacio de estados geométrico.

**Fundamento**: La dinámica del sistema puede descomponerse en transiciones entre estados que difieren en un bit (distancia Hamming = 1). La asignación de cada nodo al lado presente o futuro de la partición determina el costo de estas transiciones.

```
ALGORITMO GeometricSIA.aplicar_estrategia(cond, alc, mec, TPM, timeout)
  ENTRADA:
    cond, alc, mec: strings de selección
    TPM: matriz de transición
    timeout: tiempo máximo (opcional)
  SALIDA: Solution con la mejor partición

1.  subsistema ← sia_preparar_subsistema(estado, cond, alc, mec)
2.  flat ← aplanar_datos_ncubo(subsistema)  // matriz plana TPM

3.  estado_inicial ← subsistema.estado_inicio
4.  estado_final ← 1 - estado_inicial  // bit-flip

5.  // Búsqueda geométrica: explorar estados por distancia Hamming
6.  niveles ← []
7.  PARA d ← 0 HASTA n:
8.      nivel_d ← {estados con Hamming(estado_inicial, s) = d}
9.      PARA cada estado s EN nivel_d:
10.         costo ← calcular_costo_transición(s, flat)
11.     niveles ← niveles ∪ {nivel_d}

12.  // Programación dinámica: identificar particiones óptimas
13.  candidatos ← identificar_particiones_optimas(niveles, beam_width)
14.      // Para cada nivel, mantener solo beam_width mejores particiones
15.      // Cada partición asigna variables a presente o futuro
16.      // Evaluar usando costo acumulado

17.  mejor_particion ← argmin(φ, candidatos)
18.  RETORNAR Solution(mejor_particion, ...)
```

**Búsqueda con Beam Search**: En lugar de explorar exhaustivamente todas las 2^n particiones posibles (intratable para n > 15), se usa beam search con ancho de haz (beam_width) que mantiene solo las mejores `beam_width` soluciones parciales en cada nivel.

### 4.4 Post-Optimización Local

Después de construir la k-partición recursivamente, se aplica un post-procesamiento de optimización local:

```
ALGORITMO post_optimizar(subsistemas, sistema_preprocesado, marginal_original, N)
  ENTRADA:
    subsystems: lista de k listas de nodos
    preprocessed: System preprocesado
    original_marginal: distribución marginal de referencia
    N: número total de nodos

  SALIDA: subsystems optimizados

1.  SI N > 15: RETORNAR subsystems  // Muy costoso para sistemas grandes
2.  subsystems ← copia_profunda(subsystems)

3.  REPETIR:
4.      cambiado ← Falso
5.      phi_actual ← calcular_phi(subsystems, preprocessed, original_marginal)
6.      PARA i ← 0 HASTA k-1:
7.          PARA cada nodo EN subsystems[i]:
8.              mejor_phi ← phi_actual
9.              mejor_j ← i
10.             PARA j ← 0 HASTA k-1, j ≠ i:
11.                 Probar mover nodo de i a j
12.                 nueva_phi ← calcular_phi(nueva_particion)
13.                 SI nueva_phi < mejor_phi - ε:
14.                     mejor_phi ← nueva_phi
15.                     mejor_j ← j
16.             SI mejor_j ≠ i:
17.                 Mover nodo de i a mejor_j
18.                 phi_actual ← mejor_phi
19.                 cambiado ← Verdadero
20.  HASTA QUE NO cambiado

21.  RETORNAR subsystems
```

**Costo computacional**: O(k · N · iteraciones) evaluaciones de φ_k, donde cada evaluación cuesta O(k · 2^{|subsistema|}) en el peor caso. Por eso se limita a N ≤ 15.

### 4.5 Cálculo de φ_k

El cálculo de φ_k es la operación fundamental que mide la calidad de una k-partición:

```
ALGORITMO calcular_phi_k(sistema_preprocesado, marginal_original, subsistemas)
  ENTRADA:
    preprocessed: System preprocesado (condicionado + substraído)
    original_marginal: distribución marginal del sistema completo
    subsystems: lista de k listas de índices de nodos

  SALIDA: φ_k (pérdida de información)

1.  k_marginal ← vector_ceros(tamaño = |original_marginal|)

2.  PARA cada grupo_de_nodos EN subsystems:
3.      // Remover nodos NO pertenecientes al grupo
4.      remove_alc ← índices_ncubos - grupo_de_nodos
5.      remove_dims ← dimensiones_ncubos - grupo_de_nodos
6.      sub_system ← preprocessed.substraer(remove_alc, remove_dims)
7.      sub_marginal ← sub_system.distribucion_marginal()

8.      // Mapear distribución del subsistema al vector global
9.      PARA j, idx EN enumerate(sub_system.indices_ncubos):
10.         pos ← posición de idx en preprocessed.indices_ncubos
11.         k_marginal[pos] ← sub_marginal[j]

12.  φ ← EMD(k_marginal, original_marginal)
13.  RETORNAR φ
```

**Interpretación**: El algoritmo construye una distribución marginal combinada evaluando cada subsistema aisladamente. La EMD entre esta distribución "particionada" y la distribución original cuantifica cuánta información se pierde al tratar los subsistemas como independientes.

---

## 5. Análisis de Complejidad

### 5.1 Complejidad del Sistema Base

**System.condicionar(indices)**: Para cada NCube, condicionar sobre d dimensiones implica reducir el cubo de 2^m a 2^{m-d} elementos. Si cada NCube tiene m dimensiones, el costo es O(|ncubos| · 2^{m-d}).

**System.substraer(alcance, mecanismo)**: Similar a condicionar: marginalizar sobre dims mecanismo reduce cada cubo de 2^m a 2^{m-|mecanismo|}. Costo: O(|ncubos| · 2^{m-|mecanismo|}).

**System.distribucion_marginal()**: Seleccionar una entrada del cubo por nodo. Costo: O(N).

**Costo total de preparar_sistema()**: O(N · 2^{N - |cond| - |mec|}) donde cond y mec son las dimensiones condicionadas y substraídas. En el peor caso (sin condicionamiento), O(N · 2^N).

### 5.2 Complejidad de KQNodes

**Bi-partición individual (QNodes)**:
- Fase voraz: O(N² · cost_emd), donde cada evaluación EMD es O(N)
- Refinamiento 1-opt: O(N² · cost_emd)
- Restarts: R veces
- Total por bi-partición: O(R · N³)

Dado que la TPM tiene 2^N filas, el costo real está dominado por las operaciones sobre los cubos durante condicionar/substraer dentro de cada evaluación de EMD. Cada evaluación en el peor caso cuesta O(2^N).

**Costo real por bi-partición**: O(R · N · 2^N)

**K-particiones recursivas**: Se aplican (k-1) bi-particiones sobre subconjuntos decrecientes. En el peor caso, el primer split opera sobre N nodos, el segundo sobre ~N/2, etc.

**Costo total KQNodes**:
- Peor caso: O(R · k · 2^N) — dominado por la primera bi-partición sobre N nodos
- Caso típico: O(R · (k-1) · 2^{N/k}) — cada subproblema es más pequeño

### 5.3 Complejidad de KGeoMIP

**Bi-partición individual (GeometricSIA)**:
- Generación de niveles por distancia Hamming: O(2^N) estados
- Beam search con ancho B: O(B · N · 2^N)
- Cada evaluación de partición requiere marginalización de cubos

**Costo real por bi-partición**: O(B · 2^N) para exploración de estados

**Costo total KGeoMIP**: Similar a KQNodes: O(B · k · 2^N) en el peor caso, pero con una constante menor porque la exploración de estados no requiere reinicios.

### 5.4 Complejidad del Post-Optimizador

- Evalúa mover cada nodo a cada otro grupo: O(k · N · iteraciones) evaluaciones de φ_k
- Cada φ_k cuesta O(k · 2^{N/k}) marginalizaciones
- Total: O(k² · N · iteraciones · 2^{N/k})

**Limitación práctica**: Solo aplicable para N ≤ 15 porque 2^{15} = 32,768 es manejable, pero 2^{20} = 1,048,576 ya es prohibitivo para múltiples iteraciones.

### 5.5 Complejidad Total por Estrategia

| Estrategia | Costo Teórico (peor caso) | Costo Práctico |
|---|---|---|
| KQNodes | O(R · k · 2^N · N) | O(R · k · 2^{Neff/k}) |
| KGeoMIP | O(B · k · 2^N · N) | O(B · k · 2^{Neff/k}) |
| Post-opt (N≤15) | O(k² · N · iter · 2^{N/k}) | O(k² · N · iter · 2^{N/k}) |

Donde:
- R = número de reinicios (1-5 según N)
- B = beam_width (1-3 según N)
- k = número de particiones (3-5)
- N_eff = nodos efectivos después de condicionamiento

**Escalabilidad observada**:

| N | 2^N | Tiempo KQNodes | Tiempo KGeoMIP |
|---|---|---|---|
| 10 | 1,024 | ~2s | ~0.5s |
| 15 | 32,768 | ~3s | ~20-120s |
| 20 | 1,048,576 | ~300-1600s | ~100-200s |
| 22 | 4,194,304 | ~40 min/split | ~5-10 min/split |
| 25 | 33,554,432 | Inviable (~37h) | Inviable |

La diferencia en escalabilidad entre ambas estrategias se debe a que KGeoMIP no requiere reinicios aleatorios (R = 1 implícito), mientras que KQNodes usa R ≥ 1. Sin embargo, KGeoMIP realiza una exploración más exhaustiva del espacio de estados.

---

## 6. Resultados Experimentales

### 6.1 Configuración Experimental

**Hardware**:
- Procesador: Intel Core i7 (12ª generación)
- RAM: 32 GB DDR4
- Almacenamiento: SSD NVMe

**Software**:
- Python 3.12 (via uv)
- numpy 1.26.4, scipy 1.17.0, openpyxl 3.1.3
- pyphi 1.2.0 (framework IIT)

**Sistemas analizados**:

| Sistema | Nodos | Página | TPM | # Pruebas |
|---|---|---|---|---|
| 10A-Elementos | 10 | A | N10A.csv | 10 |
| 15B-Elementos | 15 | B | N15B.csv | 10 |
| 20A-Elementos | 20 | A | N20A.npy | 10 |

**Parámetros adaptativos**:

| Sistema | N | Restarts (QNodes) | Beam Width (Geo) |
|---|---|---|---|
| 10A | 10 | 5 | 3 |
| 15B | 15 | 3 | 2 |
| 20A | 20 | 3 | 2 |

**Post-optimización**: Aplicada solo para N ≤ 15.

### 6.2 Resultados por Sistema

#### Sistema 10A-Elementos (N = 10)

| k | Métrica | KQNodes | KGeoMIP |
|---|---------|---------|---------|
| 3 | φ promedio | 0.4861 | 0.7068 |
| 3 | φ mínimo | 0.0000 | 0.0000 |
| 3 | φ máximo | 2.0000 | 3.0000 |
| 3 | Tiempo promedio | 1.59s | 0.25s |
| 3 | Tests con φ=0 | 6/10 | 6/10 |
| 4 | φ promedio | 0.4213 | 0.6295 |
| 4 | Tiempo promedio | 2.08s | 0.38s |
| 4 | Tests con φ=0 | 7/10 | 7/10 |
| 5 | φ promedio | 0.4785 | 0.6213 |
| 5 | Tiempo promedio | 2.33s | 0.59s |
| 5 | Tests con φ=0 | 6/10 | 7/10 |

**Análisis**: En sistemas pequeños (N=10), KQNodes encuentra particiones con φ consistentemente menor o igual que KGeoMIP. Ambos métodos encuentran φ=0 en la mayoría de los tests (6-7 de 10), indicando que el sistema tiene particiones perfectas (sin pérdida de información). KQNodes es ~4-6× más lento que KGeoMIP pero los tiempos absolutos son pequeños (< 3s).

#### Sistema 15B-Elementos (N = 15)

| k | Métrica | KQNodes | KGeoMIP |
|---|---------|---------|---------|
| 3 | φ promedio | 0.00106 | 0.30139 |
| 3 | φ mínimo | 0.00000 | 0.00000 |
| 3 | φ máximo | 0.00528 | 1.00000 |
| 3 | Tiempo promedio | 1.56s | 18.36s |
| 3 | Tests con φ=0 | 8/10 | 4/10 |
| 4 | φ promedio | 0.00106 | 0.30146 |
| 4 | Tiempo promedio | 2.26s | 26.58s |
| 5 | φ promedio | 0.00106 | 0.30000 |
| 5 | Tiempo promedio | 2.63s | 119.48s |

**Análisis**: KQNodes domina claramente en N=15. Obtiene φ cercano a 0 en todos los tests (máximo 0.005), mientras KGeoMIP produce φ=1.0 en 3-4 tests debido a un bug identificado (ver Sección 6.5). Además, KQNodes es 10-45× más rápido que KGeoMIP en este sistema. La post-optimización local (N≤15) beneficia significativamente a KQNodes.

#### Sistema 20A-Elementos (N = 20)

| k | Métrica | KQNodes | KGeoMIP |
|---|---------|---------|---------|
| 3 | φ promedio | 4.1598 | 3.9598 |
| 3 | φ mínimo | 0.1419 | 0.1419 |
| 3 | φ máximo | 9.4994 | 8.4994 |
| 3 | Tiempo promedio | 288.45s | 101.79s |
| 4 | φ promedio | 4.6095 | 4.4095 |
| 4 | Tiempo promedio | 319.31s | 108.32s |
| 5 | φ promedio | 4.5093 | 4.3093 |
| 5 | Tiempo promedio | 332.70s | 208.08s |

**Análisis**: En N=20, ambos métodos producen **resultados casi idénticos** (59/90 empates exactos). Las diferencias ocurren solo en 2 de 10 tests (tests 8 y 10), donde KGeoMIP obtiene φ exactamente 1.0 menor que KQNodes. KGeoMIP es 2-3× más rápido que KQNodes. La post-optimización no está disponible para N=20.

### 6.3 Comparación KQNodes vs KGeoMIP

**Resumen general (90 comparaciones)**:

| Resultado | Cantidad | Porcentaje |
|---|---|---|
| KQNodes gana (φ menor) | 18 | 20% |
| KGeoMIP gana (φ menor) | 13 | 14% |
| Empate exacto (φ igual) | 59 | 66% |

**Por sistema**:

| Sistema | KQNodes gana | KGeoMIP gana | Empate |
|---|---|---|---|
| 10A (30 tests) | 10 | 1 | 19 |
| 15B (30 tests) | 8 | 11 | 11 |
| 20A (30 tests) | 0 | 1 | 29 |

**Interpretación**:
- **10A**: KQNodes encuentra mejores particiones (φ menor) en ~1/3 de los tests
- **15B**: KQNodes domina ampliamente (φ muy baja vs φ=1 en varios tests de KGeoMIP)
- **20A**: Ambos convergen a las mismas particiones (empate casi total), lo que sugiere que las particiones óptimas son las mismas independientemente del método

### 6.4 Análisis de Tiempos de Ejecución

**Tiempo promedio por operación**:

| Sistema | KQNodes (promedio) | KGeoMIP (promedio) | Ratio |
|---|---|---|---|
| 10A k=3 | 1.59s | 0.25s | 6.4× |
| 10A k=4 | 2.08s | 0.38s | 5.5× |
| 10A k=5 | 2.33s | 0.59s | 3.9× |
| 15B k=3 | 1.56s | 18.36s | 0.08× |
| 15B k=4 | 2.26s | 26.58s | 0.09× |
| 15B k=5 | 2.63s | 119.48s | 0.02× |
| 20A k=3 | 288.45s | 101.79s | 2.8× |
| 20A k=4 | 319.31s | 108.32s | 2.9× |
| 20A k=5 | 332.70s | 208.08s | 1.6× |

**Observaciones**:
- KQNodes es más rápido en N=15 gracias a reinicios adaptativos (R=3) y post-optimización eficiente
- KGeoMIP es más rápido en N=10 (beam_width=3 vs restarts=5) y N=20 (sin post-optimización)
- El tiempo de KGeoMIP crece más con k (especialmente k=5) porque beam search explora más combinaciones de particiones

### 6.5 Anomalías y Casos Especiales

#### Bug de φ=1.0 en KGeoMIP (15B, Tests 8-10)

**Problema**: En los tests 8, 9, 10 de 15B-Elementos, KGeoMIP producía φ=1.0 para todos los valores de k, mientras KQNodes producía φ≈0 para los mismos tests.

**Causa raíz**: La función `preparar_sistema()` en `k_partitions.py` no filtraba correctamente los nodos del alcance al crear el sistema de referencia. Cuando `alc_orig` contenía menos nodos que `mec_orig` (14 vs 15 nodos), el sistema preprocesado retenía todos los nodos del mecanismo, pero el algoritmo recursivo solo operaba sobre los nodos del alcance. El nodo "huérfano" (nodo O, índice 14) nunca se asignaba a ningún subsistema, por lo que su entrada en `k_marginal` quedaba en 0.0, mientras `original_marginal[14] = 1.0`. La EMD resultante era:

|0.0 - 1.0| = 1.0 → φ = 1.0

**Solución**: Agregar filtrado de alcance en `preparar_sistema()`:

```python
# Antes (incorrecto):
alc_remove = np.array([], dtype=np.int8)  # No filtraba alcance

# Después (corregido):
alc_remove = np.array([i for i, c in enumerate(alc_orig) if c == "0"], dtype=np.int8)
```

Con la corrección, φ baja de 1.0 a ~0.02, consistente con los resultados de KQNodes. Este fix se aplicó a ambos scripts (`k_partitions_qnodes.py` y `k_partitions.py`).

**Tests afectados** (valores originales con bug, antes de corrección):

| Test | Alcance | Mecanismo | k=3 φ | k=4 φ | k=5 φ |
|---|---|---|---|---|---|
| 8 | ABCDEFGHIJKLMN (14) | ABCDEFGHIJKLMNO (15) | 1.0 | 1.0 | 1.0 |
| 9 | ABCDEFGHIJKLMN (14) | ABCDEFGHIJKLMN (14) | 1.0 | 1.0 | 1.0 |
| 10 | ABCDEFGHIJKLMN (14) | BCDEFGHIJKLMNO (14) | 1.0 | 1.0 | 1.0 |

---

## 7. Reflexión Crítica

### 7.1 Limitaciones

**Escalabilidad**: Ambos métodos tienen complejidad exponencial O(2^N) debido a las operaciones sobre n-cubos. Para N=22, los tiempos se vuelven prohibitivos (~horas). Para N=25, son esencialmente inviables en hardware de consumo.

**Recursividad vs Optimalidad Global**: La construcción recursiva (dividir el grupo más grande) es una heurística que no garantiza optimalidad global. Una k-partición óptima podría requerir dividir simultáneamente todos los grupos, no secuencialmente.

**Post-optimización limitada**: La post-optimización local solo es viable para N≤15. Para sistemas más grandes, la calidad de la partición depende completamente de la bi-partición inicial.

**Dependencia de pyphi**: Ambas estrategias dependen del framework pyphi (IIT 3.0), que tiene su propio conjunto de limitaciones y no está siendo activamente mantenido.

### 7.2 Mejoras Potenciales

**Paralelización**: Las bi-particiones para diferentes k (3, 4, 5) son independientes y podrían ejecutarse en paralelo. También los reinicios de KQNodes son independientes.

**Poda del espacio de búsqueda**: Para KGeoMIP, el beam search podría hacerse adaptativo: empezar con beam_width grande y reducirlo cuando la varianza entre candidatos sea baja.

**Algoritmos de aproximación**: Investigar algoritmos de clustering espectral o particionamiento de grafos basados en la TPM como pre-procesamiento para reducir el espacio de búsqueda.

**Early stopping**: Si en las primeras iteraciones recursivas se encuentra φ=0, las iteraciones restantes pueden saltarse porque la partición ya es perfecta.

**Caché de evaluaciones**: La función `calcular_phi_k` se evalúa múltiples veces sobre las mismas particiones durante la post-optimización. Una caché LRU reduciría significativamente el costo.

### 7.3 Lecciones Aprendidas

**Importancia de la verificación de datos de entrada**: El bug de φ=1.0 se debió a un desajuste entre alcance y mecanismo no validado. Validar que los datos de entrada sean consistentes (número de nodos, cobertura de alcance vs mecanismo) previene resultados espurios.

**Buffer de I/O**: La escritura uno-a-uno en Excel causaba corrupción del archivo en Windows por contención de archivos. Migrar a escritura bufferizada (acumular resultados, guardar una vez por hoja) eliminó el problema.

**Parámetros adaptativos**: Ajustar restarts y beam_width según N permite balancear calidad y tiempo de ejecución. La misma configuración no funciona para todos los tamaños de sistema.

**Convergencia de estrategias**: En sistemas grandes (N=20), ambas estrategias convergen a las mismas particiones a pesar de usar enfoques algorítmicos completamente diferentes (submodular vs geométrico). Esto sugiere que las particiones óptimas están bien definidas y ambos métodos las encuentran.

**Complementariedad**: KQNodes es superior para sistemas pequeños/medianos (N≤15) donde puede explotar reinicios y post-optimización. KGeoMIP escala mejor a sistemas grandes (N≥20) por su búsqueda determinista sin reinicios. La combinación ideal sería usar KQNodes para N≤15 y KGeoMIP para N≥20.
