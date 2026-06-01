# Manual de Usuario — Proyecto K-QGMIP

**K-Particiones de Mínima Información con KQNodes y KGeoMIP**

Universidad de Caldas  
Facultad de Inteligencia Artificial e Ingenierías  
Análisis y Diseño de Algoritmos — 2026-1

---

## Tabla de Contenidos

1. [Introducción y Visión General](#1-introducción-y-visión-general)
2. [Requisitos del Sistema](#2-requisitos-del-sistema)
3. [Instalación Paso a Paso](#3-instalación-paso-a-paso)
4. [Video Tutorial](#4-video-tutorial)
5. [Guía de Uso Básico](#5-guía-de-uso-básico)
6. [Opciones y Parámetros Avanzados](#6-opciones-y-parámetros-avanzados)
7. [Solución de Problemas](#7-solución-de-problemas)
8. [Ejemplos y Tutoriales](#8-ejemplos-y-tutoriales)
9. [Referencia Rápida](#9-referencia-rápida)

---

## 1. Introducción y Visión General

### ¿Qué hace este software?

El software **K-QGMIP** encuentra la mejor manera de dividir un sistema de N elementos en k grupos (k-partición), de forma que la **pérdida de información** al separarlos sea lo más pequeña posible.

Imagina que tienes un sistema de 10 nodos (A, B, C, ..., J) que interactúan entre sí. Quieres dividirlos en 3 grupos. El software prueba diferentes formas de agruparlos y encuentra la partición que "rompe" lo menos posible las interacciones originales del sistema.

### ¿Para qué sirve?

- **Analizar sistemas complejos**: Identificar subsistemas que pueden tratarse como independientes con mínima pérdida de información.
- **Simplificar modelos**: Reducir la complejidad de un sistema grande dividiéndolo en partes más manejables.
- **Investigar integración de información**: Determinar qué tan integrado está un sistema (si no se puede dividir sin perder mucha información, está fuertemente integrado).

### Conceptos básicos (sin matemáticas)

- **K-partición**: Dividir N elementos en k grupos. Ejemplo: 10 estudiantes en 3 equipos.
- **Pérdida de información (φ, phi)**: Mide qué tanto cambia el comportamiento del sistema al separarlo en grupos. Si φ = 0, la partición es perfecta (los grupos se comportan igual que el sistema completo).
- **EMD** (Earth Mover's Distance): La "regla" que usamos para medir la diferencia entre el sistema original y el particionado.
- **TPM** (Matriz de Probabilidades de Transición): Describe cómo cambia el sistema de un estado a otro. Es el "ADN" del sistema.

### Capacidades y limitaciones

| Sistema | Tamaño (N) | Tiempo estimado | Calidad |
|---|---|---|---|
| Muy pequeño | 3-10 nodos | Segundos | Excelente |
| Pequeño | 10-15 nodos | Minutos | Muy buena |
| Mediano | 15-20 nodos | 1-10 minutos | Buena |
| Grande | 20-22 nodos | 1-3 horas | Aceptable |
| Muy grande | 25+ nodos | Inviable | No recomendado |

**Limitaciones importantes**:
- El software funciona con sistemas de hasta ~22 nodos en hardware convencional.
- Para más de 22 nodos, los tiempos de ejecución se vuelven prohibitivos (horas o días).
- Los resultados son aproximaciones heurísticas, no necesariamente óptimos globales.

---

## 2. Requisitos del Sistema

### Sistema operativo

- **Windows**: 10 u 11 (64 bits) — _recomendado y probado_
- **macOS**: 12+ (Monterey o superior)
- **Linux**: Distribución con Python 3.11+ (Ubuntu 22.04+, Fedora 38+, etc.)

### Hardware

| Componente | Mínimo | Recomendado |
|---|---|---|
| Procesador | Intel i5 / AMD Ryzen 5 | Intel i7 / AMD Ryzen 7 |
| Núcleos | 4 | 8+ |
| RAM | 8 GB | 32 GB |
| Disco | 500 MB libres | SSD con 2 GB libres |
| Resolución de pantalla | 1280×720 | 1920×1080 |

**Nota sobre RAM**: Para sistemas de 20+ nodos, la TPM ocupa ~180 MB en RAM (float64). Durante la ejecución, se crean múltiples copias temporales. Con 32 GB de RAM se puede trabajar cómodamente hasta N=22.

### Software

| Software | Versión requerida |
|---|---|
| Python | 3.11, 3.12 o 3.13 |
| pip / uv | Cualquiera (se recomienda uv) |
| Git | Opcional (para clonar repositorio) |

### Dependencias (se instalan automáticamente)

| Paquete | Versión |
|---|---|
| numpy | >=1.26.4 |
| scipy | >=1.17.0 |
| openpyxl | >=3.1.3 |
| pyphi | >=1.2.0 |
| matplotlib | >=3.10.9 |
| pandas | >=2.3.3 |

---

## 3. Instalación Paso a Paso

### 3.1 Descargar el proyecto

**Opción A: Clonar con Git (recomendado)**

```bash
git clone https://github.com/tu-repo/Proyecto_Analisis_2026_1.git
cd Proyecto_Analisis_2026_1
```

**Opción B: Descargar ZIP**
1. Ve al repositorio en GitHub
2. Haz clic en "Code" → "Download ZIP"
3. Extrae el ZIP en una carpeta (ej. `C:\Users\TuNombre\Documentos\`)

### 3.2 Verificar Python

Abre una terminal (Command Prompt, PowerShell o Terminal) y ejecuta:

```bash
python --version
```

Debe mostrar `Python 3.11.x` o superior. Si no tienes Python, descárgalo de:
- https://www.python.org/downloads/

**IMPORTANTE**: Durante la instalación de Python, marca la casilla **"Add Python to PATH"**.

### 3.3 Instalar uv (gestor de paquetes rápido)

**Windows (PowerShell)**:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS / Linux**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3.4 Instalar dependencias

Navega a la carpeta del proyecto y ejecuta:

```bash
cd Proyecto_Analisis_2026_1
cd QNodes
uv sync
```

Este comando instalará automáticamente todas las dependencias listadas en `pyproject.toml`. El proceso puede tomar 2-5 minutos la primera vez.

### 3.5 Verificar instalación

Ejecuta el siguiente comando para verificar que todo funciona:

```bash
cd Proyecto_Analisis_2026_1
uv run --directory QNodes python scripts/k_partitions_qnodes.py --sheet "10A-Elementos" --k 3
```

Si la instalación fue exitosa, verás mensajes de ejecución. Puedes interrumpir con `Ctrl+C` después de ver que arranca.

### 3.6 Instalación en una línea (todo junto)

Para usuarios avanzados, aquí están todos los comandos en secuencia:

```bash
# Windows (PowerShell)
git clone https://github.com/tu-repo/Proyecto_Analisis_2026_1.git
cd Proyecto_Analisis_2026_1
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
cd QNodes
uv sync

# macOS / Linux
git clone https://github.com/tu-repo/Proyecto_Analisis_2026_1.git
cd Proyecto_Analisis_2026_1
curl -LsSf https://astral.sh/uv/install.sh | sh
cd QNodes
uv sync
```

---

## 4. Video Tutorial

[Enlace al video tutorial (MP4)] — _disponible próximamente_

El video cubre:
1. Instalación desde cero (0:00 - 3:00)
2. Configuración inicial (3:00 - 4:30)
3. Ejecución de ejemplo completo con k=3,4,5 (4:30 - 10:00)
4. Interpretación de resultados (10:00 - 12:00)
5. Visualización de gráficas (12:00 - 15:00)

---

## 5. Guía de Uso Básico

### 5.1 Preparación de datos de entrada

Los datos de entrada están en el archivo **`DatosPruebas2026_1 (1).xlsx`**.

**Estructura del archivo**:
- Cada hoja representa un sistema (ej. "10A-Elementos", "15B-Elementos")
- Las filas 6 a 15 contienen 10 pruebas
- Columna **B**: **Alcance** — nodos que forman parte del análisis (notación letras)
- Columna **C**: **Mecanismo** — nodos con influencia causal

**Formato de alcance/mecanismo**:
- Usa letras mayúsculas (A, B, C, ...) para indicar qué nodos están activos
- Ejemplo: `"ABCDEFGHIJ"` significa que los 10 nodos (A-J) están activos
- Ejemplo: `"ACE"` significa que solo los nodos A, C, E están activos (los demás no)

**¿Cómo crear tus propios datos?**
1. Abre el archivo Excel
2. Agrega una nueva hoja con el nombre de tu sistema
3. En la fila 1, escribe los encabezados: `N° Prueba` (A), `Alcance` (B), `Mecanismo` (C)
4. En las filas 6-15, agrega tus pruebas con la notación de letras

**TPM (Matriz de Probabilidades de Transición)**:
- Debe existir un archivo CSV o NPY en la carpeta `QNodes/src/.samples/` o `GeoMIP/data/samples/`
- El nombre debe seguir el patrón: `N{num_nodos}{pagina}.csv` (ej. `N10A.csv`)
- El formato CSV debe tener 2^N filas y N columnas, separado por comas, sin encabezados

### 5.2 Ejecutar KQNodes (primera estrategia)

Para ejecutar KQNodes en una hoja específica con k=3, 4 y 5:

```bash
uv run --directory QNodes python scripts/k_partitions_qnodes.py --sheet "10A-Elementos"
```

Para ejecutar en todas las hojas disponibles:

```bash
uv run --directory QNodes python scripts/k_partitions_qnodes.py --all
```

Para ejecutar solo con k=3:

```bash
uv run --directory QNodes python scripts/k_partitions_qnodes.py --sheet "10A-Elementos" --k 3
```

### 5.3 Ejecutar KGeoMIP (segunda estrategia)

```bash
uv run --directory QNodes python scripts/k_partitions.py --sheet "10A-Elementos"
```

Para todas las hojas:

```bash
uv run --directory QNodes python scripts/k_partitions.py --all
```

### 5.4 Interpretación de resultados

Los resultados se guardan automáticamente en el archivo Excel `DatosPruebas2026_1 (1).xlsx`.

**Columnas de KQNodes**:

| k | Partición | φ (pérdida) | Tiempo (s) |
|---|---|---|---|
| 3 | Col P (16) | Col Q (17) | Col R (18) |
| 4 | Col V (22) | Col W (23) | Col X (24) |
| 5 | Col AB (28) | Col AC (29) | Col AD (30) |

**Columnas de KGeoMIP**:

| k | Partición | φ (pérdida) | Tiempo (s) |
|---|---|---|---|
| 3 | Col S (19) | Col T (20) | Col U (21) |
| 4 | Col Y (25) | Col Z (26) | Col AA (27) |
| 5 | Col AE (31) | Col AF (32) | Col AG (33) |

**Cómo leer una partición**:
- Ejemplo: `A,B,C | D,E,F | G,H,I,J`
- Significa: Grupo 1 = {A, B, C}, Grupo 2 = {D, E, F}, Grupo 3 = {G, H, I, J}
- El separador `|` divide los grupos

**Cómo interpretar φ**:
- **φ ≈ 0**: Partición excelente. Los grupos pueden separarse sin perder información.
- **φ < 1**: Buena partición. Pérdida de información baja.
- **φ > 1**: Pérdida de información significativa. El sistema está más integrado.

### 5.5 Generar gráficas de resultados

Para generar gráficas comparativas:

```bash
uv run --directory QNodes python scripts/analisis_resultados.py
```

Las gráficas se guardan en la carpeta `reports/`:
- `comparacion_k3.png` — Comparación por test para k=3
- `comparacion_k4.png` — Comparación por test para k=4
- `comparacion_k5.png` — Comparación por test para k=5
- `resumen_phi_por_hoja.png` — Resumen de φ promedio por sistema

---

## 6. Opciones y Parámetros Avanzados

### 6.1 Parámetros de KQNodes

| Parámetro | Descripción | Valores | Default |
|---|---|---|---|
| `--sheet` | Nombre exacto de la hoja en Excel | "10A-Elementos", etc. | — |
| `--all` | Ejecutar todas las hojas disponibles | Flag | — |
| `--k` | Valores de k a probar | Enteros (ej. 3 4 5) | 3 4 5 |
| `--restarts` | Número de reinicios aleatorios | 0=auto, 1-10 | 0 (auto) |

**Parámetros adaptativos** (restarts automático según N):

| N nodos | Restarts (QNodes) | Beam Width (GeoMIP) |
|---|---|---|
| ≤ 10 | 5 | 3 |
| 11-15 | 3 | 2 |
| 16-20 | 3 | 2 |
| 21+ | 1 | 1 |

### 6.2 Parámetros de KGeoMIP

| Parámetro | Descripción | Valores | Default |
|---|---|---|---|
| `--sheet` | Nombre exacto de la hoja en Excel | "10A-Elementos", etc. | — |
| `--all` | Ejecutar todas las hojas disponibles | Flag | — |
| `--k` | Valores de k a probar | Enteros (ej. 3 4 5) | 3 4 5 |
| `--beam-width` | Ancho de haz para beam search | 0=auto, 1-5 | 0 (auto) |

### 6.3 Post-optimización

Ambos scripts aplican automáticamente una **post-optimización local** después de construir la k-partición. Esto mueve nodos entre grupos para intentar reducir φ.

- Se activa automáticamente solo para sistemas de **15 nodos o menos**
- Para sistemas más grandes se omite porque es computacionalmente costoso
- No hay parámetro para desactivarlo/activarlo manualmente

### 6.4 Consejos de optimización

**Para sistemas pequeños (≤ 15 nodos)**:
- Usa KQNodes con restarts=5 (default automático)
- La post-optimización mejora significativamente la calidad

**Para sistemas medianos (15-20 nodos)**:
- KGeoMIP es generalmente más rápido
- Ambos métodos producen resultados similares

**Para sistemas grandes (20-22 nodos)**:
- Usa KGeoMIP con beam_width=1 (más rápido)
- Espera tiempos de 1-3 horas
- Considera ejecutar solo k=3 si el tiempo es crítico

**Para acelerar la ejecución**:
- Reduce los valores de k: `--k 3` (en lugar de 3 4 5)
- Reduce restarts: `--restarts 1` (KQNodes)
- Reduce beam_width: `--beam-width 1` (KGeoMIP)

---

## 7. Solución de Problemas

### 7.1 Errores comunes

#### "ModuleNotFoundError: No module named 'numpy'"

**Causa**: Las dependencias no se instalaron correctamente.

**Solución**:
```bash
cd QNodes
uv sync --force
```

#### "FileNotFoundError: No se encontró N10A.csv"

**Causa**: El archivo TPM no existe en la carpeta de samples.

**Solución**: Verifica que el archivo existe en `QNodes/src/.samples/` o `GeoMIP/data/samples/`. El nombre debe coincidir exactamente con el formato `N{num}{pagina}.csv`.

#### El programa se queda colgado sin mostrar nada

**Causa**: La TPM es muy grande (> 2²⁰ filas) o hay un problema con el búfer de salida.

**Solución**: Espera unos minutos. Para sistemas de 20+ nodos, la preparación inicial puede tomar 30-60 segundos. Si después de 5 minutos no hay actividad, interrumpe con `Ctrl+C` y verifica el tamaño de la TPM.

#### Error: "[WinError 32] Archivo en uso por otro proceso"

**Causa**: El archivo Excel está abierto en otro programa (Excel, LibreOffice).

**Solución**: Cierra el archivo Excel en todos los programas antes de ejecutar.

#### "RecursionError: maximum recursion depth exceeded"

**Causa**: Muy raro — ocurre si el sistema tiene más de ~1000 nodos recursivos.

**Solución**: El script ya configura `sys.setrecursionlimit(10000)`. Si persiste, aumenta el límite manualmente en el script.

### 7.2 Problemas de instalación

#### "uv no se reconoce como comando interno o externo"

**Causa**: uv no está en el PATH.

**Solución**: Cierra y vuelve a abrir la terminal. Si persiste, instala uv manualmente:
```bash
pip install uv
```

#### Error de permisos al instalar dependencias

**Causa**: No tienes permisos de escritura en la carpeta.

**Solución**:
```bash
# En Windows: abre la terminal como Administrador
# En macOS/Linux: usa sudo (no recomendado) o instala en un entorno virtual
```

#### "Python 3.11 required" pero tienes otra versión

**Causa**: El proyecto requiere Python 3.11+.

**Solución**: Instala Python 3.11 o superior desde python.org. Si tienes múltiples versiones, usa:
```bash
py -3.11 -m uv sync  # Windows
python3.11 -m uv sync  # macOS/Linux
```

### 7.3 Problemas de ejecución

#### Resultados inesperados (φ = 1.0 exacto)

**Causa**: Puede ser un bug de desajuste entre alcance y mecanismo (identificado y corregido en versiones recientes).

**Solución**: Asegúrate de tener la versión más reciente del código. Si el problema persiste, verifica que los datos de entrada sean consistentes (mismo número de nodos en alcance y mecanismo).

#### Memoria insuficiente para sistema de 22+ nodos

**Solución**:
1. Cierra otros programas para liberar RAM
2. Usa archivos `.npy` en lugar de `.csv` (ocupan la mitad de RAM)
3. Reduce a k=3 solamente
4. Considera ejecutar en una máquina con más RAM

### 7.4 Datos de entrada problemáticos

**Validación rápida**: Antes de ejecutar, verifica:
- El alcance y mecanismo usan solo letras mayúsculas A-Z
- El número de letras únicas no supera N (número de nodos del sistema)
- La TPM tiene exactamente 2^N filas y N columnas
- Los valores de la TPM están entre 0 y 1

---

## 8. Ejemplos y Tutoriales

### 8.1 Tutorial básico: Sistema de 10 nodos (10A-Elementos)

**Paso 1**: Abre una terminal y navega al proyecto:

```bash
cd C:\Users\TuNombre\Documentos\Proyecto_Analisis_2026_1
```

**Paso 2**: Ejecuta KQNodes para k=3:

```bash
uv run --directory QNodes python scripts/k_partitions_qnodes.py --sheet "10A-Elementos" --k 3
```

**Salida esperada** (abreviada):
```
========================================================
  K-PARTICIONES - QNODES
  k=3  restarts=auto
========================================================

  QNODES - 10A-Elementos (10 nodos, pagina A)
  k=[3]  restarts=5

  >>> PRUEBA 1/10 <<<
      alcance=ABCDEFGHIJ  mecanismo=ABCDEFGHIJ

      --- k=3 ---
      Split 1/2: phi=0.500000 t=0.45s
      Split 2/2: phi=0.000000 t=0.30s
      phi_3=0.0000000000  t=1.23s
      Particion: A,B,C,D | E,F,G | H,I,J

  (... más pruebas ...)
```

**Paso 3**: Ahora ejecuta KGeoMIP para el mismo sistema:

```bash
uv run --directory QNodes python scripts/k_partitions.py --sheet "10A-Elementos" --k 3
```

**Paso 4**: Genera las gráficas comparativas:

```bash
uv run --directory QNodes python scripts/analisis_resultados.py
```

**Paso 5**: Abre la carpeta `reports/` y revisa `comparacion_k3.png`.

### 8.2 Caso de estudio intermedio: 15B-Elementos con k=3,4,5

Ejecuta ambas estrategias para todos los k:

```bash
# Terminal 1: KQNodes
uv run --directory QNodes python scripts/k_partitions_qnodes.py --sheet "15B-Elementos"

# Terminal 2: KGeoMIP (puede ejecutarse en paralelo)
uv run --directory QNodes python scripts/k_partitions.py --sheet "15B-Elementos"
```

**Interpretación esperada**:
- KQNodes encuentra φ ≈ 0 en la mayoría de los tests
- KGeoMIP puede tener φ más altos en algunos tests
- Esto indica que KQNodes es mejor para este tamaño de sistema

### 8.3 Ejemplo avanzado: Parámetros personalizados

Para un sistema de 20 nodos donde el tiempo es crítico:

```bash
# Solo k=3, con mínimos parámetros
uv run --directory QNodes python scripts/k_partitions_qnodes.py --sheet "20A-Elementos" --k 3 --restarts 1

# KGeoMIP con beam_width mínimo
uv run --directory QNodes python scripts/k_partitions.py --sheet "20A-Elementos" --k 3 --beam-width 1
```

---

## 9. Referencia Rápida

### 9.1 Comandos principales

| Comando | Descripción |
|---|---|
| `uv run --directory QNodes python scripts/k_partitions_qnodes.py --sheet "X"` | Ejecutar KQNodes en hoja X |
| `uv run --directory QNodes python scripts/k_partitions_qnodes.py --all` | KQNodes en todas las hojas |
| `uv run --directory QNodes python scripts/k_partitions.py --sheet "X"` | Ejecutar KGeoMIP en hoja X |
| `uv run --directory QNodes python scripts/k_partitions.py --all` | KGeoMIP en todas las hojas |
| `uv run --directory QNodes python scripts/analisis_resultados.py` | Generar gráficas |

### 9.2 Tabla de parámetros

| Script | Parámetro | Tipo | Default | Descripción |
|---|---|---|---|---|
| k_partitions_qnodes.py | `--sheet` | str | — | Nombre de hoja Excel |
| k_partitions_qnodes.py | `--all` | flag | — | Todas las hojas |
| k_partitions_qnodes.py | `--k` | int[] | 3 4 5 | Valores de k |
| k_partitions_qnodes.py | `--restarts` | int | 0 (auto) | Reinicios algoritmo Q |
| k_partitions.py | `--sheet` | str | — | Nombre de hoja Excel |
| k_partitions.py | `--all` | flag | — | Todas las hojas |
| k_partitions.py | `--k` | int[] | 3 4 5 | Valores de k |
| k_partitions.py | `--beam-width` | int | 0 (auto) | Ancho de haz beam search |

### 9.3 Formato de archivos

**TPM (Matriz de Probabilidades de Transición)**:
- CSV: `N{num}{pagina}.csv`, sin encabezados, separado por comas
- Dimensiones: 2^N filas × N columnas
- Valores: [0, 1] — probabilidad de cada nodo de estar en estado 1

**Excel de resultados** (`DatosPruebas2026_1 (1).xlsx`):
- Filas 1-5: Encabezados
- Filas 6-15: 10 pruebas
- Col B: Alcance (notación letras)
- Col C: Mecanismo (notación letras)
- Cols P-AD: Resultados (partición, φ, tiempo)

### 9.4 Glosario

| Término | Definición |
|---|---|
| **K-partición** | División de un conjunto en k subconjuntos no vacíos y disjuntos |
| **φ (phi)** | Pérdida de información al particionar el sistema. Entre menor, mejor |
| **EMD** | Earth Mover's Distance — métrica para comparar distribuciones de probabilidad |
| **TPM** | Matriz de Probabilidades de Transición — describe la dinámica del sistema |
| **MIP** | Minimum Information Partition — la partición que minimiza φ |
| **QNodes** | Estrategia de búsqueda basada en optimización submodular |
| **GeometricSIA** | Estrategia de búsqueda basada en distancia geométrica y programación dinámica |
| **Beam Search** | Algoritmo de búsqueda que mantiene solo las B mejores soluciones parciales |
| **Post-optimización** | Refinamiento local que mueve nodos entre grupos para reducir φ |
| **Submodularidad** | Propiedad matemática de rendimientos decrecientes que permite optimización voraz eficiente |
