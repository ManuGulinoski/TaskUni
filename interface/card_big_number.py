import tkinter as tk

from utils.constantes import *


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

        # Linha do título com uma bolinha colorida
        linha = tk.Frame(self, bg=COR_SUPERFICIE)
        linha.pack(anchor="w")

        bolinha = tk.Canvas(linha, width=10, height=10, bg=COR_SUPERFICIE,
                            highlightthickness=0)
        bolinha.create_oval(1, 1, 9, 9, fill=cor_destaque, outline=cor_destaque)
        bolinha.pack(side="left", padx=(0, 8))

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