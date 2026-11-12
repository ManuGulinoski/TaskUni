
import tkinter as tk
from tkinter import ttk
import threading

from interface.modal_disciplina import ModalDisciplina
from interface.modal_tarefa import ModalTarefa
from interface.tela_tarefas import TelaTarefas

from services.frase_service import buscar_frase
from utils.constantes import FRASE_RESERVA


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

        # Área da frase motivacional
        self.frame_frase = tk.Frame(
            self.home,
            bg="#F3F4F6",
            padx=30,
            pady=20
        )

        self.frame_frase.pack(
            fill="x",
            padx=40,
            pady=30
        )

        self.titulo_frase = tk.Label(
            self.frame_frase,
            text="Inspire-se!",
            font=("Segoe UI", 13, "bold"),
            bg="#F3F4F6",
            fg="#5b21b6"
        )

        self.titulo_frase.pack(pady=(0, 10))

        self.label_frase = tk.Label(
            self.frame_frase,
            text=f'"{FRASE_RESERVA[0]}"',
            font=("Segoe UI", 11),
            bg="#F3F4F6",
            fg="#333333",
            wraplength=650,
            justify="center"
        )

        self.label_frase.pack(pady=5)

        self.label_autor = tk.Label(
            self.frame_frase,
            text=f"— {FRASE_RESERVA[1]}",
            font=("Segoe UI", 10, "italic"),
            bg="#F3F4F6",
            fg="#6B7280"
        )

        self.label_autor.pack(pady=5)

        self.carregar_frase()

    def carregar_frase(self):
        threading.Thread(
            target=self._buscar_frase,
            daemon=True
        ).start()

    def _buscar_frase(self):
        frase, autor = buscar_frase()

        try:
            self.janela.after(
                0,
                lambda: self._atualizar_frase(frase, autor)
            )
        except tk.TclError:
            pass

    def _atualizar_frase(self, frase, autor):
        self.label_frase.config(
            text=f'"{frase}"'
        )

        self.label_autor.config(
            text=f"— {autor}"
        )

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
            ao_salvar=lambda tarefa: (
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
