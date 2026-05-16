# Contexto del Proyecto - Análisis y Diseño 20261

## 1. Visión General

Este es un proyecto académico de **Análisis y Diseño de Software** que implementa un framework para resolver el problema de **Minimal Information Partition (MIP)** dentro del contexto de la **Integrated Information Theory (IIT)**.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         ARQUITECTURA GENERAL                             │
└─────────────────────────────────────────────────────────────────────────┘

                         ┌──────────────┐
                         │   IIT/MIP    │  Teoría de Información Integrada
                         │   Problem    │  Problema de Partición Mínima
                         └──────┬───────┘
                                │
            ┌───────────────────┼───────────────────┐
            ▼                   ▼                   ▼
     ┌────────────┐     ┌────────────┐     ┌────────────┐
     │  QNodes    │     │   GeoMIP   │     │  OpenSpec  │
     │ (Framework │     │  (Algoritmo│     │  (Sistema  │
     │   Core)    │     │  Geométrico)│     │ de Gestión │
     └────────────┘     └────────────┘     └────────────┘
```

---

## 2. Componentes del Proyecto

### 2.1 QNodes - Framework Principal

**Propósito**: Framework para resolver el problema MIP mediante múltiples estrategias.

**Estructura**:
```
QNodes/
├── src/
│   ├── main.py                 ← Punto de entrada
│   ├── exec.py                 ← Ejecutor principal
│   ├── constants/              ← Constantes y configuración
│   │   ├── base.py
│   │   ├── error.py
│   │   └── models.py
│   ├── models/                 ← Modelos de datos
│   │   ├── base/
│   │   │   ├── application.py
│   │   │   └── sia.py
│   │   ├── core/
│   │   │   ├── ncube.py
│   │   │   ├── solution.py
│   │   │   └── system.py
│   │   └── enums/
│   │       ├── distance.py
│   │       ├── notation.py
│   │       └── temporal_emd.py
│   ├── controllers/
│   │   └── manager.py          ← Gestor de redes
│   ├── funcs/                  ← Funciones utilitarias
│   │   ├── force.py
│   │   ├── format.py
│   │   └── iit.py
│   ├── middlewares/
│   │   ├── profile.py          ← Profiling de rendimiento
│   │   └── slogger.py          ← Sistema de logging
│   └── strategies/             ← Estrategias de resolución
│       ├── force.py            ← Fuerza bruta
│       ├── phi.py              ← PyPhi (referencia teórica)
│       └── q_nodes.py          ← Estrategia Q
├── tests/
│   └── PruebasIniciales.xlsx
├── .docs/
│   ├── application.md
│   └── ...
└── .samples/                   ← Redes de prueba (CSV)
    ├── N3A.csv, N3B.csv
    ├── N4A.csv, N4B.csv, N4C.csv
    └── ...
```

**Estrategias disponibles**:
| Estrategia | Descripción | Referencia |
|------------|-------------|------------|
| `BruteForce` | Fuerza bruta pura | - |
| `Phi` | Implementación con PyPhi | Teórica |
| `Q` | Estrategia Q | Secundario |

### 2.2 GeoMIP - Algoritmo Geométrico

**Propósito**: Implementación optimizada del algoritmo GeoMIP (Geometric Integrated Information) para calcular Φ (Phi) de forma eficiente.

**Estructura**:
```
GeoMIP/
├── data/
│   ├── samples/                ← Matrices de transición (TPMs)
│   │   ├── N3A.csv, N3B.csv    ← Redes de 3 nodos
│   │   ├── N4A.csv ... N8A.csv
│   │   └── N15A.csv, N15B.csv  ← Redes de 15 nodos (empíricas)
│   └── creation.py             ← Generador de redes sintéticas
├── src/
│   ├── Method1_GPU_Accelerated/    ← Método 1 (GPU)
│   │   ├── Metodo1.py
│   │   └── src/
│   │       ├── main.py
│   │       ├── controllers/
│   │       ├── models/
│   │       └── funcs/
│   └── Method2_Dynamic_Programming_Reformulation/  ← Método 2 (DP)
│       ├── exec.py
│       └── src/
│           ├── main.py
│           └── ...
├── results/
│   ├── Pruebas_Metodo1.xlsx
│   ├── Pruebas_Metodo2.xlsx
│   └── resultados_Geometric.xlsx
└── Dataset_Description.md
```

**Dos métodos de implementación**:
- **Method 1**: Acelerado por GPU
- **Method 2**: Reformulación con Programación Dinámica

**Origen de datos**:
- Redes sintéticas (<15 nodos)
- Redes empíricas (15 nodos) - derivadas de datos de Drosophila melanogaster (mosca de la fruta)

### 2.3 OpenSpec - Sistema de Gestión

**Propósito**: Sistema de gestión de cambios y artefactos para el proyecto.

```
.opencode/
├── package.json
├── package-lock.json
└── skills/
    ├── openspec-explore/
    ├── openspec-propose/
    ├── openspec-apply-change/
    └── openspec-archive-change/
```

---

## 3. Fundamentos Teóricos

### 3.1 Integrated Information Theory (IIT)

IIT es una teoría que busca caracterizar la consciencia mediante la **información integrada (Φ)** de un sistema.

### 3.2 Minimal Information Partition (MIP)

El problema MIP busca encontrar la partición de un sistema que minimice la información integrada, indicando el nivel de integración del sistema.

### 3.3 Transition Probability Matrix (TPM)

```
Ejemplo TPM para 4 nodos (ABCD):

     | 0000 | 0001 | 0010 | ... | 1111 |
-----|------|------|------|-----|------|
0000 | 0.1  | 0.2  | 0.05 | ... | 0.0  |
0001 | 0.3  | 0.1  | 0.1  | ... | 0.0  |
...
```

---

## 4. Conceptos Clave del Código

### 4.1 Representación de Estados

```python
# Estado inicial: "1000"
# ABCD#
# 1   = nodo A activo
# 0   = nodos B, C, D inactivos
```

### 4.2 Máscaras

```python
condiciones = "1110"  # nodos a mantener
alcance =     "1110"  # nodos en t+1
mecanismo =   "1110"  # nodos del mecanismo
```

### 4.3 Métricas

| Métrica | Descripción |
|---------|-------------|
| Φ (Phi) | Información integrada total |
| φ (phi) | Información integrada por bipartición |
| EMD | Earth Mover's Distance (distribución) |

---

## 5. Dependencias

```
numpy==1.26.4
scipy==1.17.0
pyphi==1.2.0          # Implementación de referencia IIT
pyinstrument==5.1.2  # Profiling
pandas==2.3.3
openpyxl==3.1.3
pyttsx3==2.98
colorama==0.4.5
```

---

## 6. Uso del Sistema

### Ejecución básica

```bash
cd QNodes
python exec.py
```

### Análisis de una red específica

```python
from src.controllers.manager import Manager
from src.strategies.force import BruteForce

gestor = Manager("1000")  # Estado inicial
mpt = gestor.cargar_red()

analizador = BruteForce(mpt)
resultado = analizador.aplicar_estrategia("1000", "1110", "1110", "1110")
```

---

## 7. Estructura de Archivos de Datos

### CSV (TPMs)

Archivos CSV con codificación UTF-8, separadores de coma y punto decimal.

```
N4A.csv → TPM para red de 4 nodos (variante A)
N15A.csv → TPM para red de 15 nodos (empírica)
```

### Excel (Resultados)

| Columna | Descripción |
|---------|-------------|
| Network | Identificador de red |
| Strategy | Algoritmo usado (PyPhi, Q, GeoMIP) |
| Phi_value | Valor Φ calculado |
| Runtime | Tiempo de ejecución (segundos) |
| Status/Notes | Notas adicionales |

---

## 8. Artifactos de Documentación

```
docs/
├── Proyecto_KGeoMIP.docx
├── ManualGeoMIP.docx
├── MANUAL DE USUARIO.docx
├── 1_Guía_Proyecto_ADAV1_2_0.pdf
└── 2_GeoMIP.pdf
```

---

## 9. Notas de Configuración

### PyPhi en Windows

PyPhi requiere Microsoft C++ Build Tools para compilar la EMD Causal.
Ver: `.docs/errors/with_pyphi.md` para troubleshooting.

---

## 10. Resumen del Flujo de Trabajo

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Datos     │────▶│  QNodes     │────▶│   GeoMIP    │
│ (TPMs CSV)  │     │ (Framework) │     │ (Optimizado)│
└─────────────┘     └─────────────┘     └─────────────┘
                           │                    │
                           ▼                    ▼
                    ┌─────────────┐     ┌─────────────┐
                    │   PyPhi     │     │   Resultados│
                    │  (Referencia)     │   (Excel)    │
                    └─────────────┘     └─────────────┘
```

---

*Documento generado automáticamente - Proyecto Análisis y Diseño 20261*