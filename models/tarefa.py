"""
Modelo Tarefa.

Responsável: Pessoa 1
Este arquivo NÃO importa tkinter nem lê o JSON.

IMPORTANTE:
- "Atrasada" e a prioridade NÃO são salvas. São calculadas na hora
  pelos métodos status_atual() e prioridade().
- A tarefa guarda o disciplina_id (e não o nome da disciplina).
"""
import uuid
from datetime import date, datetime

from utils.constantes import (
    FORMATO_DATA_JSON,
    STATUS_A_FAZER,
)


class Tarefa:
    def __init__(self, nome, tipo, prazo, disciplina_id,
                 status=STATUS_A_FAZER, descricao="", cor=None, id=None):
        self.id = id or str(uuid.uuid4())
        self.nome = nome
        self.tipo = tipo
        self.prazo = prazo              # objeto datetime.date
        self.disciplina_id = disciplina_id
        self.status = status            # só "A fazer", "Em andamento" ou "Concluída"
        self.descricao = descricao
        self.cor = cor                  # código hex ("#378ADD") ou None

    # ------------------------------------------------------------------
    # Conversão para / do JSON (Pessoa 1)
    # ------------------------------------------------------------------
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
            prazo=datetime.strptime(dados["prazo"], FORMATO_DATA_JSON).date(),
            disciplina_id=dados["disciplina_id"],
            status=dados.get("status", STATUS_A_FAZER),
            descricao=dados.get("descricao", ""),
            cor=dados.get("cor"),
        )

    # ------------------------------------------------------------------
    # Cálculos automáticos (Pessoa 1)
    # ------------------------------------------------------------------
    def dias_restantes(self, hoje=None):
        """
        Retorna quantos dias faltam até o prazo (int).
        Negativo = já passou. 0 = entrega hoje.
        O parâmetro 'hoje' existe para facilitar testes; se None, usa date.today().
        """
        # TODO (Pessoa 1)
        raise NotImplementedError

    def esta_atrasada(self, hoje=None):
        """True se o prazo já passou E a tarefa não está concluída."""
        # TODO (Pessoa 1)
        raise NotImplementedError

    def status_atual(self, hoje=None):
        """
        Status que aparece na tela e é usado nos filtros/gráficos.
        Retorna STATUS_ATRASADA se esta_atrasada(), senão self.status.
        """
        # TODO (Pessoa 1)
        raise NotImplementedError

    def prioridade(self, hoje=None):
        """
        Retorna uma das constantes de PRIORIDADES conforme a tabela:
            0 dias        -> Urgente
            1 a 3 dias    -> Alta
            4 a 7 dias    -> Média
            8 ou mais     -> Baixa
        Decidam em equipe o que retornar para tarefas atrasadas
        (sugestão: Urgente).
        """
        # TODO (Pessoa 1)
        raise NotImplementedError

    def __repr__(self):
        return f"Tarefa({self.nome!r}, prazo={self.prazo})"
