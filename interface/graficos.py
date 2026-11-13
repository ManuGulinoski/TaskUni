"""
Gráficos feitos com a biblioteca matplotlib, dentro do Tkinter.

- GraficoColunas: gráfico de colunas (usado para tarefas por status)
- GraficoPizza:   gráfico de pizza   (usado para tarefas por tipo)

Os dois têm o mesmo jeito de usar:
    grafico = GraficoColunas(parent, cores=CORES_GRAFICO_STATUS)
    grafico.pack(fill="both", expand=True)
    grafico.atualizar({"A fazer": 3, "Em andamento": 1, ...})

compacto=True deixa o gráfico menor (usado nos cards da Home).
"""
import tkinter as tk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator
from matplotlib import font_manager

from utils.constantes import (
    FONTE, COR_SUPERFICIE, COR_TEXTO, COR_TEXTO_SECUNDARIO,
    COR_GRAFICO_EIXO, COR_GRAFICO_PADRAO,
    CORES_GRAFICO_STATUS, CORES_GRAFICO_TIPO, MSG_GRAFICO_VAZIO,
)


def _fonte_disponivel():
    """Usa a fonte do tema se ela existir no computador; senão, a padrão."""
    instaladas = {f.name for f in font_manager.fontManager.ttflist}
    return FONTE if FONTE in instaladas else "DejaVu Sans"


FONTE_GRAFICO = _fonte_disponivel()


class _GraficoBase(tk.Frame):
    """Parte comum: cria a figura do matplotlib dentro de um Frame do Tkinter."""

    def __init__(self, parent, cores, compacto=False):
        super().__init__(parent, bg=COR_SUPERFICIE)

        self.cores = cores
        self.compacto = compacto
        self.contagem = {}

        self.tamanho_texto = 9 if compacto else 11

        # Figure (e não pyplot): cada gráfico tem a sua figura independente
        self.figura = Figure(
            figsize=(4, 2.6),
            dpi=100,
            facecolor=COR_SUPERFICIE,
            layout="constrained"
        )
        self.eixo = self.figura.add_subplot()

        # Liga a figura ao Tkinter
        self.canvas = FigureCanvasTkAgg(self.figura, master=self)
        widget = self.canvas.get_tk_widget()
        widget.configure(bg=COR_SUPERFICIE, highlightthickness=0)
        widget.pack(fill="both", expand=True)

    def atualizar(self, contagem):
        """Recebe o dicionário de contar_por_status / contar_por_tipo e redesenha."""
        self.contagem = dict(contagem)

        self.eixo.clear()
        self.eixo.set_facecolor(COR_SUPERFICIE)

        if sum(self.contagem.values()) == 0:
            self._mostrar_vazio()
        else:
            self._desenhar()

        self.canvas.draw_idle()

    def _mostrar_vazio(self):
        """Lista vazia: mostra uma mensagem no lugar do gráfico."""
        self.eixo.axis("off")
        self.eixo.text(
            0.5, 0.5, MSG_GRAFICO_VAZIO,
            ha="center", va="center",
            color=COR_TEXTO_SECUNDARIO,
            fontsize=self.tamanho_texto + 1,
            fontfamily=FONTE_GRAFICO,
            transform=self.eixo.transAxes
        )

    def _cor(self, categoria):
        return self.cores.get(categoria, COR_GRAFICO_PADRAO)

    def _desenhar(self):
        raise NotImplementedError


class GraficoColunas(_GraficoBase):
    """Gráfico de colunas: uma coluna por categoria, com o valor em cima."""

    def __init__(self, parent, cores=None, compacto=False):
        super().__init__(parent, cores or CORES_GRAFICO_STATUS, compacto)

    def _desenhar(self):
        ax = self.eixo

        categorias = list(self.contagem)
        valores = list(self.contagem.values())

        # Na Home o espaço é menor: "Em andamento" vira "Em\nandamento"
        nomes = [
            c.replace(" ", "\n", 1) if self.compacto and len(c) > 10 else c
            for c in categorias
        ]

        colunas = ax.bar(
            nomes,
            valores,
            color=[self._cor(c) for c in categorias],
            width=0.55,
            zorder=3
        )

        # Número em cima de cada coluna
        ax.bar_label(
            colunas,
            padding=3,
            color=COR_TEXTO,
            fontsize=self.tamanho_texto + 1,
            fontweight="bold",
            fontfamily=FONTE_GRAFICO
        )

        # Visual limpo: sem bordas, só linhas de grade bem clarinhas
        for lado in ("top", "right", "left"):
            ax.spines[lado].set_visible(False)
        ax.spines["bottom"].set_color(COR_GRAFICO_EIXO)

        ax.yaxis.set_major_locator(MaxNLocator(integer=True))  # só números inteiros
        ax.grid(axis="y", color=COR_GRAFICO_EIXO, linewidth=0.8, zorder=0)
        ax.set_ylim(0, max(valores) * 1.2)                      # espaço p/ o número

        ax.tick_params(axis="both", length=0, colors=COR_TEXTO_SECUNDARIO,
                       labelsize=self.tamanho_texto)
        for rotulo in ax.get_xticklabels() + ax.get_yticklabels():
            rotulo.set_fontfamily(FONTE_GRAFICO)
        for rotulo in ax.get_xticklabels():
            rotulo.set_color(COR_TEXTO)


class GraficoPizza(_GraficoBase):
    """Gráfico de pizza: percentual dentro das fatias e legenda com as quantidades."""

    def __init__(self, parent, cores=None, compacto=False):
        super().__init__(parent, cores or CORES_GRAFICO_TIPO, compacto)

    def _desenhar(self):
        ax = self.eixo

        # Fatias só para quem tem tarefas (fatia de 0% não aparece na pizza)
        com_tarefas = {c: v for c, v in self.contagem.items() if v > 0}

        fatias, _textos, percentuais = ax.pie(
            list(com_tarefas.values()),
            colors=[self._cor(c) for c in com_tarefas],
            startangle=90,
            counterclock=False,
            autopct=lambda p: f"{p:.0f}%" if p >= 5 else "",
            pctdistance=0.68,
            wedgeprops={"edgecolor": COR_SUPERFICIE, "linewidth": 2},
            textprops={"color": COR_TEXTO, "fontsize": self.tamanho_texto,
                       "fontweight": "bold", "fontfamily": FONTE_GRAFICO}
        )
        ax.set_aspect("equal")

        # Legenda com TODOS os tipos, inclusive os que têm 0 tarefas
        marcadores = []
        for categoria in self.contagem:
            marcador = ax.scatter([], [], color=self._cor(categoria), s=90, marker="o")
            marcadores.append(marcador)

        ax.legend(
            marcadores,
            [f"{c}: {v}" for c, v in self.contagem.items()],
            loc="center left",
            bbox_to_anchor=(1.0, 0.5),
            frameon=False,
            labelcolor=COR_TEXTO,
            prop={"family": FONTE_GRAFICO, "size": self.tamanho_texto + 1},
            handletextpad=0.3,
            labelspacing=0.9
        )
