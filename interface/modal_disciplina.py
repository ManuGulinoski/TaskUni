
import tkinter as tk
from tkinter import ttk

from services.disciplina_service import cadastrar_disciplina


class ModalDisciplina:

    def __init__(self, parent, ao_cadastrar=None):

        self.parent = parent
        self.ao_cadastrar = ao_cadastrar

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
            width=400,
            height=230
        )

        self.janela.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        self.janela.pack_propagate(False)

        ttk.Label(
            self.janela,
            text="Nova disciplina"
        ).pack(pady=(20, 10))

        ttk.Label(
            self.janela,
            text="Nome da disciplina:"
        ).pack(anchor="w", padx=25)

        self.entrada_nome = ttk.Entry(
            self.janela,
            width=40
        )

        self.entrada_nome.pack(padx=25, pady=5)
        self.entrada_nome.focus_set()

        frame_botoes = ttk.Frame(self.janela)
        frame_botoes.pack(pady=20)

        ttk.Button(
            frame_botoes,
            text="Cancelar",
            command=self.fechar
        ).pack(side="left", padx=5)

        ttk.Button(
            frame_botoes,
            text="Cadastrar",
            command=self.salvar
        ).pack(side="left", padx=5)

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
            pady=12
        )

        toast.place(
            relx=1.0,
            x=-20,
            y=20,
            anchor="ne"
        )

        toast.lift()

        tk.Label(
            toast,
            text=mensagem,
            bg=cor_fundo,
            fg="white",
            font=("Arial", 10, "bold"),
            wraplength=300
        ).pack()

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