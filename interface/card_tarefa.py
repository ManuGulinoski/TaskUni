import tkinter as tk
from utils.constantes import *
from utils.icones import criar_icones
from interface.componentes import Pilula


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
            highlightcolor=COR_BORDA,
            highlightthickness=1
        )

        self.tarefa = tarefa
        self.icones = criar_icones()

        self.columnconfigure(1, weight=1)

        # Faixa colorida à esquerda (cor escolhida na tarefa)
        faixa = tk.Frame(
            self,
            bg=cor_da_faixa(tarefa.cor),
            width=8
        )
        faixa.grid(row=0, column=0, sticky="ns")

        info = tk.Frame(self, bg=COR_CARD)
        info.grid(row=0, column=1, sticky="w", padx=18, pady=14)

        # Nome da tarefa
        tk.Label(
            info,
            text=tarefa.nome,
            bg=COR_CARD,
            fg=COR_TEXTO,
            font=(FONTE, 12, "bold")
        ).pack(anchor="w")

        prazo = tarefa.prazo.strftime(FORMATO_DATA_TELA)

        detalhes = (
            f"Prazo: {prazo}   ·   {tarefa.tipo}   ·   {nome_disciplina}"
        )

        tk.Label(
            info,
            text=detalhes,
            bg=COR_CARD,
            fg=COR_TEXTO_SECUNDARIO,
            font=(FONTE, 10)
        ).pack(anchor="w", pady=(2, 8))

        # Pílulas de status e prioridade
        linha_status = tk.Frame(info, bg=COR_CARD)
        linha_status.pack(anchor="w")

        status = status_exibido(tarefa)
        fundo, texto = CORES_PILULA_STATUS.get(status, COR_PILULA_PADRAO)

        Pilula(linha_status, status, fundo, texto).pack(side="left")

        prioridade = prioridade_exibida(tarefa)

        Pilula(
            linha_status,
            f"Prioridade: {prioridade}"
        ).pack(side="left", padx=(8, 0))

        # Ícones de ação
        icones = tk.Frame(self, bg=COR_CARD)
        icones.grid(row=0, column=2, padx=14)

        self._botao(
            icones,
            self.icones["editar"],
            "Editar",
            lambda: ao_editar(tarefa)
        ).pack(side="left", padx=4)

        self._botao(
            icones,
            self.icones["excluir"],
            "Excluir",
            lambda: ao_excluir(tarefa)
        ).pack(side="left", padx=4)

        botao_concluir = self._botao(
            icones,
            self.icones["concluir"],
            "Concluir",
            lambda: ao_concluir(tarefa)
        )

        botao_concluir.pack(side="left", padx=4)

        if tarefa.status == STATUS_CONCLUIDA:
            botao_concluir.config(state="disabled")

    def _botao(self, parent, icone, dica, comando):

        botao = tk.Button(
            parent,
            image=icone,
            command=comando,
            relief="flat",
            bd=0,
            width=32,
            height=32,
            bg=COR_CARD,
            activebackground=COR_SUAVE,
            highlightthickness=0,
            cursor="hand2",
            name=dica.lower()
        )

        # Fundo lilás clarinho ao passar o mouse
        botao.bind("<Enter>", lambda e: botao.config(bg=COR_SUAVE)
                   if str(botao["state"]) != "disabled" else None)
        botao.bind("<Leave>", lambda e: botao.config(bg=COR_CARD))

        return botao