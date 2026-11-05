import tkinter as tk
from tkinter import ttk

from interface.modal_disciplina import ModalDisciplina
from interface.modal_tarefa import ModalTarefa
from interface.tela_tarefas import TelaTarefas


class App:
    def __init__(self, janela):
        self.janela = janela

        self.janela.title("TaskUni")
        self.janela.geometry("800x500")

        self.tela_tarefas = None

        # Frame da Home
        self.home = tk.Frame(self.janela)
        self.home.pack(fill="both", expand=True)

        self.criar_home()

    def criar_home(self):
        # Menu suspenso
        self.menu_nova = tk.Menu(
            self.janela,
            tearoff=0
        )

        self.menu_nova.add_command(
            label="Tarefa",
            command=self.abrir_modal_tarefa
        )

        self.menu_nova.add_command(
            label="Disciplina",
            command=self.abrir_modal_disciplina
        )

        # Botão Nova
        self.botao_nova = ttk.Button(
            self.home,
            text="+ Nova",
            command=self.abrir_menu_nova
        )

        self.botao_nova.pack(pady=20)

        # Botão para acessar a tela de tarefas
        botao_tarefas = ttk.Button(
            self.home,
            text="Ver tarefas",
            command=self.mostrar_tarefas
        )

        botao_tarefas.pack(pady=10)

    def abrir_menu_nova(self):
        self.menu_nova.tk_popup(
            self.botao_nova.winfo_rootx(),
            self.botao_nova.winfo_rooty()
            + self.botao_nova.winfo_height()
        )

    def abrir_modal_disciplina(self):
        ModalDisciplina(self.janela)

    def abrir_modal_tarefa(self):
        ModalTarefa(
            self.janela,
            ao_cadastrar=lambda tarefa: (
                self.tela_tarefas.atualizar_lista()
                if self.tela_tarefas else None
            )
        )

    # Abre a tela de tarefas
    def mostrar_tarefas(self):
        self.home.pack_forget()

        if self.tela_tarefas is None:
            self.tela_tarefas = TelaTarefas(
                self.janela,
                app=self
            )
        else:
            # Recarrega ao voltar para a tela: disciplinas e tarefas cadastradas
            # pela Home aparecem nos cards e no filtro de disciplina
            self.tela_tarefas.atualizar_lista()

        self.tela_tarefas.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

    # Retorna para a Home
    def mostrar_home(self):
        if self.tela_tarefas:
            self.tela_tarefas.pack_forget()

        self.home.pack(
            fill="both",
            expand=True
        )


if __name__ == "__main__":
    janela = tk.Tk()
    app = App(janela)
    janela.mainloop()