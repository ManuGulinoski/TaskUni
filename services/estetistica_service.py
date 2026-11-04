#dados fictícios apenas para exemplificar
tarefas = [
    {"nome": "Estudar Matemática", "status": "concluida"},
    {"nome": "Fazer trabalho", "status": "pendente"},
    {"nome": "Ler capítulo", "status": "concluida"},
    {"nome": "Revisar conteúdo", "status": "pendente"},
    {"nome": "Entregar atividade", "status": "atrasada"}
]


def obter_estatisticas():
    total = len(tarefas)

    concluidas = 0
    pendentes = 0
    atrasadas = 0

    for tarefa in tarefas:
        if tarefa["status"] == "concluida":
            concluidas += 1

        elif tarefa["status"] == "pendente":
            pendentes += 1

        elif tarefa["status"] == "atrasada":
            atrasadas += 1

    return {
        "total": total,
        "concluidas": concluidas,
        "pendentes": pendentes,
        "atrasadas": atrasadas,
    }