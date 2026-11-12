import tkinter as tk

from utils.constantes import *
from utils.icones import criar_icones


def cor_da_faixa(cor):

    if not cor or cor in CORES_PADRAO:
        return COR_NEUTRA

    return CORES_TAREFA.get(cor, COR_NEUTRA)


def status_exibido(tarefa):

    try:
        return tarefa.status_atual()

    except NotImplementedError:
        return tarefa.status


def prioridade_exibida(tarefa):
    return tarefa.prioridade()


class CardTarefa(tk.Frame):

    def __init__(
        self,
        parent,
        tarefa,
        nome_disciplina,
        ao_editar,
        ao_excluir,
        ao_concluir
    ):

        super().__init__(
            parent,
            bg=COR_CARD,
            highlightbackground=COR_BORDA,
            highlightthickness=1
        )

        self.tarefa = tarefa
        self.icones = criar_icones()

        # Organização das colunas internas
        self.columnconfigure(1, weight=1)

        # Faixa colorida do card
        faixa = tk.Frame(
            self,
            bg=cor_da_faixa(tarefa.cor),
            width=5
        )

        faixa.grid(
            row=0,
            column=0,
            sticky="ns"
        )

        # Área das informações
        info = tk.Frame(
            self,
            bg=COR_CARD
        )

        info.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(10, 5),
            pady=10
        )

        info.columnconfigure(0, weight=1)

        # Nome da tarefa
        self.label_nome = tk.Label(
            info,
            text=tarefa.nome,
            bg=COR_CARD,
            fg=COR_TEXTO,
            font=(FONTE, 11, "bold"),
            justify="left",
            anchor="w"
        )

        self.label_nome.pack(
            anchor="w",
            fill="x"
        )

        # Prazo, tipo e disciplina
        prazo = tarefa.prazo.strftime(FORMATO_DATA_TELA)

        detalhes = (
            f"Prazo: {prazo}\n"
            f"Tipo: {tarefa.tipo}\n"
            f"Disciplina: {nome_disciplina}"
        )

        self.label_detalhes = tk.Label(
            info,
            text=detalhes,
            bg=COR_CARD,
            fg=COR_TEXTO_SECUNDARIO,
            font=(FONTE, 9),
            justify="left",
            anchor="w"
        )

        self.label_detalhes.pack(
            anchor="w",
            fill="x",
            pady=(4, 4)
        )

        # Status e prioridade
        linha_status = tk.Frame(
            info,
            bg=COR_CARD
        )

        linha_status.pack(
            anchor="w",
            fill="x"
        )

        status = status_exibido(tarefa)

        if status == STATUS_ATRASADA:
            cor_status = COR_ATRASADA
            peso = "bold"

        elif status == STATUS_CONCLUIDA:
            cor_status = COR_CONCLUIDA
            peso = "normal"

        else:
            cor_status = COR_TEXTO
            peso = "normal"

        tk.Label(
            linha_status,
            text=f"Status: {status}",
            bg=COR_CARD,
            fg=cor_status,
            font=(FONTE, 9, peso)
        ).pack(
            side="left"
        )

        prioridade = prioridade_exibida(tarefa)

        tk.Label(
            linha_status,
            text=f"  ·  Prioridade: {prioridade}",
            bg=COR_CARD,
            fg=COR_TEXTO,
            font=(FONTE, 9)
        ).pack(
            side="left"
        )

        # Botões de ação
        icones = tk.Frame(
            self,
            bg=COR_CARD
        )

        icones.grid(
            row=0,
            column=2,
            padx=(3, 8),
            pady=10,
            sticky="e"
        )

        self._botao(
            icones,
            self.icones["editar"],
            "Editar",
            lambda: ao_editar(tarefa)
        ).pack(
            pady=4
        )

        self._botao(
            icones,
            self.icones["excluir"],
            "Excluir",
            lambda: ao_excluir(tarefa)
        ).pack(
            pady=4
        )

        botao_concluir = self._botao(
            icones,
            self.icones["concluir"],
            "Concluir",
            lambda: ao_concluir(tarefa)
        )

        botao_concluir.pack(
            pady=4
        )

        if tarefa.status == STATUS_CONCLUIDA:
            botao_concluir.config(
                state="disabled"
            )

    def _botao(self, parent, icone, dica, comando):

        return tk.Button(
            parent,
            image=icone,
            command=comando,
            relief="flat",
            bd=0,
            bg=COR_CARD,
            activebackground="#F3F4F6",
            disabledforeground=COR_NEUTRA,
            highlightthickness=0,
            cursor="hand2",
            name=dica.lower()
        )
