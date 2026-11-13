import tkinter as tk
from tkinter import ttk

from interface.componentes import BotaoArredondado
from interface.graficos import GraficoColunas, GraficoPizza
from repositorio import armazenamento
from services.grafico_service import contar_por_status, contar_por_tipo
from utils.constantes import (
    COR_FUNDO, COR_TEXTO, COR_TEXTO_SECUNDARIO, FONTE, FONTE_TITULO,
    CORES_GRAFICO_STATUS, CORES_GRAFICO_TIPO,
)


class TelaGrafico(tk.Frame):
    """
    Tela com os gráficos das tarefas, em abas (biblioteca matplotlib):
    - Por status: gráfico de colunas
    - Por tipo:   gráfico de pizza
    """

    def __init__(self, parent, app=None):
        super().__init__(parent, bg=COR_FUNDO)
        self.app = app

        topo = tk.Frame(self, bg=COR_FUNDO)
        topo.pack(fill="x", pady=(0, 16))

        BotaoArredondado(topo, "← Início", self.voltar_inicio,
                         tipo="secundario").pack(side="left", padx=(0, 16))

        tk.Label(topo, text="Gráficos das tarefas ✿", bg=COR_FUNDO, fg=COR_TEXTO,
                 font=FONTE_TITULO).pack(side="left")

        # Total de tarefas, à direita do título
        self.label_total = tk.Label(topo, bg=COR_FUNDO, fg=COR_TEXTO_SECUNDARIO,
                                    font=(FONTE, 11, "bold"))
        self.label_total.pack(side="right", padx=5)

        # Abas: uma para cada gráfico
        self.abas = ttk.Notebook(self)
        self.abas.pack(fill="both", expand=True)

        self.grafico_status = GraficoColunas(self.abas, cores=CORES_GRAFICO_STATUS)
        self.grafico_tipo = GraficoPizza(self.abas, cores=CORES_GRAFICO_TIPO)

        self.abas.add(self.grafico_status, text="  Por status  ")
        self.abas.add(self.grafico_tipo, text="  Por tipo  ")

        self.atualizar()

    def atualizar(self):
        """Lê o JSON de novo e redesenha os dois gráficos.
        Chamar sempre que as tarefas mudarem."""
        _, tarefas = armazenamento.carregar()

        self.grafico_status.atualizar(contar_por_status(tarefas))
        self.grafico_tipo.atualizar(contar_por_tipo(tarefas))

        self.label_total.configure(text=f"Total: {len(tarefas)} tarefa(s)")

    def voltar_inicio(self):
        if self.app:
            self.app.mostrar_home()