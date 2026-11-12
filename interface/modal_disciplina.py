import tkinter as tk
from services.disciplina_service import cadastrar_disciplina
from interface.componentes import BotaoArredondado, exibir_toast
from utils.constantes import *


class ModalDisciplina:

    def __init__(self, parent, ao_cadastrar=None):

        self.parent = parent
        self.ao_cadastrar = ao_cadastrar

        # Cores do tema (utils/constantes.py)
        self.cor_fonte = COR_TEXTO
        self.cor_roxa = COR_PRIMARIA
        self.cor_campo = COR_CAMPO
        self.cor_cancelar = COR_SECUNDARIA

        self.overlay = tk.Frame(parent, bg=COR_OVERLAY)
        self.overlay.place(
            relx=0,
            rely=0,
            relwidth=1,
            relheight=1
        )

        self.janela = tk.Frame(
            self.overlay,
            bg=COR_SUPERFICIE,
            highlightthickness=1,
            highlightbackground=COR_BORDA,
            highlightcolor=COR_BORDA,
            width=560,
            height=400
        )

        self.janela.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        self.janela.pack_propagate(False)

        tk.Label(
            self.janela,
            text="Nova disciplina ✿",
            font=FONTE_TITULO,
            fg=self.cor_fonte,
            bg=COR_SUPERFICIE
        ).pack(
            anchor="w",
            padx=35,
            pady=(35, 5)
        )

        tk.Label(
            self.janela,
            text="Adicione uma disciplina para organizar suas tarefas",
            font=FONTE_SUBTITULO,
            fg=COR_TEXTO_SECUNDARIO,
            bg=COR_SUPERFICIE
        ).pack(
            anchor="w",
            padx=35
        )

        tk.Frame(
            self.janela,
            bg=COR_BORDA,
            height=1
        ).pack(
            fill="x",
            padx=35,
            pady=(25, 0)
        )

        formulario = tk.Frame(
            self.janela,
            bg=COR_SUPERFICIE
        )

        formulario.pack(
            fill="x",
            padx=35,
            pady=(30, 0)
        )

        tk.Label(
            formulario,
            text="Nome da disciplina:",
            font=FONTE_LABEL,
            fg=self.cor_fonte,
            bg=COR_SUPERFICIE
        ).pack(
            anchor="w",
            pady=(0, 10)
        )

        self.entrada_nome = tk.Entry(
            formulario,
            font=(FONTE, 12),
            fg=self.cor_fonte,
            bg=self.cor_campo,
            relief="flat",
            bd=0,
            insertbackground=self.cor_fonte,
            highlightthickness=1,
            highlightbackground=COR_CAMPO_BORDA,
            highlightcolor=COR_CAMPO_FOCO
        )

        self.entrada_nome.pack(
            fill="x",
            ipady=10
        )

        self.entrada_nome.focus_set()


        frame_botoes = tk.Frame(
            self.janela,
            bg=COR_SUPERFICIE
        )

        frame_botoes.pack(
            side="bottom",
            fill="x",
            padx=27,
            pady=30
        )

        frame_botoes.columnconfigure(0, weight=1)
        frame_botoes.columnconfigure(1, weight=1)

        self.criar_botao(
            frame_botoes,
            "Cancelar",
            "secundario",
            self.fechar,
            coluna=0
        )

        self.criar_botao(
            frame_botoes,
            "Adicionar",
            "primario",
            self.salvar,
            coluna=1
        )

    def criar_botao(self, parent, texto, tipo, comando, coluna):

        botao = BotaoArredondado(
            parent,
            texto,
            comando,
            tipo=tipo,
            altura=46
        )

        botao.grid(
            row=0,
            column=coluna,
            padx=8,
            sticky="ew"
        )

    def fechar(self):

        self.overlay.destroy()

    def exibir_toast(self, mensagem, tipo="sucesso"):

        exibir_toast(self.parent, mensagem, tipo)

    def salvar(self):

        nome = self.entrada_nome.get()

        try:
            disciplina = cadastrar_disciplina(nome)

            if self.ao_cadastrar:
                self.ao_cadastrar(disciplina)

            self.fechar()

            self.exibir_toast(
                "Disciplina cadastrada com sucesso!",
                "sucesso"
            )

        except ValueError as erro:
            self.exibir_toast(
                str(erro),
                "erro"
            )