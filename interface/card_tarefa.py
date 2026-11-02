"""
Card de uma tarefa (US08).

Responsável: Pessoa 3

O card só DESENHA uma tarefa. Ele não lê o JSON e não decide o que os
ícones fazem: recebe três funções (ao_editar, ao_excluir, ao_concluir) e
apenas as chama quando o ícone é clicado. Quem decide a ação é a tela
(a ligação de verdade é feita na US17).

Layout do card:
    ┌──┬──────────────────────────────────────────────┬──────────┐
    │  │ Nome da tarefa                               │ ✎  🗑  ✓ │
    │▌ │ Prazo: 05/11/2026 · Tipo: Prova · Cálculo    │          │
    │  │ Status: Atrasada · Prioridade: Alta          │          │
    └──┴──────────────────────────────────────────────┴──────────┘
     faixa com a cor da tarefa
"""
import tkinter as tk

from utils.constantes import (
    FORMATO_DATA_TELA, STATUS_CONCLUIDA, STATUS_ATRASADA, CORES_TAREFA,
)

# ---------------------------------------------------------------------------
# Aparência
# ---------------------------------------------------------------------------
FONTE = "Segoe UI"
COR_CARD = "white"
COR_BORDA = "#E5E7EB"
COR_TEXTO = "#111827"
COR_TEXTO_SECUNDARIO = "#6B7280"
COR_NEUTRA = "#D1D5DB"          # faixa da cor padrão ("Branco")
COR_ATRASADA = "#DC2626"        # destaque da tarefa atrasada
COR_CONCLUIDA = "#16A34A"

# As cores vêm de CORES_TAREFA (utils/constantes.py), as mesmas do modal de tarefa.
# O modal grava o NOME da cor ("Verde"); a cor padrão do modal é "Branco".
CORES_PADRAO = ("Branco", "Padrão")

# Ícones. Se a lixeira aparecer como um quadrado no Windows, troque por "✕".
ICONE_EDITAR = "✎"
ICONE_EXCLUIR = "🗑"
ICONE_CONCLUIR = "✓"


# ---------------------------------------------------------------------------
# Funções de apoio
# ---------------------------------------------------------------------------
def cor_da_faixa(cor):
    """Converte a cor gravada na tarefa para o código usado na faixa.
    Sem cor ou cor padrão ("Branco") -> cinza neutro da interface
    (uma faixa branca não apareceria no card branco)."""
    if not cor or cor in CORES_PADRAO:
        return COR_NEUTRA
    if cor.startswith("#"):          # já é um código de cor
        return cor
    return CORES_TAREFA.get(cor, COR_NEUTRA)   # nome -> código


def status_exibido(tarefa):
    """Status que aparece no card: "Atrasada" é calculado pela US05.
    Enquanto a US05 (Pessoa 1) não estiver pronta, mostra o status gravado."""
    try:
        return tarefa.status_atual()
    except NotImplementedError:
        return tarefa.status


def prioridade_exibida(tarefa):
    """Prioridade calculada pela US04, ou None quando não houver
    (tarefa concluída ou atrasada, ou US04 ainda não pronta)."""
    try:
        return tarefa.prioridade()
    except NotImplementedError:
        return None


# ---------------------------------------------------------------------------
# O card
# ---------------------------------------------------------------------------
class CardTarefa(tk.Frame):
    def __init__(self, parent, tarefa, nome_disciplina,
                 ao_editar, ao_excluir, ao_concluir):
        # highlightthickness desenha a borda fina em volta do card
        super().__init__(parent, bg=COR_CARD,
                         highlightbackground=COR_BORDA, highlightthickness=1)
        self.tarefa = tarefa

        # Coluna 1 (conteúdo) estica; colunas 0 (faixa) e 2 (ícones) não
        self.columnconfigure(1, weight=1)

        # ---------- Faixa colorida à esquerda ----------
        faixa = tk.Frame(self, bg=cor_da_faixa(tarefa.cor), width=6)
        faixa.grid(row=0, column=0, sticky="ns")

        # ---------- Informações ----------
        info = tk.Frame(self, bg=COR_CARD)
        info.grid(row=0, column=1, sticky="w", padx=14, pady=10)

        tk.Label(info, text=tarefa.nome, bg=COR_CARD, fg=COR_TEXTO,
                 font=(FONTE, 12, "bold")).pack(anchor="w")

        prazo = tarefa.prazo.strftime(FORMATO_DATA_TELA)   # DD/MM/AAAA
        detalhes = f"Prazo: {prazo}   ·   Tipo: {tarefa.tipo}   ·   Disciplina: {nome_disciplina}"
        tk.Label(info, text=detalhes, bg=COR_CARD, fg=COR_TEXTO_SECUNDARIO,
                 font=(FONTE, 10)).pack(anchor="w", pady=(2, 0))

        # Linha de status + prioridade (cada parte num Label, para ter cor própria)
        linha_status = tk.Frame(info, bg=COR_CARD)
        linha_status.pack(anchor="w", pady=(2, 0))

        status = status_exibido(tarefa)
        if status == STATUS_ATRASADA:
            cor_status, peso = COR_ATRASADA, "bold"      # destaque visual
        elif status == STATUS_CONCLUIDA:
            cor_status, peso = COR_CONCLUIDA, "normal"
        else:
            cor_status, peso = COR_TEXTO, "normal"
        tk.Label(linha_status, text=f"Status: {status}", bg=COR_CARD,
                 fg=cor_status, font=(FONTE, 10, peso)).pack(side="left")

        prioridade = prioridade_exibida(tarefa)
        if prioridade:   # só aparece "quando houver"
            tk.Label(linha_status, text=f"   ·   Prioridade: {prioridade}",
                     bg=COR_CARD, fg=COR_TEXTO, font=(FONTE, 10)).pack(side="left")

        # A descrição NÃO aparece no card (ela é vista no modal de edição).

        # ---------- Ícones de ação ----------
        icones = tk.Frame(self, bg=COR_CARD)
        icones.grid(row=0, column=2, padx=10)

        # lambda: o card só "avisa" a tela qual tarefa foi clicada
        self._botao(icones, ICONE_EDITAR, "Editar",
                    lambda: ao_editar(tarefa)).pack(side="left", padx=2)
        self._botao(icones, ICONE_EXCLUIR, "Excluir",
                    lambda: ao_excluir(tarefa)).pack(side="left", padx=2)

        botao_concluir = self._botao(icones, ICONE_CONCLUIR, "Concluir",
                                     lambda: ao_concluir(tarefa))
        botao_concluir.pack(side="left", padx=2)
        # Tarefa já concluída: ícone de concluir desabilitado
        if tarefa.status == STATUS_CONCLUIDA:
            botao_concluir.config(state="disabled")

    def _botao(self, parent, icone, dica, comando):
        """Cria um botão de ícone sem borda, com cursor de mãozinha."""
        return tk.Button(parent, text=icone, command=comando,
                         font=(FONTE, 13), width=2, relief="flat", bd=0,
                         bg=COR_CARD, activebackground="#F3F4F6",
                         fg=COR_TEXTO, disabledforeground=COR_NEUTRA, highlightthickness=0,
                         cursor="hand2", name=dica.lower())
