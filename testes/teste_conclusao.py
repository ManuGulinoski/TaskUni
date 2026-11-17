"""US12: testa com JSON temporário, sem alterar os dados do projeto."""
import os
import tempfile
import unittest
from datetime import date, timedelta
from unittest.mock import patch
from models.tarefa import Tarefa
from repositorio import armazenamento
from services.tarefa_service import concluir_tarefa, verificar_tarefas_atrasadas
from services.estatisticas_service import obter_estatisticas
from utils.constantes import STATUS_CONCLUIDA, STATUS_ATRASADA


class TesteConclusao(unittest.TestCase):
    def setUp(self):
        pasta = tempfile.TemporaryDirectory()
        self.addCleanup(pasta.cleanup)
        remendo = patch.object(armazenamento, 'CAMINHO_DADOS', os.path.join(pasta.name, 'dados.json'))
        remendo.start()
        self.addCleanup(remendo.stop)
        self.tarefa = Tarefa('Prova', 'Prova', date.today() - timedelta(days=1), 'd1', status=STATUS_ATRASADA)
        self.outra = Tarefa('Trabalho', 'Trabalho', date.today(), 'd1')
        armazenamento.salvar([], [self.tarefa, self.outra])

    def test_conclusao_persiste_sem_alterar_outra_tarefa(self):
        resultado = concluir_tarefa(self.tarefa.id)
        _, tarefas = armazenamento.carregar()
        self.assertEqual(resultado.status, STATUS_CONCLUIDA)
        self.assertEqual(tarefas[0].to_dict(), resultado.to_dict())
        self.assertEqual(tarefas[1].to_dict(), self.outra.to_dict())

    def test_concluida_nao_volta_a_atrasada(self):
        concluir_tarefa(self.tarefa.id)
        _, tarefas = verificar_tarefas_atrasadas()
        self.assertFalse(tarefas[0].esta_atrasada())
        self.assertEqual(tarefas[0].status_atual(), STATUS_CONCLUIDA)
        self.assertEqual(obter_estatisticas()['atrasadas'], 0)
        self.assertEqual(obter_estatisticas()['concluidas'], 1)

    def test_repetir_nao_duplica(self):
        concluir_tarefa(self.tarefa.id)
        concluir_tarefa(self.tarefa.id)
        self.assertEqual(len(armazenamento.carregar()[1]), 2)

    def test_id_inexistente_nao_altera_dados(self):
        antes = [t.to_dict() for t in armazenamento.carregar()[1]]
        with self.assertRaises(ValueError):
            concluir_tarefa('inexistente')
        self.assertEqual([t.to_dict() for t in armazenamento.carregar()[1]], antes)

    def test_falha_de_gravacao(self):
        with patch.object(armazenamento, 'salvar', side_effect=OSError('Sem acesso')):
            with self.assertRaises(OSError):
                concluir_tarefa(self.tarefa.id)
        self.assertEqual(armazenamento.carregar()[1][0].status, STATUS_ATRASADA)
