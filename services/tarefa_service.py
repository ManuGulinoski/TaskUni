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


def validar_tipo(tipo):
    """O tipo é obrigatório e precisa ser Prova, Trabalho ou Exercício."""
    if tipo not in TIPOS:
        raise ValueError("Escolha o tipo da tarefa.")

    return tipo


def validar_disciplina(disciplina_id, disciplinas):
    """A tarefa precisa estar ligada a uma disciplina que existe."""
    if not disciplinas:
        raise ValueError(
            "Cadastre uma disciplina antes de criar uma tarefa."
        )

    if disciplina_id not in {d.id for d in disciplinas}:
        raise ValueError("Escolha a disciplina da tarefa.")

    return disciplina_id


def validar_status(status):
    """
    O usuário escolhe só A fazer, Em andamento ou Concluída.
    "Atrasada" é calculada pela data e nunca é salva: se chegar
    aqui (por um dado antigo), volta a ser "A fazer".
    """
    if status == STATUS_ATRASADA:
        return STATUS_A_FAZER

    if status not in STATUS_SELECIONAVEIS:
        raise ValueError("Escolha um status válido.")

    return status


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
    tipo = validar_tipo(tipo)
    status = validar_status(status)

    disciplinas, tarefas = armazenamento.carregar()

    disciplina_id = validar_disciplina(disciplina_id, disciplinas)
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
    """
    Carrega disciplinas e tarefas para a tela.

    "Atrasada" é calculada por tarefa.status_atual() e NÃO é salva.
    Se o JSON tiver "Atrasada" gravado (versões antigas do app), o status
    volta para "A fazer". Assim, ao adiar o prazo, a tarefa deixa de
    aparecer como atrasada.
    """

    disciplinas, tarefas = armazenamento.carregar()

    houve_alteracao = False

    for tarefa in tarefas:

        if tarefa.status == STATUS_ATRASADA:
            tarefa.status = STATUS_A_FAZER
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
    tipo = validar_tipo(tipo)
    status = validar_status(status)

    disciplinas, tarefas = armazenamento.carregar()

    disciplina_id = validar_disciplina(disciplina_id, disciplinas)

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

# US12 - Concluir tarefa
def concluir_tarefa(tarefa_id):
    """Marca a tarefa como concluída e persiste a alteração no JSON."""
    disciplinas, tarefas = armazenamento.carregar()
    tarefa = next((t for t in tarefas if t.id == tarefa_id), None)

    if tarefa is None:
        raise ValueError("Tarefa não encontrada.")

    tarefa.status = STATUS_CONCLUIDA
    armazenamento.salvar(disciplinas, tarefas)
    return tarefa