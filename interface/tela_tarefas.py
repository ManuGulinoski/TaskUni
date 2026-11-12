import tkinter as tk
from tkinter import ttk

from interface.card_tarefa import CardTarefa
from interface.modal_tarefa import ModalTarefa
from services.tarefa_service import verificar_tarefas_atrasadas
from services.filtro_service import filtrar_tarefas
from utils.constantes import *


class TelaTarefas(tk.Frame):

    def __init__(self, parent, app=None):
        super().__init__(parent, bg=COR_FUNDO)

        self.app = app

        self._criar_estilo()
        self._criar_topo()
        self._criar_area_filtros()
        self._criar_lista_rolavel()

        self.atualizar_lista()

    # ==========================================================
    # ESTILOS
    # ==========================================================

    def _criar_estilo(self):
        """Configura o estilo dos campos de seleção."""

        estilo = ttk.Style()

        estilo.configure(
            "Filtros.TCombobox",
            font=(FONTE, 10),
            padding=(8, 7)
        )

    # ==========================================================
    # TOPO
    # ==========================================================

    def _criar_topo(self):

        topo = tk.Frame(self, bg=COR_FUNDO)
        topo.pack(fill="x")

        ttk.Button(
            topo,
            text="← Início",
            command=self.voltar_inicio
        ).pack(side="left", padx=(0, 15))

        tk.Label(
            topo,
            text="Tarefas",
            bg=COR_FUNDO,
            fg=COR_TEXTO,
            font=(FONTE, 18, "bold")
        ).pack(side="left")

        botao_nova = tk.Button(
            topo,
            text="+ Criar tarefa",
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
            command=self.criar_tarefa
        )

        botao_nova.pack(side="right", padx=5, pady=5)

        botao_nova.bind(
            "<Enter>",
            lambda evento: botao_nova.config(bg=COR_BOTAO_HOVER)
        )

        botao_nova.bind(
            "<Leave>",
            lambda evento: botao_nova.config(bg=COR_BOTAO_PRINCIPAL)
        )

    # ==========================================================
    # FILTROS
    # ==========================================================

    def _criar_area_filtros(self):

        # Fundo branco envolvendo todos os filtros
        self.area_filtros = tk.Frame(
            self,
            bg="#FFFFFF",
            padx=18,
            pady=15
        )

        self.area_filtros.pack(
            fill="x",
            pady=(15, 22)
        )

        self.mapa_disciplinas = {}

        self.combo_disciplina = self._criar_combo(
            "Disciplina",
            [OPCAO_TODAS],
            0
        )

        self.combo_tipo = self._criar_combo(
            "Tipo",
            [OPCAO_TODOS] + TIPOS,
            1
        )

        self.combo_status = self._criar_combo(
            "Status",
            [OPCAO_TODOS] + STATUS_TODOS,
            2
        )

        self.combo_prioridade = self._criar_combo(
            "Prioridade",
            [OPCAO_TODAS] + PRIORIDADES,
            3
        )

        # Botões Filtrar e Limpar
        botao_filtrar = self._criar_botao_filtro(
            "Filtrar",
            self.aplicar_filtros
        )

        botao_filtrar.grid(
            row=1,
            column=4,
            padx=(8, 6),
            sticky="s"
        )

        botao_limpar = self._criar_botao_filtro(
            "Limpar",
            self.limpar_filtros
        )

        botao_limpar.grid(
            row=1,
            column=5,
            padx=(4, 0),
            sticky="s"
        )

        self.filtros_aplicados = self._ler_combos()

    def _criar_combo(self, titulo, opcoes, coluna):
        """Cria o título e o campo de seleção de cada filtro."""

        tk.Label(
            self.area_filtros,
            text=titulo,
            bg="#FFFFFF",
            fg=COR_TEXTO_LABEL,
            font=(FONTE, 9, "bold")
        ).grid(
            row=0,
            column=coluna,
            sticky="w",
            padx=(0, 12),
            pady=(0, 6)
        )

        combo = ttk.Combobox(
            self.area_filtros,
            values=opcoes,
            state="readonly",
            width=19,
            style="Filtros.TCombobox"
        )

        combo.set(opcoes[0])

        combo.grid(
            row=1,
            column=coluna,
            sticky="ew",
            padx=(0, 12)
        )

        return combo

    def _criar_botao_filtro(self, texto, comando):
        """Cria os botões de filtro com efeito roxo ao passar o mouse."""

        botao = tk.Button(
            self.area_filtros,
            text=texto,
            font=(FONTE, 9, "bold"),
            bg="#E5E7EB",
            fg=COR_TEXTO,
            activebackground=COR_BOTAO_HOVER,
            activeforeground=COR_TEXTO_BOTAO,
            relief="flat",
            bd=0,
            highlightthickness=0,
            cursor="hand2",
            width=10,
            height=2,
            command=comando
        )

        botao.bind(
            "<Enter>",
            lambda evento: botao.config(
                bg=COR_BOTAO_PRINCIPAL,
                fg=COR_TEXTO_BOTAO
            )
        )

        botao.bind(
            "<Leave>",
            lambda evento: botao.config(
                bg="#E5E7EB",
                fg=COR_TEXTO
            )
        )

        return botao

    def _atualizar_opcoes_disciplina(self, disciplinas):
        """Atualiza as disciplinas disponíveis no filtro."""

        self.mapa_disciplinas = {
            disciplina.nome: disciplina.id
            for disciplina in disciplinas
        }

        nomes = sorted(
            self.mapa_disciplinas,
            key=str.lower
        )

        self.combo_disciplina["values"] = [OPCAO_TODAS] + nomes

        if self.combo_disciplina.get() not in self.mapa_disciplinas:
            self.combo_disciplina.set(OPCAO_TODAS)

    def _ler_combos(self):
        """Obtém os valores selecionados nos filtros."""

        nome_disciplina = self.combo_disciplina.get()

        return {
            "disciplina_id": self.mapa_disciplinas.get(
                nome_disciplina,
                OPCAO_TODAS
            ),
            "tipo": self.combo_tipo.get(),
            "status": self.combo_status.get(),
            "prioridade": self.combo_prioridade.get()
        }

    def aplicar_filtros(self):
        """Aplica os filtros selecionados."""

        self.filtros_aplicados = self._ler_combos()
        self.atualizar_lista()

    def limpar_filtros(self):
        """Limpa os filtros e exibe todas as tarefas."""

        for combo in (
            self.combo_disciplina,
            self.combo_tipo,
            self.combo_status,
            self.combo_prioridade
        ):
            combo.current(0)

        self.aplicar_filtros()

    # ==========================================================
    # LISTA ROLÁVEL
    # ==========================================================

    def _criar_lista_rolavel(self):

        container = tk.Frame(
            self,
            bg=COR_FUNDO
        )

        # Espaço extra entre os filtros e a primeira linha de cards
        container.pack(
            fill="both",
            expand=True,
            pady=(5, 0)
        )

        self.canvas = tk.Canvas(
            container,
            bg=COR_FUNDO,
            highlightthickness=0
        )

        barra = ttk.Scrollbar(
            container,
            orient="vertical",
            command=self.canvas.yview
        )

        self.canvas.configure(
            yscrollcommand=barra.set
        )

        barra.pack(
            side="right",
            fill="y"
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.lista = tk.Frame(
            self.canvas,
            bg=COR_FUNDO
        )

        # Duas colunas com o mesmo espaço disponível
        self.lista.grid_columnconfigure(
            0,
            weight=1,
            uniform="colunas"
        )

        self.lista.grid_columnconfigure(
            1,
            weight=1,
            uniform="colunas"
        )

        janela_lista = self.canvas.create_window(
            (0, 0),
            window=self.lista,
            anchor="nw"
        )

        self.lista.bind(
            "<Configure>",
            lambda evento: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.bind(
            "<Configure>",
            lambda evento: self.canvas.itemconfigure(
                janela_lista,
                width=evento.width
            )
        )

        self.canvas.bind(
            "<Enter>",
            lambda evento: self._ligar_roda_do_mouse(True)
        )

        self.canvas.bind(
            "<Leave>",
            lambda evento: self._ligar_roda_do_mouse(False)
        )

    def _ligar_roda_do_mouse(self, ligar):

        if ligar:
            self.canvas.bind_all(
                "<MouseWheel>",
                self._rolar
            )

            self.canvas.bind_all(
                "<Button-4>",
                lambda evento: self.canvas.yview_scroll(-1, "units")
            )

            self.canvas.bind_all(
                "<Button-5>",
                lambda evento: self.canvas.yview_scroll(1, "units")
            )

        else:
            for evento in (
                "<MouseWheel>",
                "<Button-4>",
                "<Button-5>"
            ):
                self.canvas.unbind_all(evento)

    def _rolar(self, evento):

        self.canvas.yview_scroll(
            int(-evento.delta / 120),
            "units"
        )

    # ==========================================================
    # CARDS DE TAREFAS
    # ==========================================================

    def atualizar_lista(self):
        """Limpa e monta novamente os cards de tarefas."""

        for widget in self.lista.winfo_children():
            widget.destroy()

        disciplinas, tarefas = verificar_tarefas_atrasadas()

        nomes_disciplinas = {
            disciplina.id: disciplina.nome
            for disciplina in disciplinas
        }

        self._atualizar_opcoes_disciplina(disciplinas)

        visiveis = self._filtrar(tarefas)

        visiveis = sorted(
            visiveis,
            key=lambda tarefa: tarefa.prazo
        )

        if not tarefas:
            self._mostrar_mensagem(MSG_SEM_TAREFAS)

        elif not visiveis:
            self._mostrar_mensagem(MSG_SEM_RESULTADO)

        # Distribui os cards em duas colunas
        for indice, tarefa in enumerate(visiveis):

            nome_disciplina = nomes_disciplinas.get(
                tarefa.disciplina_id,
                "Disciplina não encontrada"
            )

            card = CardTarefa(
                self.lista,
                tarefa,
                nome_disciplina,
                ao_editar=self.editar_tarefa,
                ao_excluir=self.excluir_tarefa,
                ao_concluir=self.concluir_tarefa
            )

            linha = indice // 2
            coluna = indice % 2

            card.grid(
                row=linha,
                column=coluna,
                sticky="nsew",
                padx=8,
                pady=8
            )

        self.canvas.yview_moveto(0)

    def _filtrar(self, tarefas):

        return filtrar_tarefas(
            tarefas,
            **self.filtros_aplicados
        )

    def _mostrar_mensagem(self, texto):

        tk.Label(
            self.lista,
            text=texto,
            bg=COR_FUNDO,
            fg=COR_TEXTO_MENSAGEM,
            font=(FONTE, 11)
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            pady=40
        )

    # ==========================================================
    # AÇÕES DOS CARDS
    # ==========================================================

    def criar_tarefa(self):

        ModalTarefa(
            self,
            ao_salvar=lambda tarefa: self.atualizar_lista()
        )

    def editar_tarefa(self, tarefa):

        ModalTarefa(
            self,
            tarefa=tarefa,
            ao_salvar=lambda tarefa: self.atualizar_lista()
        )

    def excluir_tarefa(self, tarefa):

        print(f"[US17] Excluir: {tarefa.nome}")

    def concluir_tarefa(self, tarefa):

        print(f"[US17] Concluir: {tarefa.nome}")

    def voltar_inicio(self):

        if self.app:
            self.app.mostrar_home()