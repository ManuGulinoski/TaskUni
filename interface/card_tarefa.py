
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

    def __init__(self, parent, tarefa, nome_disciplina,
                 ao_editar, ao_excluir, ao_concluir):

        super().__init__(
            parent,
            bg=COR_CARD,
            highlightbackground=COR_BORDA,
            highlightthickness=1
        )

        self.tarefa = tarefa
        self.icones = criar_icones()

        self.columnconfigure(1, weight=1)

        faixa = tk.Frame(
            self,
            bg=cor_da_faixa(tarefa.cor),
            width=6
        )
        faixa.grid(row=0, column=0, sticky="ns")

        info = tk.Frame(self, bg=COR_CARD)
        info.grid(row=0, column=1, sticky="w", padx=14, pady=10)

        tk.Label(
            info,
            text=tarefa.nome,
            bg=COR_CARD,
            fg=COR_TEXTO,
            font=(FONTE, 12, "bold")
        ).pack(anchor="w")

        prazo = tarefa.prazo.strftime(FORMATO_DATA_TELA)

        detalhes = (
            f"Prazo: {prazo}   ·   Tipo: {tarefa.tipo}   ·   "
            f"Disciplina: {nome_disciplina}"
        )

        tk.Label(
            info,
            text=detalhes,
            bg=COR_CARD,
            fg=COR_TEXTO_SECUNDARIO,
            font=(FONTE, 10)
        ).pack(anchor="w", pady=(2, 0))

        linha_status = tk.Frame(info, bg=COR_CARD)
        linha_status.pack(anchor="w", pady=(2, 0))

        status = status_exibido(tarefa)

        if status == STATUS_ATRASADA:
            cor_status, peso = COR_ATRASADA, "bold"
        elif status == STATUS_CONCLUIDA:
            cor_status, peso = COR_CONCLUIDA, "normal"
        else:
            cor_status, peso = COR_TEXTO, "normal"

        tk.Label(
            linha_status,
            text=f"Status: {status}",
            bg=COR_CARD,
            fg=cor_status,
            font=(FONTE, 10, peso)
        ).pack(side="left")

        prioridade = prioridade_exibida(tarefa)

        tk.Label(
            linha_status,
            text=f"   ·   Prioridade: {prioridade}",
            bg=COR_CARD,
            fg=COR_TEXTO,
            font=(FONTE, 10)
        ).pack(side="left")

        icones = tk.Frame(self, bg=COR_CARD)
        icones.grid(row=0, column=2, padx=10)

        self._botao(
            icones,
            self.icones["editar"],
            "Editar",
            lambda: ao_editar(tarefa)
        ).pack(side="left", padx=6)

        self._botao(
            icones,
            self.icones["excluir"],
            "Excluir",
            lambda: ao_excluir(tarefa)
        ).pack(side="left", padx=6)

        botao_concluir = self._botao(
            icones,
            self.icones["concluir"],
            "Concluir",
            lambda: ao_concluir(tarefa)
        )

        botao_concluir.pack(side="left", padx=6)

        if tarefa.status == STATUS_CONCLUIDA:
            botao_concluir.config(state="disabled")

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