import json
import os

from models.disciplina import Disciplina
from models.tarefa import Tarefa
from utils.constantes import CAMINHO_DADOS


def carregar():
    if not os.path.exists(CAMINHO_DADOS):
        return [], []

    with open(CAMINHO_DADOS, "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read()

    if conteudo.strip() == "":
        return [], []

    dados = json.loads(conteudo)

    disciplinas = [Disciplina.from_dict(d) for d in dados.get("disciplinas", [])]
    tarefas = [Tarefa.from_dict(t) for t in dados.get("tarefas", [])]
    return disciplinas, tarefas


def salvar(disciplinas, tarefas):
    os.makedirs(os.path.dirname(CAMINHO_DADOS), exist_ok=True)

    dados = {
        "disciplinas": [d.to_dict() for d in disciplinas],
        "tarefas": [t.to_dict() for t in tarefas],
    }

    with open(CAMINHO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)
