"""
Modelo Disciplina.

Responsável: Pessoa 1
Este arquivo NÃO importa tkinter nem lê o JSON. Ele só representa o dado.
"""
import uuid


class Disciplina:
    def __init__(self, nome, id=None):
        self.id = id or str(uuid.uuid4())
        self.nome = nome

    def to_dict(self):
        """Converte para dicionário (formato salvo no JSON)."""
        return {"id": self.id, "nome": self.nome}

    @staticmethod
    def from_dict(dados):
        """Cria uma Disciplina a partir de um dicionário lido do JSON."""
        return Disciplina(nome=dados["nome"], id=dados["id"])

    def __repr__(self):
        return f"Disciplina({self.nome!r})"
