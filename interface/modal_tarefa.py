
import tkinter as tk
from tkinter import ttk

from repositorio import armazenamento
from services.tarefa_service import cadastrar_tarefa

from utils.constantes import (
    TIPOS,
    STATUS_SELECIONAVEIS,
    CORES_TAREFA
)


class ModalTarefa:

    def __init__(self, parent, ao_cadastrar=None):
        self.parent = parent
        self.ao_cadastrar = ao_cadastrar

        self.cor_fundo = "#808080"
        self.cor_fonte = "#333333"
        self.cor_campo = "#CCCCCC"
        self.cor_roxo = "#5b21b6"
        self.cor_cinza = "#F1F1F3"
        self.cor_placeholder = "#888888"
        self.placeholder_nome = "Ex.: Prova de Algoritmos"
        self.placeholder_prazo = "DD/MM/AAAA"
        self.placeholder_descricao = "Adicione uma descrição (opcional)"

        self.overlay = tk.Frame(
            parent,
            bg=self.cor_fundo
        )

        self.overlay.place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1
        )

        self.janela = tk.Frame(
            self.overlay,
            bg="white",
            width=650,
            height=680
        )

        self.janela.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        self.janela.pack_propagate(False)

        disciplinas, tarefas = armazenamento.carregar()

        self.disciplinas = disciplinas

        self.mapa_disciplinas = {
            disciplina.nome: disciplina.id
            for disciplina in disciplinas
        }

        self.criar_interface()

    def criar_interface(self):

        tk.Label(
            self.janela,
            text="Nova tarefa",
            font=("Arial", 20, "bold"),
            bg="white",
            fg=self.cor_fonte
        ).pack(
            anchor="w",
            padx=35,
            pady=(25, 5)
        )

        tk.Label(
            self.janela,
            text="Adicione uma tarefa para organizar suas atividades",
            font=("Arial", 10),
            bg="white",
            fg="#888888"
        ).pack(
            anchor="w",
            padx=35
        )

        tk.Frame(
            self.janela,
            bg="#CCCCCC",
            height=1
        ).pack(
            fill="x",
            padx=35,
            pady=(20, 15)
        )

        formulario = tk.Frame(
            self.janela,
            bg="white"
        )

        formulario.pack(
            fill="x",
            padx=35
        )

        formulario.columnconfigure(0, weight=1)
        formulario.columnconfigure(1, weight=1)

        self.criar_label(formulario, "Nome da tarefa *", 0, 0)
        self.entrada_nome = tk.Entry(
            formulario,
            font=("Arial", 12),
            fg=self.cor_fonte,
            bg=self.cor_campo,
            relief="flat",
            bd=0,
            insertbackground=self.cor_fonte
        )

        self.entrada_nome.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            ipady=8,
            pady=(5, 12)
        )

        self.adicionar_placeholder(
            self.entrada_nome,
            self.placeholder_nome
        )

        self.criar_label(formulario, "Tipo *", 2, 0)
        self.combo_tipo = ttk.Combobox(
            formulario,
            values=TIPOS,
            state="readonly",
            font=("Arial", 11)
        )

        self.combo_tipo.grid(
            row=3,
            column=0,
            sticky="ew",
            ipady=5,
            padx=(0, 10),
            pady=(5, 12)
        )

        self.criar_label(formulario, "Disciplina *", 2, 1)
        self.combo_disciplina = ttk.Combobox(
            formulario,
            values=list(self.mapa_disciplinas.keys()),
            state="readonly",
            font=("Arial", 11)
        )

        self.combo_disciplina.grid(
            row=3,
            column=1,
            sticky="ew",
            ipady=5,
            padx=(10, 0),
            pady=(5, 12)
        )

        self.criar_label(formulario, "Prazo (DD/MM/AAAA) *", 4, 0)
        self.entrada_prazo = tk.Entry(
            formulario,
            font=("Arial", 12),
            fg=self.cor_fonte,
            bg=self.cor_campo,
            relief="flat",
            bd=0,
            insertbackground=self.cor_fonte
        )

        self.entrada_prazo.grid(
            row=5,
            column=0,
            sticky="ew",
            ipady=8,
            padx=(0, 10),
            pady=(5, 12)
        )

        self.adicionar_placeholder(
            self.entrada_prazo,
            self.placeholder_prazo
        )

        self.criar_label(formulario, "Descrição", 6, 0)
        self.entrada_descricao = tk.Entry(
            formulario,
            font=("Arial", 12),
            fg=self.cor_fonte,
            bg=self.cor_campo,
            relief="flat",
            bd=0,
            insertbackground=self.cor_fonte
        )

        self.entrada_descricao.grid(
            row=7,
            column=0,
            columnspan=2,
            sticky="ew",
            ipady=8,
            pady=(5, 12)
        )

        self.adicionar_placeholder(
            self.entrada_descricao,
            self.placeholder_descricao
        )

        self.criar_label(formulario, "Status *", 8, 0)
        self.combo_status = ttk.Combobox(
            formulario,
            values=STATUS_SELECIONAVEIS,
            state="readonly",
            font=("Arial", 11)
        )

        self.combo_status.grid(
            row=9,
            column=0,
            sticky="ew",
            ipady=5,
            padx=(0, 10),
            pady=(5, 12)
        )

        self.criar_label(formulario, "Cor", 8, 1)
        self.combo_cor = ttk.Combobox(
            formulario,
            values=list(CORES_TAREFA.keys()),
            state="readonly",
            font=("Arial", 11)
        )

        self.combo_cor.grid(
            row=9,
            column=1,
            sticky="ew",
            ipady=5,
            padx=(10, 0),
            pady=(5, 12)
        )

        self.combo_cor.set("Branco")
        self.combo_status.set("A fazer")

        botoes = tk.Frame(
            self.janela,
            bg="white"
        )

        botoes.pack(
            pady=(35, 20)
        )

        tk.Button(
            botoes,
            text="Cancelar",
            font=("Arial", 11, "bold"),
            bg=self.cor_cinza,
            fg="#777777",
            activebackground="#E5E5E5",
            activeforeground="#777777",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.fechar
        ).pack(
            side="left",
            ipadx=20,
            ipady=10,
            padx=5
        )

        tk.Button(
            botoes,
            text="Adicionar",
            font=("Arial", 11, "bold"),
            bg=self.cor_roxo,
            fg="white",
            activebackground="#4c1d95",
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.salvar
        ).pack(
            side="left",
            ipadx=20,
            ipady=10,
            padx=5
        )

        self.entrada_nome.focus_set()

    def adicionar_placeholder(self, entrada, texto):

        entrada.insert(0, texto)
        entrada.config(fg=self.cor_placeholder)

        def ao_clicar(event):

            if entrada.get() == texto:
                entrada.delete(0, tk.END)
                entrada.config(fg=self.cor_fonte)

        def ao_sair(event):

            if not entrada.get():
                entrada.insert(0, texto)
                entrada.config(fg=self.cor_placeholder)

        entrada.bind("<FocusIn>", ao_clicar)
        entrada.bind("<FocusOut>", ao_sair)

    def criar_label(self, parent, texto, linha, coluna):

        tk.Label(
            parent,
            text=texto,
            font=("Arial", 10, "bold"),
            bg="white",
            fg=self.cor_fonte
        ).grid(
            row=linha,
            column=coluna,
            sticky="w"
        )

    def salvar(self):

        nome = self.entrada_nome.get()
        tipo = self.combo_tipo.get()
        disciplina_nome = self.combo_disciplina.get()
        prazo = self.entrada_prazo.get()
        descricao = self.entrada_descricao.get()
        status = self.combo_status.get()
        cor = self.combo_cor.get()

        if nome == self.placeholder_nome:
            nome = ""

        if prazo == self.placeholder_prazo:
            prazo = ""

        if descricao == self.placeholder_descricao:
            descricao = ""

        disciplina_id = self.mapa_disciplinas.get(disciplina_nome)

        try:
            tarefa = cadastrar_tarefa(
                nome=nome,
                tipo=tipo,
                disciplina_id=disciplina_id,
                prazo=prazo,
                descricao=descricao,
                status=status,
                cor=cor
            )

            if self.ao_cadastrar:
                self.ao_cadastrar(tarefa)

            self.fechar()

            self.exibir_toast(
                "Tarefa cadastrada com sucesso!",
                "sucesso"
            )

        except ValueError as erro:
            self.exibir_toast(str(erro), "erro")

    def fechar(self):
        self.overlay.destroy()

    def exibir_toast(self, mensagem, tipo):

        cor = "#2E8B57" if tipo == "sucesso" else "#D9534F"

        toast = tk.Frame(
            self.parent,
            bg=cor
        )

        toast.place(
            relx=1.0,
            x=-20,
            y=20,
            anchor="ne"
        )

        tk.Label(
            toast,
            text=mensagem,
            font=("Arial", 10, "bold"),
            bg=cor,
            fg="white",
            wraplength=300,
            justify="left"
        ).pack(
            padx=20,
            pady=15
        )

        self.parent.after(
            3000,
            toast.destroy
        )
