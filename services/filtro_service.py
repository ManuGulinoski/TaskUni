
from datetime import date, timedelta

from utils.constantes import (
    OPCAO_TODOS, OPCAO_TODAS,
    PRAZO_HOJE, PRAZO_ESTA_SEMANA, PRAZO_SEMANA_QUE_VEM,
)


def _sem_filtro(valor):
    """True quando o critério não deve ser aplicado."""
    return valor is None or valor in (OPCAO_TODOS, OPCAO_TODAS)


def _prazo_combina(data_prazo, opcao, hoje):
    """Confere se a data do prazo está dentro da opção escolhida."""
    segunda = hoje - timedelta(days=hoje.weekday())   # weekday(): segunda=0 ... domingo=6
    domingo = segunda + timedelta(days=6)

    if opcao == PRAZO_HOJE:
        return data_prazo == hoje
    if opcao == PRAZO_ESTA_SEMANA:
        return segunda <= data_prazo <= domingo
    if opcao == PRAZO_SEMANA_QUE_VEM:
        return segunda + timedelta(days=7) <= data_prazo <= domingo + timedelta(days=7)

    raise ValueError(f"Opção de prazo inválida: {opcao}")


def filtrar_tarefas(tarefas, disciplina_id=None, tipo=None, prazo=None,
                    status=None, prioridade=None, hoje=None):
    """
    Devolve só as tarefas que atendem a TODOS os critérios escolhidos.

    tarefas        lista de objetos Tarefa (ex.: armazenamento.carregar()[1])
    disciplina_id  id da disciplina, "Todas" ou None
    tipo           "Prova", "Trabalho", "Exercício", "Todos" ou None
    prazo          "Hoje", "Esta semana", "Semana que vem", "Todos" ou None
    status         "A fazer", "Em andamento", "Concluída", "Atrasada", "Todos" ou None
    prioridade     "Urgente", "Alta", "Média", "Baixa", "Todas" ou None
    hoje           data de referência (padrão: date.today()), para testes

    Status e prioridade são CALCULADOS (status_atual / prioridade da Tarefa),
    porque "Atrasada" e a prioridade dependem da data de hoje e não ficam no JSON.
    """
    if hoje is None:
        hoje = date.today()

    resultado = []
    for tarefa in tarefas:
        if not _sem_filtro(disciplina_id) and tarefa.disciplina_id != disciplina_id:
            continue
        if not _sem_filtro(tipo) and tarefa.tipo != tipo:
            continue
        if not _sem_filtro(prazo) and not _prazo_combina(tarefa.prazo, prazo, hoje):
            continue
        if not _sem_filtro(status) and tarefa.status_atual(hoje) != status:
            continue
        if not _sem_filtro(prioridade) and tarefa.prioridade(hoje) != prioridade:
            continue
        resultado.append(tarefa)

    return resultado
