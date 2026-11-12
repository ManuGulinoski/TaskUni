import tkinter as tk
import threading

from interface.componentes import BotaoArredondado, aplicar_estilo_ttk
from interface.modal_disciplina import ModalDisciplina
from interface.modal_tarefa import ModalTarefa
from interface.tela_tarefas import TelaTarefas
from interface.tela_grafico import TelaGrafico

from services.frase_service import buscar_frase
from utils.constantes import (
    FRASE_RESERVA, TITULO_APP, TAMANHO_JANELA, TAMANHO_MINIMO, FONTE,
    FONTE_TEXTO, COR_FUNDO, COR_SUPERFICIE, COR_BORDA, COR_PRIMARIA,
    COR_TEXTO, COR_TEXTO_SECUNDARIO, COR_SUAVE, COR_TEXTO_SUAVE,
)


class App:
    def __init__(self, janela):
        self.janela = janela

        self.janela.title(TITULO_APP)
        self.janela.geometry(TAMANHO_JANELA)
        self.janela.minsize(*TAMANHO_MINIMO)
        self.janela.configure(bg=COR_FUNDO)

        # Cores do tema nos Combobox, abas e barras de rolagem
        aplicar_estilo_ttk(self.janela)

        self.tela_tarefas = None
        self.tela_grafico = None

        # Frame da Home
        self.home = tk.Frame(self.janela, bg=COR_FUNDO)
        self.home.pack(fill="both", expand=True)

        self.criar_home()

    def criar_home(self):
        # Conteúdo centralizado na tela
        centro = tk.Frame(self.home, bg=COR_FUNDO)
        centro.place(relx=0.5, rely=0.45, anchor="center")

        # Título e subtítulo
        tk.Label(
            centro,
            text="✿ TaskUni",
            font=(FONTE, 32, "bold"),
            bg=COR_FUNDO,
            fg=COR_PRIMARIA
        ).pack()

        tk.Label(
            centro,
            text="Organize seus estudos com carinho ♡",
            font=(FONTE, 12),
            bg=COR_FUNDO,
            fg=COR_TEXTO_SECUNDARIO
        ).pack(pady=(0, 28))

        # Menu suspenso do botão "+ Nova"
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

        self.menu_nova.add_command(
            label="  ✎  Tarefa",
            command=self.abrir_modal_tarefa
        )

        self.menu_nova.add_command(
            label="  ✿  Disciplina",
            command=self.abrir_modal_disciplina
        )

        # Botões principais, lado a lado
        botoes = tk.Frame(centro, bg=COR_FUNDO)
        botoes.pack()

        self.botao_nova = BotaoArredondado(
            botoes,
            "+ Nova",
            self.abrir_menu_nova,
            altura=44,
            padx=28
        )
        self.botao_nova.pack(side="left", padx=6)

        BotaoArredondado(
            botoes,
            "Ver tarefas",
            self.mostrar_tarefas,
            tipo="suave",
            altura=44,
            padx=28
        ).pack(side="left", padx=6)

        BotaoArredondado(
            botoes,
            "Ver gráficos",
            self.mostrar_grafico,
            tipo="suave",
            altura=44,
            padx=28
        ).pack(side="left", padx=6)

        # Card da frase motivacional
        self.frame_frase = tk.Frame(
            centro,
            bg=COR_SUPERFICIE,
            highlightthickness=1,
            highlightbackground=COR_BORDA,
            highlightcolor=COR_BORDA,
            padx=36,
            pady=22
        )

        self.frame_frase.pack(
            fill="x",
            pady=(40, 0)
        )

        self.titulo_frase = tk.Label(
            self.frame_frase,
            text="✨ Inspire-se!",
            font=(FONTE, 13, "bold"),
            bg=COR_SUPERFICIE,
            fg=COR_PRIMARIA
        )

        self.titulo_frase.pack(pady=(0, 10))

        self.label_frase = tk.Label(
            self.frame_frase,
            text=f'"{FRASE_RESERVA[0]}"',
            font=(FONTE, 11),
            bg=COR_SUPERFICIE,
            fg=COR_TEXTO,
            wraplength=560,
            justify="center"
        )

        self.label_frase.pack(pady=5)

        self.label_autor = tk.Label(
            self.frame_frase,
            text=f"— {FRASE_RESERVA[1]}",
            font=(FONTE, 10, "italic"),
            bg=COR_SUPERFICIE,
            fg=COR_TEXTO_SECUNDARIO
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
            ao_salvar=lambda tarefa: self.atualizar_telas()
        )

    # Recarrega as telas já abertas depois de uma alteração nas tarefas
    def atualizar_telas(self):
        if self.tela_tarefas:
            self.tela_tarefas.atualizar_lista()
        if self.tela_grafico:
            self.tela_grafico.atualizar()

    # Abre a tela dos gráficos (por status e por tipo)
    def mostrar_grafico(self):
        self.home.pack_forget()

        if self.tela_grafico is None:
            self.tela_grafico = TelaGrafico(self.janela, app=self)
        else:
            # Recarrega ao voltar: reflete tarefas criadas/alteradas
            self.tela_grafico.atualizar()

        self.tela_grafico.pack(fill="both", expand=True, padx=20, pady=20)

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
        if self.tela_grafico:
            self.tela_grafico.pack_forget()

        self.home.pack(
            fill="both",
            expand=True
        )


if __name__ == "__main__":
    janela = tk.Tk()
    app = App(janela)
    janela.mainloop()