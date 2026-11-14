import tkinter as tk
from tkinter import ttk
import threading
from queue import Queue, Empty

from interface.card_big_number import CardBigNumber
from interface.componentes import BotaoArredondado, aplicar_estilo_ttk
from interface.graficos import GraficoColunas, GraficoPizza
from interface.modal_disciplina import ModalDisciplina
from interface.modal_tarefa import ModalTarefa
from interface.tela_tarefas import TelaTarefas
from interface.tela_grafico import TelaGrafico

from repositorio import armazenamento
from services.estatisticas_service import obter_estatisticas
from services.frase_service import buscar_frase
from services.grafico_service import contar_por_status, contar_por_tipo

from utils.constantes import *
from utils.icones import criar_icones_menu, criar_icones_frase


class App:

    def __init__(self, janela):
        self.janela = janela

        self.janela.title("TaskUni")
        self.janela.geometry(TAMANHO_JANELA)
        self.janela.minsize(*TAMANHO_MINIMO)
        self.janela.configure(bg=COR_FUNDO)

        # Cores do tema nos Combobox, abas e barras de rolagem
        aplicar_estilo_ttk(self.janela)

        self.tela_tarefas = None
        self.tela_grafico = None
        self.botoes_menu = {}
        self.fila_frase = Queue()
        self.carregando_frase = False

        self.menu_lateral = tk.Frame(
            self.janela,
            bg=COR_MENU_LATERAL,
            width=LARGURA_MENU
        )

        self.menu_lateral.pack(side="left", fill="y")
        self.menu_lateral.pack_propagate(False)

        # Linha fininha separando o menu do conteúdo
        tk.Frame(
            self.janela,
            bg=COR_BORDA,
            width=1
        ).pack(side="left", fill="y")

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

    # ==========================================================
    # MENU LATERAL
    # ==========================================================

    def criar_menu(self):

        tk.Label(
            self.menu_lateral,
            text="✿ TaskUni",
            bg=COR_MENU_LATERAL,
            fg=COR_MENU_LOGO,
            font=(FONTE, 20, "bold")
        ).pack(pady=(30, 30))

        opcoes = [
            ("Home", self.mostrar_home),
            ("Tarefas", self.mostrar_tarefas),
            ("Gráficos", self.mostrar_grafico),
        ]

        for nome, acao in opcoes:

            botao = BotaoArredondado(
                self.menu_lateral,
                nome,
                acao,
                tipo="menu",
                altura=42,
                fonte=(FONTE, 11),
                alinhar="left",
                raio=12
            )

            botao.pack(fill="x", padx=14, pady=3)

            self.botoes_menu[nome] = botao

        tk.Label(
            self.menu_lateral,
            text="Bons estudos! ♡",
            bg=COR_MENU_LATERAL,
            fg=COR_TEXTO_SECUNDARIO,
            font=(FONTE, 9)
        ).pack(side="bottom", pady=20)

    def destacar_menu(self, selecionado):

        for nome, botao in self.botoes_menu.items():

            ativo = nome == selecionado

            botao.definir_tipo(
                "menu_ativo" if ativo else "menu",
                fonte=(FONTE, 11, "bold" if ativo else "normal")
            )

    # ==========================================================
    # HOME
    # ==========================================================

    def criar_home(self):

        # ---------- Topo: boas-vindas + botão "+ Nova" ----------
        self.topo = tk.Frame(
            self.home,
            bg=COR_FUNDO
        )

        self.topo.pack(
            fill="x",
            padx=10,
            pady=(0, 16)
        )

        textos = tk.Frame(self.topo, bg=COR_FUNDO)
        textos.pack(side="left")

        tk.Label(
            textos,
            text="Bem-vindo ao TaskUni! ✿",
            bg=COR_FUNDO,
            fg=COR_TEXTO,
            font=FONTE_TITULO
        ).pack(anchor="w")

        tk.Label(
            textos,
            text="Veja como estão suas tarefas ♡",
            bg=COR_FUNDO,
            fg=COR_TEXTO_SECUNDARIO,
            font=FONTE_SUBTITULO
        ).pack(anchor="w")

        self.menu_nova = tk.Menu(
            self.janela,
            tearoff=0,
            bg=COR_SUPERFICIE,
            fg=COR_TEXTO,
            activebackground=COR_SUAVE,
            activeforeground=COR_TEXTO_SUAVE,
            font=FONTE_TEXTO,
            bd=0
        )

        icones_menu = criar_icones_menu()

        self.menu_nova.add_command(
            label="  Tarefa",
            image=icones_menu["tarefa"],
            compound="left",
            command=self.abrir_modal_tarefa
        )

        self.menu_nova.add_command(
            label="  Disciplina",
            image=icones_menu["disciplina"],
            compound="left",
            command=self.abrir_modal_disciplina
        )

        self.botao_nova = BotaoArredondado(
            self.topo,
            "+ Nova",
            self.abrir_menu_nova,
            altura=42,
            padx=26
        )

        self.botao_nova.pack(side="right")

        # ---------- Cards de números ----------
        self.area_cards = tk.Frame(
            self.home,
            bg=COR_FUNDO
        )

        self.area_cards.pack(
            fill="x",
            padx=5,
            pady=(0, 14)
        )

        # ---------- Frase motivacional (fica embaixo) ----------
        self.frame_frase = tk.Frame(
            self.home,
            bg=COR_SUPERFICIE,
            highlightthickness=1,
            highlightbackground=COR_BORDA,
            highlightcolor=COR_BORDA,
            padx=24,
            pady=14
        )

        self.frame_frase.pack(
            side="bottom",
            fill="x",
            padx=10,
            pady=(14, 0)
        )

        tk.Label(
            self.frame_frase,
            text="✨ Inspire-se!",
            font=(FONTE, 12, "bold"),
            bg=COR_SUPERFICIE,
            fg=COR_PRIMARIA
        ).pack()

        self.label_frase = tk.Label(
            self.frame_frase,
            text=f'"{FRASE_RESERVA[0]}"',
            font=(FONTE, 11),
            bg=COR_SUPERFICIE,
            fg=COR_TEXTO,
            wraplength=750,
            justify="center"
        )

        self.label_frase.pack(pady=(6, 2))

        self.label_autor = tk.Label(
            self.frame_frase,
            text=f"— {FRASE_RESERVA[1]}",
            font=(FONTE, 10, "italic"),
            bg=COR_SUPERFICIE,
            fg=COR_TEXTO_SECUNDARIO
        )

        self.label_autor.pack()

        icones_frase = criar_icones_frase()

        self.botao_recarregar_frase = tk.Label(
            self.frame_frase,
            image=icones_frase["recarregar"],
            bg=COR_SUPERFICIE,
            cursor="hand2",
            padx=6,
            pady=6
        )

        self.botao_recarregar_frase.place(
            relx=1.0,
            x=-10,
            y=6,
            anchor="ne"
        )

        self.botao_recarregar_frase.bind(
            "<Button-1>",
            lambda e: self.carregar_frase()
        )

        self.botao_recarregar_frase.bind(
            "<Enter>",
            lambda e: self.botao_recarregar_frase.configure(bg=COR_SUAVE)
        )

        self.botao_recarregar_frase.bind(
            "<Leave>",
            lambda e: self.botao_recarregar_frase.configure(bg=COR_SUPERFICIE)
        )

        # ---------- Gráficos (ocupam o espaço do meio) ----------
        area_graficos = tk.Frame(
            self.home,
            bg=COR_FUNDO
        )

        area_graficos.pack(
            fill="both",
            expand=True,
            padx=5
        )

        area_graficos.columnconfigure(0, weight=1, uniform="graficos")
        area_graficos.columnconfigure(1, weight=1, uniform="graficos")
        area_graficos.rowconfigure(0, weight=1)

        # Colunas para status e pizza para tipo (biblioteca matplotlib)
        self.grafico_status_home = self._criar_card_grafico(
            area_graficos,
            "Tarefas por status",
            GraficoColunas,
            CORES_GRAFICO_STATUS,
            coluna=0
        )

        self.grafico_tipo_home = self._criar_card_grafico(
            area_graficos,
            "Tarefas por tipo",
            GraficoPizza,
            CORES_GRAFICO_TIPO,
            coluna=1
        )

    def _criar_card_grafico(self, parent, titulo, classe_grafico, cores, coluna):
        """Card branco com título, link "Ver detalhes" e um gráfico compacto."""

        card = tk.Frame(
            parent,
            bg=COR_SUPERFICIE,
            highlightthickness=1,
            highlightbackground=COR_BORDA,
            highlightcolor=COR_BORDA,
            padx=14,
            pady=10
        )

        card.grid(
            row=0,
            column=coluna,
            sticky="nsew",
            padx=5
        )

        cabecalho = tk.Frame(card, bg=COR_SUPERFICIE)
        cabecalho.pack(fill="x")

        tk.Label(
            cabecalho,
            text=titulo,
            bg=COR_SUPERFICIE,
            fg=COR_TEXTO,
            font=(FONTE, 11, "bold")
        ).pack(side="left")

        BotaoArredondado(
            cabecalho,
            "Ver detalhes →",
            self.mostrar_grafico,
            tipo="suave",
            altura=28,
            padx=12,
            fonte=(FONTE, 9, "bold")
        ).pack(side="right")

        grafico = classe_grafico(
            card,
            cores=cores,
            compacto=True
        )

        grafico.pack(fill="both", expand=True, pady=(6, 0))

        return grafico

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
        """Atualiza os cards de números e os gráficos da Home."""

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

        # Gráficos da Home
        _, tarefas = armazenamento.carregar()

        self.grafico_status_home.atualizar(contar_por_status(tarefas))
        self.grafico_tipo_home.atualizar(contar_por_tipo(tarefas))

    def carregar_frase(self):

        # Evita várias buscas ao mesmo tempo
        if self.carregando_frase:
            return

        self.carregando_frase = True
        self.botao_recarregar_frase.configure(cursor="watch")

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

        self.carregando_frase = False
        self.botao_recarregar_frase.configure(cursor="hand2")

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