from datetime import date

from models.disciplina import Disciplina
from models.tarefa import Tarefa
from repositorio import armazenamento

# 1. Monta dados de teste
calculo = Disciplina("Cálculo")
lista = Tarefa("Lista de exercícios", "Exercício", date(2026, 11, 5), calculo.id)

# 2. Salva e carrega de novo
armazenamento.salvar([calculo], [lista])
disciplinas, tarefas = armazenamento.carregar()

# 3. Confere se voltou igual
assert len(disciplinas) == 1
assert disciplinas[0].nome == "Cálculo"
assert len(tarefas) == 1
assert tarefas[0].nome == "Lista de exercícios"
assert tarefas[0].prazo == date(2026, 11, 5)
assert tarefas[0].disciplina_id == calculo.id

print("Tudo certo! Abra o dados/dados.json e confira os acentos.")
