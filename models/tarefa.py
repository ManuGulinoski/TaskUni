import uuid
from datetime import date, datetime

from utils.constantes import (
    FORMATO_DATA_JSON,
    STATUS_A_FAZER, STATUS_CONCLUIDA, STATUS_ATRASADA,
    PRIORIDADE_URGENTE, PRIORIDADE_ALTA, PRIORIDADE_MEDIA, PRIORIDADE_BAIXA,
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

    def dias_restantes(self, hoje=None):
        """
        Retorna quantos dias faltam até o prazo (int).
        Negativo = já passou. 0 = entrega hoje.
        O parâmetro 'hoje' existe para facilitar testes; se None, usa date.today().
        """
        if hoje is None:
            hoje = date.today()
        return (self.prazo - hoje).days

    def esta_atrasada(self, hoje=None):
        """True se o prazo já passou E a tarefa não está concluída."""
        return self.dias_restantes(hoje) < 0 and self.status != STATUS_CONCLUIDA

    def status_atual(self, hoje=None):
        """
        Status que aparece na tela e é usado nos filtros/gráficos.
        Retorna STATUS_ATRASADA se esta_atrasada(), senão self.status.
        """
        if self.esta_atrasada(hoje):
            return STATUS_ATRASADA
        return self.status

    def prioridade(self, hoje=None):
        """
        Retorna uma das constantes de PRIORIDADES conforme a tabela:
            0 dias        -> Urgente
            1 a 3 dias    -> Alta
            4 a 7 dias    -> Média
            8 ou mais     -> Baixa
        Decidam em equipe o que retornar para tarefas atrasadas
        (sugestão: Urgente).

        Decisão adotada aqui:
            tarefa concluída -> None (não tem urgência; o card esconde a prioridade)
            tarefa atrasada  -> Urgente
        """
        if self.status == STATUS_CONCLUIDA:
            return None

        dias = self.dias_restantes(hoje)
        if dias <= 0:          # hoje ou atrasada
            return PRIORIDADE_URGENTE
        if dias <= 3:
            return PRIORIDADE_ALTA
        if dias <= 7:
            return PRIORIDADE_MEDIA
        return PRIORIDADE_BAIXA

    def __repr__(self):
        return f"Tarefa({self.nome!r}, prazo={self.prazo})"
