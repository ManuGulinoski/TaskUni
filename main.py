import tkinter as tk
from tkinter import ttk

from interface.modal_disciplina import ModalDisciplina
from interface.modal_tarefa import ModalTarefa


def abrir_modal_disciplina():
    ModalDisciplina(janela)


def abrir_modal_tarefa():
    ModalTarefa(janela)


def abrir_menu_nova():
    menu_nova.tk_popup(
        botao_nova.winfo_rootx(),
        botao_nova.winfo_rooty() + botao_nova.winfo_height()
    )


janela = tk.Tk()
janela.title("TaskUni")
janela.geometry("800x500")


# Menu suspenso
menu_nova = tk.Menu(
    janela,
    tearoff=0
)

menu_nova.add_command(
    label="Tarefa",
    command=abrir_modal_tarefa
)

menu_nova.add_command(
    label="Disciplina",
    command=abrir_modal_disciplina
)


# Botão Nova
botao_nova = ttk.Button(
    janela,
    text="+ Nova",
    command=abrir_menu_nova
)

botao_nova.pack(pady=20)


janela.mainloop()