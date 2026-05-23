#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para ejecutar pruebas QNodes en TODAS las hojas del Excel
Automatiza: 15B, 20A, 22A, 25A (40 pruebas adicionales + 10 de 10A = 50 totales)
"""

import sys
import io
import os
import re
import subprocess
import shutil
import time
import openpyxl
from pathlib import Path

# UTF-8 setup
sys.stdout = io.TextIOWrapper(io.BufferedWriter(sys.stdout.buffer), encoding='utf-8', errors='replace')

# Agregar scripts/ al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from utils.converter import excel_a_bits, bits_a_excel
from utils.parser import parsear_salida_qnodes
from utils.excel_handler import leer_pruebas

print("="*70)
print(" PRUEBAS QNODES - TODAS LAS HOJAS (15B, 20A, 22A, 25A)")
print("="*70)
print()

# Configuración
EXCEL_FILE = "DatosPruebas2026_1 (1).xlsx"
QNODES_DIR = "QNodes"
QNODES_MAIN = "QNodes/src/main.py"

# Hojas a procesar (excepto 10A que ya está hecha)
SHEETS = ["15B-Elementos", "20A-Elementos", "22A-Elementos", "25A-Elementos "]

def obtener_n_nodos(sheet_name):
    """Extraer número de nodos del nombre de la hoja"""
    match = re.search(r'(\d+)', sheet_name)
    if match:
        return int(match.group(1))
    return None

def ejecutar_qnodes(alcance, mecanismo, n_nodos):
    """Ejecutar QNodes con parámetros específicos"""
    # Convertir Excel notation a binary
    alcance_bin = excel_a_bits(alcance, n_nodos)
    mecanismo_bin = excel_a_bits(mecanismo, n_nodos)
    
    # Estado inicial siempre es el mismo
    estado_inicial = "1" + "0" * (n_nodos - 1)
    condiciones = "1" * n_nodos
    
    # Leer el contenido actual de main.py
    with open(QNODES_MAIN, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Reemplazar parámetros
    content = re.sub(
        r'estado_inicial = "[^"]*"',
        f'estado_inicial = "{estado_inicial}"',
        content
    )
    content = re.sub(
        r'condiciones = "[^"]*"',
        f'condiciones = "{condiciones}"',
        content
    )
    content = re.sub(
        r'alcance = "[^"]*"',
        f'alcance = "{alcance_bin}"',
        content
    )
    content = re.sub(
        r'mecanismo = "[^"]*"',
        f'mecanismo = "{mecanismo_bin}"',
        content
    )
    
    # Escribir modificaciones
    with open(QNODES_MAIN, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Ejecutar
    try:
        result = subprocess.run(
            ['uv', 'run', 'exec.py'],
            cwd=QNODES_DIR,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=60
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        return None
    except Exception as e:
        print(f"    Error ejecutando QNodes: {e}")
        return None

def procesar_hoja(sheet_name):
    """Procesar una hoja completa"""
    print(f"\n{'='*70}")
    print(f" {sheet_name}")
    print('='*70)
    
    n_nodos = obtener_n_nodos(sheet_name)
    print(f"\n[PASO 1] Leyendo {n_nodos} nodos...")
    
    # Leer pruebas
    try:
        pruebas = leer_pruebas(EXCEL_FILE, sheet_name, n_pruebas=10)
        print(f"  ✓ {len(pruebas)} pruebas leídas")
    except Exception as e:
        print(f"  ✗ Error leyendo Excel: {e}")
        return False
    
    # Ejecutar QNodes
    print(f"\n[PASO 2] Ejecutando QNodes...")
    resultados = []
    
    for idx, prueba in enumerate(pruebas, 1):
        output = ejecutar_qnodes(prueba['alcance'], prueba['mecanismo'], n_nodos)
        if output:
            parsed = parsear_salida_qnodes(output)
            if not parsed.get('error'):
                resultados.append({
                    'fila': prueba['fila'],
                    'phi': parsed['phi'],
                    'tiempo': parsed['tiempo']
                })
                print(f"  Prueba {idx}/10: ✓")
            else:
                print(f"  Prueba {idx}/10: ✗ (parse error)")
        else:
            print(f"  Prueba {idx}/10: ✗ (execution error)")
    
    if not resultados:
        print("  ✗ No se obtuvieron resultados")
        return False
    
    # Crear Excel temporal y escribir
    print(f"\n[PASO 3] Escribiendo resultados...")
    
    temp_excel = f"DATOS_TEMP_{sheet_name.replace(' ', '_')}.xlsx"
    
    try:
        # Copiar original a temp
        shutil.copy(EXCEL_FILE, temp_excel)
        
        # Escribir resultados
        wb_temp = openpyxl.load_workbook(temp_excel)
        ws_temp = wb_temp[sheet_name]
        
        for res in resultados:
            ws_temp[f'E{res["fila"]}'] = res['phi']
            ws_temp[f'F{res["fila"]}'] = res['tiempo']
        
        wb_temp.save(temp_excel)
        print(f"  ✓ {len(resultados)} resultados escritos en temporal")
        
        # Backup y reemplazo
        print(f"\n[PASO 4] Actualizando Excel principal...")
        
        # Cerrar Excel si está abierto
        subprocess.run(['taskkill', '/IM', 'EXCEL.EXE', '/F'], 
                      capture_output=True)
        time.sleep(1)
        
        # Reemplazar
        backup_file = f"BACKUP_{sheet_name.replace(' ', '_')}.xlsx"
        if os.path.exists(EXCEL_FILE):
            shutil.copy(EXCEL_FILE, backup_file)
            os.remove(EXCEL_FILE)
        
        shutil.copy(temp_excel, EXCEL_FILE)
        os.remove(temp_excel)
        
        print(f"  ✓ Excel actualizado exitosamente")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Error escribiendo Excel: {e}")
        return False

# Ejecutar para cada hoja
completadas = 0
for sheet in SHEETS:
    try:
        if procesar_hoja(sheet):
            completadas += 1
    except Exception as e:
        print(f"  ✗ Error procesando {sheet}: {e}")

print(f"\n{'='*70}")
print(f" RESUMEN: {completadas}/{len(SHEETS)} hojas completadas")
print('='*70)
print()
print("✓ Pruebas completadas. Verificar DatosPruebas2026_1 (1).xlsx")
