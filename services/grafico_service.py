from datetime import date

from utils.constantes import STATUS_TODOS, TIPOS


def contar_por_status(tarefas, hoje=None):
    """
    Conta quantas tarefas existem em cada status (US do gráfico).

    tarefas  lista de objetos Tarefa (ex.: armazenamento.carregar()[1])
    hoje     data de referência (padrão: date.today()), para testes

    Retorna um dicionário com TODOS os status, na ordem de STATUS_TODOS,
    mesmo os que têm 0 tarefas. Ex.:
        {"A fazer": 3, "Em andamento": 1, "Concluída": 0, "Atrasada": 2}

    Usa status_atual(), porque "Atrasada" é calculada pela data de hoje.
    Lista vazia -> todos os status com 0.
    """
    if hoje is None:
        hoje = date.today()

    contagem = {status: 0 for status in STATUS_TODOS}

    for tarefa in tarefas:
        status = tarefa.status_atual(hoje)
        # Um status desconhecido no JSON também entra, para o total bater
        contagem[status] = contagem.get(status, 0) + 1

    return contagem


def contar_por_tipo(tarefas):
    """
    Conta quantas tarefas existem de cada tipo (US do gráfico por tipo).

    Retorna um dicionário com TODOS os tipos, na ordem de TIPOS,
    mesmo os que têm 0 tarefas. Ex.:
        {"Prova": 2, "Trabalho": 1, "Exercício": 0}

    Lista vazia -> todos os tipos com 0.
    """
    contagem = {tipo: 0 for tipo in TIPOS}

    for tarefa in tarefas:
        # Um tipo desconhecido no JSON também entra, para o total bater
        contagem[tarefa.tipo] = contagem.get(tarefa.tipo, 0) + 1

    return contagem