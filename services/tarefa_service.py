from datetime import datetime
from models.tarefa import Tarefa
from repositorio import armazenamento
from utils.constantes import *

def cadastrar_tarefa(nome, tipo, disciplina_id, prazo, descricao="", status="A fazer", cor="Branco"):

    nome = nome.strip()
    descricao = descricao.strip()

    if not nome:
        raise ValueError("Informe o nome da tarefa.")

    if len(nome) > 50:
        raise ValueError("O nome deve ter no máximo 50 caracteres.")

    if tipo not in TIPOS:
        raise ValueError("Selecione um tipo válido.")

    disciplinas, tarefas = armazenamento.carregar()

    disciplina_existe = any(
        disciplina.id == disciplina_id
        for disciplina in disciplinas
    )

    try:
        prazo = datetime.strptime(prazo, "%d/%m/%Y").date()
    except ValueError:
        raise ValueError("Informe uma data válida no formato DD/MM/AAAA.")

    if len(descricao) > 100:
        raise ValueError("A descrição deve ter no máximo 100 caracteres.")

    if not cor:
        cor = "Branco"

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