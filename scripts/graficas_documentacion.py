#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera gráficas profesionales para el Manual Técnico.
"""

import sys, os, json
from pathlib import Path
sys.setrecursionlimit(10000)
os.environ["FORCE_COLOR"] = "0"

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

PROYECTO = Path(__file__).resolve().parent.parent
DATA_FILE = PROYECTO / "reports" / "datos_extraidos.json"
DOCS_DIR = PROYECTO / "docs" / "figures"
DOCS_DIR.mkdir(exist_ok=True, parents=True)

# Cargar datos
with open(DATA_FILE) as f:
    datos = json.load(f)

COLORS = {"QNodes": "#1f77b4", "KGeoMIP": "#ff7f0e"}

def phi_promedio_por_hoja():
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    for idx, sheet in enumerate(["10A-Elementos", "15B-Elementos", "20A-Elementos"]):
        tests = datos[sheet]
        ks = [3, 4, 5]
        x = np.arange(len(ks))
        w = 0.3
        ax = axes[idx]

        q_means = []
        g_means = []
        for k in ks:
            qv = [t[f"Q{k}_phi"] for t in tests if t.get(f"Q{k}_phi") is not None]
            gv = [t[f"G{k}_phi"] for t in tests if t.get(f"G{k}_phi") is not None]
            q_means.append(np.mean(qv) if qv else 0)
            g_means.append(np.mean(gv) if gv else 0)

        bars1 = ax.bar(x - w/2, q_means, w, label="KQNodes", color=COLORS["QNodes"], edgecolor="white", linewidth=0.5)
        bars2 = ax.bar(x + w/2, g_means, w, label="KGeoMIP", color=COLORS["KGeoMIP"], edgecolor="white", linewidth=0.5)

        for bars in [bars1, bars2]:
            for bar in bars:
                h = bar.get_height()
                if h > 0.01:
                    ax.text(bar.get_x() + bar.get_width()/2, h + 0.02, f"{h:.2f}",
                            ha="center", va="bottom", fontsize=8)

        ax.set_title(sheet, fontsize=12, fontweight="bold")
        ax.set_xticks(x)
        ax.set_xticklabels([f"k = {k}" for k in ks], fontsize=10)
        ax.set_ylabel("φ promedio", fontsize=10)
        if idx == 2:
            ax.legend(fontsize=9, loc="upper left")
        ax.grid(axis="y", alpha=0.3)

    fig.suptitle("φ promedio por sistema y estrategia", fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    path = DOCS_DIR / "phi_promedio_por_sistema.png"
    plt.savefig(str(path), dpi=200, bbox_inches="tight")
    plt.close()
    print(f"  {path.name}")

def tiempo_promedio_por_hoja():
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    for idx, sheet in enumerate(["10A-Elementos", "15B-Elementos", "20A-Elementos"]):
        tests = datos[sheet]
        ks = [3, 4, 5]
        x = np.arange(len(ks))
        w = 0.3
        ax = axes[idx]

        q_means = []
        g_means = []
        for k in ks:
            qv = [t[f"Q{k}_time"] for t in tests if t.get(f"Q{k}_time") is not None]
            gv = [t[f"G{k}_time"] for t in tests if t.get(f"G{k}_time") is not None]
            q_means.append(np.mean(qv) if qv else 0)
            g_means.append(np.mean(gv) if gv else 0)

        bars1 = ax.bar(x - w/2, q_means, w, label="KQNodes", color=COLORS["QNodes"], edgecolor="white", linewidth=0.5)
        bars2 = ax.bar(x + w/2, g_means, w, label="KGeoMIP", color=COLORS["KGeoMIP"], edgecolor="white", linewidth=0.5)

        for bars in [bars1, bars2]:
            for bar in bars:
                h = bar.get_height()
                if h > 1:
                    label = f"{h:.0f}s" if h < 1000 else f"{h/60:.1f}m"
                    ax.text(bar.get_x() + bar.get_width()/2, h + max(h*0.02, 1), label,
                            ha="center", va="bottom", fontsize=7, rotation=45)

        ax.set_title(sheet, fontsize=12, fontweight="bold")
        ax.set_xticks(x)
        ax.set_xticklabels([f"k = {k}" for k in ks], fontsize=10)
        ax.set_ylabel("Tiempo promedio (s)", fontsize=10)
        if idx == 0:
            ax.legend(fontsize=9)
        ax.grid(axis="y", alpha=0.3)

    fig.suptitle("Tiempo de ejecución promedio por sistema y estrategia", fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    path = DOCS_DIR / "tiempo_promedio_por_sistema.png"
    plt.savefig(str(path), dpi=200, bbox_inches="tight")
    plt.close()
    print(f"  {path.name}")

def phi_vs_tiempo():
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    markers = {"KQNodes": "o", "KGeoMIP": "s"}
    for idx, sheet in enumerate(["10A-Elementos", "15B-Elementos", "20A-Elementos"]):
        tests = datos[sheet]
        ax = axes[idx]

        for metodo, pref, color in [("KQNodes", "Q", COLORS["QNodes"]), ("KGeoMIP", "G", COLORS["KGeoMIP"])]:
            for k in [3, 4, 5]:
                phis = []
                times = []
                for t in tests:
                    p = t.get(f"{pref}{k}_phi")
                    tm = t.get(f"{pref}{k}_time")
                    if p is not None and tm is not None:
                        phis.append(p)
                        times.append(tm)
                if phis:
                    ax.scatter(times, phis, label=f"{metodo} k={k}", 
                              color=color, marker=markers[metodo],
                              alpha=0.6, s=30, edgecolors="white", linewidth=0.3)

        ax.set_title(sheet, fontsize=12, fontweight="bold")
        ax.set_xlabel("Tiempo (s)", fontsize=10)
        ax.set_ylabel("φ", fontsize=10)
        ax.set_xscale("symlog" if sheet == "20A-Elementos" else "linear")
        ax.legend(fontsize=7, loc="upper left", ncol=2)
        ax.grid(alpha=0.3)

    fig.suptitle("Relación φ vs Tiempo de ejecución", fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    path = DOCS_DIR / "phi_vs_tiempo.png"
    plt.savefig(str(path), dpi=200, bbox_inches="tight")
    plt.close()
    print(f"  {path.name}")

def distribucion_phi():
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    for row, metodo, pref, color in [(0, "KQNodes", "Q", COLORS["QNodes"]), (1, "KGeoMIP", "G", COLORS["KGeoMIP"])]:
        for col, sheet in enumerate(["10A-Elementos", "15B-Elementos", "20A-Elementos"]):
            tests = datos[sheet]
            ax = axes[row, col]
            
            for k in [3, 4, 5]:
                phis = [t[f"{pref}{k}_phi"] for t in tests if t.get(f"{pref}{k}_phi") is not None]
                if phis:
                    ax.hist(phis, bins=8, alpha=0.5, label=f"k={k}", edgecolor="white", linewidth=0.5)

            ax.set_title(f"{metodo} - {sheet}", fontsize=11, fontweight="bold")
            ax.set_xlabel("φ", fontsize=9)
            ax.set_ylabel("Frecuencia", fontsize=9)
            ax.legend(fontsize=8)
            ax.grid(alpha=0.3)

    plt.tight_layout()
    path = DOCS_DIR / "distribucion_phi.png"
    plt.savefig(str(path), dpi=200, bbox_inches="tight")
    plt.close()
    print(f"  {path.name}")

def resumen_ganador():
    # Gráfico de torta: quién gana
    fig, axes = plt.subplots(1, 4, figsize=(16, 4))
    
    categorias = ["10A", "15B", "20A", "Total"]
    datos_ganador = {
        "10A": {"QNodes": 10, "KGeoMIP": 1, "Empate": 19},
        "15B": {"QNodes": 8, "KGeoMIP": 11, "Empate": 11},
        "20A": {"QNodes": 0, "KGeoMIP": 1, "Empate": 29},
        "Total": {"QNodes": 18, "KGeoMIP": 13, "Empate": 59},
    }

    colors = [COLORS["QNodes"], COLORS["KGeoMIP"], "#7f7f7f"]

    for idx, cat in enumerate(categorias):
        ax = axes[idx]
        d = datos_ganador[cat]
        values = [d["QNodes"], d["KGeoMIP"], d["Empate"]]
        wedges, texts, autotexts = ax.pie(values, labels=None, colors=colors,
                                          autopct="%1.0f%%", startangle=90,
                                          textprops={"fontsize": 8})
        for t in autotexts:
            t.set_fontsize(7)
            t.set_fontweight("bold")
        ax.set_title(cat, fontsize=12, fontweight="bold")

    fig.legend(["KQNodes mejor", "KGeoMIP mejor", "Empate"],
               loc="lower center", ncol=3, fontsize=10)
    plt.tight_layout()
    path = DOCS_DIR / "resumen_ganador.png"
    plt.savefig(str(path), dpi=200, bbox_inches="tight")
    plt.close()
    print(f"  {path.name}")

def main():
    print("Generando gráficas profesionales...")
    phi_promedio_por_hoja()
    tiempo_promedio_por_hoja()
    phi_vs_tiempo()
    distribucion_phi()
    resumen_ganador()
    print(f"\nGráficas guardadas en: {DOCS_DIR}/")

if __name__ == "__main__":
    main()
