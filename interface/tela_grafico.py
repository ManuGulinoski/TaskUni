import tkinter as tk
from tkinter import ttk

from interface.grafico_status import GraficoStatus
from repositorio import armazenamento
from services.grafico_service import contar_por_status
from utils.constantes import COR_FUNDO

FONTE = "Segoe UI"


class TelaGrafico(tk.Frame):
    """Tela com o gráfico de tarefas por status."""

    def __init__(self, parent, app=None):
        super().__init__(parent, bg=COR_FUNDO)
        self.app = app

        topo = tk.Frame(self, bg=COR_FUNDO)
        topo.pack(fill="x", pady=(0, 10))

        ttk.Button(topo, text="← Início",
                   command=self.voltar_inicio).pack(side="left", padx=(0, 15))

        tk.Label(topo, text="Tarefas por status", bg=COR_FUNDO,
                 font=(FONTE, 18, "bold")).pack(side="left")

        self.grafico = GraficoStatus(self)
        self.grafico.pack(fill="both", expand=True)

        self.atualizar()

    def atualizar(self):
        """Lê o JSON de novo e redesenha. Chamar sempre que as tarefas mudarem."""
        _, tarefas = armazenamento.carregar()
        self.grafico.atualizar(contar_por_status(tarefas))

    def voltar_inicio(self):
        if self.app:
            self.app.mostrar_home()
