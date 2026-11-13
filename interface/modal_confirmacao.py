import tkinter as tk

from interface.componentes import BotaoArredondado
from utils.constantes import *


class ModalConfirmacao:
    """
    Modal genérico de confirmação ("Tem certeza?").

    Uso:
        ModalConfirmacao(
            parent,
            titulo="Excluir tarefa",
            mensagem="Tem certeza que deseja excluir...?",
            texto_confirmar="Excluir",
            ao_confirmar=funcao_que_executa_a_acao
        )

    perigoso=True deixa o botão de confirmar vermelho (ações que apagam dados).
    """

    def __init__(self, parent, titulo, mensagem, ao_confirmar,
                 texto_confirmar="Confirmar", perigoso=True):

        self.ao_confirmar = ao_confirmar

        # Fundo que cobre a tela e bloqueia cliques atrás do modal
        self.overlay = tk.Frame(parent, bg=COR_OVERLAY)
        self.overlay.place(x=0, y=0, relwidth=1, relheight=1)

        self.janela = tk.Frame(
            self.overlay,
            bg=COR_SUPERFICIE,
            highlightthickness=1,
            highlightbackground=COR_BORDA,
            highlightcolor=COR_BORDA,
            width=470,
            height=240
        )
        self.janela.place(relx=0.5, rely=0.5, anchor="center")
        self.janela.pack_propagate(False)

        tk.Label(
            self.janela,
            text=titulo,
            font=(FONTE, 18, "bold"),
            bg=COR_SUPERFICIE,
            fg=COR_TEXTO
        ).pack(anchor="w", padx=30, pady=(26, 10))

        tk.Label(
            self.janela,
            text=mensagem,
            font=(FONTE, 11),
            bg=COR_SUPERFICIE,
            fg=COR_TEXTO_SECUNDARIO,
            wraplength=410,
            justify="left"
        ).pack(anchor="w", padx=30)

        botoes = tk.Frame(self.janela, bg=COR_SUPERFICIE)
        botoes.pack(side="bottom", anchor="e", padx=30, pady=24)

        BotaoArredondado(
            botoes,
            "Cancelar",
            self.fechar,
            tipo="secundario",
            altura=40,
            padx=24
        ).pack(side="left", padx=5)

        BotaoArredondado(
            botoes,
            texto_confirmar,
            self.confirmar,
            tipo="perigo" if perigoso else "primario",
            altura=40,
            padx=24
        ).pack(side="left", padx=5)

        # Tecla Esc cancela
        self.overlay.bind("<Escape>", lambda e: self.fechar())
        self.overlay.focus_set()

    def confirmar(self):
        # Fecha primeiro, depois executa a ação
        self.fechar()

        if self.ao_confirmar:
            self.ao_confirmar()

    def fechar(self):
        self.overlay.destroy()
