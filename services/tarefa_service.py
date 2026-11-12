from datetime import datetime, date

from models.tarefa import Tarefa
from repositorio import armazenamento
from utils.constantes import *


def validar_nome(nome):
    nome = nome.strip()

    if not nome:
        raise ValueError("Informe o nome da tarefa.")

    if len(nome) > MAX_NOME_TAREFA:
        raise ValueError(
            f"O nome deve ter no máximo {MAX_NOME_TAREFA} caracteres."
        )

    return nome


def validar_descricao(descricao):
    descricao = descricao.strip()

    if len(descricao) > MAX_DESCRICAO_TAREFA:
        raise ValueError(
            f"A descrição deve ter no máximo {MAX_DESCRICAO_TAREFA} caracteres."
        )

    return descricao


def cor_padrao(cor):
    if not cor:
        cor = "Branco"

    return cor


def validar_prazo(prazo):
    try:
        prazo = datetime.strptime(prazo, "%d/%m/%Y").date()

    except ValueError:
        raise ValueError(
            "Informe uma data válida no formato DD/MM/AAAA."
        )

    if prazo < date.today():
        raise ValueError(
            "O prazo não pode ser uma data passada."
        )

    return prazo


def cadastrar_tarefa(
    nome,
    tipo,
    disciplina_id,
    prazo,
    descricao="",
    status="A fazer",
    cor="Branco"
):

    nome = validar_nome(nome)
    descricao = validar_descricao(descricao)

    disciplinas, tarefas = armazenamento.carregar()

    prazo = validar_prazo(prazo)
    cor = cor_padrao(cor)

    nova_tarefa = Tarefa(
        nome,
        tipo,
        prazo,
        disciplina_id,
        status,
        descricao,
        cor
    )

    tarefas.append(nova_tarefa)

    armazenamento.salvar(disciplinas, tarefas)

    return nova_tarefa


def verificar_tarefas_atrasadas():

    disciplinas, tarefas = armazenamento.carregar()

    hoje = date.today()
    houve_alteracao = False

    for tarefa in tarefas:

        if (
            tarefa.prazo < hoje
            and tarefa.status != STATUS_CONCLUIDA
            and tarefa.status != STATUS_ATRASADA
        ):
            tarefa.status = STATUS_ATRASADA
            houve_alteracao = True

    if houve_alteracao:
        armazenamento.salvar(disciplinas, tarefas)

    return disciplinas, tarefas


def editar_tarefa(
    tarefa_id,
    nome,
    tipo,
    disciplina_id,
    prazo,
    descricao="",
    status="A fazer",
    cor="Branco"
):

    nome = validar_nome(nome)
    descricao = validar_descricao(descricao)

    disciplinas, tarefas = armazenamento.carregar()

    tarefa = next(
        (t for t in tarefas if t.id == tarefa_id),
        None
    )

    if tarefa is None:
        raise ValueError("Tarefa não encontrada.")

    try:
        novo_prazo = datetime.strptime(
            prazo,
            "%d/%m/%Y"
        ).date()

    except ValueError:
        raise ValueError(
            "Informe uma data válida no formato DD/MM/AAAA."
        )

    if novo_prazo < date.today() and novo_prazo != tarefa.prazo:
        raise ValueError(
            "O prazo não pode ser uma data passada."
        )

    cor = cor_padrao(cor)

    tarefa.nome = nome
    tarefa.tipo = tipo
    tarefa.disciplina_id = disciplina_id
    tarefa.prazo = novo_prazo
    tarefa.descricao = descricao
    tarefa.status = status
    tarefa.cor = cor

    armazenamento.salvar(disciplinas, tarefas)

    return tarefa


# ==========================================================
# US11 - EXCLUIR TAREFA
# ==========================================================

def excluir_tarefa(tarefa_id):
    """
    Exclui uma tarefa pelo seu ID e salva a lista atualizada no JSON.

    Retorna a tarefa excluída.
    """

    disciplinas, tarefas = armazenamento.carregar()

    tarefa_encontrada = next(
        (
            tarefa
            for tarefa in tarefas
            if tarefa.id == tarefa_id
        ),
        None
    )

    if tarefa_encontrada is None:
        raise ValueError("A tarefa não foi encontrada.")

    tarefas.remove(tarefa_encontrada)

    armazenamento.salvar(
        disciplinas,
        tarefas
    )

    return tarefa_encontrada