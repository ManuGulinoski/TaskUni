import tkinter as tk
import threading

from interface.modal_disciplina import ModalDisciplina
from interface.modal_tarefa import ModalTarefa
from interface.tela_tarefas import TelaTarefas

from services.frase_service import buscar_frase
from utils.constantes import *


class App:

    def __init__(self, janela):
        self.janela = janela

        self.janela.title(TITULO_APP)
        self.janela.geometry(TAMANHO_JANELA)
        self.janela.configure(bg=COR_FUNDO)

        self.tela_tarefas = None

        # Frame principal da Home
        self.home = tk.Frame(
            self.janela,
            bg=COR_FUNDO
        )

        self.home.pack(
            fill="both",
            expand=True
        )

        self.criar_home()


    def criar_home(self):

        # Barra superior
        self.topo = tk.Frame(
            self.home,
            bg=COR_FUNDO
        )

        self.topo.pack(
            fill="x",
            padx=25,
            pady=20
        )

        # Menu suspenso de criação
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

        # Botão Nova no canto superior direito
        self.botao_nova = self.criar_botao_novo(
            self.topo,
            texto="+ Nova",
            comando=self.abrir_menu_nova
        )

        self.botao_nova.pack(
            side="right",
            padx=5,
            pady=5
        )

        # Conteúdo central da Home
        conteudo = tk.Frame(
            self.home,
            bg=COR_FUNDO
        )

        conteudo.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=30
        )

        # Título da Home
        tk.Label(
            conteudo,
            text="Bem-vindo ao TaskUni!",
            font=(FONTE, 22, "bold"),
            bg=COR_FUNDO,
            fg="#111827"
        ).pack(pady=(30, 10))

        # Botão para acessar as tarefas
        tk.Button(
            conteudo,
            text="Ver tarefas",
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
            command=self.mostrar_tarefas
        ).pack(pady=15)

        # Área da frase motivacional
        self.frame_frase = tk.Frame(
            conteudo,
            bg="#FFFFFF",
            padx=30,
            pady=25
        )

        self.frame_frase.pack(
            fill="x",
            padx=40,
            pady=40
        )

        tk.Label(
            self.frame_frase,
            text="Inspire-se!",
            font=(FONTE, 14, "bold"),
            bg="#FFFFFF",
            fg=COR_BOTAO_PRINCIPAL
        ).pack(pady=(0, 12))

        # Frase reserva exibida inicialmente
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

        # Busca uma frase da API sem bloquear a interface
        self.carregar_frase()

    def criar_botao_novo(self, parent, texto, comando):

        botao = tk.Button(
            parent,
            text=texto,
            font=(FONTE, 10, "bold"),
            bg=COR_BOTAO_PRINCIPAL,
            fg=COR_TEXTO_BOTAO,
            activebackground=COR_BOTAO_HOVER,
            activeforeground=COR_TEXTO_BOTAO,
            relief="flat",
            bd=0,
            highlightthickness=0,
            cursor="hand2",
            width=14,
            height=2,
            command=comando
        )

        # Efeito ao passar o mouse
        botao.bind(
            "<Enter>",
            lambda evento: botao.config(
                bg=COR_BOTAO_HOVER
            )
        )

        botao.bind(
            "<Leave>",
            lambda evento: botao.config(
                bg=COR_BOTAO_PRINCIPAL
            )
        )

        return botao


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
            ao_salvar=lambda tarefa: (
                self.tela_tarefas.atualizar_lista()
                if self.tela_tarefas else None
            )
        )
    def carregar_frase(self):

        threading.Thread(
            target=self._buscar_frase,
            daemon=True
        ).start()

    def _buscar_frase(self):

        try:
            frase, autor = buscar_frase()

            self.janela.after(
                0,
                lambda: self._atualizar_frase(frase, autor)
            )

        except Exception:
            # Mantém a frase reserva caso ocorra algum erro
            pass

    def _atualizar_frase(self, frase, autor):

        self.label_frase.config(
            text=f'"{frase}"'
        )

        self.label_autor.config(
            text=f"— {autor}"
        )

    # ==========================================================
    # NAVEGAÇÃO
    # ==========================================================

    def mostrar_tarefas(self):

        self.home.pack_forget()

        if self.tela_tarefas is None:

            self.tela_tarefas = TelaTarefas(
                self.janela,
                app=self
            )

        else:
            # Atualiza tarefas e disciplinas ao abrir a tela
            self.tela_tarefas.atualizar_lista()

        self.tela_tarefas.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

    def mostrar_home(self):

        if self.tela_tarefas:
            self.tela_tarefas.pack_forget()

        self.home.pack(
            fill="both",
            expand=True
        )


# ==============================================================
# EXECUÇÃO
# ==============================================================

if __name__ == "__main__":

    janela = tk.Tk()

    app = App(janela)

    janela.mainloop()
