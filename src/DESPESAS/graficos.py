"""
Módulo de gráficos para o Gerenciador de Despesas.
Usa matplotlib integrado ao CustomTkinter.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.text import Text
import customtkinter as ctk


# Paleta suave para os gráficos
PALETA = [
    "#5d7bae",
    "#b0626e",
    "#7a9e5a",
    "#b8975a",
    "#9e7a55",
    "#7a6a9e",
    "#4a8a8f",
    "#6b8fb0",
    "#5a8f7a",
    "#8fa0b0",
    "#8a8a9e",
    "#7a8090",
    "#6e7585",
    "#505868",
    "#6b7394",
]

FUNDO = "#2b2b2b"  # Grafite escuro - background
COR_TEXTO = "#a9b1c6"  # Cinza azulado suave


def criar_grafico_pizza(parent, categorias, valores, coluna, linha=0):
    """Cria um gráfico de pizza dentro do frame pai."""
    fig = Figure(figsize=(4.2, 4.2), dpi=100, facecolor=FUNDO)
    ax = fig.add_subplot(111)

    cores = PALETA[: len(categorias)]

    # Limpar emojis para labels mais limpas no gráfico
    labels_curtas = [c.split(" ", 1)[-1] if " " in c else c for c in categorias]

    result = ax.pie(
        valores,
        labels=None,
        autopct="%1.1f%%",
        colors=cores,
        startangle=140,
        pctdistance=0.78,
        wedgeprops={"linewidth": 2, "edgecolor": FUNDO},
    )
    # autopct faz retornar (wedges, texts, autotexts)
    autotexts: list[Text] = list(result[2]) if len(result) > 2 else []

    for t in autotexts:
        t.set_color(COR_TEXTO)
        t.set_fontsize(9)
        t.set_fontweight("bold")

    ax.legend(
        labels_curtas,
        loc="lower center",
        ncol=2,
        fontsize=7,
        facecolor=FUNDO,
        edgecolor="#444444",
        labelcolor=COR_TEXTO,
        bbox_to_anchor=(0.5, -0.12),
    )

    ax.set_title(
        "Distribuição por Categoria",
        color=COR_TEXTO,
        fontsize=12,
        fontweight="bold",
        pad=10,
    )
    fig.set_facecolor(FUNDO)
    fig.subplots_adjust(bottom=0.2)

    frame = ctk.CTkFrame(parent, fg_color=FUNDO, corner_radius=12)
    frame.grid(row=linha, column=coluna, sticky="nsew", padx=5, pady=5)

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)


def criar_grafico_barras(parent, categorias, valores, coluna, linha=0):
    """Cria um gráfico de barras horizontais dentro do frame pai."""
    fig = Figure(figsize=(4.2, 4.2), dpi=100, facecolor=FUNDO)
    ax = fig.add_subplot(111)

    cores = PALETA[: len(categorias)]
    labels_curtas = [
        c.split(" ", 1)[-1][:15] if " " in c else c[:15] for c in categorias
    ]

    # Inverter para que o maior fique em cima
    y_pos = range(len(categorias))
    bars = ax.barh(
        list(y_pos), valores, color=cores, height=0.6, edgecolor=FUNDO, linewidth=1
    )

    ax.set_yticks(list(y_pos))
    ax.set_yticklabels(labels_curtas, fontsize=8, color=COR_TEXTO)
    ax.set_xlabel("Valor (R$)", color=COR_TEXTO, fontsize=10)
    ax.set_title(
        "Gastos por Categoria", color=COR_TEXTO, fontsize=12, fontweight="bold", pad=10
    )

    ax.set_facecolor(FUNDO)
    ax.tick_params(axis="x", colors=COR_TEXTO, labelsize=8)
    ax.tick_params(axis="y", colors=COR_TEXTO)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_color("#444444")
    ax.spines["left"].set_color("#444444")

    # Valores nas barras
    for bar, val in zip(bars, valores):
        txt = f"R${val:,.0f}".replace(",", ".")
        ax.text(
            bar.get_width() + max(valores) * 0.02,
            bar.get_y() + bar.get_height() / 2,
            txt,
            va="center",
            ha="left",
            color=COR_TEXTO,
            fontsize=8,
            fontweight="bold",
        )

    fig.tight_layout()

    frame = ctk.CTkFrame(parent, fg_color=FUNDO, corner_radius=12)
    frame.grid(row=linha, column=coluna, sticky="nsew", padx=5, pady=5)

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
