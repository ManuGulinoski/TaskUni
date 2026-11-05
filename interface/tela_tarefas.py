"""
Tela de Tarefas com cards (US08).

Responsável: Pessoa 3

De cima para baixo:
    1. Topo: título "Tarefas" e botão "Criar tarefa"
    2. Área dos filtros: disciplina, tipo, status, prioridade + "Filtrar" (US11)
    3. Lista rolável com um CardTarefa por tarefa, ordenada pelo prazo

A tela não abre o JSON por conta própria: usa armazenamento.carregar(),
a função da camada de dados (US02).

O que fica para outras US:
    - US17: o que acontece ao clicar em Criar, Editar, Excluir e Concluir
"""
import tkinter as tk
from tkinter import ttk

from repositorio import armazenamento
from interface.card_tarefa import CardTarefa
from services.filtro_service import filtrar_tarefas
from utils.constantes import (
    COR_FUNDO, TIPOS, STATUS_TODOS, PRIORIDADES, OPCAO_TODOS, OPCAO_TODAS,
)

FONTE = "Segoe UI"
MSG_SEM_TAREFAS = "Nenhuma tarefa cadastrada."
MSG_SEM_RESULTADO = "Nenhuma tarefa encontrada para os filtros selecionados."


class TelaTarefas(tk.Frame):
    def __init__(self, parent, app=None):
        super().__init__(parent, bg=COR_FUNDO)
        self.app = app   # janela principal (US01); pode ser None nos testes

        self._criar_topo()
        self._criar_area_filtros()
        self._criar_lista_rolavel()

        self.atualizar_lista()

    # ======================================================================
    # Montagem da tela
    # ======================================================================
    def _criar_topo(self):
        topo = tk.Frame(self, bg=COR_FUNDO)
        topo.pack(fill="x")

        tk.Label(topo, text="Tarefas", bg=COR_FUNDO,
                 font=(FONTE, 18, "bold")).pack(side="left")

        ttk.Button(topo, text="+ Criar tarefa",
                   command=self.criar_tarefa).pack(side="right")

    def _criar_area_filtros(self):
        """
        Filtros por disciplina, tipo, status e prioridade + botões Filtrar e Limpar.

        Os combos só guardam a ESCOLHA. O filtro só vale depois do clique em
        "Filtrar": o botão copia as escolhas para self.filtros_aplicados, e é
        esse dicionário que _filtrar usa. Assim, se a lista for recarregada por
        outro motivo (ex.: criar uma tarefa na US17), ela respeita o último
        filtro aplicado, e não uma escolha que o usuário ainda não confirmou.
        """
        self.area_filtros = tk.Frame(self, bg=COR_FUNDO)
        self.area_filtros.pack(fill="x", pady=(10, 6))

        # Nome da disciplina -> id (preenchido em _atualizar_opcoes_disciplina)
        self.mapa_disciplinas = {}

        self.combo_disciplina = self._criar_combo("Disciplina", [OPCAO_TODAS], 0)
        self.combo_tipo = self._criar_combo("Tipo", [OPCAO_TODOS] + TIPOS, 1)
        self.combo_status = self._criar_combo("Status", [OPCAO_TODOS] + STATUS_TODOS, 2)
        self.combo_prioridade = self._criar_combo("Prioridade", [OPCAO_TODAS] + PRIORIDADES, 3)

        # Botões na mesma linha dos combos
        ttk.Button(self.area_filtros, text="Filtrar",
                   command=self.aplicar_filtros).grid(row=1, column=4, padx=(4, 4), sticky="s")
        ttk.Button(self.area_filtros, text="Limpar",
                   command=self.limpar_filtros).grid(row=1, column=5, sticky="s")

        # Começa sem filtro nenhum
        self.filtros_aplicados = self._ler_combos()

    def _criar_combo(self, titulo, opcoes, coluna):
        """Cria um rótulo + Combobox somente leitura na coluna indicada."""
        tk.Label(self.area_filtros, text=titulo, bg=COR_FUNDO, fg="#374151",
                 font=(FONTE, 9, "bold")).grid(row=0, column=coluna, sticky="w", padx=(0, 10))

        combo = ttk.Combobox(self.area_filtros, values=opcoes, state="readonly", width=16)
        combo.set(opcoes[0])          # "Todos" / "Todas"
        combo.grid(row=1, column=coluna, sticky="w", padx=(0, 10))
        return combo

    def _atualizar_opcoes_disciplina(self, disciplinas):
        """Recarrega as disciplinas cadastradas no combo, mantendo a escolha atual
        se ela ainda existir (uma disciplina nova aparece sem reabrir a tela)."""
        self.mapa_disciplinas = {d.nome: d.id for d in disciplinas}
        nomes = sorted(self.mapa_disciplinas, key=str.lower)
        self.combo_disciplina["values"] = [OPCAO_TODAS] + nomes

        if self.combo_disciplina.get() not in self.mapa_disciplinas:
            self.combo_disciplina.set(OPCAO_TODAS)

    def _ler_combos(self):
        """Converte o que está selecionado nos combos para os parâmetros do
        filtro_service. Disciplina vira id; "Todos"/"Todas" são ignorados pelo serviço."""
        nome_disciplina = self.combo_disciplina.get()
        return {
            "disciplina_id": self.mapa_disciplinas.get(nome_disciplina, OPCAO_TODAS),
            "tipo": self.combo_tipo.get(),
            "status": self.combo_status.get(),
            "prioridade": self.combo_prioridade.get(),
        }

    def aplicar_filtros(self):
        """Botão "Filtrar": guarda as escolhas e redesenha os cards."""
        self.filtros_aplicados = self._ler_combos()
        self.atualizar_lista()

    def limpar_filtros(self):
        """Botão "Limpar": volta todos os combos para Todos/Todas e mostra tudo."""
        for combo in (self.combo_disciplina, self.combo_tipo,
                      self.combo_status, self.combo_prioridade):
            combo.current(0)
        self.aplicar_filtros()

    def _criar_lista_rolavel(self):
        """
        O Tkinter não tem um Frame com barra de rolagem pronto.
        O truque: um Canvas (que rola) com um Frame dentro dele (onde ficam os cards).
        """
        container = tk.Frame(self, bg=COR_FUNDO)
        container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(container, bg=COR_FUNDO, highlightthickness=0)
        barra = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=barra.set)

        barra.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Frame interno, colocado "dentro" do canvas
        self.lista = tk.Frame(self.canvas, bg=COR_FUNDO)
        janela_lista = self.canvas.create_window((0, 0), window=self.lista, anchor="nw")

        # Quando os cards mudam de tamanho, atualiza a área que pode rolar
        self.lista.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))
        # Quando a janela muda de largura, os cards acompanham
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(
            janela_lista, width=e.width))

        # Roda do mouse só rola enquanto o mouse está sobre a lista
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
        """Recarrega os dados e redesenha todos os cards.
        Chamada ao abrir a tela e, depois, sempre que algo mudar (filtros, US17)."""
        # 1. Apaga os cards antigos
        for widget in self.lista.winfo_children():
            widget.destroy()

        # 2. Lê os dados pela camada de dados (US02)
        disciplinas, tarefas = armazenamento.carregar()
        nomes_disciplinas = {d.id: d.nome for d in disciplinas}
        self._atualizar_opcoes_disciplina(disciplinas)

        # 3. Aplica os filtros e ordena pelo prazo
        visiveis = self._filtrar(tarefas)
        visiveis = sorted(visiveis, key=lambda t: t.prazo)   # mais próximo primeiro

        # 4. Mensagens de lista vazia (são duas situações diferentes)
        if not tarefas:
            self._mostrar_mensagem(MSG_SEM_TAREFAS)
        elif not visiveis:
            self._mostrar_mensagem(MSG_SEM_RESULTADO)

        # 5. Um card por tarefa
        for tarefa in visiveis:
            nome = nomes_disciplinas.get(tarefa.disciplina_id, "Disciplina não encontrada")
            card = CardTarefa(self.lista, tarefa, nome,
                              ao_editar=self.editar_tarefa,
                              ao_excluir=self.excluir_tarefa,
                              ao_concluir=self.concluir_tarefa)
            card.pack(fill="x", pady=4)

        # Volta a rolagem para o topo
        self.canvas.yview_moveto(0)

    def _filtrar(self, tarefas):
        """Aplica os filtros confirmados no botão "Filtrar" (US11)."""
        return filtrar_tarefas(tarefas, **self.filtros_aplicados)

    def _mostrar_mensagem(self, texto):
        tk.Label(self.lista, text=texto, bg=COR_FUNDO, fg="#6B7280",
                 font=(FONTE, 11)).pack(pady=40)

    # ======================================================================
    # Ações dos botões e ícones (a ligação de verdade é na US17)
    # ======================================================================
    def criar_tarefa(self):
        # US17: ModalTarefa(self, ao_cadastrar=lambda tarefa: self.atualizar_lista())
        print("[US17] Criar tarefa")

    def editar_tarefa(self, tarefa):
        print(f"[US17] Editar: {tarefa.nome}")

    def excluir_tarefa(self, tarefa):
        print(f"[US17] Excluir: {tarefa.nome}")

    def concluir_tarefa(self, tarefa):
        print(f"[US17] Concluir: {tarefa.nome}")
