import tkinter as tk
from tkinter import ttk

from repositorio import armazenamento
from interface.card_tarefa import CardTarefa
from utils.constantes import COR_FUNDO
from interface.modal_tarefa import ModalTarefa
from services.tarefa_service import verificar_tarefas_atrasadas

FONTE = "Segoe UI"
MSG_SEM_TAREFAS = "Nenhuma tarefa cadastrada."
MSG_SEM_RESULTADO = "Nenhuma tarefa encontrada para os filtros selecionados."


class TelaTarefas(tk.Frame):
    def __init__(self, parent, app=None):
        super().__init__(parent, bg=COR_FUNDO)
        self.app = app   

        self._criar_topo()
        self._criar_area_filtros()
        self._criar_lista_rolavel()

        self.atualizar_lista()

    
    def _criar_topo(self):
        topo = tk.Frame(self, bg=COR_FUNDO)
        topo.pack(fill="x")

        # Botão para voltar à Home
        ttk.Button(
            topo,
            text="← Início",
            command=self.voltar_inicio
        ).pack(side="left", padx=(0, 15))

        # Título
        tk.Label(
            topo,
            text="Tarefas",
            bg=COR_FUNDO,
            font=(FONTE, 18, "bold")
        ).pack(side="left")

        # Botão para criar tarefa
        ttk.Button(
            topo,
            text="+ Criar tarefa",
            command=self.criar_tarefa
            ).pack(side="right")

    def _criar_area_filtros(self):
        
        self.area_filtros = tk.Frame(self, bg=COR_FUNDO)
        self.area_filtros.pack(fill="x", pady=(10, 6))

        tk.Label(self.area_filtros, text="Filtros (US11)", bg=COR_FUNDO,
                 fg="#9CA3AF", font=(FONTE, 9, "italic")).pack(anchor="w")

    def _criar_lista_rolavel(self):
        
        
        
        container = tk.Frame(self, bg=COR_FUNDO)
        container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(container, bg=COR_FUNDO, highlightthickness=0)
        barra = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=barra.set)

        barra.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        
        self.lista = tk.Frame(self.canvas, bg=COR_FUNDO)
        janela_lista = self.canvas.create_window((0, 0), window=self.lista, anchor="nw")

        
        self.lista.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))

        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(
            janela_lista, width=e.width))

        
        self.canvas.bind("<Enter>", lambda e: self._ligar_roda_do_mouse(True))
        self.canvas.bind("<Leave>", lambda e: self._ligar_roda_do_mouse(False))

    def _ligar_roda_do_mouse(self, ligar):
        if ligar:
            self.canvas.bind_all("<MouseWheel>", self._rolar)                 # Windows
            self.canvas.bind_all("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))  # Linux
            self.canvas.bind_all("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))
        else:
            for evento in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
                self.canvas.unbind_all(evento)

    def _rolar(self, evento):
        self.canvas.yview_scroll(int(-evento.delta / 120), "units")

    # ======================================================================
    # Lista de cards
    # ======================================================================
    def atualizar_lista(self):
        for widget in self.lista.winfo_children():
            widget.destroy()

        disciplinas, tarefas = verificar_tarefas_atrasadas()
        nomes_disciplinas = {
            d.id: d.nome for d in disciplinas
        }

        visiveis = self._filtrar(tarefas)
        visiveis = sorted(
            visiveis, 
            key=lambda t: t.prazo
        )

        if not tarefas:
            self._mostrar_mensagem(MSG_SEM_TAREFAS)
        elif not visiveis:
            self._mostrar_mensagem(MSG_SEM_RESULTADO)

        for tarefa in visiveis:
            nome = nomes_disciplinas.get(tarefa.disciplina_id, "Disciplina não encontrada")
            card = CardTarefa(self.lista, tarefa, nome,
                              ao_editar=self.editar_tarefa,
                              ao_excluir=self.excluir_tarefa,
                              ao_concluir=self.concluir_tarefa)
            card.pack(fill="x", pady=4)

        self.canvas.yview_moveto(0)

    def _filtrar(self, tarefas):
        return tarefas

    def _mostrar_mensagem(self, texto):
        tk.Label(self.lista, text=texto, bg=COR_FUNDO, fg="#6B7280",
                 font=(FONTE, 11)).pack(pady=40)

    def criar_tarefa(self):
        ModalTarefa(
        self,
        ao_cadastrar=lambda tarefa: self.atualizar_lista()
    )

    def editar_tarefa(self, tarefa):
        print(f"[US17] Editar: {tarefa.nome}")

    def excluir_tarefa(self, tarefa):
        print(f"[US17] Excluir: {tarefa.nome}")

    def concluir_tarefa(self, tarefa):
        print(f"[US17] Concluir: {tarefa.nome}")

    def voltar_inicio(self):
        if self.app:
            self.app.mostrar_home()
