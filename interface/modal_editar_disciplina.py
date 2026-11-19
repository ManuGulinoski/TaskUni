import tkinter as tk
from tkinter import ttk

from services.disciplina_service import listar_disciplinas, editar_disciplina
from interface.componentes import BotaoArredondado, exibir_toast
from utils.constantes import *


class ModalEditarDisciplina:
    """
    US05 - Editar disciplina.

    O usuário escolhe a disciplina, digita o novo nome e salva.
    As tarefas continuam ligadas a ela, porque guardam o ID e não o nome.
    """

    def __init__(self, parent, ao_salvar=None):

        self.parent = parent
        self.ao_salvar = ao_salvar

        # Nome -> ID, para achar a disciplina escolhida no combo
        self.mapa_disciplinas = {
            disciplina.nome: disciplina.id
            for disciplina in listar_disciplinas()
        }

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
            height=470
        )

        self.janela.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        self.janela.pack_propagate(False)

        tk.Label(
            self.janela,
            text="Editar disciplina ✿",
            font=FONTE_TITULO,
            fg=COR_TEXTO,
            bg=COR_SUPERFICIE
        ).pack(
            anchor="w",
            padx=35,
            pady=(35, 5)
        )

        tk.Label(
            self.janela,
            text="Escolha a disciplina e digite o novo nome",
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
            pady=(25, 0)
        )

        self._criar_label(formulario, "Disciplina:")

        self.combo_disciplina = ttk.Combobox(
            formulario,
            values=list(self.mapa_disciplinas.keys()),
            state="readonly",
            font=(FONTE, 11)
        )

        self.combo_disciplina.pack(
            fill="x",
            ipady=5,
            pady=(0, 16)
        )

        # Ao escolher, o nome atual já aparece no campo para ser corrigido
        self.combo_disciplina.bind(
            "<<ComboboxSelected>>",
            self._preencher_nome
        )

        self._criar_label(formulario, "Novo nome:")

        self.entrada_nome = tk.Entry(
            formulario,
            font=(FONTE, 12),
            fg=COR_TEXTO,
            bg=COR_CAMPO,
            relief="flat",
            bd=0,
            insertbackground=COR_TEXTO,
            highlightthickness=1,
            highlightbackground=COR_CAMPO_BORDA,
            highlightcolor=COR_CAMPO_FOCO
        )

        self.entrada_nome.pack(
            fill="x",
            ipady=10
        )

        # Lista vazia: avisa no próprio campo
        if not self.mapa_disciplinas:
            self.combo_disciplina.set(MSG_SEM_DISCIPLINAS)

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

        BotaoArredondado(
            frame_botoes,
            "Cancelar",
            self.fechar,
            tipo="secundario",
            altura=46
        ).grid(row=0, column=0, padx=8, sticky="ew")

        BotaoArredondado(
            frame_botoes,
            "Salvar",
            self.salvar,
            tipo="primario",
            altura=46
        ).grid(row=0, column=1, padx=8, sticky="ew")

    def _criar_label(self, parent, texto):

        tk.Label(
            parent,
            text=texto,
            font=FONTE_LABEL,
            fg=COR_TEXTO,
            bg=COR_SUPERFICIE
        ).pack(
            anchor="w",
            pady=(0, 8)
        )

    def _preencher_nome(self, evento=None):

        self.entrada_nome.delete(0, tk.END)
        self.entrada_nome.insert(0, self.combo_disciplina.get())
        self.entrada_nome.focus_set()

    def fechar(self):

        self.overlay.destroy()

    def salvar(self):

        disciplina_id = self.mapa_disciplinas.get(self.combo_disciplina.get())

        try:
            if disciplina_id is None:
                raise ValueError("Escolha a disciplina que deseja editar.")

            disciplina = editar_disciplina(
                disciplina_id,
                self.entrada_nome.get()
            )

        except ValueError as erro:
            exibir_toast(self.parent, str(erro), "erro")
            return

        if self.ao_salvar:
            self.ao_salvar(disciplina)

        self.fechar()

        exibir_toast(
            self.parent,
            "Disciplina atualizada com sucesso!",
            "sucesso"
        )
