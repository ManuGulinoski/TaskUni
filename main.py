
import tkinter as tk
from tkinter import ttk
import threading
from queue import Queue, Empty

from interface.card_big_number import CardBigNumber
from interface.modal_disciplina import ModalDisciplina
from interface.modal_tarefa import ModalTarefa
from interface.tela_tarefas import TelaTarefas
from interface.tela_grafico import TelaGrafico

from services.estatisticas_service import obter_estatisticas
from services.frase_service import buscar_frase

from utils.constantes import *


class App:

    def __init__(self, janela):
        self.janela = janela

        self.janela.title("TaskUni")
        self.janela.geometry(TAMANHO_JANELA)
        self.janela.minsize(1100, 700)
        self.janela.configure(bg=COR_FUNDO)

        self.tela_tarefas = None
        self.tela_grafico = None
        self.botoes_menu = {}
        self.fila_frase = Queue()

        self.menu_lateral = tk.Frame(
            self.janela,
            bg=COR_MENU_LATERAL,
            width=LARGURA_MENU
        )

        self.menu_lateral.pack(side="left", fill="y")
        self.menu_lateral.pack_propagate(False)

        self.conteudo = tk.Frame(
            self.janela,
            bg=COR_FUNDO
        )

        self.conteudo.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.home = tk.Frame(
            self.conteudo,
            bg=COR_FUNDO
        )

        self.criar_menu()
        self.criar_home()
        self.mostrar_home()
        self.carregar_frase()

    def criar_menu(self):

        tk.Label(
            self.menu_lateral,
            text="TaskUni",
            bg=COR_MENU_LATERAL,
            fg=COR_MENU_TEXTO,
            font=("Segoe UI", 22, "bold")
        ).pack(pady=(30, 35))

        opcoes = [
            ("Home", self.mostrar_home),
            ("Tarefas", self.mostrar_tarefas),
            ("Gráficos", self.mostrar_grafico),
        ]

        for nome, acao in opcoes:

            botao = tk.Button(
                self.menu_lateral,
                text=nome,
                command=acao,
                bg=COR_MENU_LATERAL,
                fg=COR_MENU_TEXTO,
                activebackground="#374151",
                activeforeground=COR_MENU_TEXTO,
                font=("Segoe UI", 12),
                relief="flat",
                borderwidth=0,
                anchor="w",
                padx=20,
                pady=12,
                cursor="hand2"
            )

            botao.pack(fill="x", padx=10, pady=4)

            self.botoes_menu[nome] = botao

    def destacar_menu(self, selecionado):

        for nome, botao in self.botoes_menu.items():

            ativo = nome == selecionado

            botao.configure(
                bg="#374151" if ativo else COR_MENU_LATERAL,
                font=(
                    "Segoe UI",
                    12,
                    "bold" if ativo else "normal"
                )
            )

    def criar_home(self):

        self.topo = tk.Frame(
            self.home,
            bg=COR_FUNDO
        )

        self.topo.pack(
            fill="x",
            padx=25,
            pady=20
        )

        tk.Label(
            self.topo,
            text="Home",
            bg=COR_FUNDO,
            fg="#111827",
            font=("Segoe UI", 18, "bold")
        ).pack(side="left")

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

        self.botao_nova = ttk.Button(
            self.topo,
            text="+ Nova",
            command=self.abrir_menu_nova
        )

        self.botao_nova.pack(
            side="right",
            padx=5,
            pady=5
        )

        conteudo = tk.Frame(
            self.home,
            bg=COR_FUNDO
        )

        conteudo.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=20
        )

        tk.Label(
            conteudo,
            text="Bem-vindo ao TaskUni!",
            font=(FONTE, 22, "bold"),
            bg=COR_FUNDO,
            fg="#111827"
        ).pack(pady=(20, 10))

        self.area_cards = tk.Frame(
            conteudo,
            bg=COR_FUNDO
        )

        self.area_cards.pack(
            fill="x",
            pady=20
        )

        tk.Button(
            conteudo,
            text="Ver gráfico",
            font=(FONTE, 11, "bold"),
            bg=COR_BOTAO_PRINCIPAL,
            fg=COR_TEXTO_BOTAO,
            activebackground=COR_BOTAO_HOVER,
            activeforeground=COR_TEXTO_BOTAO,
            relief="flat",
            bd=0,
            cursor="hand2",
            width=18,
            height=2,
            command=self.mostrar_grafico
        ).pack(pady=10)

        self.frame_frase = tk.Frame(
            conteudo,
            bg="#FFFFFF",
            padx=30,
            pady=25
        )

        self.frame_frase.pack(
            fill="x",
            padx=10,
            pady=30
        )

        tk.Label(
            self.frame_frase,
            text="Inspire-se!",
            font=(FONTE, 14, "bold"),
            bg="#FFFFFF",
            fg=COR_BOTAO_PRINCIPAL
        ).pack(pady=(0, 12))

        self.label_frase = tk.Label(
            self.frame_frase,
            text=f'"{FRASE_RESERVA[0]}"',
            font=(FONTE, 12),
            bg="#FFFFFF",
            fg="#333333",
            wraplength=750,
            justify="center"
        )

        self.label_frase.pack(pady=5)

        self.label_autor = tk.Label(
            self.frame_frase,
            text=f"— {FRASE_RESERVA[1]}",
            font=(FONTE, 10, "italic"),
            bg="#FFFFFF",
            fg="#6B7280"
        )

        self.label_autor.pack(pady=5)

        self.atualizar_home()

    def abrir_menu_nova(self):

        try:
            self.menu_nova.tk_popup(
                self.botao_nova.winfo_rootx(),
                self.botao_nova.winfo_rooty()
                + self.botao_nova.winfo_height()
            )

        finally:
            self.menu_nova.grab_release()

    def abrir_modal_disciplina(self):

        ModalDisciplina(self.janela)

    def abrir_modal_tarefa(self):

        ModalTarefa(
            self.janela,
            ao_salvar=self.atualizar_apos_cadastro
        )

    def atualizar_apos_cadastro(self, tarefa):

        self.atualizar_telas()

    def atualizar_telas(self):

        self.atualizar_home()

        if self.tela_tarefas is not None:
            self.tela_tarefas.atualizar_lista()

        if self.tela_grafico is not None:
            self.tela_grafico.atualizar()

    def atualizar_home(self):

        for widget in self.area_cards.winfo_children():
            widget.destroy()

        estatisticas = obter_estatisticas()

        cartoes = [
            ("Total de tarefas", estatisticas["total"]),
            ("Concluídas", estatisticas["concluidas"]),
            ("Pendentes", estatisticas["pendentes"]),
            ("Atrasadas", estatisticas["atrasadas"]),
        ]

        for coluna, (titulo, numero) in enumerate(cartoes):

            self.area_cards.columnconfigure(
                coluna,
                weight=1,
                uniform="cards"
            )

            card = CardBigNumber(
                self.area_cards,
                titulo,
                numero
            )

            card.grid(
                row=0,
                column=coluna,
                sticky="nsew",
                padx=5
            )

    def carregar_frase(self):

        threading.Thread(
            target=self._buscar_frase,
            daemon=True
        ).start()

        self.janela.after(
            100,
            self._verificar_frase
        )

    def _buscar_frase(self):

        try:
            frase, autor = buscar_frase()

        except Exception:
            frase, autor = FRASE_RESERVA

        self.fila_frase.put((frase, autor))

    def _verificar_frase(self):

        try:
            frase, autor = self.fila_frase.get_nowait()

        except Empty:

            self.janela.after(
                100,
                self._verificar_frase
            )

            return

        self._atualizar_frase(frase, autor)

    def _atualizar_frase(self, frase, autor):

        self.label_frase.configure(
            text=f'"{frase}"'
        )

        self.label_autor.configure(
            text=f"— {autor}"
        )

    def ocultar_telas(self):

        self.home.pack_forget()

        if self.tela_tarefas is not None:
            self.tela_tarefas.pack_forget()

        if self.tela_grafico is not None:
            self.tela_grafico.pack_forget()

    def mostrar_home(self):

        self.ocultar_telas()
        self.atualizar_home()

        self.home.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.destacar_menu("Home")

    def mostrar_tarefas(self):

        if self.tela_tarefas is None:

            self.tela_tarefas = TelaTarefas(
                self.conteudo,
                app=self
            )

        else:
            self.tela_tarefas.atualizar_lista()

        self.ocultar_telas()

        self.tela_tarefas.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.destacar_menu("Tarefas")

    def mostrar_grafico(self):

        if self.tela_grafico is None:

            self.tela_grafico = TelaGrafico(
                self.conteudo,
                app=self
            )

        else:
            self.tela_grafico.atualizar()

        self.ocultar_telas()

        self.tela_grafico.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.destacar_menu("Gráficos")


if __name__ == "__main__":

    janela = tk.Tk()

    app = App(janela)

    janela.mainloop()
