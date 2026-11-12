import tkinter as tk
from tkinter import ttk

class CardBigNumber(ttk.Frame):

    def __init__(self, master, titulo, numero):
        super().__init__(master, padding=15)

        self.config(relief="solid")

        self.titulo = ttk.Label(
            self,
            text=titulo,
            font=("Arial", 11)
        )
        self.titulo.pack()

        self.numero = ttk.Label(
            self,
            text=str(numero),
            font=("Arial", 24, "bold")
        )
        self.numero.pack(pady=5)