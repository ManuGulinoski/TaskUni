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
from services.filtro_service import filtrar_tarefas

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

    # ---------- Disciplina + tipo juntos (US de disciplina/tipo) ----------
    def test_disciplina_e_tipo_juntos(self):
        resultado = filtrar_tarefas(self.tarefas, disciplina_id="d1",
                                    tipo="Prova", hoje=HOJE)
        self.assertEqual(ids(resultado), ["t1", "t7"])


class TesteFiltrosStatusPrioridade(unittest.TestCase):
    """
    US de status e prioridade. Data de referência: 04/11/2026.
      s1  prazo 01/11, A fazer       -> Atrasada  / Urgente
      s2  prazo 04/11, Em andamento  -> Em andamento / Urgente (entrega hoje)
      s3  prazo 06/11, A fazer       -> A fazer   / Alta  (2 dias)
      s4  prazo 10/11, Em andamento  -> Em andamento / Média (6 dias)
      s5  prazo 20/11, A fazer       -> A fazer   / Baixa (16 dias)
      s6  prazo 01/11, Concluída     -> Concluída / Urgente (concluída não vira Atrasada,
                                         mas a prioridade segue o prazo)
    """

    def setUp(self):
        self.tarefas = [
            Tarefa("s1", "Prova", date(2026, 11, 1), "d1", status="A fazer", id="s1"),
            Tarefa("s2", "Trabalho", date(2026, 11, 4), "d1", status="Em andamento", id="s2"),
            Tarefa("s3", "Exercício", date(2026, 11, 6), "d2", status="A fazer", id="s3"),
            Tarefa("s4", "Prova", date(2026, 11, 10), "d2", status="Em andamento", id="s4"),
            Tarefa("s5", "Trabalho", date(2026, 11, 20), "d1", status="A fazer", id="s5"),
            Tarefa("s6", "Exercício", date(2026, 11, 1), "d2", status="Concluída", id="s6"),
        ]

    def filtrar(self, **criterios):
        return ids(filtrar_tarefas(self.tarefas, hoje=HOJE, **criterios))

    # Status
    def test_status_a_fazer(self):
        self.assertEqual(self.filtrar(status="A fazer"), ["s3", "s5"])   # s1 virou Atrasada

    def test_status_em_andamento(self):
        self.assertEqual(self.filtrar(status="Em andamento"), ["s2", "s4"])

    def test_status_concluida(self):
        self.assertEqual(self.filtrar(status="Concluída"), ["s6"])

    def test_status_atrasada(self):
        self.assertEqual(self.filtrar(status="Atrasada"), ["s1"])        # s6 é concluída

    # Prioridade
    def test_prioridade_urgente(self):
        self.assertEqual(self.filtrar(prioridade="Urgente"), ["s1", "s2", "s6"])

    def test_prioridade_alta(self):
        self.assertEqual(self.filtrar(prioridade="Alta"), ["s3"])

    def test_prioridade_media(self):
        self.assertEqual(self.filtrar(prioridade="Média"), ["s4"])

    def test_prioridade_baixa(self):
        self.assertEqual(self.filtrar(prioridade="Baixa"), ["s5"])

    # Em conjunto
    def test_status_e_prioridade_juntos(self):
        self.assertEqual(self.filtrar(status="Em andamento", prioridade="Urgente"), ["s2"])

    def test_todos_os_quatro_filtros(self):
        self.assertEqual(self.filtrar(disciplina_id="d2", tipo="Prova",
                                      status="Em andamento", prioridade="Média"), ["s4"])

    def test_todos_todas_nao_filtram(self):
        self.assertEqual(len(self.filtrar(status="Todos", prioridade="Todas")), 6)

    def test_status_prioridade_sem_resultado(self):
        self.assertEqual(self.filtrar(status="Concluída", prioridade="Baixa"), [])


if __name__ == "__main__":
    unittest.main()