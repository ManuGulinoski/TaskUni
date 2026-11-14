import tkinter as tk

from utils.constantes import *
from utils.icones import obter_icone_card

ICONES_BIG_NUMBER = {
    "Total de tarefas": "clipboard-list",
    "Concluídas": "circle-check",
    "Pendentes": "hourglass-half",
    "Atrasadas": "triangle-exclamation",
}


class CardBigNumber(tk.Frame):
    """
    Card de número em destaque da Home (ex.: "Total de tarefas: 10").

    As cores de cada card vêm de CORES_BIG_NUMBER (utils/constantes.py),
    pelo título. Também dá para passar a cor direto: cor_numero="#..."
    """

    def __init__(self, master, titulo, numero, cor_numero=None, cor_destaque=None):
        super().__init__(
            master,
            bg=COR_SUPERFICIE,
            highlightthickness=1,
            highlightbackground=COR_BORDA,
            highlightcolor=COR_BORDA,
            padx=18,
            pady=14
        )

        cor_padrao = CORES_BIG_NUMBER.get(titulo, (COR_TEXTO, COR_NEUTRA))
        cor_numero = cor_numero or cor_padrao[0]
        cor_destaque = cor_destaque or cor_padrao[1]

        # Linha do título com o ícone colorido
        linha = tk.Frame(self, bg=COR_SUPERFICIE)
        linha.pack(anchor="w")

        nome_icone = ICONES_BIG_NUMBER.get(titulo, "circle")

        tk.Label(
            linha,
            image=obter_icone_card(nome_icone, cor_destaque),
            bg=COR_SUPERFICIE
        ).pack(side="left", padx=(0, 8))

        self.titulo = tk.Label(
            linha,
            text=titulo,
            bg=COR_SUPERFICIE,
            fg=COR_TEXTO_SECUNDARIO,
            font=(FONTE, 10)
        )
        self.titulo.pack(side="left")

        self.numero = tk.Label(
            self,
            text=str(numero),
            bg=COR_SUPERFICIE,
            fg=cor_numero,
            font=(FONTE, 26, "bold")
        )
        self.numero.pack(anchor="w", pady=(4, 0))