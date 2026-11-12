from repositorio.armazenamento import carregar
from utils.constantes import STATUS_CONCLUIDA, STATUS_ATRASADA


def obter_estatisticas():
    disciplinas, tarefas = carregar()

    resultado = {
        "total": len(tarefas),
        "concluidas": 0,
        "pendentes": 0,
        "atrasadas": 0,
    }

    for tarefa in tarefas:
        status = tarefa.status_atual()

        if status == STATUS_CONCLUIDA:
            resultado["concluidas"] += 1

        elif status == STATUS_ATRASADA:
            resultado["atrasadas"] += 1

        else:
            resultado["pendentes"] += 1

    return resultado