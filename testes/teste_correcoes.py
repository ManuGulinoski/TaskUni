"""
Testes das correções finais (US04, US05, US06/US28, US11 e US18).
Usam um JSON temporário, então NÃO mexem no dados/dados.json de vocês.

Rodar (da pasta do projeto):  python -m unittest testes.teste_correcoes -v
"""
import os
import tempfile
import unittest
from datetime import date, timedelta
from unittest import mock

from models.disciplina import Disciplina
from models.tarefa import Tarefa
from repositorio import armazenamento
from services.disciplina_service import cadastrar_disciplina, editar_disciplina
from services.filtro_service import filtrar_tarefas
from services.tarefa_service import (
    cadastrar_tarefa, editar_tarefa, verificar_tarefas_atrasadas
)
from utils.constantes import STATUS_A_FAZER, STATUS_ATRASADA, PRAZO_HOJE


def _data(dias):
    return (date.today() + timedelta(days=dias)).strftime("%d/%m/%Y")


class TesteBase(unittest.TestCase):

    def setUp(self):
        pasta = tempfile.TemporaryDirectory()
        self.addCleanup(pasta.cleanup)
        caminho = os.path.join(pasta.name, "dados", "dados.json")
        remendo = mock.patch.object(armazenamento, "CAMINHO_DADOS", caminho)
        remendo.start()
        self.addCleanup(remendo.stop)

        self.calculo = Disciplina("Cálculo I")
        armazenamento.salvar([self.calculo], [])


class TesteValidacaoTarefa(TesteBase):
    """US06 / US28 - tipo e disciplina obrigatórios."""

    def test_tarefa_sem_tipo_e_bloqueada(self):
        with self.assertRaises(ValueError):
            cadastrar_tarefa("Lista 1", "", self.calculo.id, _data(5))

    def test_tarefa_sem_disciplina_e_bloqueada(self):
        with self.assertRaises(ValueError):
            cadastrar_tarefa("Lista 1", "Exercício", None, _data(5))

    def test_sem_disciplinas_cadastradas_avisa(self):
        armazenamento.salvar([], [])
        with self.assertRaisesRegex(ValueError, "Cadastre uma disciplina"):
            cadastrar_tarefa("Lista 1", "Exercício", None, _data(5))

    def test_tarefa_valida_continua_funcionando(self):
        tarefa = cadastrar_tarefa("Lista 1", "Exercício", self.calculo.id, _data(5))
        self.assertEqual(tarefa.disciplina_id, self.calculo.id)


class TesteAtrasadaNaoESalva(TesteBase):
    """US11 - "Atrasada" é calculada pela data, nunca gravada."""

    def test_adiar_prazo_tira_o_atraso(self):
        # Dado antigo: tarefa vencida com "Atrasada" gravado no JSON
        vencida = Tarefa("Lista 2", "Exercício", date.today() - timedelta(days=2),
                         self.calculo.id, status=STATUS_ATRASADA)
        armazenamento.salvar([self.calculo], [vencida])

        _, tarefas = verificar_tarefas_atrasadas()
        tarefa = tarefas[0]
        self.assertEqual(tarefa.status_atual(), STATUS_ATRASADA)   # continua atrasada pela data

        editar_tarefa(tarefa.id, tarefa.nome, tarefa.tipo, tarefa.disciplina_id,
                      _data(10), tarefa.descricao, tarefa.status, tarefa.cor)

        _, tarefas = armazenamento.carregar()
        self.assertEqual(tarefas[0].status_atual(), STATUS_A_FAZER)

    def test_verificar_nao_grava_atrasada(self):
        vencida = Tarefa("Lista 3", "Exercício", date.today() - timedelta(days=1),
                         self.calculo.id)
        armazenamento.salvar([self.calculo], [vencida])

        verificar_tarefas_atrasadas()

        _, tarefas = armazenamento.carregar()
        self.assertEqual(tarefas[0].status, STATUS_A_FAZER)          # salvo
        self.assertEqual(tarefas[0].status_atual(), STATUS_ATRASADA)  # calculado


class TesteDisciplina(TesteBase):
    """US03 (limite de 50 caracteres) e US05 (editar disciplina)."""

    def test_nome_com_mais_de_50_caracteres_e_bloqueado(self):
        with self.assertRaises(ValueError):
            cadastrar_disciplina("X" * 51)

    def test_editar_troca_o_nome(self):
        editar_disciplina(self.calculo.id, "Cálculo Diferencial")
        disciplinas, _ = armazenamento.carregar()
        self.assertEqual(disciplinas[0].nome, "Cálculo Diferencial")

    def test_tarefas_continuam_ligadas_apos_editar(self):
        tarefa = cadastrar_tarefa("Prova 1", "Prova", self.calculo.id, _data(3))
        editar_disciplina(self.calculo.id, "Cálculo Diferencial")
        _, tarefas = armazenamento.carregar()
        self.assertEqual(tarefas[0].id, tarefa.id)
        self.assertEqual(tarefas[0].disciplina_id, self.calculo.id)

    def test_editar_bloqueia_nome_repetido(self):
        cadastrar_disciplina("Física")
        with self.assertRaises(ValueError):
            editar_disciplina(self.calculo.id, "física")

    def test_editar_mantendo_o_proprio_nome_e_permitido(self):
        editar_disciplina(self.calculo.id, "Cálculo I")

    def test_editar_com_nome_vazio_ou_longo_e_bloqueado(self):
        with self.assertRaises(ValueError):
            editar_disciplina(self.calculo.id, "   ")
        with self.assertRaises(ValueError):
            editar_disciplina(self.calculo.id, "X" * 51)


class TesteFiltroPrazo(TesteBase):
    """US18 - filtro por prazo (a tela agora tem o campo Prazo)."""

    def test_filtra_tarefas_de_hoje(self):
        hoje = Tarefa("Hoje", "Prova", date.today(), self.calculo.id)
        depois = Tarefa("Depois", "Prova", date.today() + timedelta(days=20),
                        self.calculo.id)
        resultado = filtrar_tarefas([hoje, depois], prazo=PRAZO_HOJE)
        self.assertEqual([t.nome for t in resultado], ["Hoje"])


if __name__ == "__main__":
    unittest.main()
