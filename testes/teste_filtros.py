"""
Testes da US09 com data fixa.
Rodar (da pasta do projeto):  python -m unittest testes.teste_filtros -v

Data de referência: quarta-feira, 04/11/2026
  Esta semana     = 02/11 (seg) a 08/11 (dom)
  Semana que vem  = 09/11 (seg) a 15/11 (dom)
"""
import unittest
from datetime import date

from models.tarefa import Tarefa
from servicos.filtro_service import filtrar_tarefas

HOJE = date(2026, 11, 4)


def criar_tarefas():
    return [
        Tarefa("Prova hoje", "Prova", date(2026, 11, 4), "d1", id="t1"),
        Tarefa("Trabalho segunda", "Trabalho", date(2026, 11, 2), "d2", id="t2"),
        Tarefa("Lista domingo", "Exercício", date(2026, 11, 8), "d1", id="t3"),
        Tarefa("Prova semana que vem", "Prova", date(2026, 11, 9), "d2", id="t4"),
        Tarefa("Trabalho domingo que vem", "Trabalho", date(2026, 11, 15), "d1", id="t5"),
        Tarefa("Lista daqui a 2 semanas", "Exercício", date(2026, 11, 16), "d2", id="t6"),
        Tarefa("Prova semana passada", "Prova", date(2026, 11, 1), "d1", id="t7"),
    ]


def ids(lista):
    return sorted(t.id for t in lista)


class TesteFiltros(unittest.TestCase):

    def setUp(self):
        self.tarefas = criar_tarefas()

    def test_sem_filtro_devolve_todas(self):
        resultado = filtrar_tarefas(self.tarefas, hoje=HOJE)
        self.assertEqual(len(resultado), 7)

    def test_todas_e_todos_nao_filtram(self):
        resultado = filtrar_tarefas(self.tarefas, disciplina_id="Todas",
                                    tipo="Todos", prazo="Todos", hoje=HOJE)
        self.assertEqual(len(resultado), 7)

    def test_nao_altera_lista_original(self):
        filtrar_tarefas(self.tarefas, tipo="Prova", hoje=HOJE)
        self.assertEqual(len(self.tarefas), 7)

    def test_disciplina(self):
        resultado = filtrar_tarefas(self.tarefas, disciplina_id="d1", hoje=HOJE)
        self.assertEqual(ids(resultado), ["t1", "t3", "t5", "t7"])

    def test_tipo(self):
        resultado = filtrar_tarefas(self.tarefas, tipo="Prova", hoje=HOJE)
        self.assertEqual(ids(resultado), ["t1", "t4", "t7"])

    def test_prazo_hoje(self):
        resultado = filtrar_tarefas(self.tarefas, prazo="Hoje", hoje=HOJE)
        self.assertEqual(ids(resultado), ["t1"])

    def test_prazo_esta_semana(self):
        resultado = filtrar_tarefas(self.tarefas, prazo="Esta semana", hoje=HOJE)
        self.assertEqual(ids(resultado), ["t1", "t2", "t3"])

    def test_prazo_semana_que_vem(self):
        resultado = filtrar_tarefas(self.tarefas, prazo="Semana que vem", hoje=HOJE)
        self.assertEqual(ids(resultado), ["t4", "t5"])

    def test_esta_semana_num_domingo(self):
        domingo = date(2026, 11, 8)
        resultado = filtrar_tarefas(self.tarefas, prazo="Esta semana", hoje=domingo)
        self.assertEqual(ids(resultado), ["t1", "t2", "t3"])

    def test_criterios_combinados(self):
        resultado = filtrar_tarefas(self.tarefas, disciplina_id="d1",
                                    prazo="Esta semana", hoje=HOJE)
        self.assertEqual(ids(resultado), ["t1", "t3"])

    def test_combinacao_sem_resultado(self):
        resultado = filtrar_tarefas(self.tarefas, tipo="Exercício",
                                    prazo="Hoje", hoje=HOJE)
        self.assertEqual(resultado, [])


if __name__ == "__main__":
    unittest.main()
