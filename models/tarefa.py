import uuid
from datetime import date, datetime

from utils.constantes import *


class Tarefa:
    def __init__(self, nome, tipo, prazo, disciplina_id,
                 status=STATUS_A_FAZER, descricao="", cor=None, id=None):

        self.id = id or str(uuid.uuid4())
        self.nome = nome
        self.tipo = tipo
        self.prazo = prazo
        self.disciplina_id = disciplina_id
        self.status = status
        self.descricao = descricao
        self.cor = cor

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "tipo": self.tipo,
            "prazo": self.prazo.strftime(FORMATO_DATA_JSON),
            "disciplina_id": self.disciplina_id,
            "status": self.status,
            "descricao": self.descricao,
            "cor": self.cor,
        }

    @staticmethod
    def from_dict(dados):
        return Tarefa(
            id=dados["id"],
            nome=dados["nome"],
            tipo=dados["tipo"],
            prazo=datetime.strptime(
                dados["prazo"], FORMATO_DATA_JSON
            ).date(),
            disciplina_id=dados["disciplina_id"],
            status=dados.get("status", STATUS_A_FAZER),
            descricao=dados.get("descricao", ""),
            cor=dados.get("cor"),
        )

    def dias_restantes(self, hoje=None):
        if hoje is None:
            hoje = date.today()

        return (self.prazo - hoje).days

    def esta_atrasada(self, hoje=None):
        if hoje is None:
            hoje = date.today()

        return (
            self.prazo < hoje
            and self.status != STATUS_CONCLUIDA
        )

    def status_atual(self, hoje=None):
        if self.esta_atrasada(hoje):
            return STATUS_ATRASADA

        return self.status

    def prioridade(self, hoje=None):
        dias = self.dias_restantes(hoje)

        if dias <= 0:
            return PRIORIDADE_URGENTE

        elif dias <= 3:
            return PRIORIDADE_ALTA

        elif dias <= 7:
            return PRIORIDADE_MEDIA

        else:
            return PRIORIDADE_BAIXA

    def __repr__(self):
        return f"Tarefa({self.nome!r}, prazo={self.prazo})"