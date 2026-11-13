"""
Testes da US11 - Excluir tarefa.
Usam um JSON temporário, então NÃO mexem no dados/dados.json de vocês.

Rodar (da pasta do projeto):  python -m unittest testes.teste_exclusao -v
"""
import os
import tempfile
import unittest
from datetime import date
from unittest import mock

from models.tarefa import Tarefa
from repositorio import armazenamento
from services.tarefa_service import excluir_tarefa


class TesteExclusaoTarefa(unittest.TestCase):

    def setUp(self):
        # Redireciona o armazenamento para um arquivo temporário
        self.pasta = tempfile.TemporaryDirectory()
        caminho = os.path.join(self.pasta.name, "dados", "dados.json")
        self.patch = mock.patch.object(armazenamento, "CAMINHO_DADOS", caminho)
        self.patch.start()

        self.tarefa_a = Tarefa("Prova de BD", "Prova", date(2026, 12, 1), "d1")
        self.tarefa_b = Tarefa("Trabalho de IA", "Trabalho", date(2026, 12, 5), "d1")
        armazenamento.salvar([], [self.tarefa_a, self.tarefa_b])

    def tearDown(self):
        self.patch.stop()
        self.pasta.cleanup()

    def test_remove_a_tarefa_do_arquivo(self):
        excluir_tarefa(self.tarefa_a.id)

        _, tarefas = armazenamento.carregar()
        ids = [t.id for t in tarefas]
        self.assertNotIn(self.tarefa_a.id, ids)

    def test_mantem_as_outras_tarefas(self):
        excluir_tarefa(self.tarefa_a.id)

        _, tarefas = armazenamento.carregar()
        self.assertEqual(len(tarefas), 1)
        self.assertEqual(tarefas[0].id, self.tarefa_b.id)

    def test_retorna_a_tarefa_excluida(self):
        excluida = excluir_tarefa(self.tarefa_b.id)
        self.assertEqual(excluida.nome, "Trabalho de IA")

    def test_tarefa_inexistente_gera_erro(self):
        with self.assertRaises(ValueError):
            excluir_tarefa("id-que-nao-existe")

        # E não apaga nada por engano
        _, tarefas = armazenamento.carregar()
        self.assertEqual(len(tarefas), 2)

    def test_excluir_a_ultima_deixa_lista_vazia(self):
        excluir_tarefa(self.tarefa_a.id)
        excluir_tarefa(self.tarefa_b.id)

        _, tarefas = armazenamento.carregar()
        self.assertEqual(tarefas, [])


if __name__ == "__main__":
    unittest.main()
