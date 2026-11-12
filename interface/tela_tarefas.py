import tkinter as tk
from tkinter import ttk, messagebox

from interface.card_tarefa import CardTarefa
from interface.modal_tarefa import ModalTarefa

from services.tarefa_service import (
    verificar_tarefas_atrasadas,
    excluir_tarefa as excluir_tarefa_service
)

from services.filtro_service import filtrar_tarefas
from utils.constantes import *


class TelaTarefas(tk.Frame):

    def __init__(self, parent, app=None):

        super().__init__(
            parent,
            bg=COR_FUNDO
        )

        self.app = app
        self._toast_atual = None

        self._criar_topo()
        self._criar_area_filtros()
        self._criar_lista_rolavel()

        self.atualizar_lista()

    # ==========================================================
    # TOPO
    # ==========================================================

    def _criar_topo(self):

        topo = tk.Frame(
            self,
            bg=COR_FUNDO
        )

        topo.pack(fill="x")

        ttk.Button(
            topo,
            text="← Início",
            command=self.voltar_inicio
        ).pack(
            side="left",
            padx=(0, 15)
        )

        tk.Label(
            topo,
            text="Tarefas",
            bg=COR_FUNDO,
            font=(FONTE, 18, "bold")
        ).pack(side="left")

        ttk.Button(
            topo,
            text="+ Criar tarefa",
            command=self.criar_tarefa
        ).pack(side="right")

    # ==========================================================
    # FILTROS
    # ==========================================================

    def _criar_area_filtros(self):

        self.area_filtros = tk.Frame(
            self,
            bg=COR_FUNDO
        )

        self.area_filtros.pack(
            fill="x",
            pady=(10, 6)
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

        ttk.Button(
            self.area_filtros,
            text="Filtrar",
            command=self.aplicar_filtros
        ).grid(
            row=1,
            column=4,
            padx=(4, 4),
            sticky="s"
        )

        ttk.Button(
            self.area_filtros,
            text="Limpar",
            command=self.limpar_filtros
        ).grid(
            row=1,
            column=5,
            sticky="s"
        )

        self.filtros_aplicados = self._ler_combos()

    def _criar_combo(self, titulo, opcoes, coluna):

        tk.Label(
            self.area_filtros,
            text=titulo,
            bg=COR_FUNDO,
            fg="#374151",
            font=(FONTE, 9, "bold")
        ).grid(
            row=0,
            column=coluna,
            sticky="w",
            padx=(0, 10)
        )

        combo = ttk.Combobox(
            self.area_filtros,
            values=opcoes,
            state="readonly",
            width=16
        )

        combo.set(opcoes[0])

        combo.grid(
            row=1,
            column=coluna,
            sticky="w",
            padx=(0, 10)
        )

        return combo

    def _atualizar_opcoes_disciplina(self, disciplinas):

        self.mapa_disciplinas = {
            disciplina.nome: disciplina.id
            for disciplina in disciplinas
        }

        nomes = sorted(
            self.mapa_disciplinas,
            key=str.lower
        )

        self.combo_disciplina["values"] = (
            [OPCAO_TODAS] + nomes
        )

        if self.combo_disciplina.get() not in self.mapa_disciplinas:
            self.combo_disciplina.set(OPCAO_TODAS)

    def _ler_combos(self):

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

        self.filtros_aplicados = self._ler_combos()
        self.atualizar_lista()

    def limpar_filtros(self):

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

        container.pack(
            fill="both",
            expand=True
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
                lambda evento: self.canvas.yview_scroll(
                    -1,
                    "units"
                )
            )

            self.canvas.bind_all(
                "<Button-5>",
                lambda evento: self.canvas.yview_scroll(
                    1,
                    "units"
                )
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
    # LISTA DE CARDS
    # ==========================================================

    def atualizar_lista(self):

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

        for tarefa in visiveis:

            nome = nomes_disciplinas.get(
                tarefa.disciplina_id,
                "Disciplina não encontrada"
            )

            card = CardTarefa(
                self.lista,
                tarefa,
                nome,
                ao_editar=self.editar_tarefa,
                ao_excluir=self.excluir_tarefa,
                ao_concluir=self.concluir_tarefa
            )

            card.pack(
                fill="x",
                pady=4
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
            fg="#6B7280",
            font=(FONTE, 11)
        ).pack(pady=40)

    # ==========================================================
    # US11 - EXCLUIR TAREFA
    # ==========================================================

    def excluir_tarefa(self, tarefa):

        # 1. Solicita confirmação antes de excluir
        confirmar = messagebox.askyesno(
            "Excluir tarefa",
            f"Tem certeza de que deseja excluir a tarefa "
            f'"{tarefa.nome}"?',
            parent=self.winfo_toplevel()
        )

        # 2. Se cancelar, não altera os dados
        if not confirmar:
            return

        try:

            # 3. Chama o serviço responsável pela exclusão
            excluir_tarefa_service(tarefa.id)

            # 4. Atualiza os cards da tela
            self.atualizar_lista()

            # 5. Exibe mensagem de sucesso
            self.exibir_toast(
                "Tarefa excluída com sucesso!",
                sucesso=True
            )

        except Exception as erro:

            print(f"Erro ao excluir tarefa: {erro}")

            self.exibir_toast(
                "Não foi possível excluir a tarefa.",
                sucesso=False
            )

    # ==========================================================
    # TOAST DE SUCESSO E ERRO
    # ==========================================================

    def exibir_toast(self, mensagem, sucesso=True):

        # Remove o toast anterior, se existir
        if (
            self._toast_atual is not None
            and self._toast_atual.winfo_exists()
        ):
            self._toast_atual.destroy()

        cor_fundo = "#16A34A" if sucesso else "#DC2626"

        toast = tk.Label(
            self,
            text=mensagem,
            bg=cor_fundo,
            fg="#FFFFFF",
            font=(FONTE, 10, "bold"),
            padx=18,
            pady=12
        )

        toast.place(
            relx=1.0,
            x=-20,
            y=20,
            anchor="ne"
        )

        self._toast_atual = toast

        # Remove automaticamente depois de 3 segundos
        self.after(
            3000,
            lambda: self._remover_toast(toast)
        )

    def _remover_toast(self, toast):

        if toast.winfo_exists():
            toast.destroy()

        if self._toast_atual == toast:
            self._toast_atual = None

    # ==========================================================
    # OUTRAS AÇÕES
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

    def concluir_tarefa(self, tarefa):

        print(f"[US17] Concluir: {tarefa.nome}")

    def voltar_inicio(self):

        if self.app:
            self.app.mostrar_home()