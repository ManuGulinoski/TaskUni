import tkinter as tk
from tkinter import ttk

from repositorio import armazenamento
from services.tarefa_service import *

from utils.constantes import *
from interface.componentes import BotaoArredondado, exibir_toast


class ModalTarefa:

    def __init__(self, parent, tarefa=None, ao_salvar=None):
        self.parent = parent
        self.tarefa = tarefa
        self.ao_salvar = ao_salvar
        self.modo_edicao = tarefa is not None
        # Cores do tema (utils/constantes.py)
        self.cor_fundo = COR_OVERLAY
        self.cor_fonte = COR_TEXTO
        self.cor_campo = COR_CAMPO
        self.cor_roxo = COR_PRIMARIA
        self.cor_cinza = COR_SECUNDARIA
        self.cor_placeholder = COR_PLACEHOLDER
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
            bg=COR_SUPERFICIE,
            highlightthickness=1,
            highlightbackground=COR_BORDA,
            highlightcolor=COR_BORDA
        )

        # Largura fixa; a altura se ajusta ao conteúdo
        self.janela.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            width=650
        )

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
            text="Editar tarefa" if self.modo_edicao else "Nova tarefa",
            font=(FONTE, 20, "bold"),
            bg=COR_SUPERFICIE,
            fg=self.cor_fonte
        ).pack(
            anchor="w",
            padx=35,
            pady=(24, 2)
        )

        tk.Label(
            self.janela,
            text=( "Atualize as informações da sua tarefa"
                  if self.modo_edicao
                  else "Adicione uma tarefa para organizar suas atividades"
),
            font=(FONTE, 10),
            bg=COR_SUPERFICIE,
            fg=COR_TEXTO_SECUNDARIO
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
            pady=(16, 12)
        )

        formulario = tk.Frame(
            self.janela,
            bg=COR_SUPERFICIE
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

        self.entrada_nome.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            ipady=8,
            pady=(4, 10)
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
            font=(FONTE, 11)
        )

        self.combo_tipo.grid(
            row=3,
            column=0,
            sticky="ew",
            ipady=5,
            padx=(0, 10),
            pady=(4, 10)
        )

        self.criar_label(formulario, "Disciplina *", 2, 1)
        self.combo_disciplina = ttk.Combobox(
            formulario,
            values=list(self.mapa_disciplinas.keys()),
            state="readonly",
            font=(FONTE, 11)
        )

        self.combo_disciplina.grid(
            row=3,
            column=1,
            sticky="ew",
            ipady=5,
            padx=(10, 0),
            pady=(4, 10)
        )

        self.criar_label(formulario, "Prazo (DD/MM/AAAA) *", 4, 0)
        self.entrada_prazo = tk.Entry(
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

        self.entrada_prazo.grid(
            row=5,
            column=0,
            sticky="ew",
            ipady=8,
            padx=(0, 10),
            pady=(4, 10)
        )

        self.adicionar_placeholder(
            self.entrada_prazo,
            self.placeholder_prazo
        )

        self.criar_label(formulario, "Descrição", 6, 0)
        self.entrada_descricao = tk.Entry(
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

        self.entrada_descricao.grid(
            row=7,
            column=0,
            columnspan=2,
            sticky="ew",
            ipady=8,
            pady=(4, 10)
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
            font=(FONTE, 11)
        )

        self.combo_status.grid(
            row=9,
            column=0,
            sticky="ew",
            ipady=5,
            padx=(0, 10),
            pady=(4, 10)
        )

        self.criar_label(formulario, "Cor", 8, 1)
        self.combo_cor = ttk.Combobox(
            formulario,
            values=list(CORES_TAREFA.keys()),
            state="readonly",
            font=(FONTE, 11)
        )

        self.combo_cor.grid(
            row=9,
            column=1,
            sticky="ew",
            ipady=5,
            padx=(10, 0),
            pady=(4, 10)
        )

        self.combo_cor.set("Branco")
        self.combo_status.set("A fazer")

        botoes = tk.Frame(
            self.janela,
            bg=COR_SUPERFICIE
        )

        botoes.pack(
            pady=(22, 20)
        )

        BotaoArredondado(
            botoes,
            "Cancelar",
            self.fechar,
            tipo="secundario",
            altura=42,
            padx=28
        ).pack(
            side="left",
            padx=6
        )

        BotaoArredondado(
            botoes,
            "Salvar alterações" if self.modo_edicao else "Adicionar",
            self.salvar,
            altura=42,
            padx=28
        ).pack(
            side="left",
            padx=6
        )

        if self.modo_edicao:
            self.preencher_campos()

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
            font=(FONTE, 10, "bold"),
            bg=COR_SUPERFICIE,
            fg=self.cor_fonte
        ).grid(
            row=linha,
            column=coluna,
            sticky="w"
        )

    def preencher_campos(self):
        tarefa = self.tarefa

        # Nome
        self.entrada_nome.delete(0, tk.END)
        self.entrada_nome.insert(0, tarefa.nome)
        self.entrada_nome.config(fg=self.cor_fonte)

        # Tipo
        self.combo_tipo.set(tarefa.tipo)

        # Disciplina
        nome_disciplina = next(
            (
                nome
                for nome, id_disciplina in self.mapa_disciplinas.items()
                if id_disciplina == tarefa.disciplina_id
            ),
            ""
        )

        self.combo_disciplina.set(nome_disciplina)

        # Prazo
        self.entrada_prazo.delete(0, tk.END)
        self.entrada_prazo.insert(
            0,
            tarefa.prazo.strftime("%d/%m/%Y")
        )
        self.entrada_prazo.config(fg=self.cor_fonte)

        # Descrição
        self.entrada_descricao.delete(0, tk.END)
        self.entrada_descricao.insert(0, tarefa.descricao or "")
        self.entrada_descricao.config(fg=self.cor_fonte)

        # Status
        status = tarefa.status

        if status == STATUS_ATRASADA:
            status = STATUS_A_FAZER

        self.combo_status.set(status)

        # Cor
        self.combo_cor.set(tarefa.cor or "Branco")

    def salvar(self):

        nome = self.entrada_nome.get()
        tipo = self.combo_tipo.get()
        disciplina_nome = self.combo_disciplina.get()
        prazo = self.entrada_prazo.get()
        descricao = self.entrada_descricao.get()
        status = self.combo_status.get()
        cor = self.combo_cor.get()

        # Remove os placeholders
        if nome == self.placeholder_nome:
            nome = ""

        if prazo == self.placeholder_prazo:
            prazo = ""

        if descricao == self.placeholder_descricao:
            descricao = ""

        disciplina_id = self.mapa_disciplinas.get(disciplina_nome)

        try:

            if self.modo_edicao:

                tarefa = editar_tarefa(
                    tarefa_id=self.tarefa.id,
                    nome=nome,
                    tipo=tipo,
                    disciplina_id=disciplina_id,
                    prazo=prazo,
                    descricao=descricao,
                    status=status,
                    cor=cor
                )

                mensagem = "Tarefa atualizada com sucesso!"

            else:

                tarefa = cadastrar_tarefa(
                    nome=nome,
                    tipo=tipo,
                    disciplina_id=disciplina_id,
                    prazo=prazo,
                    descricao=descricao,
                    status=status,
                    cor=cor
                )

                mensagem = "Tarefa cadastrada com sucesso!"

            if self.ao_salvar:
                self.ao_salvar(tarefa)

            self.fechar()

            self.exibir_toast(mensagem, "sucesso")

        except ValueError as erro:
            self.exibir_toast(str(erro), "erro")

    def fechar(self):
        self.overlay.destroy()

    def exibir_toast(self, mensagem, tipo):
        exibir_toast(self.parent, mensagem, tipo)