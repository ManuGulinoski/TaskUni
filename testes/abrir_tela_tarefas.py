"""
Abre só a tela de Tarefas (US08), sem precisar da janela principal (US01).

Rodar (da pasta do projeto):
    python -m testes.abrir_tela_tarefas

Clicar nos ícones imprime no terminal qual ação e qual tarefa
(a ação de verdade é ligada na US17).
"""
import tkinter as tk

from interface.tela_tarefas import TelaTarefas

janela = tk.Tk()
janela.title("Teste US08 - Tela de Tarefas")
janela.geometry("900x620")

tela = TelaTarefas(janela, app=None)
tela.pack(fill="both", expand=True, padx=20, pady=20)

janela.mainloop()
