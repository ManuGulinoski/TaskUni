import uuid

class Disciplina:
    def __init__(self, nome, id=None):
        self.id = id or str(uuid.uuid4())
        self.nome = nome

    def to_dict(self):
        return {"id": self.id, "nome": self.nome}

    @staticmethod
    def from_dict(dados):
        return Disciplina(nome=dados["nome"], id=dados["id"])

    def __repr__(self):
        return f"Disciplina({self.nome!r})"
