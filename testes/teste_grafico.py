"""
Testes da US do gráfico por status, com data fixa.
Rodar (da pasta do projeto):  python -m unittest testes.teste_grafico -v
"""
import unittest
from datetime import date

from models.tarefa import Tarefa
from services.grafico_service import contar_por_status
from utils.constantes import STATUS_TODOS

HOJE = date(2026, 11, 4)


class TesteGrafico(unittest.TestCase):

    def test_lista_vazia_tudo_zero(self):
        resultado = contar_por_status([], hoje=HOJE)
        self.assertEqual(resultado, {s: 0 for s in STATUS_TODOS})

    def test_sempre_mostra_todos_os_status_na_ordem(self):
        tarefas = [Tarefa("A", "Prova", date(2026, 11, 10), "d1")]
        resultado = contar_por_status(tarefas, hoje=HOJE)
        self.assertEqual(list(resultado), STATUS_TODOS)

    def test_conta_por_status(self):
        tarefas = [
            Tarefa("A", "Prova", date(2026, 11, 10), "d1", status="A fazer"),
            Tarefa("B", "Prova", date(2026, 11, 10), "d1", status="A fazer"),
            Tarefa("C", "Prova", date(2026, 11, 10), "d1", status="Em andamento"),
            Tarefa("D", "Prova", date(2026, 11, 10), "d1", status="Concluída"),
        ]
        resultado = contar_por_status(tarefas, hoje=HOJE)
        self.assertEqual(resultado["A fazer"], 2)
        self.assertEqual(resultado["Em andamento"], 1)
        self.assertEqual(resultado["Concluída"], 1)
        self.assertEqual(resultado["Atrasada"], 0)

    def test_prazo_vencido_conta_como_atrasada(self):
        tarefas = [Tarefa("A", "Prova", date(2026, 11, 1), "d1", status="A fazer")]
        resultado = contar_por_status(tarefas, hoje=HOJE)
        self.assertEqual(resultado["Atrasada"], 1)
        self.assertEqual(resultado["A fazer"], 0)

    def test_concluida_vencida_continua_concluida(self):
        tarefas = [Tarefa("A", "Prova", date(2026, 11, 1), "d1", status="Concluída")]
        resultado = contar_por_status(tarefas, hoje=HOJE)
        self.assertEqual(resultado["Concluída"], 1)
        self.assertEqual(resultado["Atrasada"], 0)

    def test_total_bate_com_quantidade_de_tarefas(self):
        tarefas = [
            Tarefa("A", "Prova", date(2026, 11, 1), "d1"),
            Tarefa("B", "Prova", date(2026, 11, 20), "d1", status="Em andamento"),
            Tarefa("C", "Prova", date(2026, 11, 20), "d1", status="Concluída"),
        ]
        resultado = contar_por_status(tarefas, hoje=HOJE)
        self.assertEqual(sum(resultado.values()), len(tarefas))

    def test_atualiza_apos_alteracao(self):
        tarefa = Tarefa("A", "Prova", date(2026, 11, 10), "d1", status="A fazer")
        antes = contar_por_status([tarefa], hoje=HOJE)
        tarefa.status = "Concluída"
        depois = contar_por_status([tarefa], hoje=HOJE)
        self.assertEqual(antes["A fazer"], 1)
        self.assertEqual(depois["A fazer"], 0)
        self.assertEqual(depois["Concluída"], 1)


if __name__ == "__main__":
    unittest.main()
