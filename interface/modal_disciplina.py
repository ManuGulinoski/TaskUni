
import tkinter as tk

from services.disciplina_service import cadastrar_disciplina


class ModalDisciplina:

    def __init__(self, parent, ao_cadastrar=None):

        self.parent = parent
        self.ao_cadastrar = ao_cadastrar

        self.cor_fonte = "#333333"
        self.cor_roxa = "#5b21b6"
        self.cor_campo = "#CCCCCC"
        self.cor_cancelar = "#F1F1F3"

        self.overlay = tk.Frame(parent, bg="#808080")
        self.overlay.place(
            relx=0,
            rely=0,
            relwidth=1,
            relheight=1
        )

        self.janela = tk.Frame(
            self.overlay,
            bg="white",
            width=560,
            height=420
        )

        self.janela.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        self.janela.pack_propagate(False)

        tk.Label(
            self.janela,
            text="Nova disciplina",
            font=("Arial", 20),
            fg=self.cor_fonte,
            bg="white"
        ).pack(
            anchor="w",
            padx=35,
            pady=(35, 5)
        )

        tk.Label(
            self.janela,
            text="Adicione uma disciplina para organizar suas tarefas",
            font=("Arial", 15),
            fg="#888888",
            bg="white"
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
            pady=(25, 0)
        )

        formulario = tk.Frame(
            self.janela,
            bg="white"
        )

        formulario.pack(
            fill="x",
            padx=35,
            pady=(30, 0)
        )

        tk.Label(
            formulario,
            text="Nome da disciplina:",
            font=("Arial", 11, "bold"),
            fg=self.cor_fonte,
            bg="white"
        ).pack(
            anchor="w",
            pady=(0, 10)
        )

        self.entrada_nome = tk.Entry(
            formulario,
            font=("Arial", 13),
            fg=self.cor_fonte,
            bg=self.cor_campo,
            relief="flat",
            bd=0,
            insertbackground=self.cor_fonte
        )

        self.entrada_nome.pack(
            fill="x",
            ipady=15
        )

        self.entrada_nome.focus_set()


        frame_botoes = tk.Frame(
            self.janela,
            bg="white"
        )

        frame_botoes.pack(
            side="bottom",
            fill="x",
            padx=20,
            pady=35
        )

        frame_botoes.columnconfigure(0, weight=1)
        frame_botoes.columnconfigure(1, weight=1)

        self.criar_botao(
            frame_botoes,
            "Cancelar",
            self.cor_cancelar,
            "#777777",
            self.fechar,
            coluna=0
        )

        self.criar_botao(
            frame_botoes,
            "Adicionar",
            self.cor_roxa,
            "white",
            self.salvar,
            coluna=1
        )

    def criar_botao(
        self, parent, texto, cor_fundo,
        cor_texto, comando, coluna
    ):

        botao = tk.Button(
            parent,
            text=texto,
            bg=cor_fundo,
            fg=cor_texto,
            font=("Arial", 12, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2",
            activebackground=cor_fundo,
            activeforeground=cor_texto,
            command=comando
        )

        botao.grid(
            row=0,
            column=coluna,
            padx=8,
            sticky="ew",
            ipady=16
        )

    def fechar(self):

        self.overlay.destroy()

    def exibir_toast(self, mensagem, tipo="sucesso"):

        if tipo == "sucesso":
            cor_fundo = "#2E8B57"
        else:
            cor_fundo = "#D9534F"

        toast = tk.Frame(
            self.parent,
            bg=cor_fundo,
            padx=20,
            pady=15
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
            bg=cor_fundo,
            fg="white",
            font=("Arial", 10, "bold"),
            wraplength=300,
            justify="left"
        ).pack()

        toast.lift()

        # Remove a notificação após 3 segundos
        self.parent.after(3000, toast.destroy)

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