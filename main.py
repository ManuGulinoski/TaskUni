import tkinter as tk
from tkinter import ttk

from interface.modal_disciplina import ModalDisciplina

#criado antes da US 01 só para teste da funcionalidade

def abrir_modal_disciplina():
    ModalDisciplina(janela)


janela = tk.Tk()
janela.title("TaskUni")
janela.geometry("800x500")

botao_disciplina = ttk.Button(
    janela,
    text="Cadastrar disciplina",
    command=abrir_modal_disciplina
)

botao_disciplina.pack(pady=20)

janela.mainloop()