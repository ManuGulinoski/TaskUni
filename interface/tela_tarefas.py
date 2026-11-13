import tkinter as tk
from tkinter import ttk

from interface.card_tarefa import CardTarefa
from interface.modal_tarefa import ModalTarefa
from interface.modal_confirmacao import ModalConfirmacao
from interface.componentes import BotaoArredondado, exibir_toast
from services.tarefa_service import (
    verificar_tarefas_atrasadas,
    excluir_tarefa as remover_tarefa
)
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

        BotaoArredondado(
            topo,
            "← Início",
            self.voltar_inicio,
            tipo="secundario"
        ).pack(side="left", padx=(0, 16))

        tk.Label(
            topo,
            text="Minhas tarefas ✿",
            bg=COR_FUNDO,
            fg=COR_TEXTO,
            font=FONTE_TITULO
        ).pack(side="left")

        BotaoArredondado(
            topo,
            "+ Criar tarefa",
            self.criar_tarefa,
            altura=40
        ).pack(side="right", padx=5)

    # ==========================================================
    # FILTROS
    # ==========================================================

    def _criar_area_filtros(self):

        # Fundo branco envolvendo todos os filtros
        self.area_filtros = tk.Frame(
            self,
            bg=COR_SUPERFICIE,
            highlightthickness=1,
            highlightbackground=COR_BORDA,
            highlightcolor=COR_BORDA,
            padx=18,
            pady=14
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
            self.aplicar_filtros,
            tipo="suave"
        )

        botao_filtrar.grid(
            row=1,
            column=4,
            padx=(8, 6),
            sticky="s"
        )

        botao_limpar = self._criar_botao_filtro(
            "Limpar",
            self.limpar_filtros,
            tipo="secundario"
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
            bg=COR_SUPERFICIE,
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
            width=12,
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

    def _criar_botao_filtro(self, texto, comando, tipo="suave"):
        """Cria os botões arredondados de filtro (Filtrar e Limpar)."""

        return BotaoArredondado(
            self.area_filtros,
            texto,
            comando,
            tipo=tipo,
            altura=34,
            padx=22
        )

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
            font=(FONTE, 12),
            justify="center"
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            pady=60
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
        """US11 - Pede confirmação antes de excluir a tarefa."""

        ModalConfirmacao(
            self,
            titulo="Excluir tarefa",
            mensagem=(
                f"Tem certeza que deseja excluir a tarefa \"{tarefa.nome}\"?\n"
                "Essa ação não pode ser desfeita."
            ),
            texto_confirmar="Excluir",
            ao_confirmar=lambda: self._confirmar_exclusao(tarefa)
        )

    def _confirmar_exclusao(self, tarefa):
        """Remove a tarefa do JSON e atualiza as telas."""

        try:
            remover_tarefa(tarefa.id)

        except ValueError as erro:
            # Ex.: a tarefa já tinha sido apagada
            self.exibir_toast(str(erro), "erro")
            self.atualizar_lista()
            return

        # Atualiza lista, cards da Home e gráficos de uma vez
        if self.app:
            self.app.atualizar_telas()
        else:
            self.atualizar_lista()

        self.exibir_toast(
            f"Tarefa \"{tarefa.nome}\" excluída com sucesso!",
            "sucesso"
        )

    def exibir_toast(self, mensagem, tipo):
        """Notificação no canto superior direito (some em 3 segundos)."""

        exibir_toast(self, mensagem, tipo)

    def concluir_tarefa(self, tarefa):

        print(f"[US17] Concluir: {tarefa.nome}")

    def voltar_inicio(self):

        if self.app:
            self.app.mostrar_home()